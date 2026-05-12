"""
export_hub_geometry.py
========================================================
Domain C: 分体式圆柱毂体 — 基准几何导出

两片桨叶根部在毂体中心交汇 (Y=0 平面), 翼型截面 NACA 262×50。
Φ262×50 圆柱体沿 Y 轴在 Y=0 分割为两半:
  - 上半圆柱 (Y∈[0,+25]) 与 Blade 1 合并
  - 下半圆柱 (Y∈[-25,0]) 与 Blade 2 合并
4×M12 螺栓 @ Z=0 贯穿两个半圆柱。

输出:
  - cad_sections/hub_cylinder_split_plane.sldcrv   (分割面圆 Φ262 @ Y=0)
  - cad_sections/hub_cylinder_top_face.sldcrv       (顶面圆 Φ262 @ Y=+25)
  - cad_sections/hub_cylinder_bottom_face.sldcrv    (底面圆 Φ262 @ Y=-25)
  - cad_sections/hub_clamp_bolt_{1..4}.sldcrv       (桨叶夹紧螺栓 4×M12 @ Y=0)
  - cad_sections/hub_motor_bolt_{1..6}.sldcrv       (电机法兰螺栓 @ Y=-25)
  - cad_sections/hub_motor_flange_ref.sldcrv        (电机法兰外圆参考 Ø262 @ Y=-25)
  - cad_sections/hub_shaft_bore.sldcrv              (轴孔 Ø50 @ Y=0)
  - cad_sections/_hub_summary.txt
  - cad_sections/_hub_preview.png

坐标系 (与 blade/shank 一致):
  - 原点 = 转轴中心
  - Z = 叶展方向 (Blade 1 沿 +Z, Blade 2 沿 -Z)
  - Y = 电机轴方向 (旋转轴, 同时也是圆柱轴线)
  - X = 弦向
  - 单位: mm

堆叠 (沿 Y, 分体式圆柱):
  Y=+35.0  上半圆柱顶面 (圆 Φ262)
  Y=+17.5  上半圆柱中心
  Y= 0     分割面 (Blade1/2 翼型截面 Y=0 居中 + 螺栓贯穿平面)
  Y=-17.5  下半圆柱中心
  Y=-35.0  下半圆柱底面 (圆 Φ262, 对接电机法兰)

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

# ---- 圆柱体 ----
CYLINDER_DIAMETER = 262.0     # mm, Φ262
CYLINDER_HALF     = 35.0      # mm, 半高 (总高=70mm)
SPLIT_Y           = 0.0       # mm, 分割面 Y 位置

# ---- 电机法兰接口 ----
MOTOR_FLANGE_D  = 262.0     # mm, 电机法兰外径
MOTOR_BOLT_R    = 120.0     # mm, 电机螺栓分布半径 (PCD=240mm)
MOTOR_BOLT_N    = 6         # 电机螺栓数
MOTOR_BOLT_D    = 12.0      # mm, 电机螺栓公称直径 (M12)
MOTOR_FACE_Y    = -35.0     # mm, 电机法兰面 = 下半圆柱底面

# ---- 桨叶夹紧螺栓 (4×M12 贯穿上下半圆柱, 全部在 Z=0) ----
CLAMP_BOLT_D    = 12.0      # mm, 夹紧螺栓公称直径 (M12)
CLAMP_BOLT_POSITIONS = [    # (X_mm, Z_mm) 在 X-Z 平面
    (-45.0, 0.0),           # 外左
    (-15.0, 0.0),           # 内左
    (+15.0, 0.0),           # 内右
    (+45.0, 0.0),           # 外右
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


def make_cylinder_face_circle(y_mm, label=""):
    """在 X-Z 平面 Y=y_mm 生成圆柱端面圆 (Φ262)。"""
    r = CYLINDER_DIAMETER / 2.0
    return make_circle_3d((0, y_mm, 0), (0, 1, 0), r, RESAMPLE_N)


def make_shaft_bore():
    """轴孔参考圆 (X-Z 平面, Y=SPLIT_Y)。"""
    r = SHAFT_D / 2.0
    return make_circle_3d((0, SPLIT_Y, 0), (0, 1, 0), r, RESAMPLE_N)


def make_clamp_bolt_circles():
    """生成桨叶夹紧螺栓圆 (4×M12 @ Y=SPLIT_Y, Z=0)。"""
    r_bolt = CLAMP_BOLT_D / 2.0
    bolts = {}
    for i, (cx, cz) in enumerate(CLAMP_BOLT_POSITIONS, 1):
        pts = make_circle_3d((cx, SPLIT_Y, cz), (0, 1, 0), r_bolt, RESAMPLE_N // 2)
        bolts[f"clamp_bolt_{i}"] = pts
    return bolts


def make_motor_bolt_circles():
    """生成电机法兰螺栓位置圆 (在下半圆柱底面 Y=MOTOR_FACE_Y)。"""
    r_bolt = MOTOR_BOLT_D / 2.0
    bolts = {}
    for i in range(MOTOR_BOLT_N):
        angle = 2.0 * math.pi * i / MOTOR_BOLT_N
        cx = MOTOR_BOLT_R * math.cos(angle)
        cz = MOTOR_BOLT_R * math.sin(angle)
        pts = make_circle_3d((cx, MOTOR_FACE_Y, cz), (0, 1, 0), r_bolt, RESAMPLE_N // 2)
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
    ax_xz.set_title("X-Z (hub face view)"); ax_xz.set_aspect("equal", adjustable="datalim")
    ax_xz.legend(fontsize=6, loc="best", ncol=2)
    ax_xy.set_xlabel("X"); ax_xy.set_ylabel("Y"); ax_xy.set_title("X-Y (side)")
    ax_xy.set_aspect("equal", adjustable="datalim")
    ax_yz.set_xlabel("Y"); ax_yz.set_ylabel("Z"); ax_yz.set_title("Y-Z (side)")
    ax_yz.set_aspect("equal", adjustable="datalim")

    fig.suptitle(f"Split-cylinder hub  D={CYLINDER_DIAMETER:.0f}mm, half-height={CYLINDER_HALF:.0f}mm")
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
    print("  Domain C: 分体式圆柱毂体 — 翼型直通 r=0 + 圆柱合并")
    print(f"  圆柱: D={CYLINDER_DIAMETER:.0f}mm, 总高={CYLINDER_HALF*2:.0f}mm (半高={CYLINDER_HALF:.0f}mm)")
    print(f"  分割面: Y={SPLIT_Y:+.1f}")
    print(f"  电机法兰: D={MOTOR_FLANGE_D:.0f}mm, {MOTOR_BOLT_N}×M{MOTOR_BOLT_D:.0f} @ R={MOTOR_BOLT_R:.0f}mm (Y={MOTOR_FACE_Y:+.1f})")
    print(f"  桨叶夹紧: 4×M{CLAMP_BOLT_D:.0f} @ Z=0, {CLAMP_BOLT_POSITIONS}")
    print(f"  轴孔: D={SHAFT_D:.0f}mm (占位)")
    print("=" * 90)

    all_curves = {}

    # ---- 圆柱体三个端面圆 ----
    top_y    = SPLIT_Y + CYLINDER_HALF   # +25
    bottom_y = SPLIT_Y - CYLINDER_HALF   # -25

    for y_pos, label in [(SPLIT_Y, "split_plane"), (top_y, "top_face"), (bottom_y, "bottom_face")]:
        pts = make_cylinder_face_circle(y_pos)
        pts = dedup_consecutive(pts, DEDUP_TOL_MM)
        fn = f"hub_cylinder_{label}.sldcrv"
        write_sldcrv(os.path.join(OUT_DIR, fn), pts)
        all_curves[f"cylinder_{label}"] = pts
        print(f"  {fn:<40}  Y={y_pos:+.1f}, D={CYLINDER_DIAMETER:.0f}mm, N={len(pts)}")

    # ---- 桨叶夹紧螺栓 (Y=SPLIT_Y 平面, 贯穿 Cut 上下半圆柱) ----
    clamp_bolts = make_clamp_bolt_circles()
    for name, pts in clamp_bolts.items():
        pts = dedup_consecutive(pts, DEDUP_TOL_MM)
        fn = f"hub_{name}.sldcrv"
        write_sldcrv(os.path.join(OUT_DIR, fn), pts)
        all_curves[name] = pts
        idx = int(name.split("_")[-1]) - 1
        cx_center, cz_center = CLAMP_BOLT_POSITIONS[idx]
        print(f"  {fn:<40}  Y={SPLIT_Y:+.1f}, center=({cx_center:+.1f},{cz_center:+.1f}), D={CLAMP_BOLT_D:.0f}mm, N={len(pts)}")

    # ---- 电机法兰螺栓 (在下半圆柱底面 Y=MOTOR_FACE_Y) ----
    motor_bolts = make_motor_bolt_circles()
    for name, pts in motor_bolts.items():
        pts = dedup_consecutive(pts, DEDUP_TOL_MM)
        fn = f"hub_{name}.sldcrv"
        write_sldcrv(os.path.join(OUT_DIR, fn), pts)
        all_curves[name] = pts
        idx = int(name.split("_")[-1]) - 1
        ang = 2.0 * math.pi * idx / MOTOR_BOLT_N
        cx_center, cz_center = MOTOR_BOLT_R * math.cos(ang), MOTOR_BOLT_R * math.sin(ang)
        print(f"  {fn:<40}  Y={MOTOR_FACE_Y:+.1f}, center=({cx_center:+.1f},{cz_center:+.1f}), D={MOTOR_BOLT_D:.0f}mm, N={len(pts)}")

    # ---- 电机法兰外圆参考 (下半圆柱底面) ----
    flange_pts = make_circle_3d((0, MOTOR_FACE_Y, 0), (0, 1, 0), MOTOR_FLANGE_D / 2.0, RESAMPLE_N)
    flange_pts = dedup_consecutive(flange_pts, DEDUP_TOL_MM)
    fn_flange = "hub_motor_flange_ref.sldcrv"
    write_sldcrv(os.path.join(OUT_DIR, fn_flange), flange_pts)
    all_curves["motor_flange_ref"] = flange_pts
    print(f"  {fn_flange:<40}  Y={MOTOR_FACE_Y:+.1f}, D={MOTOR_FLANGE_D:.0f}mm, N={len(flange_pts)}")

    # ---- 轴孔 (Y=SPLIT_Y) ----
    shaft_pts = make_shaft_bore()
    shaft_pts = dedup_consecutive(shaft_pts, DEDUP_TOL_MM)
    fn_shaft = "hub_shaft_bore.sldcrv"
    write_sldcrv(os.path.join(OUT_DIR, fn_shaft), shaft_pts)
    all_curves["shaft_bore"] = shaft_pts
    print(f"  {fn_shaft:<40}  Y={SPLIT_Y:+.1f}, D={SHAFT_D:.0f}mm, N={len(shaft_pts)}")

    # ---- 汇总 ----
    summary_path = os.path.join(OUT_DIR, "_hub_summary.txt")
    with open(summary_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("# Domain C: 分体式圆柱毂体汇总\n")
        fh.write(f"# 圆柱: D={CYLINDER_DIAMETER:.0f}mm, 半高={CYLINDER_HALF:.0f}mm (总高={CYLINDER_HALF*2:.0f}mm)\n")
        fh.write(f"# 分割面: Y={SPLIT_Y:+.1f}\n")
        fh.write(f"# 上半圆柱 Y∈[0,+{CYLINDER_HALF:.0f}] → 与 Blade 1 合并\n")
        fh.write(f"# 下半圆柱 Y∈[-{CYLINDER_HALF:.0f},0] → 与 Blade 2 合并\n")
        fh.write(f"# 电机法兰: D={MOTOR_FLANGE_D:.0f}mm, {MOTOR_BOLT_N}×M{MOTOR_BOLT_D:.0f} @ R={MOTOR_BOLT_R:.0f}mm (Y={MOTOR_FACE_Y:+.1f})\n")
        fh.write(f"# 桨叶夹紧: 4×M{CLAMP_BOLT_D:.0f} @ Z=0, {CLAMP_BOLT_POSITIONS}\n")
        fh.write(f"# 轴孔: D={SHAFT_D:.0f}mm (占位), 键 {SHAFT_KEY_W:.0f}x{SHAFT_KEY_H:.0f}mm\n")
        fh.write(f"# 叶片: r=0 NACA 262×50 Y=0 居中, shank r=0→0.200→...\n")
        fh.write(f"# unit: mm | newline: CRLF | sep: TAB\n#\n")
        for fn in sorted(os.listdir(OUT_DIR)):
            if fn.startswith("hub_"):
                fh.write(f"#   {fn}\n")
    print(f"\n  汇总: {summary_path}")

    # ---- 预览 ----
    if GENERATE_PREVIEW:
        plot_hub_preview(all_curves, os.path.join(OUT_DIR, "_hub_preview.png"))

    print(f"\n  完成: 写出 {len(all_curves)} 条基准曲线\n")
    print("  SolidWorks 建模:")
    print(f"    1. Blade 1 放样: shank r=0→0.200→0.350→0.500→0.580→0.676 + blade aero")
    print(f"       (r=0 截面: NACA 262×50, Y=0 居中)")
    print(f"    2. 上半圆柱:")
    print(f"       - Y={SPLIT_Y:+.1f} 平面, hub_cylinder_split_plane 为草图")
    print(f"       - Extrude {CYLINDER_HALF:.0f}mm 向 +Y → 上半圆柱 (Y∈[0,+{CYLINDER_HALF:.0f}])")
    print(f"    3. 合并: Blade 1 放样实体 + 上半圆柱 = Final Blade 1 (Combine/Union)")
    print(f"    4. Blade 2: Final Blade 1 绕 X 轴旋转 180°")
    print(f"       - 下半圆柱自动到位 Y∈[-{CYLINDER_HALF:.0f},0]")
    print(f"    5. 装配: Blade 1 上半圆柱 + Blade 2 下半圆柱 → Y=0 面贴合")
    print(f"    6. 夹紧螺栓: hub_clamp_bolt_1~4 (Y={SPLIT_Y:+.1f} 平面), Extruded Cut 沿 Y 贯穿两半圆柱")
    print(f"    7. 电机法兰: hub_motor_bolt_1~{MOTOR_BOLT_N} + hub_motor_flange_ref @ Y={MOTOR_FACE_Y:+.1f} (下半圆柱底面)")
    print(f"       - 从 Y={MOTOR_FACE_Y:+.1f} 钻孔/攻丝 (不通孔, 止于法兰面)")
    print(f"    8. 轴孔 + 键槽 @ Y={SPLIT_Y:+.1f}\n")


if __name__ == "__main__":
    main()
