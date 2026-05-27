"""
叶片弦长优化 V3 —— 多风况加权 AEP + 多雷诺数翼型极曲线
策略: 最大化 AEP = Σ f_i × P(V_i, chord)
约束: 各工况攻角均不超过失速限制 (11°)
固定: 扭角分布 twist_fixed_deg（默认使用初始扭角，可加载 V3 扭角优化结果）

风场依据 (2020-2024年7月+9月, ERA5 925hPa, 海拔~1000m, ρ=1.1 kg/m³):
  切入=3 m/s, 切出=18 m/s, 有效时间占比 45.6%
  Weibull k=2.487, c=6.156 m/s (有效段内)

  代表工况（按等能量贡献划分）:
    V (m/s)  | 时间频率 f_i | 能量贡献
    ---------+--------------+---------
     5.0     |   53.7%      |  18.2%
     6.5     |   16.4%      |  14.8%
     7.5     |   12.5%      |  17.3%   ← 能量峰值工况
     8.5     |    8.3%      |  16.8%
    11.0     |    9.1%      |  32.9%

翼型分配:
  idx 0~1   : 圆柱 (r=0.202, 0.350 m)
  idx 2~4   : DU-06-W-200 (r=0.676~1.135 m, t/c=19.8%)
  idx 5~7   : SG6050      (r=1.483~1.850 m, t/c=16.0%)
  idx 8~10  : SD7062      (r=2.036~2.565 m, t/c=14.0%)
  idx 11~13 : S1223       (r=3.024~3.498 m, t/c=12.1%)

多起点策略: 10次随机起点，规避弦长优化的锯齿形局部最优风险。

待修改参数: Section 2 叶片参数
"""

import numpy as np
import openmdao.api as om
import os
import time
from ccblade.ccblade_component import CCBladeTwist


# ================================================================
# 1. AeroDyn 格式翼型文件解析
# ================================================================

def load_aerodyn_polar(filepath):
    """解析 AeroDyn 格式翼型极曲线文件"""
    aoa_list, cl_list, cd_list, cm_list = [], [], [], []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.upper() == "EOT":
                continue
            parts = line.split()
            if len(parts) >= 4:
                try:
                    a  = float(parts[0])
                    c1 = float(parts[1])
                    c2 = float(parts[2])
                    c3 = float(parts[3])
                    if -180.0 <= a <= 180.0:
                        aoa_list.append(a)
                        cl_list.append(c1)
                        cd_list.append(c2)
                        cm_list.append(c3)
                except ValueError:
                    continue
    return (np.array(aoa_list), np.array(cl_list),
            np.array(cd_list), np.array(cm_list))


def make_cylinder_polar(common_aoa):
    """圆柱截面极曲线"""
    n = len(common_aoa)
    return np.zeros(n), np.ones(n) * 0.50, np.zeros(n)


# ================================================================
# 2. ★★★ 叶片参数 ★★★
# ================================================================

airfoil_dir   = r"Re_360polar"
cylinder_file = os.path.join(airfoil_dir, "Cylinder.dat")

Rhub       = 0.2
Rtip       = 3.5
hub_height = 10.0
precone    = 0.0
tilt       = 0.0
yaw        = 0.0
n_blades   = 2
rho        = 1.1
mu         = 1.81206e-5
shearExp   = 0.0

tsr        = 7   # 变速风机在部分负荷区保持最优 TSR
pitch_deg  = 0.0

# --- 多风况参数（来自 wind_data_analysis.md）---
V_cases   = np.array([5.0,  6.5,  7.5,  8.5,  11.0])   # m/s
f_weights = np.array([0.537, 0.164, 0.125, 0.083, 0.091])
n_cases   = len(V_cases)
I_PEAK    = 2   # 能量峰值工况索引 (V=7.5 m/s)

n_opt_twist = 8
n_opt_chord = 8

r = np.array([  0.202 , 0.350 , 0.676 , 0.967 , 1.135 ,
                1.483 , 1.664 , 1.850 , 2.036 , 2.217 ,
                2.398 , 2.565 , 3.024 , 3.498 ])

chord = np.array([  0.2500 , 0.2500 , 0.6000 , 0.5192 , 0.4681 ,
                    0.3500 , 0.3200 , 0.2896 , 0.2536 , 0.2224 ,
                    0.1954 , 0.1741 , 0.1331 , 0.1182 ])

twist_init_deg = np.array([18.20, 18.20, 18.20, 10.38,  7.54,
                            4.29,  3.46,  2.97,  2.72,  2.60,
                            2.56,  2.56,  2.45,  1.68])

rthick = np.array([100.0, 100.0, 19.8, 19.8, 19.8,
                    16.0,  16.0, 16.0, 14.0, 14.0,
                    14.0,  12.1, 12.1, 12.1])

n_fix  = 2   # 叶根固定截面数（圆柱截面，弦长不参与优化）
n_span = len(r)

is_cylinder = [True, True, False, False, False,
               False, False, False, False, False,
               False, False, False, False]

# 分截面失速约束上限 (degrees)
# 圆柱截面 (idx 0–1):    不施加约束——入流角 30–44° 由几何决定，BEM 攻角无翼型失速意义
# DU-06-W-200 (idx 2–4): Re=0.1~0.5e6 时 Cl_max ≈ 10°，约束上限取 10°
# SG6050 (idx 5–7):      Re=0.1~0.5e6 时 Cl_max ≈ 10°，约束上限取 10°
# SD7062 (idx 8–10):     Re=0.1~0.5e6 时 Cl_max ≈ 10°，约束上限取 10°
# S1223  (idx 11–13):    Re=0.1e6 时 Cl_max 在 10°，约束上限取 10°
NON_CYL_IDX      = list(range(2, n_span))          # idx 2~13，共 12 个截面（排除圆柱）
ALPHA_UPPER_NSEC = np.array([10.0, 10.0, 10.0,     # DU-06-W-200 (idx 2–4)
                              10.0, 10.0, 10.0,     # SG6050      (idx 5–7)
                              10.0, 10.0, 10.0,     # SD7062      (idx 8–10)
                              10.0, 10.0, 10.0])    # S1223       (idx 11–13)

# --- 弦长优化边界（仅对 idx n_fix: 生效）---
chord_lower = np.full(n_span, 0.05)                     # 下界 (m)，统一 0.05 m
# 上界：按截面单调递减，约为初始弦长的 1.2–1.3×；防止优化器撞全局上界
# Betz 最优弦长 c_Betz = 8πR/(9·B·Cl·TSR) ≈ 0.65 m (Cl=1)，
# 但考虑 Re 失配 / 结构约束，内段上界限制在 0.60 m 以内
chord_upper = np.array([0.30, 0.30,                     # 圆柱（不参与优化，仅占位）
                         0.60, 0.55, 0.48,              # DU-06-W-200 (idx 2–4)
                         0.35, 0.32, 0.29,              # SG6050      (idx 5–7)
                         0.26, 0.24, 0.22,              # SD7062      (idx 8–10)
                         0.20, 0.16, 0.13])             # S1223       (idx 11–13)

# --- 固定扭角输入 ---
# 可选：加载 OptimizeTwist_s1223_V3.py 的优化结果作为固定扭角
# twist_npz = np.load("twist_optimization_results_AEP.npz")
# twist_fixed_deg = twist_npz["twist_opt"]   # 已优化的最优扭角 (deg)
twist_fixed_deg = twist_init_deg.copy()   # 默认使用初始扭角


