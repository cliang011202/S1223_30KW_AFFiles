"""
export_shank_sections.py
========================================================
桨柄段截面导出 — cad_case4 版本

从适配桨毂尺寸的翼型面 (z=0.000 m) 过渡到 QBlade 气动翼型面 (z=0.530 m)。
生成 shank 截面 → .sldcrv, 用于 SolidWorks 放样。

缩放策略 (匹配桨毂圆柱 Φ280×70):
  - 对 sec03 翼型做 PCA 分解为弦向 + 厚度方向
  - 弦向缩放至 ~280mm (匹配圆柱直径)
  - 厚度方向缩放至 ~70mm (匹配圆柱厚度)
  - 保持翼型基本形状, t/c=25%, 有一定气动性能

截面布局:
  z=0.000 m : 缩小翼型 (chord~280, thickness~70)
  z=0.260 m : 过渡形 (morph)
  z=0.530 m : 气动翼型 (复用 Futher_Op_com4_sec03_z0.530.sldcrv)

桨毂: 圆柱 Φ280×70mm, 圆面在 YZ 平面, X 轴旋转轴, 形心在原点
  桨柄实体与桨毂实体交汇并合并

输出到: CAD/cad_case4/

坐标系 (与 QBlade 导出一致):
  - 原点 = 桨距轴
  - Z = 叶展方向
  - 单位: mm
========================================================
"""

import os, sys, math

sys.stdout.reconfigure(encoding="utf-8")


# ================================================================
# 1. 参数
# ================================================================

WORK_DIR = r"E:\CCBlade\test\S1223_30KW_AFFiles"
OUT_DIR  = os.path.join(WORK_DIR, "CAD", "cad_case4")

# ---- 目标翼型: QBlade 导出 sec03 (z=0.530 m) ----
SEC03_PATH = os.path.join(OUT_DIR, "1", "Futher_Op_com4_sec03_z0.530.sldcrv")

# ---- 缩小翼型 @ z=0.000 (匹配桨毂圆柱 Φ280×70) ----
CHORD_SCALE     = 0.63  # 弦向缩放倍数 → 弦长 ~280mm (匹配圆柱直径)
THICKNESS_SCALE = 0.40  # 厚度缩放倍数 → 厚度 ~70mm (匹配圆柱厚度), t/c≈25%

# ---- 过渡截面 Z 位置 (m) ----
# z=0.260 是 z=0.000→0.530 的约一半位置
MORPH_Z = [0.260]

# ---- 基础名 ----
BASE_NAME = "Futher_Op_com4"

# ---- pipeline 参数 ----
N_PTS          = 100        # 每条曲线的唯一点数 (重采样后)
ALIGN_START    = "principal-pos"
LOOP_DIRECTION = "cw"
CLOSE_CURVE    = True
DEDUP_TOL_MM   = 1e-3


# ================================================================
# 2. 文件 I/O
# ================================================================

def read_sldcrv(path):
    pts = []
    with open(path, "r") as fh:
        for line in fh:
            tok = line.strip().split("\t")
            if len(tok) == 3:
                pts.append((float(tok[0]), float(tok[1]), float(tok[2])))
    return pts


def write_sldcrv(path, pts):
    with open(path, "wb") as fh:
        for x, y, z in pts:
            fh.write(f"{x:.6f}\t{y:.6f}\t{z:.6f}\r\n".encode("ascii"))


# ================================================================
# 3. 翼型加厚
# ================================================================

