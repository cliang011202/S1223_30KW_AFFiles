"""
S1223 30kW 全风速段功率曲线扫描脚本
========================================================
功能:
  1. Cp-λ 扫描（fixed pitch=0, V_ref=8 m/s）→ 求 TSR_opt, Cp_max
  2. 自由运行功率曲线（恒 TSR，无额定限制）→ BEM 理论上界
  3. 失速调节功率曲线（pitch=0, Ω 限速）→ 小机典型控制
  4. 变桨调节功率曲线（搜 pitch 使 P=P_rated）→ 大中机典型控制
  5. 三种模式 AEP（Weibull k=2.487, c=6.156, Jul+Sep 时间占比 45.6%）
  6. 4-联图 + npz 数据存档

直接调用 CCBlade，不走 OpenMDAO（更轻、更快）
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from ccblade.ccblade import CCBlade, CCAirfoil

sys.stdout.reconfigure(encoding="utf-8")

# ================================================================
# 1. 叶片参数（与 OptimizeChord/Twist V3 保持一致）
# ================================================================
Rhub, Rtip   = 0.2, 3.5
hub_height   = 10.0
precone      = 0.0
tilt         = 0.0
yaw          = 0.0
n_blades     = 2
rho          = 1.1
mu           = 1.81206e-5
shearExp     = 0.0

P_RATED      = 30000.0   # W, 额定功率
TSR_DESIGN   = 7.0       # 设计 TSR（仅作参考）
PITCH_MAX    = 25.0      # deg, 变桨搜索上界

V_in, V_out  = 3.0, 18.0  # 切入 / 切出
WEIBULL_K    = 2.487
WEIBULL_C    = 6.156
EFF_FRAC     = 0.456     # Jul+Sep 有效时间占比

USE_OPTIMIZED = True     # True: 加载 npz 优化结果; False: 用初始几何

airfoil_dir  = "Re_360polar"


# ================================================================
# 2. 几何加载（优先使用优化结果）
# ================================================================
r = np.array([0.202, 0.350, 0.676, 0.967, 1.135,
              1.483, 1.664, 1.850, 2.036, 2.217,
              2.398, 2.565, 3.024, 3.498])

chord_init = np.array([0.2500, 0.2500, 0.6000, 0.5192, 0.4681,
                       0.3500, 0.3200, 0.2896, 0.2536, 0.2224,
                       0.1954, 0.1741, 0.1331, 0.1182])

twist_init = np.array([18.20, 18.20, 18.20, 10.38, 7.54,
                        4.29,  3.46,  2.97,  2.72, 2.60,
                        2.56,  2.56,  2.45,  1.68])

if USE_OPTIMIZED and os.path.exists("chord_optimization_results_AEP.npz"):
    chord = np.load("chord_optimization_results_AEP.npz")["chord_opt"]
    print("[info] 已加载优化弦长")
else:
    chord = chord_init.copy()

if USE_OPTIMIZED and os.path.exists("twist_optimization_results_AEP.npz"):
    twist = np.load("twist_optimization_results_AEP.npz")["twist_opt"]
    print("[info] 已加载优化扭角")
else:
    twist = twist_init.copy()


# ================================================================
# 3. 翼型加载（多 Re 极曲线 → CCAirfoil per section）
# ================================================================
def load_polar(path):
    aoa, cl, cd, cm = [], [], [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.upper() == "EOT":
                continue
            try:
                v = [float(x) for x in line.split()[:4]]
                if -180.0 <= v[0] <= 180.0:
                    aoa.append(v[0]); cl.append(v[1]); cd.append(v[2]); cm.append(v[3])
            except ValueError:
                continue
    return np.array(aoa), np.array(cl), np.array(cd), np.array(cm)


re_values = np.array([0.1e6, 0.5e6, 0.8e6, 1.0e6, 2.0e6])

family_files = {
    "DU":    [f"DU-06-W-200_Re{x}.dat" for x in ["0.100","0.500","0.800","1.000","2.000"]],
    "SG":    [f"SG6050_Re{x}.dat"      for x in ["0.100","0.500","0.800","1.000","2.000"]],
    "SD":    [f"SD7062_Re{x}.dat"      for x in ["0.100","0.500","0.800","1.000","2.000"]],
    "S1223": [f"S1223_Re{x}.dat"       for x in ["0.100","0.500","0.800","1.000","2.000"]],
}

# 截面 -> 翼型族（与优化脚本一致）
section_family = ["CYL","CYL",
                  "DU","DU","DU",
                  "SG","SG","SG",
                  "SD","SD","SD",
                  "S1223","S1223","S1223"]

# 公共 AOA 网格（用 S1223_Re2.000 作为基准，覆盖 ±180°）
aoa_base, _, _, _ = load_polar(os.path.join(airfoil_dir, "S1223_Re2.000.dat"))

family_polars = {}
for fam, files in family_files.items():
    cl2d = np.zeros((len(aoa_base), len(re_values)))
    cd2d = np.zeros_like(cl2d)
    cm2d = np.zeros_like(cl2d)
    for j, fn in enumerate(files):
        a, cl_, cd_, cm_ = load_polar(os.path.join(airfoil_dir, fn))
        cl2d[:, j] = np.interp(aoa_base, a, cl_)
        cd2d[:, j] = np.interp(aoa_base, a, cd_)
        cm2d[:, j] = np.interp(aoa_base, a, cm_)
    family_polars[fam] = (cl2d, cd2d, cm2d)

cyl_a, cyl_cl, cyl_cd, cyl_cm = load_polar(os.path.join(airfoil_dir, "Cylinder.dat"))
cyl_cl_b = np.interp(aoa_base, cyl_a, cyl_cl)
cyl_cd_b = np.interp(aoa_base, cyl_a, cyl_cd)
cyl_cm_b = np.interp(aoa_base, cyl_a, cyl_cm)

af_per_section = []
for i in range(len(r)):
    fam = section_family[i]
    if fam == "CYL":
        af_per_section.append(CCAirfoil(aoa_base, [], cyl_cl_b, cyl_cd_b, cm=cyl_cm_b))
    else:
        cl2d, cd2d, cm2d = family_polars[fam]
        af_per_section.append(CCAirfoil(aoa_base, re_values, cl2d, cd2d, cm=cm2d))


# ================================================================
# 4. 构建 CCBlade
# ================================================================
rotor = CCBlade(
    r, chord, twist, af_per_section, Rhub, Rtip,
    B=n_blades, rho=rho, mu=mu,
    precone=precone, tilt=tilt, yaw=yaw,
    shearExp=shearExp, hubHt=hub_height, nSector=4,
    tiploss=True, hubloss=True, wakerotation=True,
    derivatives=False,
)

A_disk = np.pi * Rtip ** 2


# ================================================================
# 5. Cp-λ 扫描
# ================================================================
print("\n=== [1] Cp-λ 扫描 (pitch=0°, V_ref=8 m/s) ===")
V_ref     = 8.0
TSR_grid  = np.arange(2.0, 14.01, 0.25)
Omega_TSR = TSR_grid * V_ref / Rtip * 60.0 / (2.0 * np.pi)   # RPM

V_arr  = np.full_like(TSR_grid, V_ref)
pitch0 = np.zeros_like(TSR_grid)
out, _ = rotor.evaluate(V_arr, Omega_TSR, pitch0, coefficients=True)

CP_l, CT_l, CQ_l = out["CP"], out["CT"], out["CQ"]
i_opt   = int(np.argmax(CP_l))
TSR_opt = float(TSR_grid[i_opt])
Cp_max  = float(CP_l[i_opt])
print(f"  TSR_opt = {TSR_opt:.2f}   Cp_max = {Cp_max:.4f}   "
      f"CT@opt = {CT_l[i_opt]:.4f}   (Betz = 0.593)")
print(f"  {'TSR':>5}  {'CP':>7}  {'CT':>7}  {'CQ':>7}  {'Ω(RPM)':>8}")
for k in range(0, len(TSR_grid), 4):
    mark = "  *" if k == i_opt else ""
    print(f"  {TSR_grid[k]:>5.2f}  {CP_l[k]:>7.4f}  {CT_l[k]:>7.4f}  "
          f"{CQ_l[k]:>7.4f}  {Omega_TSR[k]:>8.2f}{mark}")


# ================================================================
# 6. 功率曲线 - 自由运行（恒 TSR_opt, 无额定限制）
# ================================================================
print("\n=== [2] 自由运行功率曲线（恒 TSR_opt）===")
V_curve     = np.arange(3.0, 18.001, 0.5)
Omega_track = TSR_opt * V_curve / Rtip * 60.0 / (2.0 * np.pi)   # RPM (恒 TSR)
out1, _ = rotor.evaluate(V_curve, Omega_track, np.zeros_like(V_curve), coefficients=True)
P_free, T_free, Q_free   = out1["P"], out1["T"], out1["Q"]
CP_free, CT_free          = out1["CP"], out1["CT"]


# ================================================================
# 7. 额定点 / Ω_rated 求解
# ================================================================
above = np.where(P_free >= P_RATED)[0]
if len(above) > 0 and above[0] > 0:
    i_r       = above[0]
    V_rated   = float(np.interp(P_RATED, [P_free[i_r-1], P_free[i_r]],
                                          [V_curve[i_r-1], V_curve[i_r]]))
    Omega_rated = TSR_opt * V_rated / Rtip * 60.0 / (2.0 * np.pi)
    print(f"  V_rated ≈ {V_rated:.2f} m/s   Ω_rated ≈ {Omega_rated:.2f} RPM")
else:
    V_rated      = float(V_curve[-1])
    Omega_rated  = float(Omega_track[-1])
    print(f"  [警告] 切出风速内未达额定功率（max P = {P_free.max()/1e3:.2f} kW）")


# ================================================================
# 8. 失速调节模式（pitch=0, Ω 限速）
# ================================================================
print("\n=== [3] 失速调节功率曲线 ===")
Omega_stall = np.minimum(Omega_track, Omega_rated)
out2, _ = rotor.evaluate(V_curve, Omega_stall, np.zeros_like(V_curve), coefficients=True)
P_stall, T_stall = out2["P"], out2["T"]
CP_stall, CT_stall = out2["CP"], out2["CT"]


# ================================================================
# 9. 变桨调节模式（找 pitch 使 P = P_rated）
# ================================================================
print("\n=== [4] 变桨调节功率曲线 ===")
P_pitch     = np.zeros_like(V_curve)
T_pitch     = np.zeros_like(V_curve)
pitch_sched = np.zeros_like(V_curve)
Omega_pitch = np.minimum(Omega_track, Omega_rated)

for k, V in enumerate(V_curve):
    Omg = Omega_pitch[k]
    o0, _ = rotor.evaluate([V], [Omg], [0.0])
    if o0["P"][0] <= P_RATED:
        P_pitch[k]     = o0["P"][0]
        T_pitch[k]     = o0["T"][0]
        pitch_sched[k] = 0.0
    else:
        def f(p):
            o, _ = rotor.evaluate([V], [Omg], [p])
            return o["P"][0] - P_RATED
        # 上界处验证有解
        f_hi = f(PITCH_MAX)
        if f_hi > 0.0:
            p_sol = PITCH_MAX
        else:
            try:
                p_sol = brentq(f, 0.0, PITCH_MAX, xtol=0.05)
            except Exception:
                p_sol = PITCH_MAX
        os_, _ = rotor.evaluate([V], [Omg], [p_sol])
        P_pitch[k]     = os_["P"][0]
        T_pitch[k]     = os_["T"][0]
        pitch_sched[k] = p_sol


# ================================================================
# 10. AEP 计算（Weibull 时间加权 × 有效小时数）
# ================================================================
def weibull_pdf(V, k, c):
    return (k / c) * (V / c) ** (k - 1) * np.exp(-(V / c) ** k)

mask  = (V_curve >= V_in) & (V_curve <= V_out)
V_aep = V_curve[mask]
f_aep = weibull_pdf(V_aep, WEIBULL_K, WEIBULL_C)
dV    = V_aep[1] - V_aep[0]
hours = 8760.0 * EFF_FRAC

# 自由运行模式按 P_rated 截断（避免高估）
P_free_capped = np.minimum(P_free, P_RATED)

AEP_free  = np.sum(f_aep * P_free_capped[mask]) * dV * hours / 1000.0   # kWh
AEP_stall = np.sum(f_aep * P_stall[mask])       * dV * hours / 1000.0
AEP_pitch = np.sum(f_aep * P_pitch[mask])       * dV * hours / 1000.0

CF_stall  = AEP_stall / (P_RATED / 1000.0 * 8760.0)
CF_pitch  = AEP_pitch / (P_RATED / 1000.0 * 8760.0)

print("\n=== [5] AEP（年发电量, Jul+Sep 有效占比 45.6%）===")
print(f"  失速调节  : {AEP_stall:>9.0f} kWh   容量因子 {CF_stall*100:>5.2f}%")
print(f"  变桨调节  : {AEP_pitch:>9.0f} kWh   容量因子 {CF_pitch*100:>5.2f}%")
print(f"  自由(上界): {AEP_free:>9.0f} kWh")


# ================================================================
# 11. 功率曲线打印
# ================================================================
print("\n=== 功率曲线（kW）===")
print(f"  {'V':>5}  {'P_stall':>8}  {'P_pitch':>8}  {'T_stall':>8}  "
      f"{'pitch':>6}  {'Ω_pitch':>8}")
for k in range(0, len(V_curve), 2):
    print(f"  {V_curve[k]:>5.1f}  {P_stall[k]/1e3:>8.3f}  {P_pitch[k]/1e3:>8.3f}  "
          f"{T_stall[k]:>8.1f}  {pitch_sched[k]:>6.2f}  {Omega_pitch[k]:>8.2f}")


# ================================================================
# 12. 绘图（4 联）
# ================================================================
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

ax = axes[0, 0]
ax.plot(TSR_grid, CP_l, "b-o", ms=3, label=r"$C_P$")
ax.plot(TSR_grid, CT_l, "r-s", ms=3, label=r"$C_T$", alpha=0.6)
ax.axvline(TSR_opt, color="k", ls="--", alpha=0.5, label=fr"$\lambda_{{opt}}$={TSR_opt:.2f}")
ax.axhline(16.0/27.0, color="g", ls=":", alpha=0.5, label="Betz=0.593")
ax.set_xlabel(r"Tip Speed Ratio $\lambda$"); ax.set_ylabel("Coefficient")
ax.set_title(fr"$C_P,C_T$–$\lambda$ Curve  (V={V_ref} m/s, pitch=0°, $C_{{P,max}}$={Cp_max:.4f})")
ax.grid(alpha=0.3); ax.legend()

ax = axes[0, 1]
ax.plot(V_curve, P_free / 1e3, "b--", lw=1, alpha=0.5, label="Free (constant TSR)")
ax.plot(V_curve, P_stall / 1e3, "g-",  lw=2, label="Stall regulated")
ax.plot(V_curve, P_pitch / 1e3, "r-",  lw=2, label="Pitch regulated")
ax.axhline(P_RATED / 1e3, color="k", ls=":", label=f"Rated {P_RATED/1e3:.0f} kW")
ax.axvline(V_rated, color="gray", ls=":", alpha=0.5, label=fr"$V_{{rated}}$={V_rated:.1f} m/s")
ax.set_xlabel("Wind Speed V (m/s)"); ax.set_ylabel("Power P (kW)")
ax.set_title("Power Curve"); ax.grid(alpha=0.3); ax.legend()

ax = axes[1, 0]
ax.plot(V_curve, T_stall, "g-", lw=2, label="Stall")
ax.plot(V_curve, T_pitch, "r-", lw=2, label="Pitch")
ax.set_xlabel("Wind Speed V (m/s)"); ax.set_ylabel("Thrust T (N)")
ax.set_title("Thrust Curve"); ax.grid(alpha=0.3); ax.legend()

ax  = axes[1, 1]
ax2 = ax.twinx()
l1, = ax.plot(V_curve, Omega_stall,  "g-", lw=2, label=r"$\Omega$ stall")
l2, = ax.plot(V_curve, Omega_pitch,  "r--", lw=1, label=r"$\Omega$ pitch")
l3, = ax2.plot(V_curve, pitch_sched, "b-", lw=2, label="pitch")
ax.set_xlabel("Wind Speed V (m/s)"); ax.set_ylabel(r"Rotor Speed $\Omega$ (RPM)")
ax2.set_ylabel("Pitch Angle (deg)", color="b")
ax.set_title("Control Schedule")
ax.grid(alpha=0.3); ax.legend(handles=[l1, l2, l3], loc="center left")

plt.tight_layout()
plt.savefig("PowerCurve_s1223_V3.png", dpi=140)
print("\n[已保存] PowerCurve_s1223_V3.png")


# ================================================================
# 13. 数据存档
# ================================================================
np.savez(
    "PowerCurve_s1223_V3.npz",
    r=r, chord=chord, twist=twist,
    TSR_grid=TSR_grid, CP_lambda=CP_l, CT_lambda=CT_l, CQ_lambda=CQ_l,
    Omega_TSR_grid=Omega_TSR,
    TSR_opt=TSR_opt, Cp_max=Cp_max,
    V_curve=V_curve,
    P_free=P_free, P_stall=P_stall, P_pitch=P_pitch,
    T_free=T_free, T_stall=T_stall, T_pitch=T_pitch,
    pitch_sched=pitch_sched,
    Omega_track=Omega_track, Omega_stall=Omega_stall, Omega_pitch=Omega_pitch,
    V_rated=V_rated, Omega_rated=Omega_rated,
    AEP_stall_kWh=AEP_stall, AEP_pitch_kWh=AEP_pitch, AEP_free_kWh=AEP_free,
    CF_stall=CF_stall, CF_pitch=CF_pitch,
)
print("[已保存] PowerCurve_s1223_V3.npz")
