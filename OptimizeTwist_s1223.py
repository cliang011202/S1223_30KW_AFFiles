"""
叶片扭角优化 V3 —— 多风况加权 AEP
策略: 最大化 AEP = Σ f_i × P(V_i, twist)
约束: 各工况攻角不超过失速限制（DU-06-W-200 ≤ 9°，其余翼型 ≤ 10°）

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

  AEP = Σ f_i × P_i
    f_i: 时间频率权重 (非能量权重)
    能量贡献通过 P_i ∝ V_i^3 自然体现，f_i 无需额外乘 V^3

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
# 代表风速：按等能量贡献划分，覆盖有效发电段 [3, 18] m/s
V_cases   = np.array([5.0,  6.5,  7.5,  8.5,  11.0])   # m/s
# 时间频率权重（有效发电段内归一化，合计=1.0）
f_weights = np.array([0.537, 0.164, 0.125, 0.083, 0.091])
n_cases   = len(V_cases)
I_PEAK    = 2   # 能量峰值工况索引 (V=7.5 m/s)

n_opt_twist = 1
n_opt_chord = 8

r = np.array([  0.202 ,0.350 ,0.676 ,0.967 ,1.135 ,
                1.483 ,1.664 ,1.850 ,2.036 ,2.217 ,
                2.398 ,2.565 ,3.024 ,3.498 ])

chord = np.array([  0.2500 , 0.2500 , 0.6000 , 0.5192 , 0.4681 ,
                    0.3500 , 0.3200 , 0.2896 , 0.2536 , 0.2224 ,
                    0.1954 , 0.1741 , 0.1331 , 0.1182 ])

twist_init_deg = np.array([18.20, 18.20, 18.20, 10.38,  7.54,
                            4.29,  3.46,  2.97,  2.72,  2.60,
                            2.56,  2.56,  2.45,  1.68])

rthick = np.array([100.0, 100.0, 19.8, 19.8, 19.8,
                   16.0, 16.0, 16.0, 14.0, 14.0,
                   14.0, 12.1, 12.1, 12.1])

n_span = len(r)

is_cylinder = [True, True, False, False, False,
               False, False, False, False, False,
               False, False, False, False,]

# 分截面失速约束上限 (degrees)
# 圆柱截面 (idx 0–1):    不施加约束——入流角 30–44° 由几何决定，BEM 攻角无翼型失速意义
# DU-06-W-200 (idx 2–4): t/c=19.8%，Re≈0.3~0.5M 时实测 Cl_max 约对应 α≈9~11°；
#                         取 9° 作为失速上限，预留 ~1° 工程余量（弦长大、内段攻角敏感）
# SG6050 (idx 5–7):      Re≈0.3~0.5M 专为低 Re 设计，Cl_max 对应 α≈10~12°，取 10°
# SD7062 (idx 8–10):     Re≈0.3~0.5M 低 Re 风机翼型，Cl_max 对应 α≈10~11°，取 10°
# S1223  (idx 11–13):    Re≈0.3M 时 Cl_max 对应 α≈10°，取 10°（叶尖实度小，较安全）
NON_CYL_IDX      = list(range(2, n_span))          # idx 2~13，共 12 个截面（排除圆柱）
ALPHA_UPPER_NSEC = np.array([ 9.0,  9.0,  9.0,     # DU-06-W-200 (idx 2–4)  ← 9° 工程余量
                              10.0, 10.0, 10.0,     # SG6050      (idx 5–7)
                              10.0, 10.0, 10.0,     # SD7062      (idx 8–10)
                              10.0, 10.0, 10.0])    # S1223       (idx 11–13)

# === BEM Betz 最优初始扭角 ===
# 对于等 TSR 变速风机，入流角 φ(r) 与风速无关；Betz 最优扭角 = φ - α_des
# 圆柱段（idx 0–1）保留原始设计值；各翼型段 α_des 见下：
# DU-06-W-200 (idx 2–4): α_des=7°（厚翼型最佳工作攻角）
# SG6050      (idx 5–7): α_des=7°（中等弯度低Re翼型）
# SD7062      (idx 8–10): α_des=6°（低Re风机翼型）
# S1223       (idx 11–13): α_des=6°（高升力低Re翼型）
# 该扭角作为多起点的第一个起点，使优化器从物理最优解附近出发。
_alpha_des_init = np.zeros(n_span)
_alpha_des_init[2:5]  = 7.0   # DU-06-W-200 最佳工作攻角 (deg)
_alpha_des_init[5:8]  = 7.0   # SG6050      最佳工作攻角 (deg)
_alpha_des_init[8:11] = 6.0   # SD7062      最佳工作攻角 (deg)
_alpha_des_init[11:]  = 6.0   # S1223       最佳工作攻角 (deg)


def _betz_twist_deg(r_arr, R_tip, tsr_val, alpha_des):
    """
    Betz 最优扭角（度）：θ = φ_Betz(r) − α_des
    φ_Betz = arctan[(1−a)/((1+a')·λ_r)]，a=1/3（Betz 最优轴向诱导因子），
    a' 由叶素动量方程在 a=1/3 时求解：a'(1+a') = 2/(9λ_r²)
    """
    lam = tsr_val * r_arr / R_tip
    disc = np.sqrt(1.0 + 8.0 / (9.0 * lam**2))
    ap = 0.5 * (-1.0 + disc)                          # 切向诱导因子
    phi = np.degrees(np.arctan2(2.0 / 3.0, (1.0 + ap) * lam))
    return phi - alpha_des


twist_betz_deg = _betz_twist_deg(r, Rtip, tsr, _alpha_des_init)
twist_betz_deg[:2] = twist_init_deg[:2]               # 圆柱段保持原始设计值
# 裁剪至 ±8° 搜索范围内（Betz 最优应在此范围内；若偶发越界则限定边界）
twist_betz_deg = np.clip(twist_betz_deg, twist_init_deg - 8.0, twist_init_deg + 8.0)


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
        # 常数偏导直接声明为 val，无需在 compute_partials 中重复计算
        for i, w in enumerate(weights):
            self.declare_partials("AEP", f"P_{i}", val=float(w))

    def compute(self, inputs, outputs):
        weights = self.options["weights"]
        outputs["AEP"] = sum(weights[i] * inputs[f"P_{i}"][0]
                             for i in range(len(weights)))


# ================================================================
# 6. 辅助函数
# ================================================================

# 所有风速工况共享的输入（连续变量 + 离散变量）
# 这些变量在 promotes_inputs 中统一提升至 Problem 顶层，只需 set_val 一次
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

# 每个工况独立输出，重命名为 <var>_i 避免命名冲突
_PER_CASE_OUTPUTS = ["CP", "P", "alpha", "theta", "cl", "cd", "a", "ap", "Px_b"]


def set_shared_inputs(prob_obj):
    """设置所有工况共享的输入（仅需调用一次）"""
    prob_obj.set_val("airfoils_aoa", common_aoa, units="deg")
    prob_obj.set_val("airfoils_Re",  re_values)
    prob_obj.set_val("airfoils_cl",  cl_table)
    prob_obj.set_val("airfoils_cd",  cd_table)
    prob_obj.set_val("airfoils_cm",  cm_table)

    prob_obj.set_val("r",            r,                units="m")
    prob_obj.set_val("chord",        chord,            units="m")
    prob_obj.set_val("rthick",       rthick / 100.0)
    prob_obj.set_val("s_opt_theta",  s_opt_twist)
    prob_obj.set_val("s_opt_chord",  s_opt_chord)

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
# 7. 第一阶段：验证导数连通性（使用能量峰值工况 V=7.5 m/s）
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
prob_test.set_val("Uhub",     V_cases[I_PEAK], units="m/s")
prob_test.set_val("theta_in", twist_init_deg,  units="deg")
prob_test.run_model()

print(f"\n--- 基准输出 (V={V_cases[I_PEAK]:.1f} m/s) ---")
for name in ["CP", "P", "alpha", "cl", "cd"]:
    val = prob_test.get_val(name)
    if val.size == 1:
        print(f"  {name:>8s} = {val[0]:.6f}")
    else:
        print(f"  {name:>8s} = [{val[0]:.4f}, ..., {val[-1]:.4f}]  (len={val.size})")

print("\n--- 手动扰动检查 (第6截面 +2°) ---")
twist_perturbed = twist_init_deg.copy()
twist_perturbed[5] += 2.0
prob_test.set_val("theta_in", twist_perturbed, units="deg")
prob_test.run_model()
CP_perturbed = prob_test.get_val("CP")[0]

prob_test.set_val("theta_in", twist_init_deg, units="deg")
prob_test.run_model()
CP_original = prob_test.get_val("CP")[0]

print(f"  CP (原始)    = {CP_original:.6f}")
print(f"  CP (扰动+2°) = {CP_perturbed:.6f}")
print(f"  ΔCP          = {CP_perturbed - CP_original:.6f}")
if abs(CP_perturbed - CP_original) > 1e-10:
    print("  ✓ CP 对 theta_in 有响应，导数链连通")
else:
    print("  ✗ CP 对 theta_in 无响应，需排查")


# ================================================================
# 8. 第二阶段：多风况加权 AEP 扭角优化（多起点策略）
# ================================================================

print("\n" + "=" * 60)
print("第二阶段: 多风况加权 AEP 扭角优化（多起点）")
print("=" * 60)
print(f"代表风速 (m/s) : {V_cases}")
print(f"时间频率权重   : {f_weights}")
print(f"目标           : 最大化 AEP = Σ f_i × P_i")
print(f"约束           : DU截面(idx 2–4) alpha ≤ 9°，其余翼型截面 alpha ≤ 10°  "
      f"({n_cases} 工况 × {len(NON_CYL_IDX)} 截面 = {n_cases * len(NON_CYL_IDX)} 个约束)")


class TwistMonoComp(om.ExplicitComponent):
    """
    扭角单调递减约束辅助组件。
    输出 twist_mono_diff[k] = theta_in[non_cyl_idx[k]] − theta_in[non_cyl_idx[k+1]]
    约束 twist_mono_diff >= 0 即等价于 θ 沿展向单调递减。

    Jacobian 为常数稀疏矩阵，直接在 setup_partials 中声明，无运行时开销。
    """

    def initialize(self):
        self.options.declare("non_cyl_idx", recordable=False)
        self.options.declare("n_span",      recordable=False)

    def setup(self):
        idx    = self.options["non_cyl_idx"]
        n_diff = len(idx) - 1
        self.add_input("theta_in",        val=np.zeros(self.options["n_span"]), units="rad")
        self.add_output("twist_mono_diff", val=np.zeros(n_diff))

    def setup_partials(self):
        idx    = self.options["non_cyl_idx"]
        n_diff = len(idx) - 1
        # ∂diff[k]/∂theta_in[idx[k]]   = +1
        # ∂diff[k]/∂theta_in[idx[k+1]] = −1
        rows = np.concatenate([np.arange(n_diff), np.arange(n_diff)])
        cols = np.concatenate([np.array(idx[:-1]), np.array(idx[1:])])
        vals = np.concatenate([np.ones(n_diff), -np.ones(n_diff)])
        self.declare_partials("twist_mono_diff", "theta_in",
                              rows=rows, cols=cols, val=vals)

    def compute(self, inputs, outputs):
        idx = self.options["non_cyl_idx"]
        theta = inputs["theta_in"]
        outputs["twist_mono_diff"] = theta[idx[:-1]] - theta[idx[1:]]


def _build_prob_twist():
    """
    构建多风况扭角 AEP 优化 Problem。
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
    prob.driver.options["maxiter"]   = 1500
    prob.driver.options["tol"]       = 1e-5
    prob.driver.options["disp"]      = False

    # 设计变量：非圆柱截面扭角 (idx 2~12)，圆柱截面扭角对 BEM 无意义不参与优化
    n_fix_twist = NON_CYL_IDX[0]   # = 2
    prob.model.add_design_var(
        "theta_in",
        lower=np.deg2rad((twist_init_deg - 8.0)[n_fix_twist:]),
        upper=np.deg2rad((twist_init_deg + 8.0)[n_fix_twist:]),
        indices=NON_CYL_IDX,
        units="rad",
    )
    prob.model.add_objective("AEP", scaler=-1.0)

    # 分截面失速约束：圆柱(idx 0–1)不施加，DU(idx 2–4)≤9°，SG/SD/S1223(idx 5–13)≤10°
    for i in range(n_cases):
        prob.model.add_constraint(f"alpha_{i}", upper=ALPHA_UPPER_NSEC,
                                  units="deg", indices=NON_CYL_IDX)

    # 扭角单调递减约束：θ[k] ≥ θ[k+1]（等价于 diff[k] = θ[k]−θ[k+1] ≥ 0）
    # 适用于等 TSR 变速风机——入流角 φ(r) 随 r 单调减小，最优扭角因此单调递减；
    # 直接在优化器内部施加此约束，避免后处理光滑带来的 AEP 损失。
    model.add_subsystem(
        "twist_mono",
        TwistMonoComp(non_cyl_idx=NON_CYL_IDX, n_span=n_span),
        promotes_inputs=["theta_in"],
    )
    prob.model.add_constraint("twist_mono.twist_mono_diff", lower=0.0)

    prob.setup(force_alloc_complex=True)
    return prob


def _run_one_twist(twist_init):
    """单次多风况 AEP 扭角优化，返回 (AEP, twist_opt, status, prob)"""
    prob = _build_prob_twist()
    set_shared_inputs(prob)
    for i in range(n_cases):
        prob.set_val(f"Uhub_{i}", V_cases[i], units="m/s")
    prob.set_val("theta_in", twist_init, units="deg")

    fail = prob.run_driver()

    AEP_val   = prob.get_val("AEP")[0]
    # 取优化器决策变量 theta_in（圆柱段保持初始值，非圆柱段为真实优化结果）。
    # 不能取 theta_{I_PEAK}：CCBladeTwist 内部对 theta_in 做样条重插值，
    # 叶根端外推会产生振荡（如 idx 1 突增到 46°），不代表真实设计扭角。
    twist_res = prob.get_val("theta_in", units="deg").copy()
    status    = "✓" if not fail else "✗"
    return AEP_val, twist_res, status, prob


# ========== 多起点运行 ==========
# 起点策略：
#   Run 0 — BEM Betz 最优扭角（物理最优邻域，帮助收敛到全局最优）
#   Run 1 — 原始设计扭角（保留原始设计作为备选）
#   Run 2+ — BEM 最优扭角 + ±5° 均匀扰动（探索局部最优附近）
n_runs = n_opt_twist
np.random.seed(42)

best_AEP   = -np.inf
best_twist = None
best_prob  = None
run_log    = []

print(f"\n开始多起点扭角优化  (n_runs={n_runs}) ...")
print(f"  Run  1: 起点 = BEM Betz 最优扭角  {np.round(twist_betz_deg[2:], 2).tolist()}")
print(f"  Run  2: 起点 = 原始设计扭角")
print(f"  Run  3+: BEM 最优扭角 + ±5° 随机扰动")
_n_cyl = NON_CYL_IDX[0]   # = 2，圆柱截面数（设计变量不覆盖此范围）

for i in range(n_runs):
    if i == 0:
        twist_init_i = twist_betz_deg.copy()           # BEM 最优扭角作为第一起点
    elif i == 1:
        twist_init_i = twist_init_deg.copy()           # 原始设计扭角作为第二起点
    else:
        # BEM 最优扭角基础上叠加 ±5° 均匀扰动，保持在 ±8° 设计变量边界内
        noise = np.random.uniform(-5.0, 5.0, size=n_span)
        twist_init_i = np.clip(twist_betz_deg + noise,
                               twist_init_deg - 8.0, twist_init_deg + 8.0)
    # 圆柱截面不是设计变量，始终使用原始设计值，防止随机扰动污染输出
    twist_init_i[:_n_cyl] = twist_init_deg[:_n_cyl]

    t0 = time.time()
    AEP_i, twist_i, status, prob_i = _run_one_twist(twist_init_i)
    dt = time.time() - t0

    run_log.append({"run": i, "AEP": AEP_i, "twist": twist_i, "status": status})
    print(f"  Run {i + 1:2d}/{n_runs} {status}: AEP_proxy = {AEP_i:.1f} W  ({dt:.1f}s)")

    if AEP_i > best_AEP:
        best_AEP   = AEP_i
        best_twist = twist_i.copy()
        best_prob  = prob_i

n_success = sum(1 for lg in run_log if lg["status"] == "✓")
AEP_vals  = [lg["AEP"] for lg in run_log]
print(f"\n{'=' * 60}")
print(f"成功收敛: {n_success}/{n_runs}")
print(f"AEP_proxy 分布: min={min(AEP_vals):.1f}  max={max(AEP_vals):.1f}  "
      f"std={np.std(AEP_vals):.2e}  (std < 1 说明多起点收敛稳定)")


# ================================================================
# 8b. 单调性验证（优化器已内置约束，此处仅做断言性检查）
# ================================================================
# twist_mono.twist_mono_diff >= 0 已作为硬约束加入优化问题，
# 优化结果理论上直接满足单调递减，无需后处理光滑。
# 此检查仅用于捕获极端情况（数值精度导致的微小违反）。

theta_in_opt = best_prob.get_val("theta_in")               # shape (n_span,), rad
theta_noncyl = np.rad2deg(theta_in_opt[NON_CYL_IDX[0]:])
diffs_twist  = np.diff(theta_noncyl)
n_viol       = int(np.sum(diffs_twist > 1e-6))             # 忽略数值精度内的微小违反

if n_viol == 0:
    print("\n[扭角单调性] ✓ 满足单调递减（优化器内置约束生效）")
else:
    max_viol = np.max(diffs_twist)
    print(f"\n[扭角单调性] ⚠ 存在 {n_viol} 处违反，最大违反量 = {max_viol:.4f}°")
    print("  → 违反量极小时（< 0.01°）属数值精度，不影响工程使用；")
    print("    若违反量较大，请检查 SLSQP 收敛状态或增大 maxiter。")


# ================================================================
# 8c. 保存 SLSQP 原始最优解（后续光滑以此为基准，防止偏差叠加）
# ================================================================

best_twist_raw = best_twist.copy()
best_AEP_raw   = best_AEP

# ================================================================
# 8d. 扭角光滑后处理（修正外叶片平台区）
# ================================================================
# 问题：SLSQP 在叶尖段梯度平坦区容易停滞，导致 idx 7–12 收敛到相同值（"平台"）。
# 修正：两种光滑策略竞争 —
#   - PchipInterpolator : 保单调 C1 插值（数据已光滑时最优，严格保端点）
#   - UnivariateSpline  : 光滑样条（有平台时用，s>0 抹平阶梯，端点高权重锚定）
#   所有候选从 SLSQP 原始最优 (best_twist_raw) 出发拟合，避免偏差叠加。

from scipy.interpolate import PchipInterpolator as _Pchip
from scipy.interpolate import UnivariateSpline as _USpline
from scipy.interpolate import CubicSpline as _CubicSpline


def _smooth_twist_pchip(twist_full):
    """
    PchipInterpolator: 保单调三次 Hermite 插值。
    在严格通过所有数据点的同时保证 C1 连续和单调递减。
    适用于 SLSQP 已产出光滑扭角的场景（无平台时 AEP 损失最小）。
    圆柱段（idx 0–1）保持原值不变。
    """
    idx    = NON_CYL_IDX                      # [2, 3, ..., 13]
    r_nc   = r[idx]
    tw_nc  = twist_full[idx].copy()

    spl   = _Pchip(r_nc, tw_nc)
    tw_sp = spl(r_nc)

    result      = twist_full.copy()
    result[idx] = tw_sp
    return result


def _smooth_twist_spline(twist_full, s_factor=1.0, endpoint_weight=1e4):
    """
    UnivariateSpline 光滑样条：用 s>0 抹平 SLSQP 阶梯状平台。
    k=3 三次样条保证 C2 连续，不用于强制单调（交给选优逻辑过滤）。
    圆柱段（idx 0–1）保持原值不变。

    endpoint_weight: 端点权重。1e4=严格锚定（原始 spline-2.0），
                     10=轻度锚定允许叶尖浮动打破平台。
    """
    idx    = NON_CYL_IDX
    r_nc   = r[idx]
    tw_nc  = twist_full[idx].copy()
    n_nc   = len(idx)

    w          = np.ones(n_nc)
    w[0]       = endpoint_weight
    w[-1]      = endpoint_weight

    spl   = _USpline(r_nc, tw_nc, w=w, k=3, s=s_factor * n_nc)
    tw_sp = spl(r_nc)

    result      = twist_full.copy()
    result[idx] = tw_sp
    return result


def _smooth_twist_pruned(twist_full, plateau_tol=0.08):
    """
    平台去重 + Pchip 插值：去掉相邻差值 < plateau_tol 的重复平台点，
    保留每组平台的第一个点（代表平台起点），对去重后的稀疏点做 Pchip 插值。
    结果沿 SLSQP 趋势平滑过渡，比 Betz 更贴近原始数据，比纯 Pchip 更光滑。
    """
    idx    = NON_CYL_IDX
    r_nc   = r[idx]
    tw_nc  = twist_full[idx].copy()
    n_nc   = len(idx)

    keep = [True] * n_nc
    for j in range(1, n_nc - 1):
        if abs(tw_nc[j] - tw_nc[j - 1]) < plateau_tol:
            keep[j] = False
    keep[0] = True; keep[-1] = True

    r_sparse  = r_nc[keep]
    tw_sparse = tw_nc[keep]

    if len(r_sparse) < 3:
        spl = _Pchip(r_nc, tw_nc)
    else:
        spl = _Pchip(r_sparse, tw_sparse)

    tw_sp = spl(r_nc)
    result = twist_full.copy()
    result[idx] = tw_sp
    return result


def _prune_anchors(twist_full, plateau_tol=0.08):
    """去平台：返回稀疏锚点的 (r_sparse, tw_sparse, keep_mask)"""
    idx      = NON_CYL_IDX
    r_nc     = r[idx]
    tw_nc    = twist_full[idx].copy()
    n_nc     = len(idx)
    keep = [True] * n_nc
    for j in range(1, n_nc - 1):
        if abs(tw_nc[j] - tw_nc[j - 1]) < plateau_tol:
            keep[j] = False
    keep[0] = True; keep[-1] = True
    return r_nc[keep], tw_nc[keep], keep


def _smooth_twist_pruned_poly(twist_full):
    """去平台 + 加权 poly-5 拟合稀疏锚点"""
    idx = NON_CYL_IDX
    r_nc = r[idx]
    r_sp, tw_sp = _prune_anchors(twist_full)[:2]
    if len(r_sp) < 4:
        return _smooth_twist_pruned(twist_full)
    t_sp = (r_sp - r_sp[0]) / (r_sp[-1] - r_sp[0])
    tw_fit = _fit_poly_tw_weighted(t_sp, tw_sp, 5)
    spl = _Pchip(r_sp, tw_fit)
    tw_out = spl(r_nc)
    result = twist_full.copy()
    result[idx] = tw_out
    return result


def _smooth_twist_pruned_bezier(twist_full):
    """去平台 + bezier-5 拟合稀疏锚点（端点精确保持）"""
    idx = NON_CYL_IDX
    r_nc = r[idx]
    r_sp, tw_sp = _prune_anchors(twist_full)[:2]
    if len(r_sp) < 4:
        return _smooth_twist_pruned(twist_full)
    t_sp = (r_sp - r_sp[0]) / (r_sp[-1] - r_sp[0])
    tw_fit = _fit_bezier_tw(t_sp, tw_sp, 5)
    spl = _Pchip(r_sp, tw_fit)
    tw_out = spl(r_nc)
    result = twist_full.copy()
    result[idx] = tw_out
    return result


def _smooth_twist_pruned_cspline(twist_full):
    """去平台 + CubicSpline C2 自然边界插值。
    CubicSpline 提供 C² 连续性（d²θ/dr² 在节点处连续，端点 natural BC → d²θ/dr²=0），
    与 SolidWorks B-spline 曲面放样的连续性阶数匹配，从根源上消除边界振荡。
    圆柱段（idx 0–1）保持原值不变。
    """
    idx = NON_CYL_IDX
    r_nc = r[idx]
    r_sp, tw_sp = _prune_anchors(twist_full)[:2]
    if len(r_sp) < 4:
        return _smooth_twist_pruned(twist_full)
    cs = _CubicSpline(r_sp, tw_sp, bc_type="natural")
    tw_out = cs(r_nc)
    result = twist_full.copy()
    result[idx] = tw_out
    return result


def _smooth_twist_regularized(twist_full, lam=1.0, fix_tip=True):
    """
    正则化单调光滑 — 求解凸二次规划:
      min  ||θ − θ_slsqp||² + λ·||D²θ||²
      s.t. θ[i] ≤ θ[i−1]   (单调递减)
           θ[-1] = θ_slsqp[-1]  (叶尖锚定，不被正则化拉偏)
    其中 D² 是二阶差分矩阵。λ 控制光滑度:
      λ 小 → 贴近 SLSQP (保留平台, 推力不变)
      λ 大 → 光滑优先 (消除平台, 推力可能增加)
    工程解释: 单一可调参数 λ, 在保真度与光滑度之间做 Pareto 最优权衡。
    """
    from scipy.optimize import minimize as _minimize

    idx = NON_CYL_IDX
    tw_ref = twist_full[idx].copy()
    n = len(tw_ref)

    D2 = np.zeros((n - 2, n))
    for i in range(n - 2):
        D2[i, i] = 1.0
        D2[i, i + 1] = -2.0
        D2[i, i + 2] = 1.0
    H = D2.T @ D2

    def objective(theta):
        diff = theta - tw_ref
        curv = D2 @ theta
        return float(np.dot(diff, diff) + lam * np.dot(curv, curv))

    def gradient(theta):
        diff = theta - tw_ref
        return 2.0 * diff + 2.0 * lam * (H @ theta)

    cons = []
    for i in range(1, n):
        cons.append({"type": "ineq", "fun": lambda t, j=i: t[j - 1] - t[j]})
    if fix_tip:
        cons.append({"type": "eq", "fun": lambda t: t[-1] - tw_ref[-1]})

    bounds = [(twist_init_deg[idx[i]] - 8.0, twist_init_deg[idx[i]] + 8.0) for i in range(n)]

    res = _minimize(objective, tw_ref, method="SLSQP", jac=gradient,
                    bounds=bounds, constraints=cons,
                    options={"maxiter": 500, "ftol": 1e-10})
    result = twist_full.copy()
    result[idx] = res.x
    return result


def _smooth_twist_betz_curvature(twist_full, lam=1.0):
    """
    Betz 曲率引导光滑 — 保持 SLSQP 的值，曲率变化模式向 Betz 靠拢:
      min  ||θ − θ_slsqp||² + λ·||D²θ − D²θ_betz||²
      s.t. θ[i] ≤ θ[i−1]   (单调递减)
    Betz 提供 C∞ 曲率模板，λ 控制曲率跟随强度。
    工程解释: 复制 Betz 的曲率连续变化模式，但保持 SLSQP 气动最优值。
    """
    from scipy.optimize import minimize as _minimize

    idx = NON_CYL_IDX
    tw_ref = twist_full[idx].copy()
    tw_betz = twist_betz_deg[idx].copy()
    n = len(tw_ref)

    D2 = np.zeros((n - 2, n))
    for i in range(n - 2):
        D2[i, i] = 1.0
        D2[i, i + 1] = -2.0
        D2[i, i + 2] = 1.0
    curv_betz = D2 @ tw_betz
    D2T_D2 = D2.T @ D2
    D2T_cb = D2.T @ curv_betz

    def objective(theta):
        diff = theta - tw_ref
        cdiff = D2 @ theta - curv_betz
        return float(np.dot(diff, diff) + lam * np.dot(cdiff, cdiff))

    def gradient(theta):
        diff = theta - tw_ref
        return 2.0 * diff + 2.0 * lam * (D2T_D2 @ theta - D2T_cb)

    cons = []
    for i in range(1, n):
        cons.append({"type": "ineq", "fun": lambda t, j=i: t[j - 1] - t[j]})

    bounds = [(twist_init_deg[idx[i]] - 8.0, twist_init_deg[idx[i]] + 8.0) for i in range(n)]

    res = _minimize(objective, tw_ref, method="SLSQP", jac=gradient,
                    bounds=bounds, constraints=cons,
                    options={"maxiter": 500, "ftol": 1e-10})
    result = twist_full.copy()
    result[idx] = res.x
    return result


# ---- 平台检测（仅报告，不修改 best_twist） ----
noncyl_twist   = best_twist_raw[NON_CYL_IDX]
diffs_nc       = np.diff(noncyl_twist)
plateau_mask   = np.abs(diffs_nc) < 0.05
n_plateau_orig = int(np.sum(plateau_mask))

if n_plateau_orig > 0:
    plat_segs = [NON_CYL_IDX[k] for k in range(len(NON_CYL_IDX) - 1) if plateau_mask[k]]
    print(f"\n[平台检测] 检测到 {n_plateau_orig} 处相邻截面平台（|Δθ| < 0.05°），"
          f"涉及截面 idx: {plat_segs}")
else:
    print("\n[平台检测] 未检测到平台区，扭角分布已足够光滑。")


# ================================================================
# 8d. 统一光滑后处理：Pchip + 参数化拟合公平竞争
# ================================================================
# 所有候选从 SLSQP 原始最优 (best_twist_raw) 出发拟合，避免 §8c→§8d 偏差叠加。
# 候选方案：
#   - Pchip         : 保单调三次 Hermite 插值，C1 连续，严格通过所有数据点
#   - poly-3/4/5    : 加权多项式拟合（端点权重 100× 锚定叶根/叶尖）
#   - bezier-4/5/6  : 端点精确保持
#   - 1/r           : 叶片扭角经典反比模型
#   - Betz          : 物理一致模板（自由参数仅 α_des）
# 选优：ΔAEP ≤ 容限 + 单调 + 失速 + 叶尖偏差 ≤ 1° → 取 AEP 损失最小，同损失取曲率最小。

from scipy.special import comb as _comb
from scipy.optimize import least_squares as _lsq

_STALL_TOL_DEG     = 0.10  # 失速约束容差 (deg)

print("\n" + "=" * 60)
print("8d. 统一光滑后处理（Pchip + 参数化拟合）")
print("=" * 60)

# 所有拟合从 SLSQP 原始最优出发
_r_var_e   = r[NON_CYL_IDX[0]:]                        # idx 2..13
_tw_base_e = best_twist_raw[NON_CYL_IDX[0]:].copy()    # deg — SLSQP 原始最优，不被 §8c 修改
_AEP_ref_e = best_AEP_raw
_t_norm_e  = (_r_var_e - _r_var_e[0]) / (_r_var_e[-1] - _r_var_e[0])


def _second_diff_cost_tw(arr):
    """离散二阶差分平方和（曲率代理）"""
    return float(np.sum(np.diff(np.diff(arr)) ** 2))


def _bezier_curve_tw(t, ctrl):
    """N 阶 Bezier 曲线求值，t∈[0,1]"""
    n = len(ctrl) - 1
    vals = np.zeros_like(t, dtype=float)
    for i in range(n + 1):
        vals += _comb(n, i) * (t ** i) * ((1.0 - t) ** (n - i)) * ctrl[i]
    return vals


def _fit_bezier_tw(t_norm, tw_arr, n_ctrl):
    """端点固定的 n_ctrl 阶 Bezier 最小二乘拟合"""
    def residual(mid):
        ctrl = np.concatenate([[tw_arr[0]], mid, [tw_arr[-1]]])
        return _bezier_curve_tw(t_norm, ctrl) - tw_arr
    mid_init = np.linspace(tw_arr[0], tw_arr[-1], n_ctrl)[1:-1]
    res = _lsq(residual, mid_init)
    ctrl_full = np.concatenate([[tw_arr[0]], res.x, [tw_arr[-1]]])
    return _bezier_curve_tw(t_norm, ctrl_full)


def _fit_poly_tw_weighted(t_norm, tw_arr, order):
    """加权多项式最小二乘拟合：端点权重 100× 锚定叶根/叶尖，避免末端漂移"""
    w = np.ones(len(tw_arr))
    w[0] = 100.0
    w[-1] = 100.0
    A = np.vander(t_norm, order + 1)
    W = np.diag(np.sqrt(w))
    coef, _, _, _ = np.linalg.lstsq(W @ A, W @ tw_arr, rcond=None)
    return np.polyval(coef, t_norm)

def _fit_inverse_r(r_arr, tw_arr):
    """θ(r) = A/r + B 反比模型（叶片扭角经典形式）"""
    def residual(params):
        A, B = params
        return A / r_arr + B - tw_arr
    A_init = (tw_arr[0] - tw_arr[-1]) * r_arr[0] * r_arr[-1] / (r_arr[-1] - r_arr[0])
    B_init = tw_arr[-1] - A_init / r_arr[-1]
    res = _lsq(residual, [A_init, B_init])
    A, B = res.x
    return A / r_arr + B


def _fit_betz_template(r_arr, tw_arr, tsr_val, R_tip):
    """
    Betz 模板：θ(r) = φ_Betz(r; λ=tsr·r/R) − α_des
    自由参数仅 α_des（度），物理动机最强。
    """
    lam  = tsr_val * r_arr / R_tip
    disc = np.sqrt(1.0 + 8.0 / (9.0 * lam ** 2))
    ap   = 0.5 * (-1.0 + disc)
    phi  = np.degrees(np.arctan2(2.0 / 3.0, (1.0 + ap) * lam))

    def residual(a_des):
        return (phi - a_des[0]) - tw_arr
    res = _lsq(residual, [6.0], bounds=([0.0], [15.0]))
    return phi - res.x[0]


# 所有候选从 SLSQP 原始最优出发
_cands_e = []

# Pchip: 保单调三次 Hermite 插值（数据光滑时最优）
try:
    _tw_s = _smooth_twist_pchip(best_twist_raw)[NON_CYL_IDX[0]:]
    _cands_e.append(("pchip", _tw_s))
except Exception as _ex:
    print(f"  pchip 拟合失败: {_ex}")

# Pchip-pruned: 平台去重后 Pchip 插值（沿 SLSQP 趋势平滑，比 Betz 更贴近数据）
try:
    _tw_s = _smooth_twist_pruned(best_twist_raw)[NON_CYL_IDX[0]:]
    _cands_e.append(("pchip-prune", _tw_s))
except Exception as _ex:
    print(f"  pchip-prune 拟合失败: {_ex}")

# cspline-prune: 去平台 + CubicSpline C2 自然边界（匹配 SW B-spline 连续性）
try:
    _tw_s = _smooth_twist_pruned_cspline(best_twist_raw)[NON_CYL_IDX[0]:]
    _cands_e.append(("cspline-prune", _tw_s))
except Exception as _ex:
    print(f"  cspline-prune 拟合失败: {_ex}")

# poly5-pruned / bezier5-pruned: 去平台 + 拟合稀疏锚点
# 注意：与 pchip-prune 效果几乎相同（锚点相同，Pchip 插值结果一致），保留以备验证

# UnivariateSpline: 强光滑样条（s=2.0 用于抹平严重平台）
try:
    _tw_s = _smooth_twist_spline(best_twist_raw, s_factor=2.0)[NON_CYL_IDX[0]:]
    _cands_e.append(("spline-2.0", _tw_s))
except Exception as _ex:
    print(f"  spline-2.0 拟合失败: {_ex}")

# UnivariateSpline C2 轻光滑 (端点权重10, 逐步增大 s 打破全部平台):
#   s=0.1: 仅打破叶尖平台，内部平台残留
#   s=0.3: 中等光滑，应打破多数平台
#   s=0.5: 预期打破全部平台的最小 s
try:
    _tw_s = _smooth_twist_spline(best_twist_raw, s_factor=0.1, endpoint_weight=10.0)[NON_CYL_IDX[0]:]
    _cands_e.append(("spline-0.1", _tw_s))
except Exception as _ex:
    print(f"  spline-0.1 拟合失败: {_ex}")
try:
    _tw_s = _smooth_twist_spline(best_twist_raw, s_factor=0.3, endpoint_weight=10.0)[NON_CYL_IDX[0]:]
    _cands_e.append(("spline-0.3", _tw_s))
except Exception as _ex:
    print(f"  spline-0.3 拟合失败: {_ex}")
try:
    _tw_s = _smooth_twist_spline(best_twist_raw, s_factor=0.5, endpoint_weight=10.0)[NON_CYL_IDX[0]:]
    _cands_e.append(("spline-0.5", _tw_s))
except Exception as _ex:
    print(f"  spline-0.5 拟合失败: {_ex}")

# 多项式: poly-5（高阶，灵活拟合）
try:
    _tw_s = _fit_poly_tw_weighted(_t_norm_e, _tw_base_e, 5)
    _cands_e.append(("poly-5", _tw_s))
except Exception as _ex:
    print(f"  poly-5 拟合失败: {_ex}")

# Bezier: 仅保留 5 阶（端点固定，中间 3 个控制点）
try:
    _tw_s = _fit_bezier_tw(_t_norm_e, _tw_base_e, 5)
    _cands_e.append(("bezier-5", _tw_s))
except Exception as _ex:
    print(f"  bezier-5 拟合失败: {_ex}")

try:
    _tw_s = _fit_inverse_r(_r_var_e, _tw_base_e)
    _cands_e.append(("1/r", _tw_s))
except Exception as _ex:
    print(f"  1/r 拟合失败: {_ex}")

try:
    _tw_s = _fit_betz_template(_r_var_e, _tw_base_e, tsr, Rtip)
    _cands_e.append(("Betz", _tw_s))
except Exception as _ex:
    print(f"  Betz 模板拟合失败: {_ex}")

# 多比例混合：pchip-prune 与 poly-5 的加权平均
_tw_prune = next((tw for name, tw in _cands_e if name == "pchip-prune"), None)
_tw_poly5 = next((tw for name, tw in _cands_e if name == "poly-5"), None)
if _tw_prune is not None and _tw_poly5 is not None:
    _cands_e.append(("avg(prune+poly5)", (_tw_prune + _tw_poly5) / 2.0))
    _cands_e.append(("blend75-25", _tw_prune * 0.75 + _tw_poly5 * 0.25))

# 轻量 Betz 混合: 保持 SLSQP 值, 仅掺少量 Betz 引入曲率连续性
_tw_betz_nc = twist_betz_deg[NON_CYL_IDX[0]:]
for _alpha, _b_label in [(0.05, "betz-5%"), (0.10, "betz-10%"), (0.15, "betz-15%")]:
    _cands_e.append((_b_label, (1.0 - _alpha) * _tw_base_e + _alpha * _tw_betz_nc))

# 正则化单调光滑：min ||θ-θ_slsqp||² + λ·||D²θ||², s.t. 单调递减
# λ 越大越光滑（推力可能增加），λ 越小越贴近 SLSQP（保留平台）
for _lam, _lam_label in [(0.1, "reg-0.1"), (0.3, "reg-0.3"), (1.0, "reg-1.0"),
                          (3.0, "reg-3.0"), (10.0, "reg-10")]:
    try:
        _tw_s = _smooth_twist_regularized(best_twist_raw, lam=_lam)[NON_CYL_IDX[0]:]
        _cands_e.append((_lam_label, _tw_s))
    except Exception as _ex:
        print(f"  {_lam_label} 失败: {_ex}")

# Betz 曲率引导光滑: 保持 SLSQP 值, 曲率变化模式跟随 Betz
for _lam, _lam_label in [(0.5, "betz-curv-0.5"), (1.0, "betz-curv-1.0"),
                          (3.0, "betz-curv-3.0"), (10.0, "betz-curv-10")]:
    try:
        _tw_s = _smooth_twist_betz_curvature(best_twist_raw, lam=_lam)[NON_CYL_IDX[0]:]
        _cands_e.append((_lam_label, _tw_s))
    except Exception as _ex:
        print(f"  {_lam_label} 失败: {_ex}")

# ----- 评价每个候选 + 计算推力 -----
_lo_e = (twist_init_deg - 8.0)[NON_CYL_IDX[0]:]
_hi_e = (twist_init_deg + 8.0)[NON_CYL_IDX[0]:]

def _eval_twist_full(twist_full_deg):
    """运行 BEM，返回 (AEP, T_peak, stall_ok)"""
    best_prob.set_val("theta_in", twist_full_deg, units="deg")
    best_prob.run_model()
    aep = best_prob.get_val("AEP")[0]
    Px_peak = best_prob.get_val(f"Px_b_{I_PEAK}")
    T_peak = np.trapz(Px_peak, r) * n_blades
    stall_ok = True
    nc_arr = np.array(NON_CYL_IDX)
    for _ci in range(n_cases):
        _a = best_prob.get_val(f"alpha_{_ci}", units="deg")
        if np.any(_a[nc_arr] > ALPHA_UPPER_NSEC + _STALL_TOL_DEG):
            stall_ok = False
            break
    return aep, T_peak, stall_ok

_log_e = []
for _name, _tw_s in _cands_e:
    _tw_clip = np.clip(_tw_s, _lo_e, _hi_e)
    # 单调化 + C1 连续: 用 Pchip 重拟合替代 minimum.accumulate
    # (minimum.accumulate 制造 C0 扭折 → SolidWorks 放样自相交)
    if not np.all(np.diff(_tw_clip) <= 1e-6):
        for j in range(1, len(_tw_clip)):
            if _tw_clip[j] > _tw_clip[j - 1]:
                _tw_clip[j] = _tw_clip[j - 1] - 1e-4  # 微下调, 避免 Pchip 压平
        _tw_clip = _Pchip(_r_var_e, _tw_clip)(_r_var_e)
    _mono    = bool(np.all(np.diff(_tw_clip) <= 1e-6))
    _tw_full = best_twist_raw.copy()
    _tw_full[NON_CYL_IDX[0]:] = _tw_clip

    _aep_i, _T_i, _stall_ok = _eval_twist_full(_tw_full)
    _loss_i = (_AEP_ref_e - _aep_i) / _AEP_ref_e * 100.0
    _curv_i = _second_diff_cost_tw(_tw_clip)
    _mdev_i = float(np.max(np.abs(_tw_clip - _tw_base_e)))
    _tip_i  = float(abs(_tw_clip[-1] - _tw_base_e[-1]))

    _log_e.append({
        "name": _name, "twist": _tw_clip, "twist_full": _tw_full.copy(),
        "AEP": _aep_i, "T_peak": _T_i, "loss_pct": _loss_i, "curvature": _curv_i,
        "mono": _mono, "max_dev": _mdev_i, "tip_dev": _tip_i, "stall_ok": _stall_ok,
    })

# 计算 SLSQP 原始的 AEP 和 T 作为基准
_AEP_slsqp, _T_slsqp, _ = _eval_twist_full(best_twist_raw)

# ----- 筛选满足失速条件的候选 -----
_stall_ok_cands = [lg for lg in _log_e if lg["stall_ok"]]

print(f"\n{'=' * 100}")
print(f"  光滑方案对比 — 满足失速约束的候选 ({len(_stall_ok_cands)}/{len(_log_e)})")
print(f"  SLSQP 原始: AEP={_AEP_slsqp:.1f} W  T_peak={_T_slsqp:.1f} N")
print(f"{'=' * 100}")
print(f"  {'方案':>10s}  {'AEP(W)':>10s}  {'ΔAEP%':>8s}  {'T_peak(N)':>10s}  "
      f"{'ΔT%':>7s}  {'曲率e-4':>8s}  {'max_dev°':>8s}  {'tip_dev°':>8s}  {'单调':>4s}")
print(f"  {'-' * 86}")
for lg in _stall_ok_cands:
    _dT_pct = (lg["T_peak"] - _T_slsqp) / _T_slsqp * 100.0 if _T_slsqp != 0 else 0.0
    print(f"  {lg['name']:>10s}  {lg['AEP']:10.1f}  {lg['loss_pct']:+8.3f}%  "
          f"{lg['T_peak']:10.1f}  {_dT_pct:+7.2f}%  {lg['curvature']*1e4:8.1f}  "
          f"{lg['max_dev']:8.4f}  {lg['tip_dev']:8.4f}  "
          f"{'✓' if lg['mono'] else '✗':>4s}")

# ----- 推荐：以 pchip-prune 光滑度为基准，找推力增加最小的方案 -----
_prune_ref = next((lg for lg in _log_e if lg["name"] == "pchip-prune"), None)
if _prune_ref and _prune_ref["stall_ok"] and _prune_ref["mono"]:
    _curv_ref = _prune_ref["curvature"]
    _CURV_TOL = 0.30  # 曲率在 pchip-prune ±30% 内视为"类似光滑度"
    _AEP_LOSS_ACCEPT = 3.0  # %, 可接受的 AEP 损失上限

    _similar = [lg for lg in _stall_ok_cands
                if lg["mono"]
                and abs(lg["curvature"] - _curv_ref) / _curv_ref <= _CURV_TOL
                and lg["loss_pct"] <= _AEP_LOSS_ACCEPT]
    _similar.sort(key=lambda lg: abs((lg["T_peak"] - _T_slsqp) / _T_slsqp))

    print(f"\n  {'=' * 90}")
    print(f"  推荐基准: pchip-prune (曲率={_curv_ref*1e4:.0f}e-4, ΔT={( _prune_ref['T_peak']-_T_slsqp)/_T_slsqp*100:+.2f}%)")
    print(f"  筛选条件: 曲率在 ±{_CURV_TOL*100:.0f}% 内, ΔAEP ≤ {_AEP_LOSS_ACCEPT:.1f}%, 单调+失速OK")
    if _similar:
        print(f"  排序: 推力增加最小 → 最大")
        print(f"  {'排名':>4s}  {'方案':>12s}  {'ΔT%':>8s}  {'ΔAEP%':>8s}  {'曲率e-4':>8s}  {'tip_dev°':>10s}")
        for _rank, lg in enumerate(_similar, 1):
            _dt = (lg["T_peak"] - _T_slsqp) / _T_slsqp * 100.0
            _marker = "  ← 最佳" if _rank == 1 else ""
            print(f"  {_rank:>4d}  {lg['name']:>12s}  {_dt:+8.3f}%  {lg['loss_pct']:+8.3f}%  "
                  f"{lg['curvature']*1e4:8.0f}  {lg['tip_dev']:10.4f}{_marker}")
    else:
        print(f"  ⚠ 无候选满足曲率相似条件")
else:
    print(f"\n  ⚠ pchip-prune 不可用，无法建立光滑度基准")

# ----- 最终方案: 强制 Betz（唯一通过 SW 曲面放样验证的方案）-----
_betz_cand = next((lg for lg in _log_e if lg["name"] == "Betz"), None)
if _betz_cand and _betz_cand["stall_ok"] and _betz_cand["mono"]:
    best_twist = _betz_cand["twist_full"]
    best_AEP   = _betz_cand["AEP"]
    _dt_final = (_betz_cand["T_peak"] - _T_slsqp) / _T_slsqp * 100.0
    print(f"\n  ✓ 已选定 Betz (C∞): ΔT={_dt_final:+.2f}%, ΔAEP={_betz_cand['loss_pct']:+.3f}%")
else:
    print(f"\n  ⚠ Betz 不可用，回退到 SLSQP 原始")
    best_twist = best_twist_raw.copy()
    best_AEP   = best_AEP_raw

best_prob.set_val("theta_in", best_twist, units="deg")
best_prob.run_model()

_avg_full = None
_b75_ref = None  # 使用 Betz 时不需要 blend 参考

# ----- 可视化: Initial + SLSQP + Final + betz blends -----
# 提取 betz 混合候选（满足失速+单调的）
_betz_blends = [lg for lg in _log_e
                if lg["name"].startswith("betz-") and lg["stall_ok"] and lg["mono"]]
_betz_blends.sort(key=lambda lg: lg["name"])

try:
    import matplotlib.pyplot as _plt

    _r_full = r[NON_CYL_IDX[0]:]
    _tw_init_nc = twist_init_deg[NON_CYL_IDX[0]:]
    _tw_final = best_twist[NON_CYL_IDX[0]:]

    _fig, (_ax1, _ax2) = _plt.subplots(1, 2, figsize=(16, 6))
    _final_label = "Betz (C∞)"
    _fig.suptitle(f"Twist comparison: {_final_label} + betz blends vs SLSQP vs Initial", fontsize=14)

    _ax1.plot(_r_full, _tw_init_nc, "s--", color="gray", ms=5, lw=1.8, label="Initial (twist_init_deg)")
    _ax1.plot(_r_full, _tw_base_e, "ko-", ms=6, lw=2.5, label="SLSQP optimum")
    _ax1.plot(_r_full, _tw_final, "D-", color="#d62728", ms=6, lw=2.5, label=f"Final: {_final_label}")
    # blend75-25 参考 (仅当 final ≠ blend75-25 时显示)
    if _b75_ref and _b75_ref["stall_ok"] and _b75_ref["mono"]:
        _ax1.plot(_r_full, _b75_ref["twist"], "s-", color="#ff7f0e", ms=4, lw=1.5,
                  label=f"ref blend75-25  ΔT={(_b75_ref['T_peak']-_T_slsqp)/_T_slsqp*100:+.2f}%")

    # betz 混合曲线 (绿→蓝渐变)
    _b_colors = ["#2ca02c", "#17becf", "#1f77b4"]
    for _k, _bc in enumerate(_betz_blends):
        _col = _b_colors[_k % 3]
        _ax1.plot(_r_full, _bc["twist"], "o-", color=_col, ms=4, lw=1.5,
                  label=f"{_bc['name']}  ΔT={(_bc['T_peak']-_T_slsqp)/_T_slsqp*100:+.2f}%")

    _ax1.set_xlabel("r (m)"); _ax1.set_ylabel("Twist (deg)")
    _ax1.set_title("Full span"); _ax1.legend(fontsize=8); _ax1.grid(True, alpha=0.3)

    _mask_tip = _r_full >= 1.8
    _ax2.plot(_r_full[_mask_tip], _tw_init_nc[_mask_tip], "s--", color="gray", ms=5, lw=1.8, label="Initial")
    _ax2.plot(_r_full[_mask_tip], _tw_base_e[_mask_tip], "ko-", ms=6, lw=2.5, label="SLSQP optimum")
    _ax2.plot(_r_full[_mask_tip], _tw_final[_mask_tip], "D-", color="#d62728", ms=6, lw=2.5,
              label=f"Final: {_final_label}")
    if _b75_ref and _b75_ref["stall_ok"] and _b75_ref["mono"]:
        _ax2.plot(_r_full[_mask_tip], _b75_ref["twist"][_mask_tip], "s-", color="#ff7f0e", ms=4, lw=1.5,
                  label="ref blend75-25")
    for _k, _bc in enumerate(_betz_blends):
        _col = _b_colors[_k % 3]
        _ax2.plot(_r_full[_mask_tip], _bc["twist"][_mask_tip], "o-", color=_col, ms=4, lw=1.5,
                  label=f"{_bc['name']}")
    for i in range(len(_r_full)):
        if _mask_tip[i]:
            _ax2.annotate(f"{_tw_final[i]:.2f}", (_r_full[i], _tw_final[i]),
                         textcoords="offset points", xytext=(0, 10), fontsize=7, color="#d62728", ha="center")
    _ax2.set_xlabel("r (m)"); _ax2.set_ylabel("Twist (deg)")
    _ax2.set_title("Tip region  (r >= 1.8 m)"); _ax2.legend(fontsize=9); _ax2.grid(True, alpha=0.3)

    _plt.tight_layout()
    _plot_path = "twist_final_comparison.png"
    _fig.savefig(_plot_path, dpi=150, bbox_inches="tight")
    _plt.close(_fig)
    print(f"  最终对比图已保存: {_plot_path}")
except Exception as _ex:
    print(f"  [可视化跳过] {_ex}")


# ================================================================
# 9. 输出结果
# ================================================================

print("\n" + "=" * 60)
print("优化结果")
print("=" * 60)

AEP_opt   = best_AEP
# best_twist 已在 _run_one_twist 中改为读取 theta_in（优化器决策变量），
# 圆柱段(idx 0-1)保持初始值，无样条外推振荡。
theta_opt = best_twist

print(f"\nAEP_proxy = {AEP_opt:.1f} W  (加权平均功率)")

# 各工况汇总
print(f"\n{'工况':>4s} {'V(m/s)':>7s} {'权重f_i':>8s} {'CP':>8s} "
      f"{'P(W)':>10s} {'f_i×P(W)':>10s} {'能量贡献%':>9s}")
P_cases  = []
CP_cases = []
for i in range(n_cases):
    P_i  = best_prob.get_val(f"P_{i}")[0]
    CP_i = best_prob.get_val(f"CP_{i}")[0]
    P_cases.append(P_i)
    CP_cases.append(CP_i)
    contrib = f_weights[i] * P_i
    print(f"  V{i+1}  {V_cases[i]:7.1f}  {f_weights[i]:8.3f}  {CP_i:8.4f}  "
          f"{P_i:10.1f}  {contrib:10.1f}  {contrib/AEP_opt*100:8.1f}%")

# 推力近似（能量峰值工况）
Px_peak  = best_prob.get_val(f"Px_b_{I_PEAK}")
T_approx = np.trapz(Px_peak, r) * n_blades
print(f"\n推力 ≈ {T_approx:.1f} N  "
      f"(V={V_cases[I_PEAK]:.1f} m/s 工况，Px_b 展向积分)")

# 截面气动量（能量峰值工况）
alpha_peak = best_prob.get_val(f"alpha_{I_PEAK}", units="deg")
cl_peak    = best_prob.get_val(f"cl_{I_PEAK}")
cd_peak    = best_prob.get_val(f"cd_{I_PEAK}")
a_peak     = best_prob.get_val(f"a_{I_PEAK}")
ap_peak    = best_prob.get_val(f"ap_{I_PEAK}")

print(f"\n--- 截面气动量 (V={V_cases[I_PEAK]:.1f} m/s, 能量峰值工况) ---")
print(f"{'r(m)':>6s} {'twist_old':>10s} {'twist_new':>10s} {'Δtwist':>8s} "
      f"{'alpha':>8s} {'cl':>8s} {'cd':>8s} {'cl/cd':>8s}")
for j in range(n_span):
    ld = cl_peak[j] / cd_peak[j] if cd_peak[j] > 1e-6 else 0
    print(f"{r[j]:6.2f} {twist_init_deg[j]:10.2f} {theta_opt[j]:10.2f} "
          f"{theta_opt[j]-twist_init_deg[j]:+8.2f} "
          f"{alpha_peak[j]:8.2f} {cl_peak[j]:8.4f} {cd_peak[j]:8.4f} {ld:8.1f}")

# 保存
np.savez(
    "twist_optimization_results_AEP.npz",
    r=r, chord=chord,
    twist_init=twist_init_deg, twist_opt=theta_opt,
    V_cases=V_cases, f_weights=f_weights,
    P_cases=np.array(P_cases), CP_cases=np.array(CP_cases),
    AEP=AEP_opt,
    alpha_peak=alpha_peak, cl_peak=cl_peak, cd_peak=cd_peak,
    a_peak=a_peak, ap_peak=ap_peak, T_approx=T_approx,
)
print("\n结果已保存到 twist_optimization_results_AEP.npz")


# ================================================================
# 10. 关注风况评估：3 / 15 / 18 m/s 优化前后对比
# ================================================================
# 用独立的单工况 Problem 逐一评估，避免干扰优化结果
# T 由 Px_b 展向积分近似（CCBladeTwist 的 T 输出恒为 0）

V_eval = [3.0, 5.0, 15.0, 18.0]   # 感兴趣的风速点

# 取优化后的 theta_in（弧度），从共享变量中读取
theta_in_opt_rad = best_prob.get_val("theta_in")   # shape (n_span,), rad

# 构建一个可复用的单工况评估 Problem
prob_eval = om.Problem()
prob_eval.model.add_subsystem(
    "blade",
    CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options),
    promotes=["*"],
)
prob_eval.setup()
set_shared_inputs(prob_eval)

def _eval_at(wind_speed, theta_in_rad):
    """在给定风速和扭角下运行一次 BEM，返回 (CP, P, T_approx)"""
    prob_eval.set_val("Uhub",     wind_speed,   units="m/s")
    prob_eval.set_val("theta_in", theta_in_rad, units="rad")
    prob_eval.run_model()
    CP_val = prob_eval.get_val("CP")[0]
    P_val  = prob_eval.get_val("P")[0]
    Px_val = prob_eval.get_val("Px_b")
    T_val  = np.trapz(Px_val, r) * n_blades   # N
    return CP_val, P_val, T_val

print("\n" + "=" * 60)
print("关注风况：优化前后对比  (V = 3 / 5 / 15 / 18 m/s)")
print("=" * 60)
print(f"\n{'':>20s}  {'V=3 m/s':>20s}  {'V=5 m/s':>20s}  {'V=15 m/s':>20s}  {'V=18 m/s':>20s}")
print(f"{'':>20s}  {'CP / P(W) / T(N)':>20s}  {'CP / P(W) / T(N)':>20s}  {'CP / P(W) / T(N)':>20s}  {'CP / P(W) / T(N)':>20s}")
print("-" * 90)

results_eval = {}
_eval_label_final = "Betz (C∞)"
_eval_rows = [("优化前 (初始扭角)", np.deg2rad(twist_init_deg)),
              (f"优化后 ({_eval_label_final})", theta_in_opt_rad)]
for label, theta_rad in _eval_rows:
    row = {}
    for V in V_eval:
        cp, p, t = _eval_at(V, theta_rad)
        row[V] = (cp, p, t)
    results_eval[label] = row
    vals = "  ".join(
        f"  {row[V][0]:.4f} / {row[V][1]:7.1f} / {row[V][2]:7.1f}"
        for V in V_eval
    )
    print(f"{label:>20s}  {vals}")

print()
print("各项变化量 (优化后 / 参考 - 优化前):")
print(f"  {'指标':>6s}  {'方案':>22s}  {'V=3 m/s':>14s}  {'V=5 m/s':>14s}  {'V=15 m/s':>14s}  {'V=18 m/s':>14s}")
row_before = results_eval["优化前 (初始扭角)"]
for label, theta_rad in _eval_rows[1:]:  # skip 优化前
    row_after = results_eval[label]
    for metric, idx in [("ΔCP", 0), ("ΔP(W)", 1), ("ΔT(N)", 2)]:
        diffs = "  ".join(
            f"  {row_after[V][idx] - row_before[V][idx]:+12.4f}"
            for V in V_eval
        )
        print(f"  {metric:>6s}  {label:>20s}  {diffs}")


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
    fig.suptitle(f"多风况加权扭角优化  AEP_proxy={AEP_opt:.1f} W", fontsize=14)

    # [0,0] 扭角分布对比
    axes[0, 0].plot(r, twist_init_deg, "b--o", ms=4, label="初始")
    axes[0, 0].plot(r, theta_opt,      "r-s",  ms=4, label="优化")
    axes[0, 0].set_xlabel("r (m)"); axes[0, 0].set_ylabel("扭角 (°)")
    axes[0, 0].legend(); axes[0, 0].grid(True)
    axes[0, 0].set_title("扭角分布")

    # [0,1] 各工况攻角分布
    for i in range(n_cases):
        alpha_i = best_prob.get_val(f"alpha_{i}", units="deg")
        axes[0, 1].plot(r, alpha_i, "-o", ms=3, color=colors[i],
                        label=f"V={V_cases[i]:.1f} m/s  (f={f_weights[i]:.3f})")
    axes[0, 1].axhline(10.0, color="crimson", ls="--", lw=1.2, label="失速上限 10°")
    axes[0, 1].set_xlabel("r (m)"); axes[0, 1].set_ylabel("攻角 (°)")
    axes[0, 1].legend(fontsize=7); axes[0, 1].grid(True)
    axes[0, 1].set_title("各工况攻角分布")

    # [0,2] 各工况功率 & AEP 贡献
    bar_x   = np.arange(n_cases)
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
    plt.savefig("twist_optimization_AEP.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("图表已保存到 twist_optimization_AEP.png")
except ImportError:
    print("未安装 matplotlib, 跳过可视化")


# ==================代办=====================
# 1. 11 m/s 工况（超额定）可增加变桨角作为额外设计变量
# 2. 扭角与弦长联合优化：同时将 theta_in 和 chord 作为设计变量