# ================================================================
# 3. 构建多雷诺数极曲线表
# ================================================================
# 截面翼型分配：
#   idx 0,  1  : 圆柱（is_cylinder=True）
#   idx 2– 4   : DU-06-W-200（t/c=19.8%，叶根过渡段）
#   idx 5– 7   : SG6050     （t/c=16.0%，中内段）
#   idx 8–10   : SD7062     （t/c=14.0%，中外段）
#   idx 11–13  : S1223      （t/c=12.1%，叶尖段）
#
# 实际运行 Re 估算（V=5~11 m/s, TSR=7.0, ρ=1.1 kg/m³）:
#   圆柱截面  (r=0.20~0.35m): Re ≈ 0.06~0.15e6  → 纯阻力圆柱，不参与气动升力
#   DU段      (r=0.68~1.14m): Re ≈ 0.23~0.48e6  → DU-06-W-200 极曲线
#   SG段      (r=1.48~1.85m): Re ≈ 0.28~0.45e6  → SG6050 极曲线
#   SD段      (r=2.04~2.57m): Re ≈ 0.27~0.42e6  → SD7062 极曲线
#   S1223段   (r=3.02~3.50m): Re ≈ 0.26~0.40e6  → S1223 极曲线
# CCBladeTwist 内部会根据各截面的局部 Re 自动在表格间插值。

re_values = np.array([0.1e6, 0.5e6, 0.8e6, 1.0e6, 2.0e6])
n_Re  = len(re_values)
n_tab = 1

# S1223 极曲线文件（叶尖段，idx 11–13）
s1223_re_files = [
    os.path.join(airfoil_dir, "S1223_Re0.100.dat"),
    os.path.join(airfoil_dir, "S1223_Re0.500.dat"),
    os.path.join(airfoil_dir, "S1223_Re0.800.dat"),
    os.path.join(airfoil_dir, "S1223_Re1.000.dat"),
    os.path.join(airfoil_dir, "S1223_Re2.000.dat"),
]

# DU-06-W-200 极曲线文件（叶根过渡段，idx 2–4）
du_re_files = [
    os.path.join(airfoil_dir, "DU-06-W-200_Re0.100.dat"),
    os.path.join(airfoil_dir, "DU-06-W-200_Re0.500.dat"),
    os.path.join(airfoil_dir, "DU-06-W-200_Re0.800.dat"),
    os.path.join(airfoil_dir, "DU-06-W-200_Re1.000.dat"),
    os.path.join(airfoil_dir, "DU-06-W-200_Re2.000.dat"),
]

# SG6050 极曲线文件（中内段，idx 5–7）
sg_re_files = [
    os.path.join(airfoil_dir, "SG6050_Re0.100.dat"),
    os.path.join(airfoil_dir, "SG6050_Re0.500.dat"),
    os.path.join(airfoil_dir, "SG6050_Re0.800.dat"),
    os.path.join(airfoil_dir, "SG6050_Re1.000.dat"),
    os.path.join(airfoil_dir, "SG6050_Re2.000.dat"),
]

# SD7062 极曲线文件（中外段，idx 8–10）
sd_re_files = [
    os.path.join(airfoil_dir, "SD7062_Re0.100.dat"),
    os.path.join(airfoil_dir, "SD7062_Re0.500.dat"),
    os.path.join(airfoil_dir, "SD7062_Re0.800.dat"),
    os.path.join(airfoil_dir, "SD7062_Re1.000.dat"),
    os.path.join(airfoil_dir, "SD7062_Re2.000.dat"),
]

# 翼型分区标识
is_du = [False, False, True,  True,  True,
         False, False, False, False, False,
         False, False, False, False]

is_sg = [False, False, False, False, False,
         True,  True,  True,  False, False,
         False, False, False, False]

is_sd = [False, False, False, False, False,
         False, False, False, True,  True,
         True,  False, False, False]

# 以 S1223_Re2.000 的 AOA 网格为公共基准（所有翼型插值到此网格）
aoa_base, _, _, _ = load_aerodyn_polar(s1223_re_files[-1])
common_aoa = aoa_base.copy()
n_aoa = len(common_aoa)


def _load_polars(re_files, label):
    """加载某翼型的多 Re 极曲线并插值到公共 AOA 网格"""
    polars = []
    print(f"加载 {label} 多雷诺数极曲线:")
    for re_val, path in zip(re_values, re_files):
        aoa_i, cl_i, cd_i, cm_i = load_aerodyn_polar(path)
        cl_interp = np.interp(common_aoa, aoa_i, cl_i)
        cd_interp = np.interp(common_aoa, aoa_i, cd_i)
        cm_interp = np.interp(common_aoa, aoa_i, cm_i)
        polars.append((cl_interp, cd_interp, cm_interp))
        print(f"  Re={re_val/1e6:.3f}e6: Cl_max={cl_interp.max():.4f} "
              f"@ α={common_aoa[cl_interp.argmax()]:.1f}°  "
              f"Cd_min={cd_interp.min():.5f}")
    return polars


polars_s1223 = _load_polars(s1223_re_files, "S1223      (叶尖段  idx 11–13)")
polars_du    = _load_polars(du_re_files,    "DU-06-W-200(叶根过渡 idx 2–4 )")
polars_sg    = _load_polars(sg_re_files,    "SG6050     (中内段  idx 5–7 )")
polars_sd    = _load_polars(sd_re_files,    "SD7062     (中外段  idx 8–10)")

# 圆柱截面极曲线（Re 无关，各 Re 档位填同一份数据）
if os.path.exists(cylinder_file):
    aoa_cyl, cl_cyl, cd_cyl, cm_cyl = load_aerodyn_polar(cylinder_file)
    cl_cyl_c = np.interp(common_aoa, aoa_cyl, cl_cyl)
    cd_cyl_c = np.interp(common_aoa, aoa_cyl, cd_cyl)
    cm_cyl_c = np.interp(common_aoa, aoa_cyl, cm_cyl)
else:
    cl_cyl_c, cd_cyl_c, cm_cyl_c = make_cylinder_polar(common_aoa)

# 构建极曲线表: shape = (n_span, n_aoa, n_Re, n_tab)
cl_table = np.zeros((n_span, n_aoa, n_Re, n_tab))
cd_table = np.zeros((n_span, n_aoa, n_Re, n_tab))
cm_table = np.zeros((n_span, n_aoa, n_Re, n_tab))

for i_span in range(n_span):
    for i_re in range(n_Re):
        if is_cylinder[i_span]:
            cl_table[i_span, :, i_re, 0] = cl_cyl_c
            cd_table[i_span, :, i_re, 0] = cd_cyl_c
            cm_table[i_span, :, i_re, 0] = cm_cyl_c
        elif is_du[i_span]:
            cl_table[i_span, :, i_re, 0] = polars_du[i_re][0]
            cd_table[i_span, :, i_re, 0] = polars_du[i_re][1]
            cm_table[i_span, :, i_re, 0] = polars_du[i_re][2]
        elif is_sg[i_span]:
            cl_table[i_span, :, i_re, 0] = polars_sg[i_re][0]
            cd_table[i_span, :, i_re, 0] = polars_sg[i_re][1]
            cm_table[i_span, :, i_re, 0] = polars_sg[i_re][2]
        elif is_sd[i_span]:
            cl_table[i_span, :, i_re, 0] = polars_sd[i_re][0]
            cd_table[i_span, :, i_re, 0] = polars_sd[i_re][1]
            cm_table[i_span, :, i_re, 0] = polars_sd[i_re][2]
        else:
            cl_table[i_span, :, i_re, 0] = polars_s1223[i_re][0]
            cd_table[i_span, :, i_re, 0] = polars_s1223[i_re][1]
            cm_table[i_span, :, i_re, 0] = polars_s1223[i_re][2]

