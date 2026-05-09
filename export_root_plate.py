"""
export_root_plate.py
========================================================
交叉夹板式架构 — Blade 1 根部平板延伸截面 (含 z<0 反向 tab)

从 z=-Z_TAB (反向 tab 起点) 到 z=+0.200 (对接 Domain A NACA 桨柄),
生成 7 站截面 → .sldcrv, 用于 SolidWorks 放样。

几何分两段:
  • 交叉 tab 区 z∈[-Z_TAB, +Z_TAB] (3 站): 恒定 262×25, Y_off=+12.5, n=4
    → 两叶在此区域 Y 方向并排重叠 (Blade1 上 [0,+25], Blade2 下 [-25,0]),
       螺栓 (Z=0 一行) 贯穿两叶+夹板, 无空气间隙, 离心力压实传递
  • 过渡区 z∈[+Z_TAB, +0.200] (4 站): 等宽 262mm, 厚 25→50, Y_off 12.5→0, n 4→NACA
    → 在 150mm 内完成由平板到 NACA 桨柄截面的过渡, 已脱出夹板覆盖区

输出 (7 个截面 .sldcrv):
  - cad_sections/root_section_r-0.050_blade1.sldcrv   (tab 起点)
  - cad_sections/root_section_r0.000_blade1.sldcrv    (螺栓中心)
  - cad_sections/root_section_r0.050_blade1.sldcrv    (tab 终点)
  - cad_sections/root_section_r0.087_blade1.sldcrv    (过渡 n=3)
  - cad_sections/root_section_r0.125_blade1.sldcrv    (过渡 n=2.5)
  - cad_sections/root_section_r0.162_blade1.sldcrv    (过渡 n=2)
  - cad_sections/root_section_r0.200_blade1.sldcrv    (NACA 00xx, 对接 shank)
  - cad_sections/_root_summary.txt
  - cad_sections/_root_preview.png

坐标系 (与 blade/shank 一致):
  - 原点 = 转轴中心
  - Z = 叶展 (Blade1 沿 +Z, tab 反向延伸至 -Z)
  - X = 弦向, Y = 厚度方向 (旋转轴方向, 同时也是夹板法向)
  - 截面平面: X-Y @ Z=r

关联:
  - r=0.200 截面 = Domain A shank_section_r0.200.sldcrv (NACA, 完全一致)
  - Blade2 = Blade1 绕 X 轴旋转 180° (Y 翻转 + Z 翻转)
    → Blade2 跨 z∈[-200, +Z_TAB], 与 Blade1 在 z∈[-Z_TAB, +Z_TAB] 区域交叉
========================================================
"""

import os, sys, math
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

# ================================================================
# 1. 参数
# ================================================================

WORK_DIR = r"E:\CCBlade\test\S1223_30KW_AFFiles"
OUT_DIR  = os.path.join(WORK_DIR, "cad_sections")

# ---- 根部平板 (r=0) ----
PLATE_WIDTH     = 262.0     # mm, X 方向宽度 (≥ 电机法兰 PCD 240mm 包络)
PLATE_THICK     = 25.0      # mm, Y 方向厚度
PLATE_Y_OFFSET  = 12.5      # mm, Blade1 根板 Y 偏移 (Blade2 取负)
                             # = PLATE_THICK/2 → Blade1 跨 [0, +25], Blade2 跨 [-25, 0],
                             # 两叶根在 Y=0 平面直接贴合, 离心力直接压实传递

# ---- 交叉 tab (z<0 反向延伸, 用于贯穿夹紧螺栓) ----
Z_TAB           = 50.0      # mm, tab 单边 z 方向延伸长度
                             # Blade1 实际 z 跨度 = [-Z_TAB, +200],
                             # 在 z∈[-Z_TAB, +Z_TAB] 区域两叶恒截面 120×15 重叠,
                             # → 螺栓贯穿无空气, 夹板有效压紧

