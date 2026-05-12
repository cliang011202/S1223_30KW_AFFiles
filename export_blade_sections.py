"""
export_blade_sections.py
========================================================
BEM → CAD 桥: 把 chord_opt / twist_opt 优化结果 + 翼型 .dat 转换成
SolidWorks "曲线通过 XYZ 点" 可直接导入的 .sldcrv 文件。
输出闭合曲线 (末点 = 首点), 适用于放样 + 填充曲面。

输入:
  - 叶片几何参数 (r, chord, twist) 直接在 §1 中以数组形式定义
  - origin/{S1223,SD7062,SG6050,DU-06-W-200}.dat  (Selig 单位翼型坐标)

输出:
  - cad_sections/blade_section_idx{idx:02d}_r{r}m_{airfoil}.sldcrv
    Tab 分隔 X Y Z (mm), CRLF 行尾, 无表头, 闭合
  - cad_sections/_section_summary.txt   (本次导出的全部参数记录)
  - cad_sections/_preview.png           (3D 截面预览)

关键约定 (修改 §1 即可重跑):
  - 桨距轴 @ 30% 弦 (PITCH_AXIS_FRAC)
  - 坐标系: z 沿叶展 (root→tip), x 沿弦向(零扭时), y 厚度方向
  - 单位: 输出 mm
  - 正扭转角 = LE 抬起 (CCBlade 约定, 右手绕 +z); 反向改 TWIST_SIGN = -1
  - idx 0–1 圆柱段不导出 (在 SW 里独立做结构桨柄)

放样稳定性 pipeline (来自 split_qblade_sections.py):
  - dedup: 删除相邻重复点 (避免自相交)
  - enforce direction: 全部统一 CW (从 +Z 看), 防止放样曲面折叠
  - align start: 用 PCA 主轴把每节起点对齐到 TE, 防止节间扭转
  - resample: 沿弧长均匀重采样到固定点数 N, 保证各节点数一致
  - close: 末点重复首点 → 闭合曲线, SW 放样 + 填充能识别
========================================================
"""

import os
import sys
import math
import numpy as np
from scipy.interpolate import PchipInterpolator

sys.stdout.reconfigure(encoding="utf-8")

# ================================================================
# 1. 参数 — 修改这一节即可重跑
# ================================================================

PITCH_AXIS_FRAC = 0.30        # 桨距轴在弦上的位置 (0=LE, 1=TE)
TWIST_SIGN      = +1          # 扭转方向: +1=RH about +z; SW 里反向则改 -1

WORK_DIR    = r"E:\CCBlade\test\S1223_30KW_AFFiles"
AIRFOIL_DIR = os.path.join(WORK_DIR, "origin")
OUT_DIR     = os.path.join(WORK_DIR, "cad_sections")

# ---- 叶片几何参数 (修改此处即可重跑, 无需依赖 .npz) ----
# r [m], chord [m], twist [deg] — 14 站 (idx 0–13)
_r_array  = np.array([0.202, 0.350, 0.676, 0.967, 1.135,
                      1.483, 1.664, 1.850, 2.036, 2.217,
                      2.398, 2.565, 3.024, 3.498])
_chord_array = np.array([0.2500, 0.2500, 0.6000, 0.5192, 0.4681,
                          0.3500, 0.3200, 0.2896, 0.2536, 0.2224,
                          0.1954, 0.1741, 0.1331, 0.1182])
_twist_array = np.array([18.20, 18.20, 18.20, 10.38,  7.54,
                          4.29,  3.46,  2.97,  2.72,  2.60,
                          2.56,  2.56,  2.45,  1.68])

# idx → 翼型文件名 (无 .dat 扩展)。None = 不导出 (圆柱段)
AIRFOIL_MAP = {
    0:  None,            1:  None,                        # 圆柱段 → 结构桨柄域
    2:  "DU-06-W-200",   3:  "DU-06-W-200",  4: "DU-06-W-200",
    5:  "SG6050",        6:  "SG6050",       7: "SG6050",
    8:  "SD7062",        9:  "SD7062",      10: "SD7062",
    11: "S1223",        12:  "S1223",      13: "S1223",
}