s_opt_twist = np.linspace(0.0, 1.0, n_opt_twist)
s_opt_chord = np.linspace(0.0, 1.0, n_opt_chord)


# ================================================================
# 4. 配置选项
# ================================================================

modeling_options = {
    "WISDEM": {
        "RotorSE": {
            "n_span": n_span,
            "n_aoa":  n_aoa,
            "n_Re":   n_Re,
            "n_tab":  n_tab,
        }
    },
    "assembly": {
        "number_of_blades": n_blades,
    },
    "airfoils": {
        "n_aoa":  n_aoa,
        "n_Re":   n_Re,
        "n_tab":  n_tab,
    },
}

opt_options = {
    "design_variables": {
        "blade": {
            "aero_shape": {
                "chord": {"n_opt": n_opt_chord},
                "twist": {
                    "n_opt":   n_opt_twist,
                    "inverse": False,
                    "flag":    False,
                },
            }
        }
    },
    "constraints": {
        "blade": {
            "stall": {"margin": 0.05233},
        }
    },
}


# ================================================================
# 5. AEP 聚合组件
# ================================================================

class AEPAggregator(om.ExplicitComponent):
    """
    计算多工况加权平均功率（正比于 AEP）:

        AEP_proxy = Σ f_i × P_i

    其中 f_i 为时间频率权重，P_i 为各工况实际功率输出（含 V^3 因子）。
    解析偏导 ∂(AEP)/∂(P_i) = f_i，无需有限差分。
    """

    def initialize(self):
        self.options.declare("weights", recordable=False)

    def setup(self):
        weights = self.options["weights"]
        for i in range(len(weights)):
            self.add_input(f"P_{i}", val=0.0, units="W")
        self.add_output("AEP", val=0.0, units="W")
        for i, w in enumerate(weights):
            self.declare_partials("AEP", f"P_{i}", val=float(w))

    def compute(self, inputs, outputs):
        weights = self.options["weights"]
        outputs["AEP"] = sum(weights[i] * inputs[f"P_{i}"][0]
                             for i in range(len(weights)))


# ================================================================
# 6. 辅助函数
# ================================================================

# 所有风速工况共享的输入（chord 和 theta_in 均在此列表中，在顶层共享）
_SHARED_INPUTS = [
    "theta_in", "rthick", "s_opt_theta", "s_opt_chord",
    "airfoils_aoa", "airfoils_Re", "airfoils_cl", "airfoils_cd", "airfoils_cm",
    "r", "chord",
    "Rhub", "Rtip", "hub_height", "precone", "tilt", "yaw",
    "precurve", "precurveTip", "presweep", "presweepTip",
    "rho", "mu", "shearExp",
    "tsr", "pitch",
    "nBlades", "nSector", "tiploss", "hubloss", "wakerotation", "usecd",
]

_PER_CASE_OUTPUTS = ["CP", "P", "alpha", "theta", "cl", "cd", "a", "ap", "Px_b"]


def set_shared_inputs(prob_obj):
    """
    设置所有工况共享的固定输入。
    弦长 chord 由外部单独赋初值（多起点策略中每次单独 set_val）。
    扭角 theta_in 在此固定为 twist_fixed_deg（不作为设计变量）。
    """
    prob_obj.set_val("airfoils_aoa", common_aoa, units="deg")
    prob_obj.set_val("airfoils_Re",  re_values)
    prob_obj.set_val("airfoils_cl",  cl_table)
    prob_obj.set_val("airfoils_cd",  cd_table)
    prob_obj.set_val("airfoils_cm",  cm_table)

    prob_obj.set_val("r",            r,                units="m")
    prob_obj.set_val("rthick",       rthick / 100.0)
    prob_obj.set_val("s_opt_theta",  s_opt_twist)
    prob_obj.set_val("s_opt_chord",  s_opt_chord)
    prob_obj.set_val("theta_in",     twist_fixed_deg,  units="deg")

    prob_obj.set_val("Rhub",         Rhub,             units="m")
    prob_obj.set_val("Rtip",         Rtip,             units="m")
    prob_obj.set_val("hub_height",   hub_height,       units="m")
    prob_obj.set_val("precone",      precone,          units="deg")
    prob_obj.set_val("tilt",         tilt,             units="deg")
    prob_obj.set_val("yaw",          yaw,              units="deg")
    prob_obj.set_val("precurve",     np.zeros(n_span), units="m")
    prob_obj.set_val("precurveTip",  0.0,              units="m")
    prob_obj.set_val("presweep",     np.zeros(n_span), units="m")
    prob_obj.set_val("presweepTip",  0.0,              units="m")
    prob_obj.set_val("rho",          rho,              units="kg/m**3")
    prob_obj.set_val("mu",           mu,               units="kg/(m*s)")
    prob_obj.set_val("shearExp",     shearExp)
    prob_obj.set_val("nBlades",      n_blades)
    prob_obj.set_val("nSector",      1)
    prob_obj.set_val("tiploss",      True)
    prob_obj.set_val("hubloss",      True)
    prob_obj.set_val("wakerotation", True)
    prob_obj.set_val("usecd",        True)
    prob_obj.set_val("tsr",          tsr)
    prob_obj.set_val("pitch",        pitch_deg,        units="deg")


# ================================================================
# 7. 第一阶段：验证弦长对 CP 的导数连通性
# ================================================================

print("=" * 60)
print(f"第一阶段: 导数连通性验证  (V={V_cases[I_PEAK]:.1f} m/s, 能量峰值工况)")
print("=" * 60)

prob_test = om.Problem()
prob_test.model.add_subsystem(
    "blade",
    CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options),
    promotes=["*"],
)
prob_test.setup(force_alloc_complex=True)
set_shared_inputs(prob_test)
prob_test.set_val("chord", chord,           units="m")
prob_test.set_val("Uhub",  V_cases[I_PEAK], units="m/s")
prob_test.run_model()

print(f"\n--- 基准输出 (V={V_cases[I_PEAK]:.1f} m/s) ---")
for name in ["CP", "P", "alpha", "cl", "cd"]:
    val = prob_test.get_val(name)
    if val.size == 1:
        print(f"  {name:>8s} = {val[0]:.6f}")
    else:
        print(f"  {name:>8s} = [{val[0]:.4f}, ..., {val[-1]:.4f}]  (len={val.size})")

print("\n--- 手动扰动检查 (第6截面弦长 +0.05 m) ---")
chord_perturbed = chord.copy()
chord_perturbed[5] += 0.05
prob_test.set_val("chord", chord_perturbed, units="m")
prob_test.run_model()
CP_perturbed = prob_test.get_val("CP")[0]

prob_test.set_val("chord", chord, units="m")
prob_test.run_model()
CP_original = prob_test.get_val("CP")[0]

print(f"  CP (原始)       = {CP_original:.6f}")
print(f"  CP (弦长+0.05m) = {CP_perturbed:.6f}")
print(f"  ΔCP             = {CP_perturbed - CP_original:.6f}")
if abs(CP_perturbed - CP_original) > 1e-10:
    print("  ✓ CP 对 chord 有响应，导数链连通")
