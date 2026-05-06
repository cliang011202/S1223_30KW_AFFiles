import numpy as np
import openmdao.api as om
import os
import time
from scipy.interpolate import BSpline, make_lsq_spline
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
# 2. 叶片参数
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

V_design   = 18
tsr        = 4.79
pitch_deg  = 0.0

n_opt_twist = 8
n_opt_chord = 8

r = np.array([0.300, 0.500, 0.676, 0.967, 1.302,
              1.664, 2.036, 2.398, 2.733, 3.024,
              3.256, 3.417, 3.496])

chord = np.array([  0.250 ,0.250 ,0.4802,0.3378,0.2709,
                    0.2231,0.185 ,0.1596,0.1426,0.1232,
                    0.0893,0.1092,0.0924])

twist_init_deg = np.array([21.64, 21.64, 21.64, 12.46, 8.01,
                           5.26,  3.07,  1.89,  1.6, 1.42,
                          -0.09, -2.89, -5.02])

rthick = np.array([100.0, 100.0, 12.1, 12.1, 12.1,
                    12.1,  12.1, 12.1, 12.1, 12.1,
                    12.1,  12.1, 12.1])

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
# 4. B-Spline 参数化组件
# ================================================================

class BsplineTwist(om.ExplicitComponent):
    """
    用 B-spline 控制点生成平滑的扭角分布。

    输入: twist_cp  — n_cp 个控制点值 (rad)
    输出: theta_in  — n_span 个截面的扭角 (rad)

    B-spline 基函数矩阵在 setup 中预计算，compute 只做矩阵乘法，
    解析 Jacobian = 基函数矩阵本身，无需有限差分。
    """

    def initialize(self):
        self.options.declare("n_cp", types=int, desc="Number of B-spline control points")
        self.options.declare("n_span", types=int, desc="Number of blade span stations")
        self.options.declare("r", types=np.ndarray, desc="Radial stations array (m)")
        self.options.declare("spline_order", default=4, types=int,
                             desc="B-spline order (4 = cubic)")

    def setup(self):
        n_cp   = self.options["n_cp"]
        n_span = self.options["n_span"]
        r_arr  = self.options["r"]
        k      = self.options["spline_order"]

        # 归一化展向坐标 [0, 1]
        s = (r_arr - r_arr[0]) / (r_arr[-1] - r_arr[0])
        self.s_span = s

        # 构建 B-spline 节点向量 (clamped knot vector)
        # 内部节点数 = n_cp - k
        n_internal = n_cp - k
        if n_internal < 0:
            # 控制点太少，降阶
            k = n_cp
            n_internal = 0
            self.options["spline_order"] = k

        if n_internal > 0:
            internal_knots = np.linspace(0.0, 1.0, n_internal + 2)[1:-1]
        else:
            internal_knots = np.array([])

        knots = np.concatenate([
            np.zeros(k),
            internal_knots,
            np.ones(k)
        ])
        self.knots = knots
        self.k = k

        # 预计算基函数矩阵 B: shape (n_span, n_cp)
        # B[i, j] = N_j(s_i)
        self.B_matrix = np.zeros((n_span, n_cp))
        for j in range(n_cp):
            # 构造第 j 个基函数: 控制点全0，第j个为1
            c_j = np.zeros(n_cp)
            c_j[j] = 1.0
            bspl = BSpline(knots, c_j, k - 1, extrapolate=False)
            vals = bspl(s)
            # 处理边界 NaN
            vals = np.nan_to_num(vals, nan=0.0)
            self.B_matrix[:, j] = vals

        # 确保每行基函数之和为 1 (partition of unity)
        row_sums = self.B_matrix.sum(axis=1)
        row_sums[row_sums == 0] = 1.0
        # B-spline 本身满足 partition of unity，这里仅做安全检查
        for i in range(n_span):
            if abs(row_sums[i] - 1.0) > 1e-10:
                self.B_matrix[i, :] /= row_sums[i]

        # 声明输入输出
        self.add_input("twist_cp", val=np.zeros(n_cp), units="rad",
                       desc="B-spline control point values for twist")
        self.add_output("theta_in", val=np.zeros(n_span), units="rad",
                        desc="Twist angle at each blade section")

        # 解析 Jacobian
        self.declare_partials("theta_in", "twist_cp", val=self.B_matrix)

    def compute(self, inputs, outputs):
        outputs["theta_in"] = self.B_matrix @ inputs["twist_cp"]

    def fit_initial_twist(self, twist_rad):
        """
        给定初始扭角分布 (n_span,)，用最小二乘拟合出最优控制点。
        返回 (n_cp,) 的控制点值 (rad)。
        """
        n_cp = self.options["n_cp"]
        # 最小二乘: min ||B @ cp - twist||^2
        # cp = (B^T B)^{-1} B^T twist
        B = self.B_matrix
        cp, residuals, rank, sv = np.linalg.lstsq(B, twist_rad, rcond=None)
        return cp