# ---- 对接面 (r=0.200) ----
SHANK_R         = 0.200     # m
SHANK_WIDTH     = 262.0     # mm  (LE=-131, TE=+131)
SHANK_THICK     = 50.0      # mm

# ---- 过渡站 ----
# (r_m, type, width_mm, thick_mm, y_offset_mm, n_exp)
# type: "superellipse" | "naca_sym"
# r=0.200 为 NACA 00xx, 与 Domain A shank r=0.200 截面完全一致 → 根板放样终点 = 桨柄放样起点
# n_exp: superellipse 形状控制 (2=椭圆, 4=圆角矩形), naca_sym 此项为 None
ROOT_STATIONS = [
    # ── 交叉夹板 tab 区 (恒定 262×25, Y_off=+12.5, n=4): z∈[-Z_TAB, +Z_TAB] ──
    # 这一段两片叶根恒截面重叠, Blade1 占 Y∈[0,+25], Blade2 占 Y∈[-25,0],
    # 螺栓 (Z=0 一行 4 颗) 贯穿两叶 + 前后夹板, 无空气间隙
    (-0.050, "superellipse", 262.0, 25.0,  12.500, 4),    # tab 起点 (反向延伸至 z=-50)
    ( 0.000, "superellipse", 262.0, 25.0,  12.500, 4),    # 螺栓孔中心平面
    ( 0.050, "superellipse", 262.0, 25.0,  12.500, 4),    # tab 终点, 过渡起点
    # ── 过渡区 (等宽 262mm, 厚 25→50 线性, Y_off 12.5→0 线性, 长 150mm): z∈[+Z_TAB, +200] ──
    ( 0.0875, "superellipse", 262.0, 31.25,  9.375, 3),   # frac=0.25
    ( 0.125,  "superellipse", 262.0, 37.50,  6.250, 2.5), # frac=0.50
    ( 0.1625, "superellipse", 262.0, 43.75,  3.125, 2),   # frac=0.75, n=2 纯椭圆
    ( 0.200,  "naca_sym",     262.0, 50.0,   0.000, None),# 对接 Domain A shank, 截面形状一致
]

# ---- 输出参数 ----
RESAMPLE_N      = 100
LOOP_DIRECTION  = "cw"
ALIGN_START     = "principal-pos"   # 起点对齐到主轴正方向 (= TE 端), 与 shank/blade 脚本一致
                                     # → 7 个 root 截面起点统一; r=0.200 root 与 shank 起点对齐
CLOSE_CURVE     = True
DEDUP_TOL_MM    = 1e-3

GENERATE_PREVIEW = True


# ================================================================
# 2. 截面生成
# ================================================================

def naca_sym_thickness(x_norm, t_over_c):
    """NACA 00xx 对称厚度分布 (归一化半厚度)。

    a4=-0.0996 钝 TE: r=0.200 处 TE 全厚≈2mm, 与 shank 脚本一致。
    """
    a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
    a4 = -0.0996
    x = np.maximum(np.asarray(x_norm), 0.0)
    y = (t_over_c / 0.20) * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)
    return np.maximum(y, 0.0)


def make_superellipse(width_mm, thick_mm, y_offset_mm, n_exp, n_pts=100):
    """在 X-Y 平面生成超椭圆闭合曲线。

    超椭圆: |2x/W|^n + |2(y - y_offset)/T|^n = 1
    """
    a = width_mm / 2.0
    b = thick_mm / 2.0

    pts = []
    for i in range(n_pts):
        theta = 2.0 * math.pi * i / n_pts
        c_val = math.cos(theta)
        s_val = math.sin(theta)
        x = math.copysign(1, c_val) * a * (abs(c_val) ** (2.0 / n_exp))
        y = y_offset_mm + math.copysign(1, s_val) * b * (abs(s_val) ** (2.0 / n_exp))
        pts.append((x, y))

    pts.append(pts[0])
    return pts