else:
    print("  ✗ CP 对 chord 无响应，需排查")


# ================================================================
# 8. 第二阶段：多风况加权 AEP 弦长优化（多起点策略）
# ================================================================

print("\n" + "=" * 60)
print("第二阶段: 多风况加权 AEP 弦长优化（多起点）")
print("=" * 60)
print(f"代表风速 (m/s)  : {V_cases}")
print(f"时间频率权重    : {f_weights}")
print(f"设计变量        : chord[{n_fix}:] (共 {n_span - n_fix} 个截面弦长)")
print(f"弦长范围        : 下界 {chord_lower[n_fix]:.2f} m，上界 {chord_upper[n_fix]:.2f}~{chord_upper[-1]:.2f} m (各截面递减)")
print(f"约束            : 各翼型截面 alpha ≤ 10°  "
      f"({n_cases} 工况 × {len(NON_CYL_IDX)} 截面 = {n_cases * len(NON_CYL_IDX)} 个约束)")


class ChordMonoComp(om.ExplicitComponent):
    """
    弦长单调递减约束辅助组件。
    输出 chord_mono_diff[k] = chord[non_cyl_idx[k]] − chord[non_cyl_idx[k+1]]
    约束 chord_mono_diff >= 0 即等价于弦长沿展向单调递减（从叶根气动截面到叶尖）。

    Jacobian 为常数稀疏矩阵，直接在 setup_partials 中声明，无运行时开销。
    """

    def initialize(self):
        self.options.declare("non_cyl_idx", recordable=False)
        self.options.declare("n_span",      recordable=False)

    def setup(self):
        idx    = self.options["non_cyl_idx"]
        n_diff = len(idx) - 1
        self.add_input("chord",            val=np.zeros(self.options["n_span"]), units="m")
        self.add_output("chord_mono_diff", val=np.zeros(n_diff))

    def setup_partials(self):
        idx    = self.options["non_cyl_idx"]
        n_diff = len(idx) - 1
        rows = np.concatenate([np.arange(n_diff), np.arange(n_diff)])
        cols = np.concatenate([np.array(idx[:-1]), np.array(idx[1:])])
        vals = np.concatenate([np.ones(n_diff), -np.ones(n_diff)])
        self.declare_partials("chord_mono_diff", "chord",
                              rows=rows, cols=cols, val=vals)

    def compute(self, inputs, outputs):
        idx = self.options["non_cyl_idx"]
        outputs["chord_mono_diff"] = inputs["chord"][idx[:-1]] - inputs["chord"][idx[1:]]


def _build_prob():
    """
    构建多风况 AEP 优化 Problem。
    每次多起点调用独立创建，避免优化状态残留。
    """
    prob = om.Problem()
    model = prob.model

    for i in range(n_cases):
        promotes_out = [(var, f"{var}_{i}") for var in _PER_CASE_OUTPUTS]
        model.add_subsystem(
            f"blade_{i}",
            CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options),
            promotes_inputs=_SHARED_INPUTS + [("Uhub", f"Uhub_{i}")],
            promotes_outputs=promotes_out,
        )

    model.add_subsystem(
        "aep_comp",
        AEPAggregator(weights=f_weights),
        promotes_inputs=[f"P_{i}" for i in range(n_cases)],
        promotes_outputs=["AEP"],
    )

    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options["optimizer"] = "SLSQP"
    prob.driver.options["maxiter"]   = 500
    prob.driver.options["tol"]       = 1e-5
    prob.driver.options["disp"]      = False

    # 设计变量：非圆柱截面弦长，idx n_fix: 即 idx 2~12
    # 注意：indices 对应 chord 数组下标，圆柱截面(idx 0~1)不在优化范围内
    prob.model.add_design_var(
        "chord",
        lower=chord_lower[n_fix:],
        upper=chord_upper[n_fix:],
        units="m",
        indices=list(range(n_fix, n_span)),
        ref=0.2,
    )
    prob.model.add_objective("AEP", scaler=-1.0)

    # 失速约束：圆柱(idx 0–1)不施加，DU/SG/SD/S1223(idx 2–13)均≤10°
    for i in range(n_cases):
        prob.model.add_constraint(f"alpha_{i}", upper=ALPHA_UPPER_NSEC,
                                  units="deg", indices=NON_CYL_IDX)

    # 弦长单调递减约束：chord[k] ≥ chord[k+1]（从 idx 2 到 idx 13 全程单调）
    # 防止优化器产生局部锯齿或 idx 边界处的弦长跳降
    model.add_subsystem(
        "chord_mono",
        ChordMonoComp(non_cyl_idx=NON_CYL_IDX, n_span=n_span),
        promotes_inputs=["chord"],
    )
    prob.model.add_constraint("chord_mono.chord_mono_diff", lower=0.0)

    # 若 CCBladeTwist 解析梯度出现问题，可取消注释以下行切换为有限差分：
    # prob.model.approx_totals(method="fd", step=1e-5, form="central")

    prob.setup(force_alloc_complex=True)
    return prob


def _run_one(chord_init):
    """单次多风况 AEP 弦长优化，返回 (AEP, chord_opt, status, prob)"""
    prob = _build_prob()
    set_shared_inputs(prob)
    for i in range(n_cases):
        prob.set_val(f"Uhub_{i}", V_cases[i], units="m/s")
    prob.set_val("chord", chord_init, units="m")

    fail = prob.run_driver()

    AEP_val    = prob.get_val("AEP")[0]
    chord_res  = prob.get_val("chord", units="m").copy()
    status     = "✓" if not fail else "✗"
    return AEP_val, chord_res, status, prob


# ========== 多起点运行 ==========
n_runs = 8
np.random.seed(42)

best_AEP   = -np.inf
best_chord = None
best_prob  = None
run_log    = []

print(f"\n开始多起点优化  (n_runs={n_runs}) ...")
for i in range(n_runs):
    if i == 0:
        chord_init_i = chord.copy()   # 第一次用原始弦长
    else:
        # 在原始弦长基础上叠加比例扰动，覆盖 [0.05, 0.70] 上下界
        noise = np.random.uniform(-0.30, 0.50, size=n_span - n_fix) * chord[n_fix:]
        chord_init_i = chord.copy()
        chord_init_i[n_fix:] = np.clip(chord[n_fix:] + noise,
                                        chord_lower[n_fix:], chord_upper[n_fix:])

    t0 = time.time()
    AEP_i, chord_i, status, prob_i = _run_one(chord_init_i)
    dt = time.time() - t0

    run_log.append({"run": i, "AEP": AEP_i, "chord": chord_i, "status": status})
    print(f"  Run {i + 1:2d}/{n_runs} {status}: AEP_proxy = {AEP_i:.1f} W  ({dt:.1f}s)")

    if AEP_i > best_AEP:
        best_AEP   = AEP_i
        best_chord = chord_i.copy()
        best_prob  = prob_i

n_success = sum(1 for lg in run_log if lg["status"] == "✓")
AEP_vals  = [lg["AEP"] for lg in run_log]
print(f"\n{'=' * 60}")
print(f"成功收敛: {n_success}/{n_runs}")
print(f"AEP_proxy 分布: min={min(AEP_vals):.1f}  max={max(AEP_vals):.1f}  "
      f"std={np.std(AEP_vals):.2e}  (std < 1 说明收敛稳定)")