# ================================================================
# 5. 辅助函数：统一设置 CCBladeTwist 的输入
# ================================================================

def set_ccblade_inputs(prob_obj, prefix=""):
    """设置 CCBladeTwist 需要的所有输入参数（theta_in 除外）"""
    p = prefix
    prob_obj.set_val(f"{p}airfoils_aoa", common_aoa, units="deg")
    prob_obj.set_val(f"{p}airfoils_Re",  np.array([2.0e6]))
    prob_obj.set_val(f"{p}airfoils_cl",  cl_table)
    prob_obj.set_val(f"{p}airfoils_cd",  cd_table)
    prob_obj.set_val(f"{p}airfoils_cm",  cm_table)

    prob_obj.set_val(f"{p}r",       r,       units="m")
    prob_obj.set_val(f"{p}chord",   chord,   units="m")
    prob_obj.set_val(f"{p}rthick",  rthick / 100.0)
    prob_obj.set_val(f"{p}s_opt_theta", s_opt_twist)
    prob_obj.set_val(f"{p}s_opt_chord", s_opt_chord)

    prob_obj.set_val(f"{p}Uhub",  V_design, units="m/s")
    prob_obj.set_val(f"{p}tsr",   tsr)
    prob_obj.set_val(f"{p}pitch", pitch_deg, units="deg")

    prob_obj.set_val(f"{p}Rhub",         Rhub,             units="m")
    prob_obj.set_val(f"{p}Rtip",         Rtip,             units="m")
    prob_obj.set_val(f"{p}hub_height",   hub_height,       units="m")
    prob_obj.set_val(f"{p}precone",      precone,          units="deg")
    prob_obj.set_val(f"{p}tilt",         tilt,             units="deg")
    prob_obj.set_val(f"{p}yaw",          yaw,              units="deg")
    prob_obj.set_val(f"{p}precurve",     np.zeros(n_span), units="m")
    prob_obj.set_val(f"{p}precurveTip",  0.0,              units="m")
    prob_obj.set_val(f"{p}presweep",     np.zeros(n_span), units="m")
    prob_obj.set_val(f"{p}presweepTip",  0.0,              units="m")
    prob_obj.set_val(f"{p}rho",          rho,              units="kg/m**3")
    prob_obj.set_val(f"{p}mu",           mu,               units="kg/(m*s)")
    prob_obj.set_val(f"{p}shearExp",     shearExp)
    prob_obj.set_val(f"{p}nBlades",      n_blades)
    prob_obj.set_val(f"{p}nSector",      1)
    prob_obj.set_val(f"{p}tiploss",      True)
    prob_obj.set_val(f"{p}hubloss",      True)
    prob_obj.set_val(f"{p}wakerotation", True)
    prob_obj.set_val(f"{p}usecd",        True)


# ================================================================
# 6. 配置选项
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
# 7. B-spline 控制点数量选择
# ================================================================

N_CP = 8  # B-spline 控制点数量 (可调: 5~8)
        # 越少越平滑，越多越灵活
        # 6 个控制点 + 三次B样条 = 很好的平滑/灵活平衡