def scale_airfoil(pts_open, chord_scale, thick_scale):
    """
    在弦向和厚度方向上分别缩放翼型。

    用 PCA 分解为弦向 (主成分) 和厚度方向 (次成分),
    弦向缩放 chord_scale 倍, 厚度方向缩放 thick_scale 倍。
    返回缩放后的点列 (保持原顺序, 不含 Z 闭合点)。
    """
    cx = sum(p[0] for p in pts_open) / len(pts_open)
    cy = sum(p[1] for p in pts_open) / len(pts_open)

    sxx = syy = sxy = 0.0
    for x, y, _ in pts_open:
        dx, dy = x - cx, y - cy
        sxx += dx * dx; syy += dy * dy; sxy += dx * dy
    n = len(pts_open)
    sxx /= n; syy /= n; sxy /= n

    tr = sxx + syy
    det = sxx * syy - sxy * sxy
    disc = max(0.0, tr * tr / 4.0 - det)
    lam1 = tr / 2.0 + math.sqrt(disc)  # 大特征值 → 弦向

    if abs(sxy) > 1e-18:
        ux_c, uy_c = lam1 - syy, sxy
    else:
        ux_c, uy_c = (1.0, 0.0) if sxx >= syy else (0.0, 1.0)
    norm = math.hypot(ux_c, uy_c) or 1.0
    ux_c, uy_c = ux_c / norm, uy_c / norm

    # 厚度方向 = 弦向逆时针旋转 90° (右手系, +Z 朝外)
    ux_t, uy_t = -uy_c, ux_c

    out = []
    for x, y, z in pts_open:
        dx, dy = x - cx, y - cy
        chord_proj  = dx * ux_c + dy * uy_c
        thick_proj  = dx * ux_t + dy * uy_t
        new_chord   = chord_proj * chord_scale
        new_thick   = thick_proj * thick_scale
        new_x = cx + new_chord * ux_c + new_thick * ux_t
        new_y = cy + new_chord * uy_c + new_thick * uy_t
        out.append((new_x, new_y, z))

    return out


def shift_pitch_axis(pts_open, ux_c, uy_c, target_chord_pct):
    """
    沿弦向平移截面, 使原点 (变桨轴) 落在 target_chord_pct% 弦长处。
    保持截面形状不变, 仅改变其相对于变桨轴的位置。
    """
    # 各点在弦向上的投影 (以原点为参考, 原点投影=0)
    chord_proj = [p[0] * ux_c + p[1] * uy_c for p in pts_open]
    le_proj = min(chord_proj)
    te_proj = max(chord_proj)
    chord_len = te_proj - le_proj

    # 目标: 原点投影 = le_proj + target_chord_pct/100 * chord_len
    # 平移后 new_le = le_proj + shift, 要求 0 = new_le + pct*chord_len
    # → shift = -(le_proj + pct * chord_len)
    target_origin_proj = le_proj + (target_chord_pct / 100.0) * chord_len
    shift = -target_origin_proj

    out = []
    for x, y, z in pts_open:
        out.append((x + shift * ux_c, y + shift * uy_c, z))
    return out


# ================================================================
# 4. Pipeline 工具
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
    for i in range(len(pts)):
        x1, y1, _ = pts[i]
        x2, y2, _ = pts[(i + 1) % len(pts)]
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
    if len(work) >= 2 and (
        abs(work[0][0] - work[-1][0]) < 1e-9 and
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
            p1[0] + t * (p2[0] - p1[0]),
            p1[1] + t * (p2[1] - p1[1]),
            p1[2] + t * (p2[2] - p1[2]),
        ))
    return out


# ================================================================
# 5. 截面处理 pipeline
# ================================================================

def process_section(pts, n_unique=N_PTS, align=True):
    """标准 pipeline: dedup → direction → [PCA-align] → resample → close。"""
    pts_dd, n_dup = dedup_consecutive(pts, DEDUP_TOL_MM)
    pts_dir = enforce_direction(pts_dd, LOOP_DIRECTION)
    if align:
        axis = principal_axis(pts_dir)
        pts_aligned = cyclic_shift_to_start(pts_dir, ALIGN_START, axis=axis)
    else:
        pts_aligned = pts_dir
    pts_resampled = resample_arclength_closed(pts_aligned, n_unique)
    if CLOSE_CURVE and len(pts_resampled) >= 2 and pts_resampled[0] != pts_resampled[-1]:
        pts_final = pts_resampled + [pts_resampled[0]]
    else:
        pts_final = pts_resampled
    return pts_final, n_dup


def get_open_curve(pts):
    if len(pts) >= 2 and pts[0] == pts[-1]:
        return pts[:-1]
    return list(pts)


