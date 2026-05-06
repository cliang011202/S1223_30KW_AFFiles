"""
叶片扭角优化
策略: 最大化 CP (即最小化 -CP)
约束: 攻角不超过失速限制

待修改参数: “2.叶片参数”


"""

import numpy as np
import openmdao.api as om
import os
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

V_design   = 18     #18->22m/s风轮面风速, 
tsr        = 7.98   #18→22——392r/min——tsr6.53
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

n_span = len(r)

is_cylinder = [True, True, False, False, False, 
               False,False, False, False, False, 
               False,False, False]


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
# 5. 辅助函数：统一设置输入
# ================================================================

def set_all_inputs(prob_obj):
    """设置所有输入参数"""
    prob_obj.set_val("airfoils_aoa", common_aoa, units="deg")
    prob_obj.set_val("airfoils_Re",  np.array([2.0e6]))
    prob_obj.set_val("airfoils_cl",  cl_table)
    prob_obj.set_val("airfoils_cd",  cd_table)
    prob_obj.set_val("airfoils_cm",  cm_table)

    prob_obj.set_val("r",       r,       units="m")
    prob_obj.set_val("chord",   chord,   units="m")
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
# 6. 第一阶段：验证哪些输出能被 theta_in 影响
# ================================================================

print("=" * 60)
print("第一阶段: 手动验证导数连通性")
print("=" * 60)

prob_test = om.Problem()
comp_test = CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options)
prob_test.model.add_subsystem("blade", comp_test, promotes=["*"])
prob_test.setup(force_alloc_complex=True)
set_all_inputs(prob_test)
prob_test.set_val("theta_in", twist_init_deg, units="deg")
prob_test.run_model()

# 打印所有输出的当前值
print("\n--- 所有输出变量的当前值 ---")
outputs_to_check = ["CP", "CM", "T", "P", "Q", "theta", "alpha", "cl", "cd"]
for name in outputs_to_check:
    val = prob_test.get_val(name)
    if val.size == 1:
        print(f"  {name:>10s} = {val[0]:.6f}")
    else:
        print(f"  {name:>10s} = [{val[0]:.4f}, ..., {val[-1]:.4f}]  (len={val.size})")

# 手动扰动 theta_in 检查 CP 是否变化
print("\n--- 手动扰动检查 ---")
twist_perturbed = twist_init_deg.copy()
twist_perturbed[5] += 2.0  # 第6个截面扭角 +2°

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
    print("  ✓ CP 对 theta_in 有响应，可以用 CP 做优化目标/约束")
else:
    print("  ✗ CP 对 theta_in 无响应，需要排查问题")

T_original  = prob_test.get_val("T")[0]
prob_test.set_val("theta_in", twist_perturbed, units="deg")
prob_test.run_model()
T_perturbed = prob_test.get_val("T")[0]
print(f"\n  T (原始)    = {T_original:.6f}")
print(f"  T (扰动+2°) = {T_perturbed:.6f}")
print(f"  ΔT          = {T_perturbed - T_original:.6f}")

if abs(T_original) < 1e-10:
    print("  ⚠ T 始终为 0 — 源码 compute() 中未给 T 赋值！")
    print("  → 不能用 T 做优化目标，改用 CP 或 Px_b")


# ================================================================
# 7. 第二阶段：正式优化
# ================================================================

print("\n" + "=" * 60)
print("第二阶段: 扭角优化")
print("=" * 60)

# ---- 根据第一阶段结果选择优化策略 ----
# 策略 A: 最大化 CP (最可靠)
# 策略 B: 如果 T 有响应，最小化 T 且约束 CP≥0.42
USE_STRATEGY = "A"  # 先用 A，确认能跑通后再尝试B

prob2 = om.Problem()
comp2 = CCBladeTwist(modeling_options=modeling_options, opt_options=opt_options)
prob2.model.add_subsystem("blade", comp2, promotes=["*"])

# --- 优化器 ---    优化时间=单次run_model*截面数量*每次迭代次数*maxiter, eg.0.23*2*3*5=6.9s
prob2.driver = om.ScipyOptimizeDriver()
prob2.driver.options["optimizer"] = "SLSQP"
prob2.driver.options["maxiter"]   = 1500       
prob2.driver.options["tol"]       = 1e-5    
prob2.driver.options["disp"]      = True

# --- 设计变量: theta_in ---
prob2.model.add_design_var(
    "theta_in",
    lower=np.deg2rad(twist_init_deg - 8.0),
    upper=np.deg2rad(twist_init_deg + 8.0),
    units="rad",
    # indices=key_indices,    #新增：仅对特定截面扭角优化
)

if USE_STRATEGY == "A":
    # ★ 策略A: 最大化 CP (即最小化 -CP)
    prob2.model.add_objective("CP", scaler=-1.0)
    # 约束: 攻角不超过失速限制
    prob2.model.add_constraint("alpha", upper=11.0, units="deg")
    print("优化策略 A: 最大化 CP, 约束 alpha ≤ 11°")

elif USE_STRATEGY == "B":
    # ★ 策略B: 最小化推力, 约束 CP≥0.42
    # 仅当第一阶段确认 T 有响应时使用
    prob2.model.add_objective("CP", scaler=-1.0)#prob2.model.add_objective("T")
    prob2.model.add_constraint("T", upper=5000.0)
    # prob2.model.add_constraint("CP", lower=0.42)
    prob2.model.add_constraint("alpha", upper=11.0, units="deg")
    print("优化策略 B: 最大化 CP, 约束 T≤5000, alpha≤11°")