# ================================================================
# 8. 构建 OpenMDAO 模型: BsplineTwist -> CCBladeTwist
# ================================================================
# ---- 约束: 控制点单调递减 ----
# twist_cp[i] - twist_cp[i+1] >= min_drop  (即相邻控制点必须递减)
# 用线性约束实现: 构造差分矩阵 D，使得 D @ twist_cp >= min_drop
#
# 但 OpenMDAO 不直接支持对设计变量做线性差分约束，
# 所以我们加一个小组件来输出相邻控制点之差，再约束它 >= 0
class TwistCpDiff(om.ExplicitComponent):
    """输出相邻控制点之差: diff[i] = twist_cp[i] - twist_cp[i+1]"""
    def initialize(self):
        self.options.declare("n_cp", types=int)

    def setup(self):
        n_cp = self.options["n_cp"]
        self.add_input("twist_cp", val=np.zeros(n_cp), units="rad")
        self.add_output("twist_cp_diff", val=np.zeros(n_cp - 1), units="rad")

        # 解析 Jacobian
        rows = np.arange(n_cp - 1)
        # d(diff[i])/d(cp[i]) = +1
        self.declare_partials("twist_cp_diff", "twist_cp",
                              rows=np.concatenate([rows, rows]),
                              cols=np.concatenate([rows, rows + 1]),
                              val=np.concatenate([np.ones(n_cp - 1),
                                                  -np.ones(n_cp - 1)]))

    def compute(self, inputs, outputs):
        cp = inputs["twist_cp"]
        outputs["twist_cp_diff"] = cp[:-1] - cp[1:]

class TwistOptGroup(om.Group):
    """
    将 B-spline 参数化与 CCBlade 气动分析串联。

    数据流:
        twist_cp (N_CP) -> [BsplineTwist] -> theta_in (n_span) -> [CCBladeTwist] -> CP, T, alpha, ...
    """

    def initialize(self):
        self.options.declare("modeling_options")
        self.options.declare("opt_options")
        self.options.declare("n_cp", types=int)
        self.options.declare("r", types=np.ndarray)

    def setup(self):
        mod_opt = self.options["modeling_options"]
        opt_opt = self.options["opt_options"]
        n_cp    = self.options["n_cp"]
        r_arr   = self.options["r"]
        n_span_local = len(r_arr)

        # 1) B-spline 参数化组件
        self.add_subsystem(
            "bspline",
            BsplineTwist(n_cp=n_cp, n_span=n_span_local, r=r_arr, spline_order=4),
            promotes_inputs=["twist_cp"],
            promotes_outputs=["theta_in"],
        )

        # 2) CCBlade 气动分析组件
        self.add_subsystem(
            "ccblade",
            CCBladeTwist(modeling_options=mod_opt, opt_options=opt_opt),
            promotes_inputs=["theta_in",
                             "r", "chord", "rthick",
                             "s_opt_theta", "s_opt_chord",
                             "Uhub", "tsr", "pitch",
                             "airfoils_aoa", "airfoils_Re",
                             "airfoils_cl", "airfoils_cd", "airfoils_cm",
                             "Rhub", "Rtip", "hub_height",
                             "precone", "tilt", "yaw",
                             "precurve", "precurveTip",
                             "presweep", "presweepTip",
                             "rho", "mu", "shearExp",
                             "nBlades", "nSector",
                             "tiploss", "hubloss",
                             "wakerotation", "usecd"],
            promotes_outputs=["CP", "CM", "T", "P", "Q",
                              "theta", "alpha", "cl", "cd",
                              "a", "ap", "Px_b", "Py_b", "Pz_b",
                              "Px_af", "Py_af", "Pz_af",
                              "LiftF", "DragF",
                              "local_airfoil_velocities"],
        )

        # 3) 控制点单调性差分组件
        self.add_subsystem(
            "cp_diff",
            TwistCpDiff(n_cp=n_cp),
            promotes_inputs=["twist_cp"],
            promotes_outputs=["twist_cp_diff"],
        )


# ================================================================
# 9. 第一阶段: 验证 B-spline 拟合质量
# ================================================================

print("=" * 60)
print("第一阶段: B-spline 拟合验证")
print("=" * 60)

