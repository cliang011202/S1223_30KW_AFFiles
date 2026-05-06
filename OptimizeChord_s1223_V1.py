"""
叶片弦长优化V1: 逐站优化OpenMDAO driver
设计变量: 每个非圆柱截面的弦长
优化问题: 最大化功率系数CP, 设置各截面弦长范围c_i, 攻角α ≤11°
弦长分布: 各截面弦长没有任何关联约束, 可能会出现“锯齿形”局部最优

输入参数: “2.叶片参数”“7. 正式优化”
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

V_design   = 22     #18m/s环境风速，22m/s风轮面风速
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

twist_init_deg = np.array([66.82, 35.96, 21.64, 12.46, 8.01,
                           5.26,  3.07,  1.89,  1.6, 1.42,
                          -0.09, -2.89, -5.02])

rthick = np.array([100.0, 100.0, 12.1, 12.1, 12.1,
                   12.1, 12.1, 12.1, 12.1, 12.1,
                   12.1, 12.1, 12.1])

n_fix = 2  # 叶根固定站位数

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
# ===================Version7.1：初值附近梯度优化=====================
# prob2 = om.Problem()
# comp2 = CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options)
# prob2.model.add_subsystem("blade", comp2, promotes=["*"])

# # ★★★ 关键：在模型层面用 FD 近似总导数，绕过组件级偏导问题 ★★★
# prob2.model.approx_totals(method="fd", step=1e-6, form="central")   #fd有限差分法；step扰动步长

# # 优化器
# prob2.driver = om.ScipyOptimizeDriver()
# prob2.driver.options["optimizer"] = "SLSQP" #Sequential Least Squares Programming，序列最小二乘规划
# prob2.driver.options["maxiter"]   = 2000    #最大迭代次数500
# prob2.driver.options["tol"]       = 1e-5    #收敛容差
# prob2.driver.options["disp"]      = True

# # 设计变量: 仅弦长
# prob2.model.add_design_var(
#     "chord",
#     lower=0.05,
#     upper=1.00,
#     units="m",
#     ref=0.2,    # 缩放参考值，建议设为弦长平均值
# )

# # 策略A: 最大化 CP（默认）
# prob2.model.add_objective("CP", scaler=-1.0)
# prob2.model.add_constraint("alpha", upper=11.0, units="deg")

# # 策略B: 最大化 CP + 推力约束（需确认 T 导数通路正常）
# # prob2.model.add_objective("CP", scaler=-1.0)
# # prob2.model.add_constraint("T", upper=12000.0)
# # prob2.model.add_constraint("alpha", upper=11.0, units="deg")

# prob2.setup()
# set_all_inputs(prob2)
# prob2.set_val("chord", chord, units="m")

print("\n开始优化...")
# t0 = time.time()
# fail = prob2.run_driver()
# t1 = time.time()
# print(f"总耗时: {t1 - t0:.1f} 秒")

# if fail:
#     print("⚠ 优化未完全收敛")
# else:
#     print("✓ 优化收敛成功!")
# ===================Version7.1：初值附近梯度优化=====================


# ===================Version7.2：多起点策略==========================
def run_optimization(chord_init, run_id):
    """单次优化运行"""
    prob = om.Problem()
    comp = CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options)
    prob.model.add_subsystem("blade", comp, promotes=["*"])
    prob.model.approx_totals(method="fd", step=1e-5, form="central")    #step步长

    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options["optimizer"] = "SLSQP"
    prob.driver.options["maxiter"]   = 500      #迭代次数
    prob.driver.options["tol"]       = 1e-5     #收敛容差
    prob.driver.options["disp"]      = False
    
    prob.model.add_design_var("chord", lower=0.05, upper=1.00, units="m", ref=0.3,indices=list(range(n_fix, n_span)))#只优化第2+1个截面起的弦长
    prob.model.add_objective("CP", scaler=-1.0)
    prob.model.add_constraint("alpha", upper=11.0, units="deg")

    prob.setup()
    set_all_inputs(prob)
    prob.set_val("chord", chord_init, units="m")

    fail = prob.run_driver()

    CP_opt    = prob.get_val("CP")[0]
    P_opt     = prob.get_val("P")[0]
    T_opt     = prob.get_val("T")[0]
    chord_opt = prob.get_val("chord", units="m").copy()

    status = "✓" if not fail else "✗"
    return CP_opt, P_opt, T_opt, chord_opt, status


# ========== 多起点运行 ==========
n_runs = 10
n_success = 0
best_CP = -np.inf
best_chord = None
best_P = 0.0
best_T = 0.0
results = []

np.random.seed(42)

for i in range(n_runs):
    # 生成随机初始弦长：在原始弦长基础上加随机扰动
    if i == 0:
        chord_init_i = chord.copy()  # 第一次用原始值
    else:
        # 方法1：原始值 ± 随机扰动，从第2+1个截面开始扰动
        chord_init_i = chord.copy()
        noise = np.random.uniform(-0.1, 0.5, size=n_span - n_fix)
        chord_init_i[n_fix:] = np.clip(chord[n_fix:] + noise, 0.05, 1.00)

    t0 = time.time()
    CP_i, P_i, T_i, chord_i, status = run_optimization(chord_init_i, i)
    dt = time.time() - t0

    if status == "✓":
        n_success += 1
    #错误1：Positive directional derivative for linesearch。即SLSQP 在搜索方向上找不到能让目标函数下降的步长
    #1.有限差分梯度不准确（步长不合适或数值噪声） 2.已经非常接近某个局部最优，但数值精度不够判定收敛 3.约束边界处梯度矛盾
    #错误2：Iteration limit reached。迭代了 500 次还没收敛
    #1.初始弦长离最优解太远，需要更多迭代 2.优化在约束边界附近反复振荡

    results.append({"run": i, "CP": CP_i, "P": P_i, "T": T_i,"chord": chord_i, "status": status})
    print(f"  Run {i+1:2d}/{n_runs} {status}: CP = {CP_i:.6f}  P = {P_i:.1f} W  T = {T_i:.1f} N  ({dt:.1f}s)")

    if CP_i > best_CP:
        best_CP = CP_i
        best_P  = P_i
        best_T  = T_i
        best_chord = chord_i.copy()

print(f"\n{'='*60}")
print(f"成功收敛: {n_success}/{n_runs}")
print(f"最优 CP = {best_CP:.6f}")
print(f"最优 P  = {best_P:.1f} W")
print(f"最优 T  = {best_T:.1f} N")
print(f"CP 分布: min={min(r['CP'] for r in results):.6f}, "
      f"max={max(r['CP'] for r in results):.6f}, "
      f"std={np.std([r['CP'] for r in results]):.6e}")  # 如果 std 很小（< 1e-4），说明大概率已找到全局最优
print(f"\n最优弦长分布:")
print(f"{'r(m)':>6s}  {'chord_init':>10s}  {'chord_opt':>10s}  {'Δchord':>8s}")
for i in range(n_span):
    dc = best_chord[i] - chord[i]
    print(f"{r[i]:6.2f}  {chord[i]:10.4f}  {best_chord[i]:10.4f}  {dc:+8.4f}")

np.savez("chord_optimization_results_tsr6.53.npz",
         r=r, chord_init=chord, chord_opt=best_chord,
         best_CP=best_CP, best_P=best_P, best_T=best_T)
print(f"\n结果已保存到 chord_optimization_results_tsr6.53.npz")
# ===================Version7.2：多起点策略==========================

# ================================================================
# 8. 输出结果
# ================================================================
# print("\n" + "=" * 60)
# print("优化结果")
# print("=" * 60)

# CP_opt    = prob2.get_val("CP")[0]
# P_opt     = prob2.get_val("P")[0]
# T_opt     = prob2.get_val("T")[0]
# theta_out = prob2.get_val("theta", units="deg")
# alpha_opt = prob2.get_val("alpha", units="deg")
# cl_opt    = prob2.get_val("cl")
# cd_opt    = prob2.get_val("cd")
# a_opt     = prob2.get_val("a")
# ap_opt    = prob2.get_val("ap")
# Px_opt    = prob2.get_val("Px_b")
# chord_opt = prob2.get_val("chord", units="m")

# T_approx = np.trapz(Px_opt, r) * n_blades

# print(f"CP = {CP_opt:.4f}")
# print(f"P  = {P_opt:.1f} W")
# print(f"T  = {T_opt:.1f} N")
# print(f"T (Px_b积分) = {T_approx:.1f} N")

# print(f"\n{'r(m)':>6s}  {'chord_old':>10s}  {'chord_new':>10s}  {'Δchord':>8s}")
# for i in range(n_span):
#     dc = chord_opt[i] - chord[i]
#     print(f"{r[i]:6.2f}  {chord[i]:10.4f}  {chord_opt[i]:10.4f}  {dc:+8.4f}")

# print(f"\n{'r(m)':>6s}  {'alpha(°)':>8s}  {'cl':>8s}  {'cd':>8s}  {'a':>8s}  {'ap':>8s}")
# for i in range(n_span):
#     print(f"{r[i]:6.2f}  {alpha_opt[i]:8.2f}  {cl_opt[i]:8.4f}  {cd_opt[i]:8.5f}  {a_opt[i]:8.4f}  {ap_opt[i]:8.4f}")

# # 保存
# np.savez("chord_optimization_results_tsr5.75.npz",
#          r=r,
#          chord_init=chord,
#          chord_opt=chord_opt,
#          twist=twist_init_deg,
#          theta_out=theta_out,
#          alpha=alpha_opt, cl=cl_opt, cd=cd_opt,
#          a=a_opt, ap=ap_opt,
#          CP=CP_opt, P=P_opt, T=T_opt, T_approx=T_approx)
# print("\n结果已保存到 chord_optimization_results_tsr5.75.npz")

# ================================================================
# 9. 结果可视化
# ================================================================
# import numpy as np
# import matplotlib.pyplot as plt

# data = np.load("chord_optimization_results_tsr5.75.npz")

# fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# # 弦长对比
# axes[0, 0].plot(data["r"], data["chord_init"], "b--o", label="初始", markersize=3)
# axes[0, 0].plot(data["r"], data["chord_opt"],  "r-s",  label="优化后", markersize=3)
# axes[0, 0].set_xlabel("r [m]")
# axes[0, 0].set_ylabel("Chord [m]")
# axes[0, 0].legend()
# axes[0, 0].set_title(f"弦长分布 (CP: {float(data['CP']):.4f})")

# # 攻角
# axes[0, 1].plot(data["r"], data["alpha"], "g-o", markersize=3)
# axes[0, 1].axhline(y=11.0, color="r", linestyle="--", label="失速限制")
# axes[0, 1].set_xlabel("r [m]")
# axes[0, 1].set_ylabel("Alpha [°]")
# axes[0, 1].legend()
# axes[0, 1].set_title("攻角分布")

# # 升力系数
# axes[1, 0].plot(data["r"], data["cl"], "m-o", markersize=3)
# axes[1, 0].set_xlabel("r [m]")
# axes[1, 0].set_ylabel("Cl")
# axes[1, 0].set_title("升力系数分布")

# # 诱导因子
# axes[1, 1].plot(data["r"], data["a"],  "b-o", label="a",  markersize=3)
# axes[1, 1].plot(data["r"], data["ap"], "r-s", label="a'", markersize=3)
# axes[1, 1].set_xlabel("r [m]")
# axes[1, 1].set_ylabel("诱导因子")
# axes[1, 1].legend()
# axes[1, 1].set_title("诱导因子分布")

# plt.tight_layout()
# plt.savefig("chord_optimization_results.png", dpi=150)
# plt.show()