# --- Fix C: 锯齿形局部最优过滤 ---
# 若多次运行中有 AEP 在最优值 0.5% 以内的方案，优先选展向弦长更平滑的解
# 平滑度指标：相邻截面弦长差的平方和（越小越平滑）
def _smoothness(c):
    return float(np.sum(np.diff(c[n_fix:]) ** 2))

AEP_threshold = best_AEP * 0.995   # 容忍 0.5% 以内的 AEP 损失
candidates = [lg for lg in run_log
              if lg["status"] == "✓" and lg["AEP"] >= AEP_threshold]
if len(candidates) > 1:
    best_candidate = min(candidates, key=lambda lg: _smoothness(lg["chord"]))
    if best_candidate["run"] != next(
        (lg["run"] for lg in run_log if lg["AEP"] == best_AEP), -1
    ):
        alt_AEP = best_candidate["AEP"]
        alt_smooth = _smoothness(best_candidate["chord"])
        orig_smooth = _smoothness(best_chord)
        print(f"\n[锯齿过滤] 在 AEP ≥ {AEP_threshold:.1f} W 的方案中选最平滑解:")
        print(f"  原最优: AEP={best_AEP:.1f} W  平滑度={orig_smooth:.6f}")
        print(f"  平滑优先: AEP={alt_AEP:.1f} W  平滑度={alt_smooth:.6f}")
        # 若平滑度改善超过 20%，切换到更平滑的解
        if alt_smooth < orig_smooth * 0.80:
            best_chord = best_candidate["chord"].copy()
            best_AEP   = best_candidate["AEP"]
            # 重新取对应的 prob（需重新运行以获取输出量）
            best_prob = _run_one(best_chord)[3]
            print(f"  → 已切换到平滑解 (平滑度改善 {(1-alt_smooth/orig_smooth)*100:.1f}%)")
        else:
            print(f"  → 平滑度改善不足 20%，保持 AEP 最优解")


# ================================================================
# 8c. 后处理：弦长单调递减光滑（工程要求）
# ================================================================
# 实际叶片从最大弦长位置到叶尖必须单调递减，锯齿状分布工程上不被允许
# （会导致三维流动分离、制造困难、结构应力集中）。
# 若优化结果存在单调性违反，自动寻找最小样条平滑因子使其满足单调递减；
# 若样条仍不够则用 Pool-Adjacent-Violators (PAV) 兜底。

from scipy.interpolate import UnivariateSpline as _USpline


def _monotone_smooth_chord(c_raw, r_arr, n_fix_idx, c_lower, c_upper):
    """
    对 idx n_fix_idx: 的弦长做单调递减光滑。
    返回 (chord_smoothed, smooth_factor_used)
    """
    r_var = r_arr[n_fix_idx:]
    c_var = c_raw[n_fix_idx:]
    n_var = len(r_var)
    lo    = c_lower[n_fix_idx:]
    hi    = c_upper[n_fix_idx:]

    # 从最小平滑因子开始递增搜索
    for sf in [0.0, 1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2]:
        if sf == 0.0:
            c_s = c_var.copy()
        else:
            spl = _USpline(r_var, c_var, k=3, s=sf * n_var)
            c_s = spl(r_var)
        c_s = np.clip(c_s, lo, hi)
        if np.all(np.diff(c_s) <= 1e-8):          # 满足单调递减（含数值容差）
            chord_out = c_raw.copy()
            chord_out[n_fix_idx:] = c_s
            return chord_out, sf

    # 兜底：PAV 算法强制单调递减
    c_pav = c_var.copy()
    changed = True
    while changed:
        changed = False
        for k in range(len(c_pav) - 1):
            if c_pav[k] < c_pav[k + 1]:
                avg = 0.5 * (c_pav[k] + c_pav[k + 1])
                c_pav[k] = c_pav[k + 1] = avg
                changed = True
    c_pav = np.clip(c_pav, lo, hi)
    chord_out = c_raw.copy()
    chord_out[n_fix_idx:] = c_pav
    return chord_out, "PAV"


def _eval_aep_only(chord_val):
    """仅 run_model（不优化），评估给定弦长的 AEP，供光滑后校验。"""
    _p = _build_prob()
    set_shared_inputs(_p)
    for _i in range(n_cases):
        _p.set_val(f"Uhub_{_i}", V_cases[_i], units="m/s")
    _p.set_val("chord", chord_val, units="m")
    _p.run_model()
    return _p.get_val("AEP")[0], _p


# 检查当前最优弦长是否满足单调递减
diffs = np.diff(best_chord[n_fix:])
if np.all(diffs <= 0):
    print("\n[弦长光滑] 优化结果已满足单调递减，无需光滑。")
else:
    n_viol = np.sum(diffs > 0)
    print(f"\n[弦长光滑] 检测到 {n_viol} 处单调性违反，开始光滑处理 ...")

    chord_smoothed, sf_used = _monotone_smooth_chord(
        best_chord, r, n_fix, chord_lower, chord_upper
    )
    AEP_smoothed, prob_smoothed = _eval_aep_only(chord_smoothed)
    AEP_loss_pct = (best_AEP - AEP_smoothed) / best_AEP * 100

    print(f"  平滑因子      : {sf_used}")
    print(f"  光滑前 AEP    : {best_AEP:.2f} W")
    print(f"  光滑后 AEP    : {AEP_smoothed:.2f} W  (损失 {AEP_loss_pct:.3f}%)")

    # 无论损失多少都采用光滑结果（工程约束优先），但打印警告
    if AEP_loss_pct > 1.0:
        print(f"  ⚠ AEP 损失超过 1%，建议检查光滑结果是否合理。")
    best_chord = chord_smoothed
    best_AEP   = AEP_smoothed
    best_prob  = prob_smoothed
    print(f"  → 已采用光滑结果（弦长单调递减满足工程要求）")


# ================================================================
# 8d. [已禁用] 弦长曲线光滑优化（曲率最小化）
# ================================================================
# 原因: 含 Prandtl tip loss 的最优弦长在叶尖段 (r > 2.5m) 应快速下降
#   (Wind Energy Handbook Fig 3.37: 叶尖段 blade geometry parameter
#   约为无 tip loss 的一半)。曲率最小化会惩罚叶尖段的快速弦长变化，
#   将物理上正确的 tip-loss-driven chord drop 抹平为近似线性 taper。
# 如需重新启用：设 ENABLE_SMOOTHING_8D = True
ENABLE_SMOOTHING_8D = False

if ENABLE_SMOOTHING_8D:
    print("\n" + "=" * 60)
    print("8d. 弦长曲线光滑优化（曲率最小化）")
    print("=" * 60)

if not ENABLE_SMOOTHING_8D:
    print()
    print("=" * 60)
    print("8d,8e. [跳过] 曲率最小化 & 参数化拟合")
    print("=" * 60)
    print("ENABLE_SMOOTHING_8D=False, tip loss driven chord drop preserved")