def make_naca_sym_section(width_mm, thick_mm, y_offset_mm, n_pts=100):
    """在 X-Y 平面生成 NACA 00xx 对称截面。

    用于 r=0.200 对接站 — 与 Domain A shank NACA 截面完全一致,
    确保根板放样终点 = 桨柄放样起点, 消除截面类型不匹配。
    """
    t_over_c = thick_mm / width_mm
    half = n_pts // 2
    theta_vals = np.linspace(0.0, math.pi, half + 1)
    x_norm = (1.0 - np.cos(theta_vals)) / 2.0  # cos spacing, LE/TE 密
    y_half = naca_sym_thickness(x_norm, t_over_c) * width_mm

    upper = []
    for i in range(len(x_norm)):
        x_phys = -width_mm / 2.0 + x_norm[i] * width_mm  # LE at -W/2
        y = y_offset_mm + y_half[i]
        upper.append((x_phys, y))

    lower = []
    for i in range(len(x_norm) - 1, -1, -1):
        x_phys = -width_mm / 2.0 + x_norm[i] * width_mm
        y = y_offset_mm - y_half[i]
        lower.append((x_phys, y))

    pts = upper[:-1] + lower
    pts.append(pts[0])
    return pts


# ================================================================
# 3. Pipeline 工具
# ================================================================

def dedup_consecutive(pts, tol):
    if len(pts) < 2:
        return list(pts)
    out = [pts[0]]
    for p in pts[1:]:
        q = out[-1]
        d2 = (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2
        if d2 < tol * tol:
            continue
        out.append(p)
    return out


def section_centroid(pts):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return cx, cy


def principal_axis(pts):
    """惯性主轴方向 (X-Y 投影). 对于细长截面, 主轴 ≈ 弦向."""
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
    """循环移位曲线起点. 与 shank/blade 脚本同步:
       'principal-pos' = 起点移到沿主轴 +方向投影最大的点 (≈ TE 端).
    """
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
        cum.append(cum[-1] + math.sqrt(dx*dx + dy*dy + dz*dz))
    dx = work[0][0] - work[-1][0]
    dy = work[0][1] - work[-1][1]
    dz = work[0][2] - work[-1][2]
    cum.append(cum[-1] + math.sqrt(dx*dx + dy*dy + dz*dz))
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
            p1[0] + t*(p2[0] - p1[0]),
            p1[1] + t*(p2[1] - p1[1]),
            p1[2] + t*(p2[2] - p1[2]),
        ))
    return out


def write_sldcrv(path, pts):
    with open(path, "wb") as fh:
        for x, y, z in pts:
            fh.write(f"{x:.6f}\t{y:.6f}\t{z:.6f}\r\n".encode("ascii"))


# ================================================================
# 4. 预览
# ================================================================