# ================================================================
# 6. 截面 morph: 按上下表面分片插值
# ================================================================

def split_upper_lower(pts_open):
    """
    将去闭合曲线在 LE 和 TE 处分为上表面 (TE→LE) 和下表面 (LE→TE)。
    用 PCA 弦向投影极值找 TE/LE。
    """
    if len(pts_open) < 4:
        return list(pts_open), []

    cx = sum(p[0] for p in pts_open) / len(pts_open)
    cy = sum(p[1] for p in pts_open) / len(pts_open)
    sxx = sum((p[0] - cx)**2 for p in pts_open)
    syy = sum((p[1] - cy)**2 for p in pts_open)
    sxy = sum((p[0] - cx) * (p[1] - cy) for p in pts_open)

    if abs(sxy) > 1e-18:
        tr = sxx + syy
        det = sxx * syy - sxy * sxy
        disc = max(0.0, tr * tr / 4.0 - det)
        lam1 = tr / 2.0 + math.sqrt(disc)
        ux, uy = lam1 - syy, sxy
        norm = math.hypot(ux, uy) or 1.0
        ux, uy = ux / norm, uy / norm
    else:
        ux, uy = 1.0, 0.0

    proj = [(p[0] - cx) * ux + (p[1] - cy) * uy for p in pts_open]
    i_te = max(range(len(pts_open)), key=lambda i: proj[i])
    i_le = min(range(len(pts_open)), key=lambda i: proj[i])

    n = len(pts_open)
    if i_te < i_le:
        upper = pts_open[i_te:i_le + 1]
        lower = pts_open[i_le:] + pts_open[:i_te + 1]
    else:
        upper = pts_open[i_te:] + pts_open[:i_le + 1]
        lower = pts_open[i_le:i_te + 1]

    return upper, lower


def resample_arc_open(pts_open, n_out):
    if n_out < 2 or len(pts_open) < 2:
        return list(pts_open)
    cum = [0.0]
    for i in range(1, len(pts_open)):
        dx = pts_open[i][0] - pts_open[i - 1][0]
        dy = pts_open[i][1] - pts_open[i - 1][1]
        cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy))
    total = cum[-1]
    if total <= 0:
        return [pts_open[int(i * (len(pts_open) - 1) / (n_out - 1))] for i in range(n_out)]
    out = [pts_open[0]]
    j = 1
    for k in range(1, n_out - 1):
        s = total * k / (n_out - 1)
        while j < len(cum) - 1 and cum[j] < s:
            j += 1
        seg = cum[j] - cum[j - 1] or 1.0
        t = (s - cum[j - 1]) / seg
        t = max(0.0, min(1.0, t))
        x = pts_open[j - 1][0] + t * (pts_open[j][0] - pts_open[j - 1][0])
        y = pts_open[j - 1][1] + t * (pts_open[j][1] - pts_open[j - 1][1])
        out.append((x, y))
    out.append(pts_open[-1])
    return out


def morph_sections_smart(pts_from_open, pts_to_open, fraction, z_mm, n_half=50):
    """
    按上下表面分片 morph: TE→LE (upper) 和 LE→TE (lower) 各自插值,
    保持 LE/TE 位置对应, 避免弧长参数错位导致的中间截面塌缩。
    """
    upper_f, lower_f = split_upper_lower(pts_from_open)
    upper_t, lower_t = split_upper_lower(pts_to_open)

    upper_f = resample_arc_open(upper_f, n_half)
    lower_f = resample_arc_open(lower_f, n_half)
    upper_t = resample_arc_open(upper_t, n_half)
    lower_t = resample_arc_open(lower_t, n_half)

    out_upper = []
    for i in range(n_half):
        x = upper_f[i][0] + fraction * (upper_t[i][0] - upper_f[i][0])
        y = upper_f[i][1] + fraction * (upper_t[i][1] - upper_f[i][1])
        out_upper.append((x, y, z_mm))

    out_lower = []
    for i in range(n_half):
        x = lower_f[i][0] + fraction * (lower_t[i][0] - lower_f[i][0])
        y = lower_f[i][1] + fraction * (lower_t[i][1] - lower_f[i][1])
        out_lower.append((x, y, z_mm))

    # 拼接: upper (TE→LE) + lower(1:-1) (LE→TE, 去重 LE)
    out = out_upper + out_lower[1:]
    out.append(out[0])
    return out