else:
    _AEP_LOSS_TOL  = 1.0   # AEP 损失容忍上限 (%)
    _AEP_LOSS_WARN = 0.5   # AEP 损失警告阈值 (%)

    r_var    = r[n_fix:]
    c_base   = best_chord[n_fix:].copy()
    n_var_sm = len(r_var)


    def _second_diff_cost(c_arr):
        """离散二阶差分平方和（曲率代理，越小越平滑）"""
        return float(np.sum(np.diff(np.diff(c_arr)) ** 2))


    sf_grid    = [0.0, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 3e-2, 6e-2, 0.10, 0.20]
    smooth_log = []
    AEP_ref    = best_AEP

    print(f"\n搜索平滑因子（AEP 损失容限 {_AEP_LOSS_TOL:.1f}%）:")
    print(f"  {'sf':>8s}  {'曲率(×10⁻⁴)':>12s}  {'AEP(W)':>10s}  {'ΔAEP%':>8s}  {'单调':>4s}")

    for _sf in sf_grid:
        if _sf <= 0:
            _c_s = c_base.copy()
        else:
            _spl = _USpline(r_var, c_base, k=3, s=_sf * n_var_sm)
            _c_s = _spl(r_var)
        _c_s    = np.clip(_c_s, chord_lower[n_fix:], chord_upper[n_fix:])
        _mono   = bool(np.all(np.diff(_c_s) <= 1e-8))
        _c_full = best_chord.copy()
        _c_full[n_fix:] = _c_s
        _aep_s, _prob_s = _eval_aep_only(_c_full)
        _loss   = (AEP_ref - _aep_s) / AEP_ref * 100.0
        _curv   = _second_diff_cost(_c_s)
        smooth_log.append({
            "sf": _sf, "chord": _c_s.copy(), "AEP": _aep_s,
            "loss_pct": _loss, "curvature": _curv,
            "mono": _mono, "prob": _prob_s,
        })
        print(f"  {_sf:8.2e}  {_curv * 1e4:12.6f}  {_aep_s:10.1f}  {_loss:+8.3f}%  {'✓' if _mono else '✗'}")

    # 选 AEP 损失 ≤ 容限且弦长单调递减的方案中曲率最小（最平滑）的
    _valid_sm = [lg for lg in smooth_log
                 if lg["loss_pct"] <= _AEP_LOSS_TOL and lg["mono"]]
    if not _valid_sm:
        # 放宽单调约束（单调递减已由 8c 保证，此处仅为兜底）
        _valid_sm = [lg for lg in smooth_log if lg["loss_pct"] <= _AEP_LOSS_TOL]

    if not _valid_sm:
        print(f"\n[曲线光滑] 所有平滑因子均超过 AEP 损失 {_AEP_LOSS_TOL:.1f}%，跳过。")
    else:
        _chosen = min(_valid_sm, key=lambda lg: lg["curvature"])
        _chord_sm = best_chord.copy()
        _chord_sm[n_fix:] = _chosen["chord"]

        _curv_base = _second_diff_cost(c_base)
        _curv_impv = (1.0 - _chosen["curvature"] / _curv_base) * 100.0 if _curv_base > 0 else 0.0

        print(f"\n[曲线光滑] 最优方案  sf = {_chosen['sf']:.2e}")
        print(f"  光滑前曲率 (×10⁻⁴) : {_curv_base * 1e4:.6f}")
        print(f"  光滑后曲率 (×10⁻⁴) : {_chosen['curvature'] * 1e4:.6f}  (改善 {_curv_impv:.1f}%)")
        print(f"  AEP 损失            : {_chosen['loss_pct']:+.3f}%")
        if _chosen["loss_pct"] > _AEP_LOSS_WARN:
            print(f"  ⚠ AEP 损失超过 {_AEP_LOSS_WARN:.1f}%，请确认是否接受。")

        # 打印光滑前后弦长对比
        print(f"\n  {'r(m)':>6s}  {'优化弦长':>10s}  {'光滑弦长':>10s}  {'Δchord':>8s}")
        for _j, (_r, _co, _cs) in enumerate(zip(r[n_fix:], c_base, _chosen["chord"])):
            print(f"  {_r:6.3f}  {_co:10.4f}  {_cs:10.4f}  {_cs - _co:+8.4f}")

        best_chord = _chord_sm
        best_AEP   = _chosen["AEP"]
        best_prob  = _chosen["prob"]
        print(f"\n  → 已采用光滑弦长结果")


    # ================================================================
    # 8e. 工程光滑后处理：参数化曲线拟合（工程质量优先，允许 AEP 损失）
    # ================================================================
    # 从叶片设计工程视角，光滑弦长分布的工程价值：
    #   ① 单调递减 + C∞ 连续 → 无锯齿、无应力集中、无 3D 流动分离
    #   ② 低曲率             → 便于模具加工与纤维铺层贴合
    #   ③ 根段到叶尖自然收束 → 结构-气动匹配良好
    # 8d 已在 ΔAEP ≤ 1% 内做过样条光滑；本节允许更高 AEP 损失
    # (_AEP_LOSS_ENG_TOL，默认 3%)，以换取更强的工程可制造性。
    # 候选方案：
    #   - 多项式拟合 (阶 2/3/4/5)：C∞ 连续、无任何锯齿
    #   - Bezier 曲线 (n_ctrl 4/5/6)：端点严格保持、形状可控
    #   - 幂律模型 c(r) = a·(R−r)^p + b：经典变桨叶片工程形式
    # 选优：AEP 损失 ≤ 容限 且 单调递减，取曲率代理最小者。

    from scipy.special import comb as _comb
    from scipy.optimize import least_squares as _lsq

    _AEP_LOSS_ENG_TOL  = 3.0   # %, AEP 损失容忍上限（工程质量优先，可放宽）
    _AEP_LOSS_ENG_WARN = 2.0   # %, AEP 损失警告阈值

    print("\n" + "=" * 60)
    print(f"8e. 工程光滑后处理（参数化拟合，AEP 损失容限 {_AEP_LOSS_ENG_TOL:.1f}%）")
    print("=" * 60)

    _r_var_e   = r[n_fix:]
    _c_base_e  = best_chord[n_fix:].copy()
    _AEP_ref_e = best_AEP
    _t_norm_e  = (_r_var_e - _r_var_e[0]) / (_r_var_e[-1] - _r_var_e[0])


    def _bezier_curve(t, ctrl):
        """N 阶 Bezier 曲线求值，t∈[0,1]"""
        n = len(ctrl) - 1
        vals = np.zeros_like(t, dtype=float)
        for i in range(n + 1):
            vals += _comb(n, i) * (t ** i) * ((1.0 - t) ** (n - i)) * ctrl[i]
        return vals


    def _fit_bezier(t_norm, c_arr, n_ctrl):
        """端点固定的 n_ctrl 阶 Bezier 最小二乘拟合"""
        def residual(mid):
            ctrl = np.concatenate([[c_arr[0]], mid, [c_arr[-1]]])
            return _bezier_curve(t_norm, ctrl) - c_arr
        mid_init = np.linspace(c_arr[0], c_arr[-1], n_ctrl)[1:-1]
        res = _lsq(residual, mid_init)
        ctrl_full = np.concatenate([[c_arr[0]], res.x, [c_arr[-1]]])
        return _bezier_curve(t_norm, ctrl_full)


    def _fit_poly(t_norm, c_arr, order):
        """阶数为 order 的多项式最小二乘拟合（t 归一化以改善数值条件）"""
        coef = np.polyfit(t_norm, c_arr, order)
        return np.polyval(coef, t_norm)


    def _fit_power_law(r_arr, c_arr):
        """c(r) = a·(R_end − r)^p + b 幂律拟合（经典叶片工程形式）"""
        R_end = r_arr[-1] + 1e-3
        def residual(params):
            a, p, b = params
            return a * (R_end - r_arr) ** p + b - c_arr
        params_init = [max(c_arr[0] - c_arr[-1], 0.05), 1.0, c_arr[-1]]
        bounds = ([0.0, 0.1, 0.0], [2.0, 5.0, 1.0])
        res = _lsq(residual, params_init, bounds=bounds)
        a, p, b = res.x
        return a * (R_end - r_arr) ** p + b


    # ----- 构建候选方案 -----
    _cands_e = []

    for _ord in [2, 3, 4, 5]:
        try:
            _c_s = _fit_poly(_t_norm_e, _c_base_e, _ord)
            _cands_e.append((f"poly-{_ord}", _c_s))
        except Exception as _ex:
            print(f"  poly-{_ord} 拟合失败: {_ex}")

    for _n in [4, 5, 6]:
        try:
            _c_s = _fit_bezier(_t_norm_e, _c_base_e, _n)
            _cands_e.append((f"bezier-{_n}", _c_s))
        except Exception as _ex:
            print(f"  bezier-{_n} 拟合失败: {_ex}")

    try:
        _c_s = _fit_power_law(_r_var_e, _c_base_e)
        _cands_e.append(("power-law", _c_s))
    except Exception as _ex:
        print(f"  power-law 拟合失败: {_ex}")

    # ----- 评价每个候选 -----
    print(f"\n{'方案':>10s}  {'曲率(×10⁻⁴)':>12s}  {'最大偏差(m)':>11s}  "
          f"{'AEP(W)':>10s}  {'ΔAEP%':>8s}  {'单调':>4s}")
    print("-" * 72)

    _log_e = []
    for _name, _c_s in _cands_e:
        _c_clip = np.clip(_c_s, chord_lower[n_fix:], chord_upper[n_fix:])
        _mono   = bool(np.all(np.diff(_c_clip) <= 1e-8))
        _cf     = best_chord.copy()
        _cf[n_fix:] = _c_clip
        _aep_i, _prob_i = _eval_aep_only(_cf)
        _loss_i = (_AEP_ref_e - _aep_i) / _AEP_ref_e * 100.0
        _curv_i = _second_diff_cost(_c_clip)
        _mdev_i = float(np.max(np.abs(_c_clip - _c_base_e)))
        _log_e.append({
            "name": _name, "chord": _c_clip, "AEP": _aep_i,
            "loss_pct": _loss_i, "curvature": _curv_i,
            "mono": _mono, "max_dev": _mdev_i, "prob": _prob_i,
        })
        print(f"  {_name:>8s}  {_curv_i * 1e4:12.6f}  {_mdev_i:11.5f}  "
              f"{_aep_i:10.1f}  {_loss_i:+8.3f}%  {'✓' if _mono else '✗'}")

    # ----- 选优：AEP 损失在容限内且单调递减，取曲率最小 -----
    _valid_e = [lg for lg in _log_e
                if lg["loss_pct"] <= _AEP_LOSS_ENG_TOL and lg["mono"]]

    if not _valid_e:
        print(f"\n[工程光滑] 无候选满足 (AEP 损失 ≤ {_AEP_LOSS_ENG_TOL:.1f}% 且单调递减)，"
              f"保留 8d 结果。")
    else:
        _best_e = min(_valid_e, key=lambda lg: lg["curvature"])
        _curv_b = _second_diff_cost(_c_base_e)
        _impv_e = ((1.0 - _best_e["curvature"] / _curv_b) * 100.0
                   if _curv_b > 0 else 0.0)

        print(f"\n[工程光滑] 最优方案: {_best_e['name']}")
        print(f"  曲率 (×10⁻⁴)       : {_curv_b * 1e4:.6f} → "
              f"{_best_e['curvature'] * 1e4:.6f}  (改善 {_impv_e:.1f}%)")
        print(f"  最大弦长偏差       : {_best_e['max_dev']:.5f} m")
        print(f"  AEP 损失           : {_best_e['loss_pct']:+.3f}%")
        if _best_e["loss_pct"] > _AEP_LOSS_ENG_WARN:
            print(f"  ⚠ AEP 损失 > {_AEP_LOSS_ENG_WARN:.1f}%，请工程师确认是否接受。")

        print(f"\n  {'r(m)':>6s}  {'优化弦长':>10s}  {'工程光滑':>10s}  {'Δchord':>8s}")
        for _rj, _cob, _cse in zip(r[n_fix:], _c_base_e, _best_e["chord"]):
            print(f"  {_rj:6.3f}  {_cob:10.4f}  {_cse:10.4f}  {_cse - _cob:+8.4f}")

        _chord_eng = best_chord.copy()
        _chord_eng[n_fix:] = _best_e["chord"]
        best_chord = _chord_eng
        best_AEP   = _best_e["AEP"]
        best_prob  = _best_e["prob"]
        print(f"\n  → 已采用工程光滑结果（制造/结构友好，工程质量优先）")