# ---- pipeline 参数 ----
RESAMPLE_N      = 100         # 每节均匀重采样到 N 点 (建议 80–120; 0 = 不重采样)
ALIGN_START     = "principal-pos"  # 起点对齐: principal-pos = TE 端 (PCA 长轴正向)
LOOP_DIRECTION  = "cw"        # 强制方向: "cw" / "ccw" (从 +Z 看)
CLOSE_CURVE     = True        # 末点 = 首点 → 闭合曲线 (SW 放样 + 填充必需)
DEDUP_TOL_MM    = 1e-3        # 相邻点距阈值 (mm), 删除小于此值的重复点

# ---- 展向曲面参数 (重建 QBlade 的内部 3D 叶片曲面) ----
N_AF_POINTS     = 160         # 翼型归一化点数 (所有翼型重采样到此数, 保证弦向参数一致)
SPANWISE_SMOOTH = 0.0         # 展向光滑因子 (PchipInterpolator 保证 C1 连续; >0 时改为 UnivariateSpline 光滑)

GENERATE_PREVIEW = True       # 写一张 _preview.png 三视图供肉眼校核


# ================================================================
# 2. 翼型读取 + 截面变换
# ================================================================

def read_selig_dat(path):
    """读 Selig 格式 .dat, 返回 (x, y) ndarray 单位归一弦长。
    保留原始点 (含可能的闭合 TE 重复点); 重复点统一在后续 pipeline dedup 处理。"""
    pts = []
    with open(path, "r", errors="ignore") as fh:
        for line in fh:
            tok = line.strip().split()
            if len(tok) != 2:
                continue
            try:
                x, y = float(tok[0]), float(tok[1])
            except ValueError:
                continue
            if not (-0.1 <= x <= 1.5 and -1.0 <= y <= 1.0):
                continue
            pts.append((x, y))
    if len(pts) < 10:
        raise RuntimeError(f"翼型解析失败 (点数<10): {path}")
    arr = np.array(pts)
    return arr[:, 0], arr[:, 1]


def transform_section(x_af, y_af, chord_m, twist_deg, r_m,
                      pitch_axis=PITCH_AXIS_FRAC, twist_sign=TWIST_SIGN):
    """单截面变换: 翼型单位坐标 → 旋翼坐标 (mm)。"""
    x = (x_af - pitch_axis) * chord_m
    y = (y_af - 0.0)        * chord_m
    th = twist_sign * np.deg2rad(twist_deg)
    c, s = math.cos(th), math.sin(th)
    X = x * c - y * s
    Y = x * s + y * c
    Z = np.full_like(X, r_m)
    return X * 1000.0, Y * 1000.0, Z * 1000.0


# ================================================================
# 3. Pipeline 工具 (改编自 split_qblade_sections.py)
# ================================================================

def drop_closing_duplicate(pts):
    """如果首末点(近)重合, 删末点。"""
    if len(pts) >= 2:
        x0, y0, z0 = pts[0]
        xn, yn, zn = pts[-1]
        if abs(x0 - xn) < 1e-6 and abs(y0 - yn) < 1e-6 and abs(z0 - zn) < 1e-6:
            return pts[:-1]
    return pts


def dedup_consecutive(pts, tol):
    """删除相邻重复点 (距离 < tol, 单位与点坐标一致)。"""
    if len(pts) < 2:
        return list(pts), 0
    out = [pts[0]]
    removed = 0
    for p in pts[1:]:
        q = out[-1]
        d2 = (p[0] - q[0])**2 + (p[1] - q[1])**2 + (p[2] - q[2])**2
        if d2 < tol * tol:
            removed += 1
            continue
        out.append(p)
    return out, removed


def enforce_direction(pts, sense):
    """统一回路方向 (从 +Z 看)。 sense ∈ {'cw', 'ccw'}。
    用 shoelace 公式判定: s>0 = CW (屏幕坐标系)。"""
    if len(pts) < 3 or sense not in ("cw", "ccw"):
        return pts
    s = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1, _ = pts[i]
        x2, y2, _ = pts[(i + 1) % n]
        s += (x2 - x1) * (y2 + y1)
    is_cw = s > 0
    want_cw = sense == "cw"
    if is_cw != want_cw:
        return [pts[0]] + list(reversed(pts[1:]))
    return pts


def section_centroid(pts):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return cx, cy


