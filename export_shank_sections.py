"""
export_shank_sections.py
========================================================
Domain A: 结构桨柄 + 法兰过渡截面导出

从法兰面 (r=0.20 m) 到 DU-06-W-200 翼型起始 (r=0.676 m)
生成 4 个椭圆/过渡截面 → .sldcrv, 用于 SolidWorks 放样。

输入:
  - origin/DU-06-W-200.dat  (用于 blend 截面的 camber/thickness 参考)
  - cad_sections/blade_section_idx02_r0.676m_DU-06-W-200.sldcrv  (已有, 对接参考)

输出:
  - cad_sections/shank_section_r0.200_ellipse.sldcrv
  - cad_sections/shank_section_r0.350_ellipse.sldcrv
  - cad_sections/shank_section_r0.500_ellipse.sldcrv
  - cad_sections/shank_section_r0.580_blend.sldcrv
  - cad_sections/_shank_summary.txt
  - cad_sections/_shank_preview.png

坐标系 (与 export_blade_sections.py 一致):
  - 原点 = 桨距轴 @ 30% chord
  - X = 弦向 (LE→TE), Y = 厚度方向, Z = 叶展 (root→tip)
  - 正扭转 = RH about +Z
  - 单位: mm

设计依据:
  - 桨柄 NACA 对称截面 → DU 翼型的平滑过渡
  - 根板对接面 (r=0.200): 262mm 宽 × 50mm 厚 (与 Domain A' 终点一致)
  - 桨柄厚度 50→105 mm: 铺层 ply drop 累积区 + 离心承拉
  - t/c 全程维持 ~19-20%, 与 DU-06-W-200 (19.8%) 一致
========================================================
"""

import os, sys, math
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

# ================================================================
# 1. 参数 — 修改本节即可重跑
# ================================================================

PITCH_AXIS_FRAC = 0.30  
TWIST_SIGN      = +1

WORK_DIR    = r"E:\CCBlade\test\S1223_30KW_AFFiles"
AIRFOIL_DIR = os.path.join(WORK_DIR, "origin")
OUT_DIR     = os.path.join(WORK_DIR, "cad_sections")

# ---- shank 截面定义 ----
# (r_m, type, le_x_mm, te_x_mm, thickness_mm, twist_deg)
# type: "ellipse" | "blend"
# le_x / te_x = 前/后缘相对桨距轴位置 (mm, LE 通常为负值)
# LE 和 TE 从法兰到 DU 截面走平滑曲线, 保证 SolidWorks 放样引导线连续
# thickness = 最大厚度 (mm)
SHANK_STATIONS = [
    (0.200, "ellipse", -131, +131,  50,  0.0),   # 根板对接面: 262mm宽, t/c=19.1%
    (0.350, "ellipse", -146, +222,  72,  9.0),   # 桨柄中段, width=368, t/c=19.6%
    (0.500, "ellipse", -162, +313,  93, 14.0),   # 桨柄末端, width=475, t/c=19.6%
    (0.580, "blend",   -170, +362, 105, 16.0),   # 过渡形: width=532, t/c=19.7%→DU
]

# DU 参考: LE=-180, TE=+420 (chord=600, pitch@30%)

# DU 翼型参考截面 (已有, 来自 export_blade_sections.py)
DU_R      = 0.676    # m
DU_CHORD  = 0.600    # m
DU_TWIST  = 18.01    # deg  (来自 chord_optimization_results_AEP.npz idx=2)
DU_TC     = 0.198    # t/c = 19.8% (DU-06-W-200)

# ---- pipeline 参数 (与 export_blade_sections.py 一致) ----
RESAMPLE_N      = 100
ALIGN_START     = "principal-pos"
LOOP_DIRECTION  = "cw"
CLOSE_CURVE     = True
DEDUP_TOL_MM    = 1e-3

GENERATE_PREVIEW = True


# ================================================================
# 2. 翼型工具: 读取 + camber/thickness 分解
# ================================================================

def read_selig_dat(path):
    """读 Selig 格式 .dat, 返回 (x, y) 归一化坐标."""
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