# ================================================================
# 9. 输出结果
# ================================================================

print("\n" + "=" * 60)
print("优化结果")
print("=" * 60)
print(f"\nAEP_proxy = {best_AEP:.1f} W  (加权平均功率，最优弦长)")

P_cases  = []
CP_cases = []
print(f"\n{'工况':>4s} {'V(m/s)':>7s} {'权重f_i':>8s} {'CP':>8s} "
      f"{'P(W)':>10s} {'f_i×P(W)':>10s} {'能量贡献%':>9s}")
for i in range(n_cases):
    P_i  = best_prob.get_val(f"P_{i}")[0]
    CP_i = best_prob.get_val(f"CP_{i}")[0]
    P_cases.append(P_i)
    CP_cases.append(CP_i)
    contrib = f_weights[i] * P_i
    print(f"  V{i + 1}  {V_cases[i]:7.1f}  {f_weights[i]:8.3f}  {CP_i:8.4f}  "
          f"{P_i:10.1f}  {contrib:10.1f}  {contrib / best_AEP * 100:8.1f}%")

Px_peak  = best_prob.get_val(f"Px_b_{I_PEAK}")
T_approx = np.trapz(Px_peak, r) * n_blades
print(f"\n推力 ≈ {T_approx:.1f} N  "
      f"(V={V_cases[I_PEAK]:.1f} m/s 工况，Px_b 展向积分)")

alpha_peak = best_prob.get_val(f"alpha_{I_PEAK}", units="deg")
cl_peak    = best_prob.get_val(f"cl_{I_PEAK}")
cd_peak    = best_prob.get_val(f"cd_{I_PEAK}")

print(f"\n--------- 截面气动量 (V={V_cases[I_PEAK]:.1f} m/s, 能量峰值工况) ---------")
print(f"{'r(m)':>6s} {'chord_old':>10s} {'chord_new':>10s} {'Δchord':>8s} "
      f"{'alpha':>8s} {'cl':>8s} {'cd':>8s} {'cl/cd':>8s}")
for j in range(n_span):
    ld = cl_peak[j] / cd_peak[j] if cd_peak[j] > 1e-6 else 0
    dc = best_chord[j] - chord[j]
    print(f"{r[j]:6.2f} {chord[j]:10.4f} {best_chord[j]:10.4f} "
          f"{dc:+8.4f} "
          f"{alpha_peak[j]:8.2f} {cl_peak[j]:8.4f} {cd_peak[j]:8.4f} {ld:8.1f}")

np.savez(
    "chord_optimization_results_AEP.npz",
    r=r, chord_init=chord, chord_opt=best_chord,
    twist_fixed=twist_fixed_deg,
    V_cases=V_cases, f_weights=f_weights,
    P_cases=np.array(P_cases), CP_cases=np.array(CP_cases),
    AEP=best_AEP, T_approx=T_approx,
    alpha_peak=alpha_peak, cl_peak=cl_peak, cd_peak=cd_peak,
)
print("\n结果已保存到 chord_optimization_results_AEP.npz")


