"""
export_hub_geometry.py
========================================================
Domain C: 交叉夹板式轮毂 — 基准几何导出

两片桨叶根部平板在中心叠放 (Y 偏移 ±offset),
前后两块圆形夹板 + 4×M12 贯穿螺栓压紧,
中心开轴孔连接电机轴。

输出:
  - cad_sections/hub_clamp_plate_front.sldcrv   (前夹板 Ø280)
  - cad_sections/hub_clamp_plate_rear.sldcrv    (后夹板 Ø280, 对接电机法兰)
  - cad_sections/hub_motor_flange_ref.sldcrv    (电机法兰外圆参考 Ø262)
  - cad_sections/hub_motor_bolt_{1..N}.sldcrv   (电机法兰螺栓 @ R=120)
  - cad_sections/hub_clamp_bolt_{1..4}.sldcrv   (桨叶夹紧螺栓 4×M12)
  - cad_sections/hub_shaft_bore.sldcrv          (轴孔 Ø50)
  - cad_sections/_hub_summary.txt
  - cad_sections/_hub_preview.png

坐标系 (与 blade/shank/root 一致):
  - 原点 = 转轴中心 + 桨叶平面交点
  - Z = 叶展方向 (blade 1 沿 +Z, blade 2 沿 -Z)
  - Y = 电机轴方向 (旋转轴, 同时也是夹板法向)
  - X = 弦向
  - 单位: mm

堆叠 (沿 Y):
  Y=+28  前夹板外表面 (Ø280, 厚 12mm, 从 Y=+16 向 +Y 挤出)
  Y=+16  前夹板内表面 (贴 Blade1 顶面 +15.5, 0.5mm 过盈)
  Y=+8   Blade 1 根板 (120×15mm 平板)
  Y=-8   Blade 2 根板 (120×15mm 平板, Blade1 的 Y 镜像)
  Y=-16  后夹板内表面 (贴 Blade2 底面 -15.5, 0.5mm 过盈)
  Y=-28  后夹板外表面 (Ø280, 厚 12mm, 从 Y=-16 向 -Y 挤出, 对接电机法兰)

可调参数 → 修改 §1 重跑
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

# ---- 夹板 ----
CLAMP_DIAMETER  = 280.0     # mm, 圆形夹板外径 (匹配电机法兰 Ø262)
CLAMP_THICK     = 12.0      # mm, 夹板厚度
# 桨叶根板 r=0 截面 Y 范围: Blade1 [+0.5, +15.5], Blade2 [-15.5, -0.5]
# 夹板内表面紧贴桨叶外表面 (0.5mm 过盈由螺栓预紧消除)
CLAMP_FRONT_Y   = 16.0      # mm, 前夹板内表面 Y 位置 (贴 Blade1 顶面 +15.5)
CLAMP_REAR_Y    = -16.0     # mm, 后夹板内表面 Y 位置 (贴 Blade2 底面 -15.5)

# ---- 电机法兰接口 ----
MOTOR_FLANGE_D  = 262.0     # mm, 电机法兰外径
MOTOR_BOLT_R    = 120.0     # mm, 电机螺栓分布半径 (PCD=240mm)
MOTOR_BOLT_N    = 6         # 电机螺栓数
MOTOR_BOLT_D    = 12.0      # mm, 电机螺栓公称直径 (M12)

# ---- 桨叶夹紧螺栓 (4×M12 贯穿, 近中心) ----
CLAMP_BOLT_D    = 12.0      # mm, 夹紧螺栓公称直径 (M12)
CLAMP_BOLT_POSITIONS = [    # (X_mm, Z_mm) 在 X-Z 平面, 根板重叠区
    (+35.0, +15.0),
    (-35.0, +15.0),
    (-35.0, -15.0),
    (+35.0, -15.0),
]

# ---- 轴接口 ----
SHAFT_D         = 50.0      # mm, 电机轴径 (占位)
SHAFT_KEY_W     = 14.0      # mm, 键槽宽 (A 型平键)
SHAFT_KEY_H     = 9.0       # mm, 键槽深 (毂体侧)

# ---- 输出参数 ----
RESAMPLE_N      = 120
DEDUP_TOL_MM    = 1e-3

GENERATE_PREVIEW = True


# ================================================================
# 2. 几何生成
# ================================================================

def make_circle_3d(center, normal, radius, n):
    """在指定平面内生成 3D 闭合圆。"""
    nx, ny, nz = normal
    nl = math.sqrt(nx*nx + ny*ny + nz*nz)
    nx, ny, nz = nx/nl, ny/nl, nz/nl

    if abs(nx) < 0.9:
        ux, uy, uz = 1.0, 0.0, 0.0
    else:
        ux, uy, uz = 0.0, 1.0, 0.0
    dot = ux*nx + uy*ny + uz*nz
    ux, uy, uz = ux - dot*nx, uy - dot*ny, uz - dot*nz
    ul = math.sqrt(ux*ux + uy*uy + uz*uz)
    ux, uy, uz = ux/ul, uy/ul, uz/ul
    vx = ny*uz - nz*uy
    vy = nz*ux - nx*uz
    vz = nx*uy - ny*ux

    cx, cy, cz = center
    pts = []
    for i in range(n):
        theta = 2.0 * math.pi * i / n
        x = cx + radius * (ux*math.cos(theta) + vx*math.sin(theta))
        y = cy + radius * (uy*math.cos(theta) + vy*math.sin(theta))
        z = cz + radius * (uz*math.cos(theta) + vz*math.sin(theta))
        pts.append((x, y, z))
    pts.append(pts[0])
    return pts


def make_clamp_plate(y_mm):
    """在 X-Z 平面 Y=y_mm 生成圆形夹板外轮廓 + 中心轴孔。"""
    r = CLAMP_DIAMETER / 2.0
    return make_circle_3d((0, y_mm, 0), (0, 1, 0), r, RESAMPLE_N)


def make_shaft_bore():
    """轴孔参考圆 (X-Z 平面, Y=0)。"""
    r = SHAFT_D / 2.0
    return make_circle_3d((0, 0, 0), (0, 1, 0), r, RESAMPLE_N)


def make_clamp_bolt_circles():
    """生成桨叶夹紧螺栓圆 (4×, 近中心, Y=0 平面)。"""
    r_bolt = CLAMP_BOLT_D / 2.0
    bolts = {}
    for i, (cx, cz) in enumerate(CLAMP_BOLT_POSITIONS, 1):
        pts = make_circle_3d((cx, 0, cz), (0, 1, 0), r_bolt, RESAMPLE_N // 2)
        bolts[f"clamp_bolt_{i}"] = pts
    return bolts


def make_motor_bolt_circles():
    """生成电机法兰螺栓位置圆 (在后夹板 Y=CLAMP_REAR_Y 平面)。"""
    r_bolt = MOTOR_BOLT_D / 2.0
    bolts = {}
    for i in range(MOTOR_BOLT_N):
        angle = 2.0 * math.pi * i / MOTOR_BOLT_N
        cx = MOTOR_BOLT_R * math.cos(angle)
        cz = MOTOR_BOLT_R * math.sin(angle)
        pts = make_circle_3d((cx, CLAMP_REAR_Y, cz), (0, 1, 0), r_bolt, RESAMPLE_N // 2)
        bolts[f"motor_bolt_{i+1}"] = pts
    return bolts


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


def write_sldcrv(path, pts):
    with open(path, "wb") as fh:
        for x, y, z in pts:
            fh.write(f"{x:.6f}\t{y:.6f}\t{z:.6f}\r\n".encode("ascii"))


# ================================================================
# 4. 预览
# ================================================================

def plot_hub_preview(curves, out_path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("  [skip preview] matplotlib n/a")
        return

    fig = plt.figure(figsize=(14, 10))
    ax3d  = fig.add_subplot(2, 2, 1, projection="3d")
    ax_xz = fig.add_subplot(2, 2, 2)
    ax_xy = fig.add_subplot(2, 2, 3)
    ax_yz = fig.add_subplot(2, 2, 4)

    cmap = plt.get_cmap("tab10")
    for i, (name, pts) in enumerate(curves.items()):
        col = cmap(i % 10)
        X, Y, Z = [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts]
        ax3d.plot(X, Y, Z, color=col, lw=0.8)
        ax_xz.plot(X, Z, color=col, lw=0.8, label=name)
        ax_xy.plot(X, Y, color=col, lw=0.8)
        ax_yz.plot(Y, Z, color=col, lw=0.8)

    ax3d.set_xlabel("X"); ax3d.set_ylabel("Y"); ax3d.set_zlabel("Z"); ax3d.set_title("Hub 3D")
    ax_xz.set_xlabel("X"); ax_xz.set_ylabel("Z")
    ax_xz.set_title("X-Z (clamp face view)"); ax_xz.set_aspect("equal", adjustable="datalim")
    ax_xz.legend(fontsize=6, loc="best", ncol=2)
    ax_xy.set_xlabel("X"); ax_xy.set_ylabel("Y"); ax_xy.set_title("X-Y (side)")
    ax_xy.set_aspect("equal", adjustable="datalim")
    ax_yz.set_xlabel("Y"); ax_yz.set_ylabel("Z"); ax_yz.set_title("Y-Z (side)")
    ax_yz.set_aspect("equal", adjustable="datalim")

    fig.suptitle(f"Cross-clamp hub  D={CLAMP_DIAMETER:.0f}mm, motor flange D={MOTOR_FLANGE_D:.0f}mm")
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
    print("  Domain C: 交叉夹板式轮毂 — 适配电机制造商法兰")
    print(f"  夹板: Ø{CLAMP_DIAMETER:.0f}mm x {CLAMP_THICK:.0f}mm 厚")
    print(f"  电机法兰: Ø{MOTOR_FLANGE_D:.0f}mm, {MOTOR_BOLT_N}×M{MOTOR_BOLT_D:.0f} @ R={MOTOR_BOLT_R:.0f}mm")
    print(f"  桨叶夹紧: 4×M{CLAMP_BOLT_D:.0f} 贯穿, {CLAMP_BOLT_POSITIONS}")
    print(f"  轴孔: Ø{SHAFT_D:.0f}mm (占位)")
    print("=" * 90)

    all_curves = {}

    # ---- 前后夹板 ----
    for y_pos, label in [(CLAMP_FRONT_Y, "front"), (CLAMP_REAR_Y, "rear")]:
        pts = make_clamp_plate(y_pos)
        pts = dedup_consecutive(pts, DEDUP_TOL_MM)
        fn = f"hub_clamp_plate_{label}.sldcrv"
        write_sldcrv(os.path.join(OUT_DIR, fn), pts)
        all_curves[f"clamp_{label}"] = pts
        print(f"  {fn:<40}  Y={y_pos:+.0f}, D={CLAMP_DIAMETER:.0f}mm, N={len(pts)}")

    # ---- 前夹板桨叶夹紧螺栓 (Y=0 平面投影, 用于贯穿 Cut) ----
    clamp_bolts = make_clamp_bolt_circles()
    for name, pts in clamp_bolts.items():
        pts = dedup_consecutive(pts, DEDUP_TOL_MM)
        fn = f"hub_{name}.sldcrv"
        write_sldcrv(os.path.join(OUT_DIR, fn), pts)
        all_curves[name] = pts
        x, _, z = pts[0][0], pts[0][1], pts[0][2]
        print(f"  {fn:<40}  X={x:+.1f}, Z={z:+.1f}, D={CLAMP_BOLT_D:.0f}mm, N={len(pts)}")

    # ---- 后夹板电机法兰螺栓 ----
    motor_bolts = make_motor_bolt_circles()
    for name, pts in motor_bolts.items():
        pts = dedup_consecutive(pts, DEDUP_TOL_MM)
        fn = f"hub_{name}.sldcrv"
        write_sldcrv(os.path.join(OUT_DIR, fn), pts)
        all_curves[name] = pts
        r_calc = math.sqrt(pts[0][0]**2 + pts[0][2]**2)
        print(f"  {fn:<40}  Y={CLAMP_REAR_Y:+.0f}, R={r_calc:.0f}mm, D={MOTOR_BOLT_D:.0f}mm, N={len(pts)}")

    # ---- 电机法兰外圆参考 (后夹板平面) ----
    flange_pts = make_circle_3d((0, CLAMP_REAR_Y, 0), (0, 1, 0), MOTOR_FLANGE_D / 2.0, RESAMPLE_N)
    flange_pts = dedup_consecutive(flange_pts, DEDUP_TOL_MM)
    fn_flange = "hub_motor_flange_ref.sldcrv"
    write_sldcrv(os.path.join(OUT_DIR, fn_flange), flange_pts)
    all_curves["motor_flange_ref"] = flange_pts
    print(f"  {fn_flange:<40}  Y={CLAMP_REAR_Y:+.0f}, D={MOTOR_FLANGE_D:.0f}mm, N={len(flange_pts)}")

    # ---- 轴孔 ----
    shaft_pts = make_shaft_bore()
    shaft_pts = dedup_consecutive(shaft_pts, DEDUP_TOL_MM)
    fn_shaft = "hub_shaft_bore.sldcrv"
    write_sldcrv(os.path.join(OUT_DIR, fn_shaft), shaft_pts)
    all_curves["shaft_bore"] = shaft_pts
    print(f"  {fn_shaft:<40}  D={SHAFT_D:.0f}mm, N={len(shaft_pts)}")

    # ---- 汇总 ----
    summary_path = os.path.join(OUT_DIR, "_hub_summary.txt")
    with open(summary_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("# Domain C: 交叉夹板式轮毂汇总\n")
        fh.write(f"# 夹板: Ø{CLAMP_DIAMETER:.0f}mm x {CLAMP_THICK:.0f}mm, 前 Y=+{CLAMP_FRONT_Y:.0f}, 后 Y={CLAMP_REAR_Y:.0f}\n")
        fh.write(f"# 电机法兰: Ø{MOTOR_FLANGE_D:.0f}mm, {MOTOR_BOLT_N}×M{MOTOR_BOLT_D:.0f} @ R={MOTOR_BOLT_R:.0f}mm\n")
        fh.write(f"# 桨叶夹紧: 4×M{CLAMP_BOLT_D:.0f} 贯穿, {CLAMP_BOLT_POSITIONS}\n")
        fh.write(f"# 轴孔: Ø{SHAFT_D:.0f}mm (占位), 键 {SHAFT_KEY_W:.0f}x{SHAFT_KEY_H:.0f}mm\n")
        fh.write(f"# 根板叠放: Blade1 Y=+8, Blade2 Y=-8\n")
        fh.write(f"# unit: mm | newline: CRLF | sep: TAB\n#\n")
        for fn in sorted(os.listdir(OUT_DIR)):
            if fn.startswith("hub_"):
                fh.write(f"#   {fn}\n")
    print(f"\n  汇总: {summary_path}")

    # ---- 预览 ----
    if GENERATE_PREVIEW:
        plot_hub_preview(all_curves, os.path.join(OUT_DIR, "_hub_preview.png"))

    print(f"\n  完成: 写出 {len(all_curves)} 条基准曲线\n")
    front_outer = CLAMP_FRONT_Y + CLAMP_THICK
    rear_outer  = CLAMP_REAR_Y - CLAMP_THICK
    print("  SolidWorks 建模:")
    print("    1. 后夹板 (电机接口):")
    print(f"       - Y={CLAMP_REAR_Y:.0f} 平面, hub_clamp_plate_rear 为草图")
    print(f"       - Extrude {CLAMP_THICK:.0f}mm 向 -Y → 外表面 Y={rear_outer:.0f}")
    print(f"       - hub_motor_bolt_1~{MOTOR_BOLT_N} + hub_motor_flange_ref 定位电机法兰孔")
    print("    2. 前夹板:")
    print(f"       - Y={CLAMP_FRONT_Y:.0f} 平面, Extrude {CLAMP_THICK:.0f}mm 向 +Y → 外表面 Y={front_outer:.0f}")
    print(f"       - 内表面 Y={CLAMP_FRONT_Y:.0f} 贴合 Blade1 根板顶面")
    print("    3. Blade 根板:")
    print("       - Blade 1: root_section_r*.sldcrv (含 r=0.200 NACA) 放样 + shank + aero")
    print("       - Blade 2: Mirror (Y flip) Blade 1")
    print("    4. 装配堆叠:")
    print(f"       前夹板 | Blade1 (Y≈+0.5~+15.5) | Blade2 (Y≈-15.5~-0.5) | 后夹板")
    print(f"    5. 桨叶夹紧孔: hub_clamp_bolt_1~4, Extruded Cut 沿 Y 贯穿 4 层")
    print(f"    6. 电机法兰孔: hub_motor_bolt_1~{MOTOR_BOLT_N}, 后夹板 Extruded Cut")
    print("    7. 轴孔 + 键槽 + 倒角\n")


if __name__ == "__main__":
    main()