def airfoil_camber_thickness(x_af, y_af, n_interp=200):
    """从 Selig 翼型坐标提取 camber 和 thickness 分布。

    返回: x_interp (归一化), camber (归一化), thickness (归一化)
    三者等长, x_interp 在 [0, 1] 均匀分布。
    """
    # 找 LE (最小 x)
    i_le = int(np.argmin(x_af))
    # 上表面: LE → TE (x 递增方向), 沿 suction side
    # Selig 格式: TE→LE (upper) → LE→TE (lower)
    # 即 pts[0..i_le] = upper (TE→LE), pts[i_le..] = lower (LE→TE)
    x_upper_raw = x_af[:i_le + 1][::-1]  # LE→TE
    y_upper_raw = y_af[:i_le + 1][::-1]
    x_lower_raw = x_af[i_le:]           # LE→TE
    y_lower_raw = y_af[i_le:]

    # 在归一化弦向 [0, 1] 上插值上下表面
    x_grid = np.linspace(0.0, 1.0, n_interp)
    y_upper_interp = np.interp(x_grid, x_upper_raw, y_upper_raw)
    y_lower_interp = np.interp(x_grid, x_lower_raw, y_lower_raw)

    camber    = (y_upper_interp + y_lower_interp) / 2.0
    thickness = y_upper_interp - y_lower_interp

    return x_grid, camber, thickness


# ================================================================
# 3. 截面生成
# ================================================================

def naca_sym_thickness(x_norm, t_over_c):
    """NACA 00xx 对称厚度分布 (归一化半厚度)。

    x_norm: [0, 1] 弦向位置
    t_over_c: 最大厚度/弦长
    返回: 半厚度 / 弦长

    LE 半径 = 1.1019 * t_over_c² * chord (vs 椭圆 R = b²/a ≈ t²/(2c))
    例如 t/c=0.20, c=400mm: R_NACA=17.6mm vs R_ell=8mm — NACA 的 LE 圆钝得多,
    与翼型 LE 形态一致, 避免放样 LE 棱线。

    a4=-0.0996 钝 TE: r=0.200 处 TE 全厚≈2mm (vs -0.1036 闭合→0mm);
    结构桨柄段 TE 太尖锐会在脱模/搬运中崩裂。
    """
    a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
    a4 = -0.0996  # 钝 TE: y(1.0)≈0.005 @ t/c=0.25 → TE 全厚≈2mm
    x = np.maximum(np.asarray(x_norm), 0.0)
    y = (t_over_c / 0.20) * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)
    return np.maximum(y, 0.0)


def generate_ellipse(le_x_mm, te_x_mm, thickness_mm, twist_deg, r_m, n=100):
    """生成 NACA 00xx 对称截面 (替代数学椭圆, 用于桨柄段)。

    NACA 厚度分布提供与翼型一致的 LE 圆角半径 + 最大厚度 @ 30% 弦。
    零弯度, 适合结构桨柄。闭合曲线: 包含闭合重复点 (首=末)。
    """
    width_mm = te_x_mm - le_x_mm
    t_over_c = thickness_mm / width_mm
    th = TWIST_SIGN * math.radians(twist_deg)
    c_th_val, s_th_val = math.cos(th), math.sin(th)

    # 弦向采样: cos-spaced, LE/TE 密 → 中部疏
    n_half = n // 2
    theta_vals = np.linspace(0.0, math.pi, n_half + 1)
    t_vals = (1.0 - np.cos(theta_vals)) / 2.0        # [0, 1]
    y_half = naca_sym_thickness(t_vals, t_over_c) * width_mm  # 半厚度 (mm)

    upper, lower = [], []
    for i in range(len(t_vals)):
        x_phys = le_x_mm + t_vals[i] * width_mm
        y = y_half[i]
        X_up = x_phys * c_th_val - y * s_th_val
        Y_up = x_phys * s_th_val + y * c_th_val
        Z = r_m * 1000.0
        upper.append((X_up, Y_up, Z))

    for i in range(len(t_vals) - 1, -1, -1):
        x_phys = le_x_mm + t_vals[i] * width_mm
        y = -y_half[i]
        X_lo = x_phys * c_th_val - y * s_th_val
        Y_lo = x_phys * s_th_val + y * c_th_val
        Z = r_m * 1000.0
        lower.append((X_lo, Y_lo, Z))

    pts = upper[:-1] + lower
    pts.append(pts[0])
    return pts