def principal_axis(pts, degenerate_tol=0.05):
    """PCA 主轴 (X-Y 平面)。返回 ((ux, uy), is_degenerate)。
    退化 = 圆形截面 (主次轴长度比 < degenerate_tol)。"""
    cx, cy = section_centroid(pts)
    sxx = syy = sxy = 0.0
    for x, y, _ in pts:
        dx, dy = x - cx, y - cy
        sxx += dx * dx; syy += dy * dy; sxy += dx * dy
    n = len(pts)
    sxx /= n; syy /= n; sxy /= n
    tr = sxx + syy
    det = sxx * syy - sxy * sxy
    disc = max(0.0, tr * tr / 4.0 - det)
    lam1 = tr / 2.0 + math.sqrt(disc)
    lam2 = tr / 2.0 - math.sqrt(disc)
    is_degen = (lam1 < 1e-18) or ((lam1 - lam2) / lam1 < degenerate_tol)
    if abs(sxy) > 1e-18:
        ux, uy = lam1 - syy, sxy
    else:
        ux, uy = (1.0, 0.0) if sxx >= syy else (0.0, 1.0)
    norm = math.hypot(ux, uy) or 1.0
    return (ux / norm, uy / norm), is_degen


def resolve_axes(sections):
    """每节 PCA 主轴, 退化 (圆) 节点借用最近邻; 全局符号对齐避免 180° 翻转。"""
    raw = [principal_axis(s) for s in sections]
    axes = [a for a, _ in raw]
    degen = [d for _, d in raw]
    n = len(sections)
    fixed = list(axes)
    for i in range(n):
        if not degen[i]:
            continue
        best = None
        for d in range(1, n):
            for j in (i - d, i + d):
                if 0 <= j < n and not degen[j]:
                    best = axes[j]
                    break
            if best is not None:
                break
        if best is not None:
            fixed[i] = best
    k0 = next((i for i in range(n) if not degen[i]), 0)
    refx, refy = fixed[k0]
    for i in range(n):
        ux, uy = fixed[i]
        if ux * refx + uy * refy < 0:
            fixed[i] = (-ux, -uy)
    return fixed, degen


def cyclic_shift_to_start(pts, mode, axis=None):
    """按指定模式找起点, 把列表循环移位让起点在前。"""
    if not pts:
        return pts
    if mode in ("principal-pos", "principal-neg"):
        cx, cy = section_centroid(pts)
        ux, uy = axis if axis is not None else (1.0, 0.0)
        sign = 1.0 if mode == "principal-pos" else -1.0
        idx = max(range(len(pts)),
                  key=lambda i: sign * ((pts[i][0] - cx) * ux + (pts[i][1] - cy) * uy))
    elif mode == "max-x":   idx = max(range(len(pts)), key=lambda i: pts[i][0])
    elif mode == "min-x":   idx = min(range(len(pts)), key=lambda i: pts[i][0])
    else:
        return pts
    return pts[idx:] + pts[:idx]


def resample_arclength_closed(pts, n_unique):
    """把 pts 视为闭合循环 (含 pts[-1]→pts[0] 段), 均匀重采样到 n_unique 个不重合点。
    输出最后一段 (pts[n-1]→pts[0]) 长度 = 周长/n_unique, 与其他段一致。
    输入若已含闭合重复点 (pts[0]≈pts[-1]) 会自动剥除。

    与早期'保留端点'版本的差别: 旧版会让重采样后的末点恰好落在原始末点上,
    若原始首末点几近重合 (闭合 TE 翼型如 SD7062), 末点和首点距离 << 平均段长,
    导致 SW 闭合 B 样条在该微距上自相交。本函数避免了这个 corner case。"""
    if n_unique < 4 or len(pts) < 3:
        return list(pts)
    work = list(pts)
    if (abs(work[0][0] - work[-1][0]) < 1e-9 and
        abs(work[0][1] - work[-1][1]) < 1e-9 and
        abs(work[0][2] - work[-1][2]) < 1e-9):
        work = work[:-1]
    m = len(work)
    cum = [0.0]
    for i in range(1, m):
        dx = work[i][0] - work[i - 1][0]
        dy = work[i][1] - work[i - 1][1]
        dz = work[i][2] - work[i - 1][2]
        cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy + dz * dz))
    # 闭环段 work[m-1] → work[0]
    dx = work[0][0] - work[-1][0]
    dy = work[0][1] - work[-1][1]
    dz = work[0][2] - work[-1][2]
    cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy + dz * dz))
    total = cum[-1]
    if total <= 0:
        return list(pts)

    out = []
    j = 0
    for k in range(n_unique):
        s = total * k / n_unique           # k=0 → 起点 work[0]; k=n_unique 重合于起点 (闭环)
        while j + 1 < len(cum) and cum[j + 1] < s - 1e-12:
            j += 1
        seg = cum[j + 1] - cum[j]
        if seg < 1e-12:
            out.append(work[j % m])
            continue
        t = (s - cum[j]) / seg
        p1 = work[j % m]
        p2 = work[(j + 1) % m]
        out.append((
            p1[0] + t * (p2[0] - p1[0]),
            p1[1] + t * (p2[1] - p1[1]),
            p1[2] + t * (p2[2] - p1[2]),
        ))
    return out