# ================================================================
# 10. 关注风况评估：3 / 15 / 18 m/s 优化前后对比
# ================================================================

V_eval = [3.0, 5.0, 15.0, 18.0]

prob_eval = om.Problem()
prob_eval.model.add_subsystem(
    "blade",
    CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options),
    promotes=["*"],
)
prob_eval.setup()
set_shared_inputs(prob_eval)


def _eval_at(wind_speed, chord_in):
    """在给定风速和弦长下运行一次 BEM，返回 (CP, P, T_approx)"""
    prob_eval.set_val("Uhub",  wind_speed, units="m/s")
    prob_eval.set_val("chord", chord_in,   units="m")
    prob_eval.run_model()
    CP_val = prob_eval.get_val("CP")[0]
    P_val  = prob_eval.get_val("P")[0]
    T_val  = np.trapz(prob_eval.get_val("Px_b"), r) * n_blades
    return CP_val, P_val, T_val


print("\n" + "=" * 60)
print("关注风况：优化前后对比  (V = 3 / 5 / 15 / 18 m/s)")
print("=" * 60)
print(f"\n{'':>22s}  {'V=3 m/s':>20s} {'V=5 m/s':>20s} {'V=15 m/s':>20s}  {'V=18 m/s':>20s}")
print(f"{'':>22s}  {'CP / P(W) / T(N)':>20s}  {'CP / P(W) / T(N)':>20s}  {'CP / P(W) / T(N)':>20s}  {'CP / P(W) / T(N)':>20s}")
print("-" * 86)

results_eval = {}
for label, chord_in in [("优化前 (初始弦长)", chord),
                         ("优化后 (AEP最优)",  best_chord)]:
    row = {}
    for V in V_eval:
        cp, p, t = _eval_at(V, chord_in)
        row[V] = (cp, p, t)
    results_eval[label] = row
    vals = "  ".join(
        f"  {row[V][0]:.4f} / {row[V][1]:7.1f} / {row[V][2]:7.1f}"
        for V in V_eval
    )
    print(f"{label:>22s}  {vals}")

print()
print("各项变化量 (优化后 - 优化前):")
print(f"  {'指标':>6s}  {'V=3 m/s':>14s}  {'V=5 m/s':>14s}  {'V=15 m/s':>14s}  {'V=18 m/s':>14s}")
for metric, idx in [("ΔCP", 0), ("ΔP(W)", 1), ("ΔT(N)", 2)]:
    row_before = results_eval["优化前 (初始弦长)"]
    row_after  = results_eval["优化后 (AEP最优)"]
    diffs = "  ".join(
        f"  {row_after[V][idx] - row_before[V][idx]:+12.4f}"
        for V in V_eval
    )
    print(f"  {metric:>6s}  {diffs}")


# ================================================================
# 11. 可视化
# ================================================================

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(f"多风况加权弦长优化  AEP_proxy={best_AEP:.1f} W", fontsize=14)

    # [0,0] 弦长分布对比
    axes[0, 0].plot(r, chord,      "b--o", ms=4, label="初始")
    axes[0, 0].plot(r, best_chord, "r-s",  ms=4, label="优化")
    axes[0, 0].set_xlabel("r (m)"); axes[0, 0].set_ylabel("弦长 (m)")
    axes[0, 0].legend(); axes[0, 0].grid(True)
    axes[0, 0].set_title("弦长分布")

    # [0,1] 各工况攻角分布
    for i in range(n_cases):
        alpha_i = best_prob.get_val(f"alpha_{i}", units="deg")
        axes[0, 1].plot(r, alpha_i, "-o", ms=3, color=colors[i],
                        label=f"V={V_cases[i]:.1f} m/s  (f={f_weights[i]:.3f})")
    axes[0, 1].axhline(10.0, color="crimson", ls="--", lw=1.2, label="失速上限 10°")
    axes[0, 1].set_xlabel("r (m)"); axes[0, 1].set_ylabel("攻角 (°)")
    axes[0, 1].legend(fontsize=7); axes[0, 1].grid(True)
    axes[0, 1].set_title("各工况攻角分布")

    # [0,2] 各工况功率与 AEP 贡献
    bar_x    = np.arange(n_cases)
    contribs = [f_weights[i] * P_cases[i] for i in range(n_cases)]
    axes[0, 2].bar(bar_x, P_cases, color=colors, alpha=0.6, label="P_i")
    ax2 = axes[0, 2].twinx()
    ax2.plot(bar_x, contribs, "k-D", ms=6, label="f_i×P_i (AEP贡献)")
    axes[0, 2].set_xticks(bar_x)
    axes[0, 2].set_xticklabels([f"{v:.1f}" for v in V_cases])
    axes[0, 2].set_xlabel("风速 (m/s)"); axes[0, 2].set_ylabel("功率 P_i (W)")
    ax2.set_ylabel("AEP贡献 f_i×P_i (W)")
    axes[0, 2].set_title("各工况功率与 AEP 贡献")
    ax2.legend(loc="upper left", fontsize=8)

    # [1,0] 多起点收敛散点
    run_ids  = [lg["run"] + 1 for lg in run_log]
    aep_vals = [lg["AEP"]     for lg in run_log]
    dot_cols = ["g" if lg["status"] == "✓" else "r" for lg in run_log]
    axes[1, 0].scatter(run_ids, aep_vals, c=dot_cols, s=60, zorder=3)
    axes[1, 0].axhline(best_AEP, color="k", ls="--", lw=1,
                        label=f"最优 {best_AEP:.1f} W")
    axes[1, 0].set_xlabel("起点编号"); axes[1, 0].set_ylabel("AEP_proxy (W)")
    axes[1, 0].legend(fontsize=8); axes[1, 0].grid(True)
    axes[1, 0].set_title("多起点收敛分布  (绿=成功 红=未收敛)")

    # [1,1] 升阻比（能量峰值工况）
    ld = np.where(cd_peak > 1e-6, cl_peak / cd_peak, 0)
    axes[1, 1].plot(r, ld, "m-o", ms=4)
    axes[1, 1].set_xlabel("r (m)"); axes[1, 1].set_ylabel("Cl/Cd")
    axes[1, 1].grid(True)
    axes[1, 1].set_title(f"升阻比  (V={V_cases[I_PEAK]:.1f} m/s)")

    # [1,2] AEP 贡献饼图
    labels = [f"V={v:.1f} m/s\nf={w:.3f}" for v, w in zip(V_cases, f_weights)]
    axes[1, 2].pie(contribs, labels=labels, colors=colors,
                   autopct="%1.1f%%", startangle=90,
                   textprops={"fontsize": 8})
    axes[1, 2].set_title("AEP 贡献分布 (f_i×P_i)")

    plt.tight_layout()
    plt.savefig("chord_optimization_AEP.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("图表已保存到 chord_optimization_AEP.png")
except ImportError:
    print("未安装 matplotlib，跳过可视化")


# ==================代办=====================
# 1. 弦长与扭角联合优化：同时将 theta_in 和 chord 作为设计变量
# 2. 加载扭角优化结果：取消注释 Section 2 中 twist_npz 相关代码，接力使用最优扭角
# 3. 若仍有锯齿，可进一步缩紧 chord_upper 或增大 maxiter