def generate_blend(le_x_mm, te_x_mm, thickness_mm, twist_deg, r_m,
                   du_x_norm, du_camber, du_thickness,
                   blend_factor=0.455, n=100):
    """生成 NACA 对称 → DU 翼型的过渡截面 (物理 mm, 已扭转 + 定位)。

    方法: camber+thickness 分解后线性混合。
      - camber_blend(x)   = blend_factor * DU_camber(x_norm)
      - thickness_blend(x) = (1-blend_factor) * naca_thickness(x_norm)
                           + blend_factor * DU_thickness(x_norm) * scale

    参数:
      blend_factor: 0 = 纯 NACA 对称, 1 = 纯 DU。
    """
    width_mm = te_x_mm - le_x_mm
    t_over_c = thickness_mm / width_mm
    th = TWIST_SIGN * math.radians(twist_deg)
    c_th_val, s_th_val = math.cos(th), math.sin(th)

    # 弦向采样: cos-spaced
    n_half = n // 2
    theta_vals = np.linspace(0.0, math.pi, n_half + 1)
    t_vals = (1.0 - np.cos(theta_vals)) / 2.0
    x_phys = le_x_mm + t_vals * width_mm
    x_norm = t_vals

    # ---- NACA 对称厚度 ----
    naca_half = naca_sym_thickness(x_norm, t_over_c)
    naca_thick = 2.0 * naca_half * width_mm  # 物理全厚度

    # ---- DU camber + thickness ----
    du_c = np.interp(x_norm, du_x_norm, du_camber)
    du_t = np.interp(x_norm, du_x_norm, du_thickness)

    du_t_max = float(np.max(du_thickness)) if len(du_thickness) > 0 else 0.198
    du_t_scale = thickness_mm / (du_t_max * width_mm + 1e-12)
    du_t_phys = du_t * width_mm * du_t_scale

    # ---- 混合 ----
    blend_t = (1.0 - blend_factor) * naca_thick + blend_factor * du_t_phys
    blend_c = blend_factor * du_c * width_mm

    # ---- 组装 ----
    upper, lower = [], []
    for i in range(len(x_phys)):
        y = blend_c[i] + blend_t[i] / 2.0
        x = x_phys[i]
        X_u = x * c_th_val - y * s_th_val
        Y_u = x * s_th_val + y * c_th_val
        Z = r_m * 1000.0
        upper.append((X_u, Y_u, Z))

    for i in range(len(x_phys) - 1, -1, -1):
        y = blend_c[i] - blend_t[i] / 2.0
        x = x_phys[i]
        X_l = x * c_th_val - y * s_th_val
        Y_l = x * s_th_val + y * c_th_val
        Z = r_m * 1000.0
        lower.append((X_l, Y_l, Z))

    pts = upper[:-1] + lower
    return pts


# ================================================================
# 4. Pipeline 工具 (与 export_blade_sections.py 共享)
# ================================================================

def dedup_consecutive(pts, tol):
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


def principal_axis(pts):
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
    if abs(sxy) > 1e-18:
        ux, uy = lam1 - syy, sxy
    else:
        ux, uy = (1.0, 0.0) if sxx >= syy else (0.0, 1.0)
    norm = math.hypot(ux, uy) or 1.0
    return (ux / norm, uy / norm)


def cyclic_shift_to_start(pts, mode, axis=None):
    if not pts or mode == "none":
        return pts
    if mode in ("principal-pos", "principal-neg"):
        cx, cy = section_centroid(pts)
        ux, uy = axis if axis is not None else (1.0, 0.0)
        sign = 1.0 if mode == "principal-pos" else -1.0
        idx = max(range(len(pts)),
                  key=lambda i: sign * ((pts[i][0] - cx) * ux + (pts[i][1] - cy) * uy))
    elif mode == "max-x":
        idx = max(range(len(pts)), key=lambda i: pts[i][0])
    elif mode == "min-x":
        idx = min(range(len(pts)), key=lambda i: pts[i][0])
    else:
        return pts
    return pts[idx:] + pts[:idx]


def resample_arclength_closed(pts, n_unique):
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
        s = total * k / n_unique
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


# ================================================================
# 5. 文件输出
# ================================================================

def write_sldcrv(path, pts):
    with open(path, "wb") as fh:
        for x, y, z in pts:
            fh.write(f"{x:.6f}\t{y:.6f}\t{z:.6f}\r\n".encode("ascii"))