def normalize_airfoil_closed(x_af, y_af, n_pts):
    """把单位翼型 (Selig 格式, 可能的闭合重复) 沿弧长均匀重采样到 n_pts 点。

    所有翼型归一化到同一弦向参数化 → 同一索引在不同翼型间对应同一几何位置
    (TE→上表面→LE→下表面→TE), 这是展向样条曲面必需的。
    """
    if n_pts < 4:
        return x_af, y_af
    pts = list(zip(x_af, y_af))
    # 去除闭合重复
    if len(pts) >= 2 and abs(pts[0][0] - pts[-1][0]) < 1e-9 and abs(pts[0][1] - pts[-1][1]) < 1e-9:
        pts = pts[:-1]
    m = len(pts)
    # 弧长累积
    cum = [0.0]
    for i in range(1, m):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy))
    dx = pts[0][0] - pts[-1][0]
    dy = pts[0][1] - pts[-1][1]
    cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy))
    total = cum[-1]
    if total <= 0:
        return x_af, y_af

    out_x, out_y = [], []
    j = 0
    for k in range(n_pts):
        s = total * k / n_pts
        while j + 1 < len(cum) and cum[j + 1] < s - 1e-12:
            j += 1
        seg = cum[j + 1] - cum[j]
        if seg < 1e-12:
            out_x.append(pts[j % m][0])
            out_y.append(pts[j % m][1])
            continue
        t = (s - cum[j]) / seg
        p1, p2 = pts[j % m], pts[(j + 1) % m]
        out_x.append(p1[0] + t * (p2[0] - p1[0]))
        out_y.append(p1[1] + t * (p2[1] - p1[1]))
    return np.array(out_x), np.array(out_y)


def build_spanwise_surface(station_data, smooth=0.0):
    """对每个弦向索引 j 做展向 Pchip 插值 (C1), 重建 3D 叶片曲面。

    station_data: list of (r_m, pts_3d)  其中 pts_3d 是 [(x,y,z), ...]  mm 单位
    smooth: 0.0 → PchipInterpolator (C1, 过点).  >0 → UnivariateSpline (光滑但不保证过点).

    返回: 与 station_data 相同结构的 smoothed_pts_3d (每站坐标由展向样条曲面评估得到)
    """
    if len(station_data) < 2:
        return [list(pts) for _, pts in station_data]

    r_arr = np.array([r for r, _ in station_data])
    n_af = len(station_data[0][1])
    for _, pts in station_data:
        if len(pts) != n_af:
            raise ValueError("所有截面必须具有相同点数 — 请先用 normalize_airfoil_closed")

    # 为每个弦向索引 j 建立展向插值器
    interpolators = []
    for j in range(n_af):
        x_j = np.array([pts[j][0] for _, pts in station_data])
        y_j = np.array([pts[j][1] for _, pts in station_data])
        z_j = np.array([pts[j][2] for _, pts in station_data])
        if smooth > 0:
            from scipy.interpolate import UnivariateSpline
            ip_x = UnivariateSpline(r_arr, x_j, s=smooth)
            ip_y = UnivariateSpline(r_arr, y_j, s=smooth)
            ip_z = UnivariateSpline(r_arr, z_j, s=smooth)
        else:
            ip_x = PchipInterpolator(r_arr, x_j)
            ip_y = PchipInterpolator(r_arr, y_j)
            ip_z = PchipInterpolator(r_arr, z_j)
        interpolators.append((ip_x, ip_y, ip_z))

    # 在每站 r 处评估
    result = []
    for i, (r, _) in enumerate(station_data):
        pts_smooth = []
        for ip_x, ip_y, ip_z in interpolators:
            pts_smooth.append((float(ip_x(r)), float(ip_y(r)), float(ip_z(r))))
        result.append(pts_smooth)
    return result


