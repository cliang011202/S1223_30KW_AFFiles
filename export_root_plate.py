"""
export_root_plate.py
========================================================
交叉夹板式架构 — Blade 1 根部平板延伸截面

从 r=0 (中心平板, 叠放夹持) 到 r=0.200 (对接 Domain A NACA 桨柄),
生成超椭圆过渡截面 → .sldcrv, 用于 SolidWorks 放样。

输出:
  - cad_sections/root_section_r0.000_blade1.sldcrv  (中心平板, 超椭圆 n=4)
  - cad_sections/root_section_r0.050_blade1.sldcrv  (超椭圆 n=3)
  - cad_sections/root_section_r0.100_blade1.sldcrv  (超椭圆 n=2.5)
  - cad_sections/root_section_r0.150_blade1.sldcrv  (超椭圆 n=2, 纯椭圆)
  - cad_sections/root_section_r0.200_blade1.sldcrv  (NACA 00xx, 对接 shank)
  - cad_sections/_root_summary.txt
  - cad_sections/_root_preview.png

坐标系 (与 blade/shank 一致):
  - 原点 = 转轴中心
  - Z = 叶展 (blade 1 沿 +Z)
  - X = 弦向, Y = 厚度方向
  - 截面平面: X-Y @ Z=r

关联:
  - r=0.200 截面 = 现有 shank_section_r0.200_ellipse.sldcrv (NACA)
  - r=0 平板与 Blade 2 根板在 Y 方向叠放 (Blade1 偏 +Y, Blade2 偏 -Y)
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
PLATE_WIDTH     = 120.0     # mm, X 方向宽度
PLATE_THICK     = 15.0      # mm, Y 方向厚度
PLATE_Y_OFFSET  = 8.0       # mm, Blade1 根板 Y 偏移 (Blade2 取负)

# ---- 对接面 (r=0.200) ----
SHANK_R         = 0.200     # m
SHANK_WIDTH     = 200.0     # mm  (LE=-100, TE=+100)
SHANK_THICK     = 50.0      # mm

# ---- 过渡站 ----
# (r_m, type, width_mm, thick_mm, y_offset_mm, n_exp)
# type: "superellipse" | "naca_sym"
# r=0.200 为 NACA 00xx, 与 Domain A shank r=0.200 截面完全一致 → 根板放样终点 = 桨柄放样起点
# n_exp: superellipse 形状控制 (2=椭圆, 4=圆角矩形), naca_sym 此项为 None
ROOT_STATIONS = [
    (0.000, "superellipse", 120.0, 15.0,  8.0, 4),     # n=4 圆角, 降应力集中
    (0.050, "superellipse", 140.0, 23.8,  6.0, 3),
    (0.100, "superellipse", 160.0, 32.5,  4.0, 2.5),
    (0.150, "superellipse", 180.0, 41.2,  2.0, 2),     # n=2 纯椭圆, 最接近 NACA
    (0.200, "naca_sym",     200.0, 50.0,  0.0, None),  # 对接 Domain A shank, 截面形状一致
]

# ---- 输出参数 ----
RESAMPLE_N      = 100
LOOP_DIRECTION  = "cw"
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
    print("  Blade 1 Root Plate Extension — 交叉夹板式根部平板延伸截面")
    print(f"  r=0 平板: {PLATE_WIDTH:.0f}x{PLATE_THICK:.0f}mm, Y偏移 +{PLATE_Y_OFFSET:.0f}mm")
    print(f"  r={SHANK_R:.3f} 对接: NACA 00xx, {SHANK_WIDTH:.0f}x{SHANK_THICK:.0f}mm")
    print(f"  过渡: 超椭圆(n=4→2) + NACA @ r=0.200")
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

        # Pipeline
        pts_dd = dedup_consecutive(pts_3d, DEDUP_TOL_MM)
        pts_dir = enforce_direction(pts_dd, LOOP_DIRECTION)
        pts_resampled = resample_arclength_closed(pts_dir, RESAMPLE_N)
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
        fh.write(f"# r=0 平板: {PLATE_WIDTH:.0f}x{PLATE_THICK:.0f}mm, Y偏移 +{PLATE_Y_OFFSET:.0f}mm\n")
        fh.write(f"# r={SHANK_R:.3f} 对接: NACA 00xx (与 Domain A shank 截面一致)\n")
        fh.write(f"# Blade 2 根板: 取 Y 偏移为负 (镜像)\n")
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
    print("    1. 插入 5 个 root_section_r*.sldcrv (含 r=0.200 NACA)")
    print("    2. 放样: r=0 → r=0.050 → r=0.100 → r=0.150 → r=0.200")
    print("       - r=0.200 为 NACA 00xx, 与 Domain A shank 首站截面完全一致")
    print("       - 根板放样终点 (r=0.200) = 桨柄放样起点 → 无接缝")
    print("       - 起始/终止约束 = '无'")
    print("    3. Blade 2 根板: Mirror Body 关于 X-Z 平面 (Y 翻转)")
    print("       - 或旋转 180° 关于 Y 轴, 视叶片相对方位确定")
    print("    4. 根板在 r=0 处有 4×M12 螺栓通孔 (在 hub 脚本中定位)")
    print("    5. 合并: Root (r=0→0.200) + Shank (r=0.200→0.676) + Aero (r=0.676→3.498) → Single Body (Blade 1)\n")


if __name__ == "__main__":
    main()
