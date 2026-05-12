"""
SLM_loads_estimate.py
========================================================
IEC 61400-2 简化载荷模型 (SLM) — S1223 30 kW 浮空涵道转子轮毂设计输入

输出: 叶根 6 分量极限载荷 envelope (3 力 + 3 矩) 跨多个 DLC, 含 IEC 安全系数。

坐标约定 (IEC 61400-2:2013 叶根坐标系):
    z_B : 叶轴向 (root → tip), F_zB = 离心轴向力
    x_B : 挥舞方向 (rotor 平面法向), M_xB = 挥舞弯矩 (推力驱动)
    y_B : 摆振方向 (rotor 平面内), M_yB = 摆振弯矩 (扭矩 + 重力)
    M_zB: 叶根扭转 (气动俯仰)

参考: IEC 61400-2:2013 §7.4 + Annex G。
公式部分采用工程估算等价形式 (清楚标注), 用于初步定螺栓 PCD/法兰厚度,
正式定型仍需系统级仿真 DEL。

更新点 (后续重跑只需改这些):
  - m_B, R_cog: 铺层方案出来后回填真值
  - Omega_design / Omega_max: 涵道效率敲定后调整
  - duct_shield: 涵道团队给出停机入流衰减后修正
========================================================
"""

import sys
import numpy as np
from dataclasses import dataclass, fields

sys.stdout.reconfigure(encoding="utf-8")


# ================================================================
# 1. 参数 — 修改这一节即可重跑
# ================================================================

# ---- 转子几何 ----
B            = 2          # 叶数
R            = 3.5        # 转子半径 [m]
R_hub        = 0.20       # 桨毂半径 [m]
R_eff_thrust = 2 * R / 3  # 推力等效力臂 (三角形分布近似) [m]
R_eff_torque = 0.7 * R    # 扭矩等效力臂 [m]

# ---- 大气环境 (1000 m, Jul+Sep) ----
rho          = 1.1        # 空气密度 [kg/m³]
g            = 9.81       # 重力加速度 [m/s²]
V_ave        = 5.46       # 年均风速 [m/s]   (Weibull k=2.487, c=6.156, c·Γ(1+1/k))
V_design     = 1.4 * V_ave
V_ref        = 5.0 * V_ave        # 50-yr 参考风
V_e50        = 1.4 * V_ref        # 50-yr 极阵风

# ---- 运行点 ----
Omega_design = 41.0                       # rad/s ≈ 392 RPM (V=18 m/s, TSR=7.98)
Omega_max    = 1.25 * Omega_design        # IEC 默认超速因子 25%
Q_design     = 1340.0                     # 设计扭矩 [N·m]   (= P_max / Ω)
T_design     = 5544.0                     # 设计推力 [N]    (裸转子, 涵道修正前)
TSR_design   = 7.98

# ---- 故障/极限场景 ----
M_brake_factor = 3.0   # 短路气隙峰值力矩 / 设计扭矩 (典型 2–5; 30 kW PMSG 取 3 保守)
gust_factor    = 1.5   # DLC D 极阵风对设计推力的放大
duct_shield    = 0.5   # 停机时涵道对 V_e50 的衰减系数 (待涵道团队确认)

# ---- DLC A 疲劳 1P 周期因子 ----
cyc_1P_flap    = 0.30  # 挥舞 1P 振幅 / 均值 (偏航误差 + 风剪)

# ---- 叶片质量特性 *** 铺层方案敲定后更新 *** ----
m_B          = 8.0     # 单叶质量 [kg]      (保守占位)
R_cog        = 1.4     # 叶根→质心距 [m]   (保守占位)

# ---- 翼型俯仰 ----
Cm_root      = 0.05    # 根部翼型俯仰系数 (薄弯翼型典型值)
chord_root   = 0.25    # 根部弦长 [m] (用于 M_zB 估算)