# ================================================================
# 4. 写文件
# ================================================================

def write_sldcrv(path, pts):
    """SolidWorks 'Curve Through XYZ Points' 格式: Tab 分隔, CRLF, 无表头, mm。"""
    with open(path, "wb") as fh:
        for x, y, z in pts:
            fh.write(f"{x:.6f}\t{y:.6f}\t{z:.6f}\r\n".encode("ascii"))


def plot_preview(sections, out_path):
    """三视图 + 3D, 肉眼检查截面排布。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # noqa
    except ImportError:
        print("  [skip preview] matplotlib 不可用")
        return
    fig = plt.figure(figsize=(14, 10))
    ax3d  = fig.add_subplot(2, 2, 1, projection="3d")
    ax_xz = fig.add_subplot(2, 2, 2)
    ax_yz = fig.add_subplot(2, 2, 3)
    ax_xy = fig.add_subplot(2, 2, 4)
    cmap = plt.get_cmap("viridis")
    for i, (idx, r, pts, name) in enumerate(sections):
        col = cmap(i / max(len(sections) - 1, 1))
        X = [p[0] for p in pts]; Y = [p[1] for p in pts]; Z = [p[2] for p in pts]
        ax3d.plot(X, Y, Z, color=col, lw=0.8)
        ax_xz.plot(X, Z, color=col, lw=0.8)
        ax_yz.plot(Y, Z, color=col, lw=0.8)
        ax_xy.plot(X, Y, color=col, lw=0.8, label=f"idx{idx} r={r:.2f}")
        # mark start point (★) on 端视图 — 起点应集中在 TE 附近
        ax_xy.plot(X[0], Y[0], marker="*", color=col, markersize=8, mec="k", mew=0.5)

    ax3d.set_xlabel("X (mm)"); ax3d.set_ylabel("Y (mm)"); ax3d.set_zlabel("Z (mm, span)")
    ax3d.set_title("3D stacked sections")
    ax_xz.set_xlabel("X (mm, chord)");     ax_xz.set_ylabel("Z (mm, span)"); ax_xz.set_title("Side view X-Z"); ax_xz.set_aspect("equal", adjustable="datalim")
    ax_yz.set_xlabel("Y (mm, thickness)"); ax_yz.set_ylabel("Z (mm, span)"); ax_yz.set_title("Top view Y-Z");  ax_yz.set_aspect("equal", adjustable="datalim")
    ax_xy.set_xlabel("X (mm)");            ax_xy.set_ylabel("Y (mm)");       ax_xy.set_title("End view X-Y (start = star)")
    ax_xy.set_aspect("equal", adjustable="datalim")
    ax_xy.legend(fontsize=6, loc="best", ncol=2)
    fig.suptitle(f"Blade section preview  (pitch axis @ {PITCH_AXIS_FRAC*100:.0f}% chord, "
                 f"twist_sign={TWIST_SIGN:+d}, dir={LOOP_DIRECTION}, N={RESAMPLE_N or 'native'})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  预览图: {out_path}")


# ================================================================
# 5. 主流程
# ================================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    r_arr     = _r_array
    chord_arr = _chord_array
    twist_arr = _twist_array
    n         = len(r_arr)

    # ---- 第一步: 归一化翼型 + 变换 ----
    af_cache = {}
    raw_sections = []   # list of (idx, r, c, t, af_name, [(X,Y,Z), ...])
    for idx in range(n):
        af_name = AIRFOIL_MAP.get(idx)
        r = float(r_arr[idx]); c = float(chord_arr[idx]); t = float(twist_arr[idx])
        if af_name is None:
            raw_sections.append((idx, r, c, t, None, None))
            continue
        if af_name not in af_cache:
            x_raw, y_raw = read_selig_dat(os.path.join(AIRFOIL_DIR, af_name + ".dat"))
            # 归一化到一致点数 → 弦向参数一致 (展向样条必需)
            af_cache[af_name] = normalize_airfoil_closed(x_raw, y_raw, N_AF_POINTS)
        x_af, y_af = af_cache[af_name]
        X, Y, Z = transform_section(x_af, y_af, c, t, r)
        pts = list(zip(X.tolist(), Y.tolist(), Z.tolist()))
        raw_sections.append((idx, r, c, t, af_name, pts))

    # ---- 第二步: 展向样条曲面 (重建 QBlade 内部 3D 曲面, 保证 C1 连续) ----
    valid_entries = [(i, r, pts) for i, (_, r, _, _, _, pts) in enumerate(raw_sections) if pts is not None]
    if len(valid_entries) >= 2 and N_AF_POINTS >= 4:
        station_data = [(r, pts) for _, r, pts in valid_entries]
        smoothed = build_spanwise_surface(station_data, smooth=SPANWISE_SMOOTH)
        for k, (i, r, _) in enumerate(valid_entries):
            _, _, c, t, af_name, _ = raw_sections[i]
            raw_sections[i] = (raw_sections[i][0], r, c, t, af_name, smoothed[k])
        n_span = len(station_data)
        n_af = len(station_data[0][1])
        print(f"\n  展向曲面: {n_span} 站 × {n_af} 点, Pchip C1 连续 (smooth={SPANWISE_SMOOTH})")
    elif N_AF_POINTS < 4:
        print(f"\n  展向曲面: 已跳过 (N_AF_POINTS={N_AF_POINTS}<4)")
    else:
        print(f"\n  展向曲面: 已跳过 (有效截面<2)")

    # ---- 第二步: pipeline (dedup + direction + axes + align + resample + close) ----
    prepared = []   # list of (idx, r, c, t, af_name, pts_processed, n_dedup, was_closed)
    pts_list_for_pca = []
    for idx, r, c, t, af_name, pts in raw_sections:
        if pts is None:
            prepared.append((idx, r, c, t, af_name, None, 0, False))
            pts_list_for_pca.append(None)
            continue
        was_closed = (
            len(pts) >= 2
            and abs(pts[0][0] - pts[-1][0]) < 1e-6
            and abs(pts[0][1] - pts[-1][1]) < 1e-6
            and abs(pts[0][2] - pts[-1][2]) < 1e-6
        )
        pts = drop_closing_duplicate(pts)
        pts, n_dup = dedup_consecutive(pts, DEDUP_TOL_MM)
        pts = enforce_direction(pts, LOOP_DIRECTION)
        prepared.append((idx, r, c, t, af_name, pts, n_dup, was_closed))
        pts_list_for_pca.append(pts)

    # 计算 PCA 主轴 (用于 align_start), 跳过 None
    valid_idx = [i for i, p in enumerate(pts_list_for_pca) if p is not None]
    valid_pts = [pts_list_for_pca[i] for i in valid_idx]
    axes_valid, degen_valid = resolve_axes(valid_pts) if valid_pts else ([], [])
    axes_full = [None] * len(prepared)
    for k, i in enumerate(valid_idx):
        axes_full[i] = axes_valid[k]

    # ---- 第三步: align_start + resample + close + write ----
    print("=" * 110)
    print(f"  叶片截面导出 — 桨距轴 @ {PITCH_AXIS_FRAC*100:.0f}% 弦,  twist_sign = {TWIST_SIGN:+d}")
    print(f"  Pipeline:  norm_af={N_AF_POINTS}pts  →  spanwise_spline(Pchip, s={SPANWISE_SMOOTH})"
          f"  →  dedup<{DEDUP_TOL_MM}mm  →  dir={LOOP_DIRECTION}"
          f"  →  align_start={ALIGN_START}  →  resample N={RESAMPLE_N}  →  closed={CLOSE_CURVE}")
    print(f"  输入:  硬编码叶片几何 (r, chord, twist) — 修改 §1 重跑")
    print(f"  输出:  {OUT_DIR}")
    print("=" * 110)
    print(f"  {'idx':>3}  {'r [m]':>7}  {'chord [m]':>9}  {'twist [°]':>9}  {'airfoil':<14}  "
          f"{'N_in→N_out':>11}  {'flags':<14}  file")
    print("-" * 110)

    summary_rows = []
    preview_data = []
    n_written = 0

    for i, (idx, r, c, t, af_name, pts, n_dup, was_closed) in enumerate(prepared):
        if af_name is None:
            print(f"  {idx:>3d}  {r:>7.3f}  {c:>9.4f}  {t:>9.3f}  {'(cylinder)':<14}  "
                  f"{'-':>11}  {'skipped':<14}  --")
            summary_rows.append((idx, r, c, t, "(cylinder)", "skipped"))
            continue

        n_in = len(pts) + (1 if was_closed else 0) + n_dup    # 还原成原始点数
        if ALIGN_START != "none":
            pts = cyclic_shift_to_start(pts, ALIGN_START, axis=axes_full[i])
        if RESAMPLE_N and RESAMPLE_N >= 4:
            pts = resample_arclength_closed(pts, RESAMPLE_N)
        if CLOSE_CURVE and (pts[0] != pts[-1]):
            pts = pts + [pts[0]]

        fn = f"blade_section_idx{idx:02d}_r{r:.3f}m_{af_name}.sldcrv"
        out_path = os.path.join(OUT_DIR, fn)
        write_sldcrv(out_path, pts)

        flags = []
        if was_closed: flags.append("was_closed")
        if n_dup:      flags.append(f"dedup={n_dup}")
        flag_str = ",".join(flags) if flags else "-"

        print(f"  {idx:>3d}  {r:>7.3f}  {c:>9.4f}  {t:>9.3f}  {af_name:<14}  "
              f"{n_in:>4d}→{len(pts):>4d}  {flag_str:<14}  {fn}")
        summary_rows.append((idx, r, c, t, af_name, fn))
        preview_data.append((idx, r, pts, af_name))
        n_written += 1

    # 汇总
    summary_path = os.path.join(OUT_DIR, "_section_summary.txt")
    with open(summary_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(f"# 叶片截面导出汇总\n")
        fh.write(f"# pitch_axis = {PITCH_AXIS_FRAC*100:.1f}% chord\n")
        fh.write(f"# twist_sign = {TWIST_SIGN:+d}\n")
        fh.write(f"# pipeline: dedup<{DEDUP_TOL_MM}mm | dir={LOOP_DIRECTION} | "
                 f"align={ALIGN_START} | resample={RESAMPLE_N} | closed={CLOSE_CURVE}\n")
        fh.write(f"# unit: mm | newline: CRLF | sep: TAB\n")
        fh.write(f"# data source: §1 硬编码数组 (_r_array, _chord_array, _twist_array)\n#\n")
        fh.write(f"# {'idx':>3}  {'r[m]':>7}  {'chord[m]':>9}  {'twist[deg]':>10}  {'airfoil':<14}  file\n")
        for row in summary_rows:
            fh.write(f"  {row[0]:>3d}  {row[1]:>7.3f}  {row[2]:>9.4f}  {row[3]:>10.3f}  {row[4]:<14}  {row[5]}\n")
    print(f"\n  汇总: {summary_path}")

    if GENERATE_PREVIEW and preview_data:
        plot_preview(preview_data, os.path.join(OUT_DIR, "_preview.png"))

    print(f"\n  完成: 写出 {n_written} 个闭合截面 .sldcrv\n")
    print("  下一步 SolidWorks:")
    print("    1. 插入→曲线→曲线通过 XYZ 点 → 逐个加载 (或宏批量)")
    print("    2. 插入→凸台/曲面→放样: 按 idx02→idx13 顺序")
    print("       - 阶数 3, 起始/终止约束 = '无' 或 '法向于轮廓'")
    print(f"       - 推荐加 LE/TE 引导线 (3D 草图穿过所有截面同序号点)")
    print("    3. 叶尖封头: 用'填充曲面'封 idx13, 然后'缝合曲面'")
    print("    4. r=0.676 m (idx02) 是与结构桨柄对接面, 该截面位置/扭转必须锁定\n")


if __name__ == "__main__":
    main()