def plot_root_preview(sections, out_path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("  [skip preview] matplotlib n/a")
        return

    fig = plt.figure(figsize=(14, 8))
    ax3d  = fig.add_subplot(1, 2, 1, projection="3d")
    ax_xy = fig.add_subplot(1, 2, 2)

    cmap = plt.get_cmap("viridis")
    for i, (label, r, pts) in enumerate(sections):
        col = cmap(i / max(len(sections) - 1, 1))
        X = [p[0] for p in pts]; Y = [p[1] for p in pts]; Z = [p[2] for p in pts]
        ax3d.plot(X, Y, Z, color=col, lw=0.8)
        ax_xy.plot(X, Y, color=col, lw=0.8, label=f"{label} r={r:.3f}m")

    ax3d.set_xlabel("X (mm)"); ax3d.set_ylabel("Y (mm)"); ax3d.set_zlabel("Z (mm, span)")
    ax3d.set_title("Root plate 3D")
    ax_xy.set_xlabel("X (mm)"); ax_xy.set_ylabel("Y (mm)"); ax_xy.set_title("X-Y end view")
    ax_xy.set_aspect("equal", adjustable="datalim")
    ax_xy.legend(fontsize=7, loc="best")
    fig.suptitle(f"Root plate sections (Blade 1)  — Y-offset {PLATE_Y_OFFSET:.0f}mm at r=0")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  预览图: {out_path}")


# ================================================================
# 5. 主流程
# ================================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("=" * 90)
    print("  Blade 1 Root Plate Extension — 交叉夹板式根部平板 (含反向 tab)")
    print(f"  Tab 区 z∈[-{Z_TAB:.0f}, +{Z_TAB:.0f}]: 恒 {PLATE_WIDTH:.0f}x{PLATE_THICK:.0f}mm, Y偏移 +{PLATE_Y_OFFSET:.1f}mm")
    print(f"  过渡区 z∈[+{Z_TAB:.0f}, +{SHANK_R*1000:.0f}]: 等宽 {PLATE_WIDTH:.0f}mm, 厚 {PLATE_THICK:.0f}→{SHANK_THICK:.0f}mm (长 {SHANK_R*1000-Z_TAB:.0f}mm)")
    print(f"  形状插值: 超椭圆 n=4→3→2.5→2 → NACA 00xx")
    print("=" * 90)
    print(f"  {'r [m]':>7}  {'type':<14}  {'width':>7}  {'thick':>7}  {'Y-off':>7}  {'n':>5}  {'N_in→out':>10}  file")
    print("-" * 90)

    summary_rows = []
    preview_data = []
    n_written = 0

    for r_m, stype, w_mm, t_mm, y_off, n_exp in ROOT_STATIONS:
        # 生成 2D 截面
        if stype == "superellipse":
            pts_2d = make_superellipse(w_mm, t_mm, y_off, n_exp, n_pts=RESAMPLE_N)
        elif stype == "naca_sym":
            pts_2d = make_naca_sym_section(w_mm, t_mm, y_off, n_pts=RESAMPLE_N)
        else:
            raise ValueError(f"未知截面类型: {stype}")

        # 放置到 Z=r*1000
        pts_3d = [(x, y, r_m * 1000.0) for (x, y) in pts_2d]
        n_raw = len(pts_3d)

        # Pipeline (与 shank/blade 脚本同步)
        pts_dd = dedup_consecutive(pts_3d, DEDUP_TOL_MM)
        pts_dir = enforce_direction(pts_dd, LOOP_DIRECTION)
        # 起点对齐到主轴 +方向 (≈TE 端) → 7 站起点统一,
        # 且 r=0.200 root 截面与 shank 第一站 (r=0.200 ellipse) 起点完全一致
        axis = principal_axis(pts_dir)
        pts_aligned = cyclic_shift_to_start(pts_dir, ALIGN_START, axis=axis)
        pts_resampled = resample_arclength_closed(pts_aligned, RESAMPLE_N)
        if CLOSE_CURVE and (pts_resampled[0] != pts_resampled[-1]):
            pts_final = pts_resampled + [pts_resampled[0]]
        else:
            pts_final = pts_resampled

        fn = f"root_section_r{r_m:.3f}_blade1.sldcrv"
        out_path = os.path.join(OUT_DIR, fn)
        write_sldcrv(out_path, pts_final)

        n_str = f"{n_exp:.1f}" if n_exp is not None else "-"
        print(f"  {r_m:>7.3f}  {stype:<14}  {w_mm:>5.0f}mm  {t_mm:>5.1f}mm  {y_off:>+5.1f}mm  "
              f"{n_str:>5}  {n_raw:>4d} →{len(pts_final):>4d}  {fn}")

        summary_rows.append((r_m, stype, w_mm, t_mm, y_off, n_exp, fn))
        preview_data.append((f"r{r_m:.3f}", r_m, pts_final))
        n_written += 1

    # ---- 汇总 ----
    summary_path = os.path.join(OUT_DIR, "_root_summary.txt")
    with open(summary_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("# Blade 1 Root Plate Extension 汇总\n")
        fh.write(f"# 架构: 交叉夹板式 — 根板延伸穿过毂体中心\n")
        fh.write(f"# Tab 区 z∈[-{Z_TAB:.0f}, +{Z_TAB:.0f}]: 恒 {PLATE_WIDTH:.0f}x{PLATE_THICK:.0f}mm, Y偏移 +{PLATE_Y_OFFSET:.2f}mm (= 半厚)\n")
        fh.write(f"# 过渡区 z∈[+{Z_TAB:.0f}, +{SHANK_R*1000:.0f}]: 等宽 {PLATE_WIDTH:.0f}mm, 厚 {PLATE_THICK:.0f}→{SHANK_THICK:.0f}mm (Domain A shank 起点)\n")
        fh.write(f"# Blade 2: Blade 1 绕 X 轴旋转 180°, 跨 z∈[-200, +{Z_TAB:.0f}]\n")
        fh.write(f"# 交叉重叠区 z∈[-{Z_TAB:.0f}, +{Z_TAB:.0f}]: 两叶恒截面并排 (Blade1 上 Blade2 下), 螺栓贯穿两叶\n")
        fh.write(f"# unit: mm | newline: CRLF | sep: TAB\n#\n")
        fh.write(f"# {'r[m]':>7}  {'type':<14}  {'W[mm]':>7}  {'T[mm]':>7}  {'Yoff[mm]':>8}  {'n':>5}  file\n")
        for row in summary_rows:
            n_str = f"{row[5]:.1f}" if row[5] is not None else "-"
            fh.write(f"  {row[0]:>7.3f}  {row[1]:<14}  {row[2]:>7.1f}  {row[3]:>7.1f}  "
                     f"{row[4]:>+8.1f}  {n_str:>5}  {row[6]}\n")
    print(f"\n  汇总: {summary_path}")

    if GENERATE_PREVIEW and preview_data:
        plot_root_preview(preview_data, os.path.join(OUT_DIR, "_root_preview.png"))

    print(f"\n  完成: 写出 {n_written} 个根板截面 .sldcrv\n")
    print("  SolidWorks 操作:")
    print(f"    1. 插入 7 个 root_section_r*.sldcrv (含反向 tab z=-{Z_TAB:.0f} 起点 + r=+0.200 NACA 终点)")
    print(f"    2. 放样: z=-{Z_TAB:.0f} → 0 → +{Z_TAB:.0f} → +87.5 → +125 → +162.5 → +200")
    print(f"       - tab 段 (z∈[-{Z_TAB:.0f}, +{Z_TAB:.0f}]) 三站全等 → 恒截面棱柱")
    print(f"       - 过渡段 (z∈[+{Z_TAB:.0f}, +200]) 4 站递进 → 平滑 NACA 过渡")
    print("       - 起始/终止约束 = '无'")
    print("    3. Blade 2 根板: 绕 X 轴旋转 Blade 1 整体 180°")
    print(f"       - 旋转后 Blade 2 跨 z∈[-200, +{Z_TAB:.0f}], 与 Blade 1 在 z∈[-{Z_TAB:.0f}, +{Z_TAB:.0f}] 交叉重叠")
    print("       - Blade 1 占 Y∈[0, +25], Blade 2 占 Y∈[-25, 0], 在 Y=0 面贴合")
    print("    4. 螺栓孔: hub 脚本输出 4 颗 M12 在 Z=0 一行, 全部位于交叉 tab 区内")
    print("    5. 合并: Root (z=-50→+200) + Shank (z=200→676) + Aero (z=676→3498) → Single Body")
    print(f"       注意: Domain A shank 起点 = z=200, 与本脚本终点 (NACA {SHANK_WIDTH:.0f}×{SHANK_THICK:.0f}) 完全衔接\n")


if __name__ == "__main__":
    main()