# 创建临时 BsplineTwist 实例来拟合初始扭角
bspl_temp = BsplineTwist(n_cp=N_CP, n_span=n_span, r=r, spline_order=4)
# 手动调用 setup 的核心逻辑来获取 B_matrix
# 为此我们用一个临时 Problem
prob_fit = om.Problem()
prob_fit.model.add_subsystem("bspl", bspl_temp, promotes=["*"])
prob_fit.setup()

# 拟合初始控制点
twist_init_rad = np.deg2rad(twist_init_deg)
cp_init = bspl_temp.fit_initial_twist(twist_init_rad)

# 验证拟合精度
prob_fit.set_val("twist_cp", cp_init, units="rad")
prob_fit.run_model()
theta_fitted = prob_fit.get_val("theta_in", units="deg")

print(f"\nB-spline 控制点数: {N_CP}")
print(f"叶片截面数: {n_span}")
print(f"\n{'r(m)':>6s} {'原始扭角':>10s} {'拟合扭角':>10s} {'误差(°)':>10s}")
for i in range(n_span):
    err = theta_fitted[i] - twist_init_deg[i]
    print(f"{r[i]:6.2f} {twist_init_deg[i]:10.2f} {theta_fitted[i]:10.2f} {err:+10.3f}")

max_err = np.max(np.abs(theta_fitted - twist_init_deg))
rms_err = np.sqrt(np.mean((theta_fitted - twist_init_deg) ** 2))
print(f"\n最大拟合误差: {max_err:.3f}°")
print(f"RMS 拟合误差: {rms_err:.3f}°")

cp_init_deg = np.rad2deg(cp_init)
print(f"\n初始控制点 (deg): {np.round(cp_init_deg, 2)}")


# ================================================================
# 10. 第二阶段: 验证导数连通性
# ================================================================

print("\n" + "=" * 60)
print("第二阶段: 导数连通性验证")
print("=" * 60)

prob_check = om.Problem()
prob_check.model.add_subsystem(
    "opt_group",
    TwistOptGroup(
        modeling_options=modeling_options,
        opt_options=opt_options,
        n_cp=N_CP,
        r=r,
    ),
    promotes=["*"],
)
prob_check.setup(force_alloc_complex=True)
set_ccblade_inputs(prob_check)
prob_check.set_val("twist_cp", cp_init, units="rad")
prob_check.run_model()

CP_base = prob_check.get_val("CP")[0]
print(f"\n基准 CP = {CP_base:.6f}")

# 扰动第3个控制点
cp_perturbed = cp_init.copy()
cp_perturbed[2] += np.deg2rad(2.0)
prob_check.set_val("twist_cp", cp_perturbed, units="rad")
prob_check.run_model()
CP_pert = prob_check.get_val("CP")[0]
print(f"扰动控制点[2]+2° 后 CP = {CP_pert:.6f}")
print(f"ΔCP = {CP_pert - CP_base:.6f}")

if abs(CP_pert - CP_base) > 1e-10:
    print("✓ CP 对 twist_cp 有响应，导数链连通")
else:
    print("✗ CP 对 twist_cp 无响应，需排查")


# ================================================================
# 11. 第三阶段: 正式优化
# ================================================================


print("\n" + "=" * 60)
print("第三阶段: B-spline 扭角优化")
print("=" * 60)

prob = om.Problem()
prob.model.add_subsystem(
    "opt_group",
    TwistOptGroup(
        modeling_options=modeling_options,
        opt_options=opt_options,
        n_cp=N_CP,
        r=r,
    ),
    promotes=["*"],
)

# ---- 优化器配置 ----
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options["optimizer"] = "SLSQP"
prob.driver.options["maxiter"]   = 200
prob.driver.options["tol"]       = 1e-6
prob.driver.options["disp"]      = True

# ---- 设计变量: B-spline 控制点 ----
# 上下界基于初始值 ± 15°（控制点空间）
cp_lower = cp_init - np.deg2rad(15.0)
cp_upper = cp_init + np.deg2rad(15.0)