# ---- IEC 61400-2 Table 4 局部安全系数 ----
gamma_f_ult  = 1.35    # 极限载荷分项
gamma_m_ult  = 1.10    # 极限材料分项
gamma_f_fat  = 1.00    # 疲劳载荷分项
gamma_m_fat  = 1.25    # 疲劳材料分项

# ---- 叶根螺栓预校核 (可选) ----
n_bolts        = 4
bolt_PCD       = 0.18  # 螺栓节圆直径 [m]
bolt_label     = "M16 8.8"
bolt_proof_kN  = 88.0  # M16 8.8 屈服拉力 ≈ 88 kN


# ================================================================
# 2. 数据容器
# ================================================================

@dataclass
class Load6:
    """叶根 6 分量 (IEC 61400-2 约定)。力 [N], 矩 [N·m]。"""
    F_xB: float = 0.0   # 挥舞剪力
    F_yB: float = 0.0   # 摆振剪力
    F_zB: float = 0.0   # 轴向 (+ = 离心拉力)
    M_xB: float = 0.0   # 挥舞弯矩
    M_yB: float = 0.0   # 摆振弯矩
    M_zB: float = 0.0   # 叶根扭转

    def __mul__(self, k: float) -> "Load6":
        return Load6(**{f.name: getattr(self, f.name) * k for f in fields(self)})

    def to_array(self) -> np.ndarray:
        return np.array([getattr(self, f.name) for f in fields(self)])


# ================================================================
# 3. DLC 载荷计算
# ================================================================

def DLC_A_fatigue() -> Load6:
    """正常运行疲劳载荷范围 (peak-to-peak)。
    主导项: 摆振重力翻转 ΔM_yB = 2·m_B·g·R_cog (每转一次)。"""
    L = Load6()
    L.F_zB = 2 * m_B * g                         # 重力分量翻转
    L.M_yB = 2 * m_B * g * R_cog                 # 摆振重力翻转 (主导疲劳)
    M_xB_mean = (T_design / B) * R_eff_thrust
    L.M_xB = 2 * cyc_1P_flap * M_xB_mean         # 挥舞 1P 范围 (±cyc → 2·cyc·mean)
    return L


def DLC_D_extreme_thrust() -> Load6:
    """极阵风工况 → 最大挥舞载荷。"""
    L = Load6()
    T_max = gust_factor * T_design
    F_x_per_blade = T_max / B
    L.F_xB = F_x_per_blade
    L.M_xB = F_x_per_blade * R_eff_thrust + m_B * g * R_cog   # 挥舞: 推力 + 重力 (叶水平)
    L.M_yB = Q_design / B + m_B * g * R_cog                   # 摆振: 扭矩 + 重力
    L.F_zB = m_B * Omega_design**2 * R_cog                    # 离心 (设计转速)
    L.F_yB = (Q_design / B) / R_eff_torque                    # 摆振剪力 (扭矩反作用)
    # 叶根俯仰: 0.5·Cm·ρ·U_rel²·c²·L (取 0.7R 处条件代表整段)
    U_rel = Omega_design * R_eff_thrust
    L.M_zB = 0.5 * Cm_root * rho * U_rel**2 * chord_root**2 * R_eff_thrust
    return L


def DLC_E_max_speed() -> Load6:
    """超速工况 (1.25·Ω_design) → 离心载荷极限。"""
    L = Load6()
    L.F_zB = m_B * Omega_max**2 * R_cog          # 离心 (主导)
    L.F_xB = T_design / B                        # 同步保留稳态推力
    L.M_xB = (T_design / B) * R_eff_thrust
    L.M_yB = Q_design / B
    L.F_yB = (Q_design / B) / R_eff_torque
    return L


