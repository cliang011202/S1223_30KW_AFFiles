"""
QBlade 翼型极坐标文件 → CCBlade (AeroDyn v13) 格式转换器
将 QBlade CE 导出的 .dat 文件转换为 CCBlade 可读的格式（参考 Cylinder2.dat）

用法:
    python qblade2ccblade_aerodyn.py <输入文件> <输出文件> [选项]

示例:
    python qblade2ccblade_aerodyn.py Circular_Foil_CD1_20.dat Circular_Foil_CD1_20_ccblade.dat
    python qblade2ccblade_aerodyn.py Circular_Foil_CD1_20.dat output.dat --re 1.0 --desc "My airfoil"
"""

import argparse
import sys
import os


def parse_qblade(filepath):
    """解析 QBlade 导出的翼型极坐标文件，返回 header 参数字典和极坐标数据列表。"""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        raw_lines = f.readlines()

    # 去掉 Windows 换行符，过滤完全空行
    lines = [line.rstrip('\r\n') for line in raw_lines]

    # ---- 解析 header（前12行）----
    # Line 0: 软件描述行  → 提取翼型名称用于注释
    # Line 1: Polar 名称  → 用于输出第1行注释
    # Line 2: Number of tables（固定为1，忽略）
    # Line 3: Table ID（忽略）
    # Line 4: Stall angle
    # Line 5~7: "No longer used"（3行，忽略）
    # Line 8: Zero lift AoA (Cn curve)
    # Line 9: Cn slope
    # Line 10: Cn at stall +
    # Line 11: Cn at stall -
    # Line 12: AoA for min CD
    # Line 13: Minimum CD value
    # Line 14+: 极坐标数据行

    def get_value(line):
        """取一行第一个空白分隔的 token 作为数值字符串。"""
        return line.strip().split()[0]

    # QBlade 文件固定 header 偏移
    desc_line   = lines[0]   # 软件信息
    polar_line  = lines[1]   # Polar 名称
    # lines[2] = "1  Number of airfoil tables"
    # lines[3] = "0  Table ID"
    stall_angle = get_value(lines[4])          # Stall angle (deg)
    # lines[5~7] = "0  No longer used" × 3
    zero_cn_aoa = get_value(lines[8])          # Zero-lift AoA for Cn curve
    cn_slope    = get_value(lines[9])          # Cn slope
    cn_stall_p  = get_value(lines[10])         # Cn at stall (+)
    cn_stall_n  = get_value(lines[11])         # Cn at stall (-)
    aoa_min_cd  = get_value(lines[12])         # AoA for min CD
    min_cd      = get_value(lines[13])         # Minimum CD

    # ---- 解析极坐标数据（alpha  Cl  Cd  Cm）----
    polar_data = []
    for line in lines[14:]:
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        if len(parts) < 3:
            continue
        try:
            alpha = float(parts[0])
            cl    = float(parts[1])
            cd    = float(parts[2])
            cm    = float(parts[3]) if len(parts) >= 4 else 0.0
            polar_data.append((alpha, cl, cd, cm))
        except ValueError:
            continue  # 跳过非数据行

    # 去除重复的 ±180° 行（QBlade 末尾有时重复 180.0）
    seen = set()
    unique_data = []
    for row in polar_data:
        key = round(row[0], 6)
        if key not in seen:
            seen.add(key)
            unique_data.append(row)

    # 提取 polar 名称（第2行）用于注释
    polar_name = polar_line.strip()

    return {
        'desc_line':   desc_line,
        'polar_name':  polar_name,
        'stall_angle': stall_angle,
        'zero_cn_aoa': zero_cn_aoa,
        'cn_slope':    cn_slope,
        'cn_stall_p':  cn_stall_p,
        'cn_stall_n':  cn_stall_n,
        'aoa_min_cd':  aoa_min_cd,
        'min_cd':      min_cd,
    }, unique_data