prob.model.add_design_var(
    "twist_cp",
    lower=cp_lower,
    upper=cp_upper,
    units="rad",
)

# # ---- 目标1: 最大化 CP ----
# prob.model.add_objective("CP", scaler=-1.0)
# # ---- 约束1: 攻角不超过失速限制 ----
# prob.model.add_constraint("alpha", upper=11.0, units="deg")

# ---- 目标2: 最小化推力 T ----
prob.model.add_objective("T", scaler=1.0)
# ---- 约束2: 1)CP 不低于 0.42 2)攻角不超过失速限制 3)用法向载荷 Px_b 的最小值 > 0 来间接保证推力为正----
prob.model.add_constraint("CP", lower=0.3)
prob.model.add_constraint("alpha", upper=11.0, units="deg")
prob.model.add_constraint("Px_b", lower=0.0, units="N/m")

# 控制点必须单调递减，最小降幅 0.5°（防止相邻控制点相等导致局部回升）
prob.model.add_constraint(
    "twist_cp_diff",
    lower=np.deg2rad(0.1),  # 每对相邻控制点至少递减 0.1°
    units="rad",
)

print(f"\n设计变量: {N_CP} 个 B-spline 控制点")
print(f"目标: 最大化 CP")
print(f"约束: alpha ≤ 11°")
print(f"控制点初始值 (deg): {np.round(np.rad2deg(cp_init), 2)}")
print(f"控制点下界 (deg): {np.round(np.rad2deg(cp_lower), 2)}")
print(f"控制点上界 (deg): {np.round(np.rad2deg(cp_upper), 2)}")

# ---- Setup & 设置输入 ----
prob.setup(force_alloc_complex=True)
set_ccblade_inputs(prob)
prob.set_val("twist_cp", cp_init, units="rad")

# ---- 运行优化 ----
print("\n开始优化...")
t0 = time.time()
fail = prob.run_driver()
t1 = time.time()
print(f"优化耗时: {t1 - t0:.1f} 秒")

if fail:
    print("⚠ 优化未完全收敛，但结果可能仍有改善")
else:
    print("✓ 优化收敛成功!")


# ================================================================
# 12. 输出结果
# ================================================================

print("\n" + "=" * 60)
print("优化结果")
print("=" * 60)

CP_opt    = prob.get_val("CP")[0]
P_opt     = prob.get_val("P")[0]
T_opt     = prob.get_val("T")[0]
Q_opt     = prob.get_val("Q")[0]
theta_opt = prob.get_val("theta", units="deg")
alpha_opt = prob.get_val("alpha", units="deg")
cl_opt    = prob.get_val("cl")
cd_opt    = prob.get_val("cd")
a_opt     = prob.get_val("a")
ap_opt    = prob.get_val("ap")
Px_opt    = prob.get_val("Px_b")
cp_opt    = prob.get_val("twist_cp", units="rad")

# 推力近似
T_approx = np.trapz(Px_opt, r) * n_blades

print(f"\nCP = {CP_opt:.4f}")
print(f"P  = {P_opt:.1f} W")
print(f"T  = {T_opt:.1f} N")
print(f"Q  = {Q_opt:.1f} N·m")
print(f"推力(Px_b积分近似) = {T_approx:.1f} N")

print(f"\n优化后控制点 (deg): {np.round(np.rad2deg(cp_opt), 2)}")

print(f"\n{'r(m)':>6s} {'twist_old':>10s} {'twist_new':>10s} {'Δtwist':>8s} "
      f"{'alpha':>8s} {'cl':>8s} {'cd':>8s} {'cl/cd':>8s}")
for i in range(n_span):
    ld = cl_opt[i] / cd_opt[i] if cd_opt[i] > 1e-6 else 0
    print(f"{r[i]:6.2f} {twist_init_deg[i]:10.2f} {theta_opt[i]:10.2f} "
          f"{theta_opt[i] - twist_init_deg[i]:+8.2f} "
          f"{alpha_opt[i]:8.2f} {cl_opt[i]:8.4f} {cd_opt[i]:8.4f} {ld:8.1f}")