def plot_shank_preview(sections, du_pts, out_path):
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
    all_sections = list(sections)
    if du_pts is not None:
        all_sections.append(("DU", DU_R, du_pts, "DU-06-W-200"))
    n_all = len(all_sections)

    for i, (label, r, pts, desc) in enumerate(all_sections):
        col = cmap(i / max(n_all - 1, 1))
        X = [p[0] for p in pts]; Y = [p[1] for p in pts]; Z = [p[2] for p in pts]
        ax3d.plot(X, Y, Z, color=col, lw=0.8)
        ax_xz.plot(X, Z, color=col, lw=0.8)
        ax_yz.plot(Y, Z, color=col, lw=0.8)
        ax_xy.plot(X, Y, color=col, lw=0.8, label=f"{label} r={r:.3f}m")
        ax_xy.plot(X[0], Y[0], marker="*", color=col, markersize=8, mec="k", mew=0.5)

    ax3d.set_xlabel("X (mm)"); ax3d.set_ylabel("Y (mm)"); ax3d.set_zlabel("Z (mm)")
    ax3d.set_title("Shank + DU3D stacked sections")
    ax_xz.set_xlabel("X (mm)"); ax_xz.set_ylabel("Z (mm)"); ax_xz.set_title("Side view X-Z"); ax_xz.set_aspect("equal", adjustable="datalim")
    ax_yz.set_xlabel("Y (mm)"); ax_yz.set_ylabel("Z (mm)"); ax_yz.set_title("Top view Y-Z");  ax_yz.set_aspect("equal", adjustable="datalim")
    ax_xy.set_xlabel("X (mm)"); ax_xy.set_ylabel("Y (mm)"); ax_xy.set_title("End view X-Y (star = start)")
    ax_xy.set_aspect("equal", adjustable="datalim")
    ax_xy.legend(fontsize=6, loc="best", ncol=2)
    fig.suptitle(f"Shank section preview  (pitch axis @ {PITCH_AXIS_FRAC*100:.0f}% chord, N={RESAMPLE_N})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  预览图: {out_path}")