def DLC_G_short_circuit() -> Load6:
    """发电机短路制动 → 摆振峰值。
    短路气隙峰值力矩 ≈ M_brake_factor × Q_design, 通过叶片摆振传递。"""
    L = Load6()
    M_brake = M_brake_factor * Q_design
    L.F_xB = T_design / B
    L.M_xB = (T_design / B) * R_eff_thrust
    L.M_yB = M_brake / B + m_B * g * R_cog        # 摆振 (峰值)
    L.F_yB = (M_brake / B) / R_eff_torque
    L.F_zB = m_B * Omega_design**2 * R_cog
    return L


def DLC_H_parked_extreme() -> Load6:
    """停机 + 50-yr 极风 (含涵道屏蔽)。
    叶片侧风停机, 阻力主导。"""
    L = Load6()
    V_eff   = duct_shield * V_e50
    chord_avg = 0.30                              # 估算平均弦长 [m]
    A_proj  = chord_avg * R                       # 单叶投影面积
    Cd      = 1.2                                 # 板状钝体阻力系数
    F_drag  = Cd * 0.5 * rho * V_eff**2 * A_proj
    L.F_xB  = F_drag
    L.M_xB  = F_drag * R / 2                      # 阻力质心 ≈ 半径中点
    return L


# ================================================================
# 4. envelope + 安全系数
# ================================================================

def envelope(dlcs: dict, exclude=("A_fatigue",)) -> Load6:
    """各分量 |·| 最大值。A_fatigue 是 range 不参与 envelope。"""
    env = Load6()
    for name, L in dlcs.items():
        if name in exclude:
            continue
        for f in fields(env):
            setattr(env, f.name, max(abs(getattr(env, f.name)), abs(getattr(L, f.name))))
    return env


# ================================================================
# 5. 输出
# ================================================================

_HEADER = ("F_xB[kN]", "F_yB[kN]", "F_zB[kN]", "M_xB[kN·m]", "M_yB[kN·m]", "M_zB[kN·m]")


def _row(L: Load6):
    return [f"{L.F_xB/1e3:9.2f}", f"{L.F_yB/1e3:9.2f}", f"{L.F_zB/1e3:9.2f}",
            f"{L.M_xB/1e3:11.3f}", f"{L.M_yB/1e3:11.3f}", f"{L.M_zB/1e3:11.3f}"]


def report(dlcs: dict, env_unfac: Load6, env_fac: Load6):
    width = 24 + 6 * 13
    print("=" * width)
    print(" IEC 61400-2 SLM 叶根载荷 — S1223 30 kW 浮空涵道转子")
    print("=" * width)
    print(f" 输入: m_B = {m_B} kg,  R_cog = {R_cog} m       (铺层方案出来后更新)")
    print(f"       Ω_design = {Omega_design:.2f} rad/s ({Omega_design*60/(2*np.pi):.0f} RPM)"
          f"   Ω_max = {Omega_max:.2f} rad/s ({Omega_max*60/(2*np.pi):.0f} RPM)")
    print(f"       T_design = {T_design:.0f} N  (裸转子, 涵道修正前)"
          f"     Q_design = {Q_design:.0f} N·m")
    print(f"       γ_f·γ_m (极限) = {gamma_f_ult}·{gamma_m_ult} = {gamma_f_ult*gamma_m_ult:.3f}")
    print("-" * width)
    print(f"{'DLC':<24}" + "  ".join(f"{h:>11}" for h in _HEADER))
    print("-" * width)
    for name, L in dlcs.items():
        tag = " (range)" if name == "A_fatigue" else ""
        print(f"{name+tag:<24}" + "  ".join(f"{v:>11}" for v in _row(L)))
    print("-" * width)
    print(f"{'ENVELOPE (unfactored)':<24}" + "  ".join(f"{v:>11}" for v in _row(env_unfac)))
    print(f"{'ENVELOPE × γ_f·γ_m':<24}" + "  ".join(f"{v:>11}" for v in _row(env_fac)))
    print("=" * width)