def write_ccblade(header, polar_data, out_path,
                  description=None, author=None, reynolds=1.0):
    """
    按照 CCBlade（AeroDyn v13）格式写出翼型文件。

    CCBlade 格式（对照 Cylinder2.dat）:
        Line 1: 任意描述（注释）
        Line 2: 任意描述（注释）
        Line 3: "line"（固定关键字，CCBlade 识别标志）
        Line 4: "N  Number of airfoil tables in this file"
        Line 5: "Re  Reynolds numbers in millions"
        Line 6: "ctrl  Control setting"
        Line 7: "stall  Stall angle (deg)"
        Line 8: "zero_aoa  Zero lift angle of attack (deg)"
        Line 9: "cn_slope  Cn slope for zero lift (dimensionless)"
        Line 10: "cn_p  Cn at stall value for positive angle of attack"
        Line 11: "cn_n  Cn at stall value for negative angle of attack"
        Line 12: "aoa_cd  Angle of attack for minimum CD (deg)"
        Line 13: "min_cd  Minimum CD value"
        Data:    alpha(deg)  Cl  Cd  Cm
        Last:    "EOT"
    """
    polar_name = header['polar_name']

    if description is None:
        description = polar_name
    if author is None:
        author = f"Converted from QBlade export: {polar_name}"

    lines_out = []

    # --- 两行注释 ---
    lines_out.append(description)
    lines_out.append(author)

    # --- "line" 关键字（CCBlade 识别此格式的标志）---
    lines_out.append("line")

    # --- 参数 header ---
    lines_out.append(f"   1        Number of airfoil tables in this file")
    lines_out.append(f"   {reynolds:.1f}     Reynolds numbers in millions")
    lines_out.append(f" 0.0      Control setting")
    lines_out.append(f" {float(header['stall_angle']):.1f}      Stall angle (deg)")
    lines_out.append(f" {float(header['zero_cn_aoa']):.1f}      Zero lift angle of attack (deg)")
    lines_out.append(f" {float(header['cn_slope']):.1f}      Cn slope for zero lift (dimensionless)")
    lines_out.append(f" {float(header['cn_stall_p']):.4f}      Cn at stall value for positive angle of attack")
    lines_out.append(f" {float(header['cn_stall_n']):.4f}      Cn at stall value for negative angle of attack")
    lines_out.append(f" {float(header['aoa_min_cd']):.1f}      Angle of attack for minimum CD (deg)")
    lines_out.append(f"   {float(header['min_cd']):.2f}     Minimum CD value")

    # --- 极坐标数据行 ---
    for (alpha, cl, cd, cm) in polar_data:
        lines_out.append(f"{alpha:8.2f}  {cl:8.4f}   {cd:.4f}   {cm:.4f}")

    # --- 结束标志 ---
    lines_out.append("EOT")
    lines_out.append("")  # 末尾空行（与参考格式一致）

    with open(out_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lines_out))

    print(f"[OK] 已写出: {out_path}  ({len(polar_data)} 个极坐标数据点)")


def convert(input_path, output_path, reynolds=1.0, description=None, author=None):
    if not os.path.isfile(input_path):
        print(f"[ERROR] 输入文件不存在: {input_path}")
        sys.exit(1)

    print(f"[INFO] 读取 QBlade 文件: {input_path}")
    header, polar_data = parse_qblade(input_path)

    print(f"[INFO] 极坐标行数: {len(polar_data)}")
    print(f"[INFO] AoA 范围: {polar_data[0][0]:.1f}° ~ {polar_data[-1][0]:.1f}°")
    print(f"[INFO] Min CD (from header): {header['min_cd']}")

    write_ccblade(header, polar_data, output_path,
                  description=description, author=author, reynolds=reynolds)


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="将 QBlade 导出的翼型 .dat 文件转换为 CCBlade (AeroDyn v13) 格式"
    )
    parser.add_argument("input",  help="输入文件路径（QBlade 格式）")
    parser.add_argument("output", help="输出文件路径（CCBlade 格式）")
    parser.add_argument("--re",   type=float, default=1.0,
                        help="Reynolds number (百万为单位，默认 1.0)")
    parser.add_argument("--desc", type=str, default=None,
                        help="输出文件第1行描述（默认使用 QBlade Polar 名称）")
    parser.add_argument("--author", type=str, default=None,
                        help="输出文件第2行作者/注释（默认自动生成）")

    args = parser.parse_args()
    convert(args.input, args.output,
            reynolds=args.re,
            description=args.desc,
            author=args.author)