# ================================================================
# 6. 主流程
# ================================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- 6a. 读 DU 翼型, 分解 camber/thickness ----
    du_path = os.path.join(AIRFOIL_DIR, "DU-06-W-200.dat")
    x_du, y_du = read_selig_dat(du_path)
    du_x_norm, du_camber, du_thickness = airfoil_camber_thickness(x_du, y_du)
    print(f"DU-06-W-200: {len(x_du)} 点 → camber/thickness 分解完成")
    print(f"  max camber = {float(np.max(np.abs(du_camber))):.4f}  (归一化)")
    print(f"  max thickness = {float(np.max(du_thickness)):.4f}  (归一化)")

    # ---- 6b. 读已有 DU 截面 (用于预览) ----
    du_sldcrv_path = os.path.join(OUT_DIR, "blade_section_idx02_r0.676m_DU-06-W-200.sldcrv")
    du_preview_pts = None
    if os.path.exists(du_sldcrv_path):
        du_preview_pts = []
        with open(du_sldcrv_path, "r") as fh:
            for line in fh:
                tok = line.strip().split("\t")
                if len(tok) == 3:
                    du_preview_pts.append((float(tok[0]), float(tok[1]), float(tok[2])))
        print(f"  已加载 DU 参考截面: {len(du_preview_pts)} 点")

    # ---- 6c. 生成 shank 截面 ----
    r_ell_last = SHANK_STATIONS[-2][0] if len(SHANK_STATIONS) >= 2 and SHANK_STATIONS[-2][1] == "ellipse" else 0.500

    print("\n" + "=" * 110)
    print(f"  Domain A: 结构桨柄截面导出 — pitch axis @ {PITCH_AXIS_FRAC*100:.0f}% chord")
    print(f"  Pipeline:  dedup<{DEDUP_TOL_MM}mm  →  dir={LOOP_DIRECTION}"
          f"  →  align_start={ALIGN_START}  →  resample N={RESAMPLE_N}  →  closed={CLOSE_CURVE}")
    print(f"  输出:  {OUT_DIR}")
    print("=" * 110)
    print(f"  {'r [m]':>7}  {'type':<8}  {'LE':>8}  {'TE':>8}  {'width':>7}  {'t_max':>7}  {'twist':>7}  "
          f"{'blend':>7}  {'N_in→N_out':>11}  file")
    print("-" * 110)

    summary_rows = []
    preview_data = []
    n_written = 0

    for r_m, stype, le_x, te_x, t_mm, twist_deg in SHANK_STATIONS:
        w_mm = te_x - le_x   # 实际弦向宽度

        # blend_factor
        if stype == "blend":
            blend_factor = (r_m - r_ell_last) / (DU_R - r_ell_last)
        else:
            blend_factor = 0.0

        # 生成原始点列
        if stype == "ellipse":
            raw_pts = generate_ellipse(le_x, te_x, t_mm, twist_deg, r_m, n=RESAMPLE_N)
        elif stype == "blend":
            raw_pts = generate_blend(le_x, te_x, t_mm, twist_deg, r_m,
                                     du_x_norm, du_camber, du_thickness,
                                     blend_factor=blend_factor, n=RESAMPLE_N)
        else:
            raise ValueError(f"未知截面类型: {stype}")

        # Pipeline
        n_raw = len(raw_pts)
        pts_dd, n_dup = dedup_consecutive(raw_pts, DEDUP_TOL_MM)
        pts_dir = enforce_direction(pts_dd, LOOP_DIRECTION)
        axis = principal_axis(pts_dir)
        pts_aligned = cyclic_shift_to_start(pts_dir, ALIGN_START, axis=axis)
        pts_resampled = resample_arclength_closed(pts_aligned, RESAMPLE_N)
        if CLOSE_CURVE and (pts_resampled[0] != pts_resampled[-1]):
            pts_final = pts_resampled + [pts_resampled[0]]
        else:
            pts_final = pts_resampled

        fn = f"shank_section_r{r_m:.3f}_{stype}.sldcrv"
        out_path = os.path.join(OUT_DIR, fn)
        write_sldcrv(out_path, pts_final)

        print(f"  {r_m:>7.3f}  {stype:<8}  {le_x:>+5d}mm  {te_x:>+5d}mm  {w_mm:>5d}mm  {t_mm:>5d}mm  {twist_deg:>5.1f}°  "
              f"{blend_factor:>6.3f}  {n_raw:>4d}→{len(pts_final):>4d}  {fn}")

        summary_rows.append((r_m, stype, le_x, te_x, w_mm, t_mm, twist_deg, blend_factor, fn))
        preview_data.append((f"r{r_m:.3f}", r_m, pts_final, stype))
        n_written += 1

    # ---- 6d. 汇总 ----
    summary_path = os.path.join(OUT_DIR, "_shank_summary.txt")
    with open(summary_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("# Domain A: 结构桨柄截面导出汇总\n")
        fh.write(f"# pitch_axis = {PITCH_AXIS_FRAC*100:.1f}% chord (x=0)\n")
        fh.write(f"# twist_sign = {TWIST_SIGN:+d}\n")
        fh.write(f"# pipeline: dedup<{DEDUP_TOL_MM}mm | dir={LOOP_DIRECTION} | "
                 f"align={ALIGN_START} | resample={RESAMPLE_N} | closed={CLOSE_CURVE}\n")
        fh.write(f"# unit: mm | newline: CRLF | sep: TAB\n")
        fh.write(f"# DU reference: r={DU_R:.3f} m, chord={DU_CHORD*1000:.0f} mm, "
                 f"LE={-PITCH_AXIS_FRAC*DU_CHORD*1000:.0f}, TE={+(1-PITCH_AXIS_FRAC)*DU_CHORD*1000:.0f} mm\n")
        fh.write(f"#\n")
        fh.write(f"# {'r[m]':>7}  {'type':<8}  {'LE[mm]':>8}  {'TE[mm]':>8}  {'width[mm]':>9}  "
                 f"{'t_max[mm]':>9}  {'twist[deg]':>10}  blend  file\n")
        for row in summary_rows:
            fh.write(f"  {row[0]:>7.3f}  {row[1]:<8}  {row[2]:>+5d}     {row[3]:>+5d}     "
                     f"{row[4]:>9d}  {row[5]:>9d}  {row[6]:>10.1f}  {row[7]:.3f}  {row[8]}\n")
    print(f"\n  汇总: {summary_path}")

    # ---- 6e. 预览 ----
    if GENERATE_PREVIEW and preview_data:
        plot_shank_preview(preview_data, du_preview_pts,
                          os.path.join(OUT_DIR, "_shank_preview.png"))

    # ---- 6f. 打印 SolidWorks 操作指南 ----
    print(f"\n  完成: 写出 {n_written} 个 shank 截面 .sldcrv\n")
    print("  Domain A SolidWorks 操作:")
    print("    1. 插入→曲线→曲线通过 XYZ 点 → 按序加载 4 个 shank_section_*.sldcrv")
    print("    2. 插入→曲面/凸台→放样:")
    print("       - 轮廓顺序: r0.200 → r0.350 → r0.500 → r0.580 → r0.676 (DU)")
    print("       - 起始/终止约束 = '无'")
    print("       - 推荐加 3 条引导线: LE 连线, TE 连线, max-thickness 连线")
    print("         (3D 草图→通过各截面同序号点画样条)")
    print("    3. 法兰: 在 r=0.200 平面建草图 → 外径 220mm 圆盘, 厚 15-20mm")
    print("       - 钻 8×M16 通孔, PCD=180mm")
    print("       - 法兰与桨柄根部合并 (Combine/Merge)")
    print("    4. Domain A 与 Domain B 对接:")
    print(f"       - DU 截面 (r={DU_R:.3f}m) 是共享轮廓")
    print("       - 两侧 loft 实体在 DU 面处合并, 或预先画一个 DU 曲面作为相切约束")
    print(f"    5. 气动整流罩 (可选): 单独旋转体覆盖法兰+螺栓头")


if __name__ == "__main__":
    main()