# ================================================================
# 7. 主流程
# ================================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- 7a. 读取目标翼型 (sec03 @ z=0.530) ----
    sec03_raw = read_sldcrv(SEC03_PATH)
    if not sec03_raw:
        print(f"ERROR: 无法读取 {SEC03_PATH}", file=sys.stderr)
        sys.exit(1)
    z_target = sec03_raw[0][2] / 1000.0  # m
    print(f"目标翼型: {SEC03_PATH}")
    print(f"  原始点数: {len(sec03_raw)}, Z = {z_target:.3f} m")

    # ---- 7b. 处理目标翼型 (pipeline → open) ----
    sec03_processed, n_dup = process_section(sec03_raw)
    sec03_open = get_open_curve(sec03_processed)
    print(f"  pipeline 后: {len(sec03_open)} 唯一点 (去重 {n_dup})")

    # PCA 轴 (从 sec03 获取, 所有截面共用)
    ux_c, uy_c = principal_axis(sec03_open)
    ux_t, uy_t = -uy_c, ux_c

    # Helper: 计算变桨轴 (原点) 在弦向的百分比位置
    def pitch_chord_pct(pts_open, ux_c, uy_c):
        proj = [p[0] * ux_c + p[1] * uy_c for p in pts_open]
        le = min(proj); te = max(proj)
        chord = te - le
        if chord < 1e-6:
            return 50.0
        return (0.0 - le) / chord * 100.0  # 原点投影 = 0

    # Helper: chord/thickness span
    def span_in_dir(pts_open, ux, uy):
        proj = [p[0] * ux + p[1] * uy for p in pts_open]
        return max(proj) - min(proj)

    # 变桨轴目标位置
    PITCH_PCT_ROOT  = 50.0   # z=0.000: 50% chord
    PITCH_PCT_MORPH = 40.0   # z=0.260: ~40% chord
    # sec03 固定 (QBlade), 大约 35%

    print(f"  sec03 变桨轴: {pitch_chord_pct(sec03_open, ux_c, uy_c):.1f}% chord")
    print(f"  sec03 弦向 ~{span_in_dir(sec03_open, ux_c, uy_c):.0f}mm, 厚度 ~{span_in_dir(sec03_open, ux_t, uy_t):.0f}mm")

    # ---- 7c. 生成缩小翼型 @ z=0.000 (匹配桨毂圆柱 Φ280×70) ----
    z_root = 0.000
    z_root_mm = z_root * 1000.0
    root_open_scaled = scale_airfoil(sec03_open, CHORD_SCALE, THICKNESS_SCALE)

    # 平移使变桨轴到 50% chord
    root_open_shifted = shift_pitch_axis(root_open_scaled, ux_c, uy_c, PITCH_PCT_ROOT)

    # 更新 Z 坐标
    root_open_final = [(x, y, z_root_mm) for x, y, _ in root_open_shifted]
    # 闭合 → pipeline (no realign, keep TE correspondence)
    root_closed = root_open_final + [root_open_final[0]]
    root_processed, _ = process_section(root_closed, align=False)

    chord_root = span_in_dir(root_open_final, ux_c, uy_c)
    thick_root = span_in_dir(root_open_final, ux_t, uy_t)
    t_c = thick_root / chord_root * 100
    pct_root_actual = pitch_chord_pct(root_open_final, ux_c, uy_c)
    print(f"缩小翼型 @ z={z_root:.3f}m: chord~{chord_root:.0f}mm, thick~{thick_root:.0f}mm, t/c~{t_c:.1f}%")
    print(f"  变桨轴: {pct_root_actual:.1f}% chord (target {PITCH_PCT_ROOT:.0f}%)")

    # ---- 7d. 生成 morph 过渡截面 ----
    morph_stations = [(z_root, "root", root_processed)]

    for z_m in MORPH_Z:
        frac = (z_target - z_m) / (z_target - z_root)  # 0=全root, 1=全sec03
        z_mm = z_m * 1000.0
        root_open_for_morph = get_open_curve(root_processed)
        morph_pts = morph_sections_smart(root_open_for_morph, sec03_open, frac, z_mm, n_half=N_PTS // 2)
        morph_processed, _ = process_section(morph_pts, align=False)
        morph_open = get_open_curve(morph_processed)
        pct_morph = pitch_chord_pct(morph_open, ux_c, uy_c)
        morph_stations.append((z_m, "morph", morph_processed))
        print(f"过渡截面 @ z={z_m:.3f}m: fraction={frac:.3f}, 变桨轴={pct_morph:.1f}% chord")

    # sec03 as the final station
    morph_stations.append((z_target, "airfoil", sec03_processed))

    # ---- 7e. 写出文件 ----
    print()
    print("=" * 110)
    print(f"  桨柄段截面导出 — cad_case4")
    print(f"  策略: chord×{CHORD_SCALE} thick×{THICKNESS_SCALE} @ z=0 → morph → sec03 @ z=0.530")
    print(f"  变桨轴: root={PITCH_PCT_ROOT:.0f}% → morph≈{PITCH_PCT_MORPH:.0f}% → sec03≈{pitch_chord_pct(sec03_open, ux_c, uy_c):.0f}% chord")
    print(f"  Pipeline: dedup<{DEDUP_TOL_MM}mm → dir={LOOP_DIRECTION}"
          f" → align_start={ALIGN_START} → resample N={N_PTS} → closed={CLOSE_CURVE}")
    print(f"  输出: {OUT_DIR}")
    print("=" * 110)
    print(f"  {'z [m]':>7}  {'type':<8}  {'N':>5}  {'chord':>8}  {'thick':>7}  {'t/c':>6}  {'pitch':>7}  file")
    print("-" * 110)

    for z_m, stype, pts in morph_stations:
        pts_open = get_open_curve(pts)
        ch = span_in_dir(pts_open, ux_c, uy_c)
        th = span_in_dir(pts_open, ux_t, uy_t)
        tc = th / ch * 100 if ch > 0 else 0
        pp = pitch_chord_pct(pts_open, ux_c, uy_c)

        if stype == "airfoil":
            print(f"  {z_m:>7.3f}  {stype:<8}  {len(pts):>5}  {ch:>7.0f}  {th:>6.0f}  {tc:>5.1f}%  {pp:>5.1f}%  (复用 QBlade)")
            continue

        fn = f"{BASE_NAME}_shank_z{z_m:.3f}_{stype}.sldcrv"
        out_path = os.path.join(OUT_DIR, fn)
        write_sldcrv(out_path, pts)
        print(f"  {z_m:>7.3f}  {stype:<8}  {len(pts):>5}  {ch:>7.0f}  {th:>6.0f}  {tc:>5.1f}%  {pp:>5.1f}%  {fn}")

    print()
    print("完成。")
    print()
    print("SolidWorks 放样流程:")
    print(f"  1. 插入→曲线→曲线通过 XYZ 点 → 加载 shank 截面:")
    print(f"     - {BASE_NAME}_shank_z0.000_root.sldcrv")
    for z_m in MORPH_Z:
        print(f"     - {BASE_NAME}_shank_z{z_m:.3f}_morph.sldcrv")
    print(f"     - {BASE_NAME}_sec03_z0.530.sldcrv (气动翼型, 已有)")
    print(f"  2. 放样: 缩小翼型(root) → 过渡(morph) → 翼型(sec03)")
    print(f"  3. 气动段放样: sec03 (z=0.530) → ... → sec21 (z=3.500)")
    print(f"  4. 桨毂: 圆柱 Φ280×70mm, YZ 圆面, X 轴旋转")
    print(f"  5. 桨柄实体 + 桨毂实体 → Combine/Merge")


if __name__ == "__main__":
    main()