def bolt_check(env_fac: Load6):
    """初步螺栓校核: 轴向拉力 + 弯矩在最远纤维上叠加。
    n 个螺栓均布于 PCD: 弯矩下单个螺栓拉力 F_M = 2·M / (n·r)。"""
    r = bolt_PCD / 2
    F_axial = max(env_fac.F_zB, 0.0) / n_bolts
    F_moment = 2 * env_fac.M_xB / (n_bolts * r)        # 挥舞 (主导)
    F_moment_edge = 2 * env_fac.M_yB / (n_bolts * r)   # 摆振 (一般小)
    F_peak = F_axial + max(F_moment, F_moment_edge)    # 最危险螺栓 (轴向 + 弯矩外纤维)
    util = F_peak / (bolt_proof_kN * 1e3)
    print(f"\n[初步螺栓校核] {n_bolts} × {bolt_label}, PCD = {bolt_PCD*1000:.0f} mm")
    print(f"  轴向分摊  / 螺栓 = {F_axial/1e3:7.2f} kN")
    print(f"  挥舞弯矩  / 螺栓 = {F_moment/1e3:7.2f} kN")
    print(f"  摆振弯矩  / 螺栓 = {F_moment_edge/1e3:7.2f} kN")
    print(f"  峰值螺栓拉力     = {F_peak/1e3:7.2f} kN  (proof {bolt_proof_kN:.0f} kN)")
    print(f"  利用率           = {util*100:5.1f}%   →  ", end="")
    if util < 0.50:
        print("OK (大裕度)")
    elif util < 0.75:
        print("OK")
    elif util < 1.00:
        print("MARGINAL — 增大 PCD 或螺栓规格")
    else:
        print("不足 — 必须改大螺栓 / 多螺栓 / 加大 PCD")


def fatigue_note(dlcs: dict):
    rng = dlcs["A_fatigue"]
    rng_fac = rng * (gamma_f_fat * gamma_m_fat)
    r = bolt_PCD / 2
    dF_per_bolt = 2 * rng_fac.M_yB / (n_bolts * r)    # 摆振重力翻转占主导
    print(f"\n[疲劳提示] DLC A 摆振范围 ΔM_yB = {rng.M_yB:.0f} N·m  "
          f"→ × γ_fat ({gamma_f_fat*gamma_m_fat}) = {rng_fac.M_yB:.0f} N·m")
    print(f"  对应单螺栓拉力范围 ≈ {dF_per_bolt/1e3:.2f} kN  "
          f"→ 对照 8.8 级 S-N (σ_a 极限 ~80 MPa @ 2e6 cycles, M16 应力面积 157 mm² → "
          f"F_a 极限 ≈ 12.6 kN/螺栓)")


# ================================================================
# 6. 入口
# ================================================================

if __name__ == "__main__":
    DLCS = {
        "A_fatigue":         DLC_A_fatigue(),
        "D_extreme_thrust":  DLC_D_extreme_thrust(),
        "E_max_speed":       DLC_E_max_speed(),
        "G_short_circuit":   DLC_G_short_circuit(),
        "H_parked_extreme":  DLC_H_parked_extreme(),
    }
    env_unfac = envelope(DLCS)
    env_fac   = env_unfac * (gamma_f_ult * gamma_m_ult)

    report(DLCS, env_unfac, env_fac)
    bolt_check(env_fac)
    fatigue_note(DLCS)

    # 存档供下游 SolidWorks/FEA 使用
    out = {f"{name}_{f.name}": getattr(L, f.name)
           for name, L in DLCS.items() for f in fields(L)}
    out["env_unfac"]    = env_unfac.to_array()
    out["env_factored"] = env_fac.to_array()
    out["component_names"] = np.array([f.name for f in fields(env_unfac)])
    out["gamma_f_ult"]  = gamma_f_ult
    out["gamma_m_ult"]  = gamma_m_ult
    np.savez("SLM_loads_envelope.npz", **out)
    print("\n已保存: SLM_loads_envelope.npz")