prob2.setup(force_alloc_complex=True)
set_all_inputs(prob2)
prob2.set_val("theta_in", twist_init_deg, units="deg")

import time
print("\n开始优化...")
t0 = time.time()
fail = prob2.run_driver()
t1 = time.time()
print(f"总耗时: {t1-t0:.1f} 秒")

# 查看结果
CP_opt = prob2.get_val("CP")[0]
theta_opt = prob2.get_val("theta", units="deg")
print(f"\nCP: {CP_opt:.4f}")
print(f"优化后扭角: {np.round(theta_opt, 2)}")

if fail:
    print("⚠ 优化未完全收敛")
else:
    print("✓ 优化收敛成功!")


# ================================================================
# 8. 输出结果
# ================================================================

print("\n" + "=" * 60)
print("优化结果")
print("=" * 60)

CP_opt    = prob2.get_val("CP")[0]
P_opt     = prob2.get_val("P")[0]
theta_opt = prob2.get_val("theta", units="deg")
alpha_opt = prob2.get_val("alpha", units="deg")
cl_opt    = prob2.get_val("cl")
cd_opt    = prob2.get_val("cd")
a_opt     = prob2.get_val("a")
ap_opt    = prob2.get_val("ap")
Px_opt    = prob2.get_val("Px_b")

# 用 Px_b 积分近似推力
T_approx = np.trapz(Px_opt, r) * n_blades
print(f"\nCP = {CP_opt:.4f}")
print(f"\nP  = {P_opt:.1f} W")
print(f"\nT  = {T_approx:.1f} N  (Px_b 沿展向积分)")

print(f"\n{'r(m)':>6s} {'twist_old':>10s} {'twist_new':>10s} {'Δtwist':>8s} "
      f"{'alpha':>8s} {'cl':>8s} {'cd':>8s} {'cl/cd':>8s}")
for i in range(n_span):
    ld = cl_opt[i] / cd_opt[i] if cd_opt[i] > 1e-6 else 0
    print(f"{r[i]:6.2f} {twist_init_deg[i]:10.2f} {theta_opt[i]:10.2f} "
          f"{theta_opt[i]-twist_init_deg[i]:+8.2f} "
          f"{alpha_opt[i]:8.2f} {cl_opt[i]:8.4f} {cd_opt[i]:8.4f} {ld:8.1f}")

# 保存
np.savez("twist_optimization_results_tsr6.53.npz",
         r=r, chord=chord,
         twist_init=twist_init_deg, twist_opt=theta_opt,
         alpha=alpha_opt, cl=cl_opt, cd=cd_opt,
         a=a_opt, ap=ap_opt, CP=CP_opt, T_approx=T_approx)
print("\n结果已保存到 twist_optimization_results_tsr6.53.npz")

# ================================================================
# 9. 可视化
# ================================================================

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle(f"扭角优化结果  CP={CP_opt:.4f}  T≈{T_approx:.1f}N", fontsize=14)

    axes[0,0].plot(r, twist_init_deg, "b--o", ms=4, label="初始")
    axes[0,0].plot(r, theta_opt, "r-s", ms=4, label="优化")
    axes[0,0].set_xlabel("r (m)"); axes[0,0].set_ylabel("扭角 (°)")
    axes[0,0].legend(); axes[0,0].grid(True); axes[0,0].set_title("扭角分布")

    axes[0,1].plot(r, alpha_opt, "g-o", ms=4)
    axes[0,1].axhline(11.0, color="r", ls="--", label="失速限制")
    axes[0,1].set_xlabel("r (m)"); axes[0,1].set_ylabel("攻角 (°)")
    axes[0,1].legend(); axes[0,1].grid(True); axes[0,1].set_title("攻角分布")

    axes[0,2].plot(r, cl_opt, "b-o", ms=4)
    axes[0,2].set_xlabel("r (m)"); axes[0,2].set_ylabel("Cl")
    axes[0,2].grid(True); axes[0,2].set_title("升力系数")

    axes[1,0].plot(r, cd_opt, "r-o", ms=4)
    axes[1,0].set_xlabel("r (m)"); axes[1,0].set_ylabel("Cd")
    axes[1,0].grid(True); axes[1,0].set_title("阻力系数")

    ld = np.where(cd_opt > 1e-6, cl_opt/cd_opt, 0)
    axes[1,1].plot(r, ld, "m-o", ms=4)
    axes[1,1].set_xlabel("r (m)"); axes[1,1].set_ylabel("Cl/Cd")
    axes[1,1].grid(True); axes[1,1].set_title("升阻比")

    axes[1,2].plot(r, a_opt, "b-o", ms=4, label="a")
    axes[1,2].plot(r, ap_opt, "r-s", ms=4, label="a'")
    axes[1,2].set_xlabel("r (m)"); axes[1,2].set_ylabel("诱导因子")
    axes[1,2].legend(); axes[1,2].grid(True); axes[1,2].set_title("诱导因子")

    plt.tight_layout()
    plt.savefig("twist_optimization.png", dpi=150, bbox_inches="tight")
    plt.show()
except ImportError:
    print("未安装 matplotlib, 跳过可视化")


# ==================代办=====================
# 1.跳出局部最优解