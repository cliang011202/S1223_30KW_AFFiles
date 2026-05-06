"""
叶片弦长优化V2: 控制点 + 插值(scipy.minimize)
设计变量: 仅取 n_ctrl(5) 个控制截面的弦长
插值映射: 用 PCHIP(分段三次 Hermite 插值)从控制点生成完整弦长, PCHIP 构造一个分段三次多项式
优化问题: 最大化功率系数CP, 设置各截面弦长范围c_i, 攻角α ≤11°
弦长分布: 被限制在光滑曲线子空间中

输入参数: “2.叶片参数”“7. 正式优化”
"""

import numpy as np
import openmdao.api as om
import os
import time
from ccblade.ccblade_component import CCBladeTwist
from scipy.interpolate import PchipInterpolator
from scipy.optimize import minimize

# ================================================================
# 1. AeroDyn 格式翼型文件解析
# ================================================================
def load_aerodyn_polar(filepath):
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
    n = len(common_aoa)
    return np.zeros(n), np.ones(n) * 0.50, np.zeros(n)


# ================================================================
# 2. ★★★ 叶片参数 ★★★
# ================================================================
airfoil_dir   = ""
s1223_file    = os.path.join(airfoil_dir, "S1223_Re2.000.dat")
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

V_design   = 18     #18m/s环境风速，22m/s风轮面风速
tsr        = 6.53   #18→22——392r/min——tsr6.53
pitch_deg  = 0.0

n_opt_twist = 8
n_opt_chord = 8

r = np.array([  0.300 ,0.500 ,0.676 ,0.967 ,1.302 ,
                1.664 ,2.036 ,2.398 ,2.733 ,3.024 ,
                3.256 ,3.417 ,3.496 ])

chord = np.array([  0.250 ,0.250 ,0.4802,0.3378,0.2709,
                    0.2231,0.185 ,0.1596,0.1426,0.1232,
                    0.0893,0.1092,0.0924])

twist_init_deg = np.array([21.64,21.64, 21.64, 12.46, 8.01,
                           5.26,  3.07,  1.89,  1.6, 1.42,
                          -0.09, -2.89, -5.02])

rthick = np.array([100.0, 100.0, 12.1, 12.1, 12.1,
                   12.1, 12.1, 12.1, 12.1, 12.1,
                   12.1, 12.1, 12.1])

n_fix = 2  # 叶根固定站位数
r_all = r.copy()
r_opt = r_all[n_fix:]
chord_root = chord[:n_fix].copy()

# 选取5个控制点（均匀分布在优化区域）
n_ctrl = 5
idx_ctrl = np.linspace(0, len(r_opt) - 1, n_ctrl, dtype=int)
r_ctrl = r_opt[idx_ctrl]
chord_ctrl_init = chord[n_fix:][idx_ctrl]
print(f"控制点位置: {r_ctrl}")
print(f"控制点初始弦长: {chord_ctrl_init}")

n_span = len(r)

is_cylinder = [True, True, False, False, False,
               False, False, False, False, False,
               False, False, False]


# ================================================================
# 3. 构建极曲线表
# ================================================================
aoa_s1223, cl_s1223, cd_s1223, cm_s1223 = load_aerodyn_polar(s1223_file)
print(f"S1223: {len(aoa_s1223)} 点, Cl_max={cl_s1223.max():.3f}")

common_aoa = aoa_s1223.copy()
n_aoa = len(common_aoa)
n_Re  = 1
n_tab = 1

cl_table = np.zeros((n_span, n_aoa, n_Re, n_tab))
cd_table = np.zeros((n_span, n_aoa, n_Re, n_tab))
cm_table = np.zeros((n_span, n_aoa, n_Re, n_tab))

for i in range(n_span):
    if is_cylinder[i]:
        if os.path.exists(cylinder_file):
            aoa_cyl, cl_cyl, cd_cyl, cm_cyl = load_aerodyn_polar(cylinder_file)
            cl_table[i, :, 0, 0] = np.interp(common_aoa, aoa_cyl, cl_cyl)
            cd_table[i, :, 0, 0] = np.interp(common_aoa, aoa_cyl, cd_cyl)
            cm_table[i, :, 0, 0] = np.interp(common_aoa, aoa_cyl, cm_cyl)
        else:
            cl_c, cd_c, cm_c = make_cylinder_polar(common_aoa)
            cl_table[i, :, 0, 0] = cl_c
            cd_table[i, :, 0, 0] = cd_c
            cm_table[i, :, 0, 0] = cm_c
    else:
        cl_table[i, :, 0, 0] = cl_s1223
        cd_table[i, :, 0, 0] = cd_s1223
        cm_table[i, :, 0, 0] = cm_s1223

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
# 5. 辅助函数：统一设置输入（不含 chord，chord 由设计变量控制）
# ================================================================
def set_all_inputs(prob_obj):
    prob_obj.set_val("airfoils_aoa", common_aoa, units="deg")
    prob_obj.set_val("airfoils_Re",  np.array([2.0e6]))
    prob_obj.set_val("airfoils_cl",  cl_table)
    prob_obj.set_val("airfoils_cd",  cd_table)
    prob_obj.set_val("airfoils_cm",  cm_table)

    prob_obj.set_val("r",       r,       units="m")
    # !!!chord 不在这里设，由外部单独设!!!
    prob_obj.set_val("theta_in", np.deg2rad(twist_init_deg), units="rad")
    prob_obj.set_val("rthick",  rthick / 100.0)
    prob_obj.set_val("s_opt_theta", s_opt_twist)
    prob_obj.set_val("s_opt_chord", s_opt_chord)

    prob_obj.set_val("Uhub",  V_design, units="m/s")
    prob_obj.set_val("tsr",   tsr)
    prob_obj.set_val("pitch", pitch_deg, units="deg")

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
    prob_obj.set_val("nSector",      1) #4
    prob_obj.set_val("tiploss",      True)
    prob_obj.set_val("hubloss",      True)
    prob_obj.set_val("wakerotation", True)
    prob_obj.set_val("usecd",        True)