# 检查平滑性: 相邻截面扭角差
dtheta = np.diff(theta_opt)
print(f"\n相邻截面扭角差 (deg):")
for i in range(len(dtheta)):
    marker = " ⚠" if abs(dtheta[i]) > 5.0 else ""
    print(f"  [{i}]->[{i+1}]: {dtheta[i]:+.2f}°{marker}")

max_jump = np.max(np.abs(dtheta))
print(f"\n最大相邻跳变: {max_jump:.2f}°")
if max_jump < 5.0:
    print("✓ 扭角分布平滑，无锯齿")
else:
    print("⚠ 仍有较大跳变，可尝试减少控制点数或增加平滑约束")


# ================================================================
# 13. 保存结果
# ================================================================

np.savez("twist_bspline_optimization_results.npz",
         r=r, chord=chord,
         twist_init=twist_init_deg, twist_opt=theta_opt,
         twist_cp_init=np.rad2deg(cp_init), twist_cp_opt=np.rad2deg(cp_opt),
         alpha=alpha_opt, cl=cl_opt, cd=cd_opt,
         a=a_opt, ap=ap_opt,
         CP=CP_opt, P=P_opt, T=T_opt, Q=Q_opt, T_approx=T_approx,
         B_matrix=prob.model.opt_group.bspline.B_matrix)
print("\n结果已保存到 twist_bspline_optimization_results.npz")


# ================================================================
# 14. 可视化 (可选)
# ================================================================

try:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # (a) 扭角对比
    ax = axes[0, 0]
    s_norm = (r - r[0]) / (r[-1] - r[0])
    s_cp = np.linspace(0, 1, N_CP)
    ax.plot(s_norm, twist_init_deg, 'bo-', label='Initial twist', markersize=6)
    ax.plot(s_norm, theta_opt, 'rs-', label='Optimized twist (B-spline)', markersize=6)
    # 绘制拟合的初始曲线
    ax.plot(s_norm, theta_fitted, 'b--', alpha=0.5, label='B-spline fit of initial')
    # 标记控制点
    ax.plot(s_cp, np.rad2deg(cp_init), 'b^', markersize=10, alpha=0.5, label='Initial CPs')
    ax.plot(s_cp, np.rad2deg(cp_opt), 'rv', markersize=10, alpha=0.5, label='Optimized CPs')
    ax.set_xlabel('Normalized span')
    ax.set_ylabel('Twist (deg)')
    ax.set_title('Twist Distribution')
    ax.legend(fontsize=8)
    ax.grid(True)

    # (b) 攻角分布
    ax = axes[0, 1]
    ax.plot(s_norm, alpha_opt, 'go-', markersize=6)
    ax.axhline(y=11.0, color='r', linestyle='--', label='Stall limit (11°)')
    ax.set_xlabel('Normalized span')
    ax.set_ylabel('Angle of attack (deg)')
    ax.set_title('Angle of Attack Distribution')
    ax.legend()
    ax.grid(True)

    # (c) 升力系数
    ax = axes[1, 0]
    ax.plot(s_norm, cl_opt, 'mo-', markersize=6)
    ax.set_xlabel('Normalized span')
    ax.set_ylabel('Cl')
    ax.set_title('Lift Coefficient Distribution')
    ax.grid(True)

    # (d) 升阻比
    ax = axes[1, 1]
    ld_ratio = np.where(cd_opt > 1e-6, cl_opt / cd_opt, 0)
    ax.plot(s_norm, ld_ratio, 'co-', markersize=6)
    ax.set_xlabel('Normalized span')
    ax.set_ylabel('Cl/Cd')
    ax.set_title('Lift-to-Drag Ratio')
    ax.grid(True)

    plt.suptitle(f'B-spline Twist Optimization (N_CP={N_CP}, CP={CP_opt:.4f})', fontsize=14)
    plt.tight_layout()
    plt.savefig("twist_bspline_optimization.png", dpi=150)
    plt.show()
    print("\n图表已保存到 twist_bspline_optimization.png")

except ImportError:
    print("\n未安装 matplotlib，跳过可视化")