# ================================================================
# 6. 第一阶段：验证哪些输出能被 chord 影响
# ================================================================
print("=" * 60)
print("验证: 手动扰动检查")
print("=" * 60)

prob_test = om.Problem()
comp_test = CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options)
prob_test.model.add_subsystem("blade", comp_test, promotes=["*"])
prob_test.setup(force_alloc_complex=True)
set_all_inputs(prob_test)
prob_test.set_val("chord", chord, units="m")
prob_test.run_model()

CP_original = prob_test.get_val("CP")[0]
T_original  = prob_test.get_val("T")[0]

chord_perturbed = chord.copy()
chord_perturbed[5] += 0.3
prob_test.set_val("chord", chord_perturbed, units="m")
prob_test.run_model()
CP_perturbed = prob_test.get_val("CP")[0]
T_perturbed  = prob_test.get_val("T")[0]

print(f"  CP: {CP_original:.6f} -> {CP_perturbed:.6f}  ΔCP = {CP_perturbed - CP_original:.6e}")
print(f"  T:  {T_original:.6f} -> {T_perturbed:.6f}  ΔT  = {T_perturbed - T_original:.6e}")

# ================================================================
# 7. 正式优化
# ================================================================
print("\n" + "=" * 60)
print("弦长优化: 最大化 CP")
print("=" * 60)
# ===================Version7.2：多起点策略==========================
# 评估用 Problem（不加 driver）
prob_eval = om.Problem()
comp_eval = CCBladeTwist(
    modeling_options=modeling_options,
    opt_options=opt_options,
)
prob_eval.model.add_subsystem("blade", comp_eval, promotes=["*"])
prob_eval.setup()
set_all_inputs(prob_eval)


def ctrl_to_full(chord_ctrl):
    interp = PchipInterpolator(r_ctrl, chord_ctrl)
    chord_interp = np.clip(interp(r_opt), 0.05, 1.00)
    return np.concatenate([chord_root, chord_interp])


def objective(chord_ctrl):
    chord_full = ctrl_to_full(chord_ctrl)
    prob_eval.set_val("chord", chord_full, units="m")
    prob_eval.run_model()
    CP = prob_eval.get_val("CP")[0]
    alpha = prob_eval.get_val("alpha", units="deg")
    penalty = 100.0 * np.sum(np.maximum(alpha - 11.0, 0.0) ** 2)
    return -CP + penalty

# ========== 多起点优化 ==========
n_runs = 500
best_CP = -np.inf
best_P = 0.0
best_T = 0.0
best_chord = None
bounds = [(0.05, 1.00)] * n_ctrl
np.random.seed(42)

for i in range(n_runs):
    if i == 0:
        x0 = chord_ctrl_init.copy()
    else:
        noise = np.random.uniform(-0.10, 0.10, size=n_ctrl)
        x0 = np.clip(chord_ctrl_init + noise, 0.05, 1.00)

    t0 = time.time()
    res = minimize(objective, x0, method="SLSQP", bounds=bounds,
                   options={"maxiter": 500, "ftol": 1e-7, "disp": False})
    dt = time.time() - t0

    chord_full = ctrl_to_full(res.x)
    prob_eval.set_val("chord", chord_full, units="m")
    prob_eval.run_model()
    CP_i = prob_eval.get_val("CP")[0]
    P_i  = prob_eval.get_val("P")[0]
    T_i  = prob_eval.get_val("T")[0]

    status = "✓" if res.success else "✗"
    print(f"  Run {i+1:2d}/{n_runs} {status}: CP={CP_i:.6f}  P={P_i:.1f}W  T={T_i:.1f}N  ({dt:.1f}s)")

    if CP_i > best_CP:
        best_CP, best_P, best_T = CP_i, P_i, T_i
        best_chord = chord_full.copy()

print(f"\n{'='*60}")
print(f"最优 CP = {best_CP:.6f}")
print(f"最优 P  = {best_P:.1f} W")
print(f"最优 T  = {best_T:.1f} N")
print(f"\n{'r(m)':>6s}  {'init':>10s}  {'opt':>10s}  {'Δ':>8s}  {'备注':>4s}")
for j in range(n_span):
    dc = best_chord[j] - chord[j]
    note = "固定" if j < n_fix else ""
    print(f"{r_all[j]:6.2f}  {chord[j]:10.4f}  {best_chord[j]:10.4f}  {dc:+8.4f}  {note}")

np.savez("chord_optimization_results_tsr6.53.npz",
         r=r, chord_init=chord, chord_opt=best_chord,
         best_CP=best_CP, best_P=best_P, best_T=best_T)
print(f"\n结果已保存到 chord_optimization_results_tsr6.53.npz")