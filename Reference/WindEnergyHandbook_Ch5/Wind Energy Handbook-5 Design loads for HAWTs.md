# Design loads for HAWTs

# 5.1 National and international standards

# 5.1.1 Historical development

The preparation of national and international standards containing rules for the design of wind turbines began in the eighties. The rrst publication was a set of regulations for certircation drawn up by Germanischer Lloyd (GL) in 1986. These initial rules were subsequently considerably rerned as the state of knowledge grew, leading to the publication by GL of the Regulation for the CertiScation of Wind Energy Conversion Systems in 1993. Revised editions – latterly entitled Guideline for the CertiScation of Wind Turbines – were published in 1999, 2003, and 2010. Meanwhile national standards were published in The Netherlands (NEN 6096) and Denmark (DS 472) in 1988 and 1992, respectively.

The International Electrotechnical Commission (IEC) began work on the rrst international standard in 1988, leading to the publication of IEC 1400-1, Wind Turbine Generator Systems – Part 1: Safety Requirements in 1994. Second, third, and fourth editions, each containing some signircant changes and bearing the new number IEC 61400-1, appeared in 1999, 2005, and 2019, respectively. IEC-61400-1 has now superseded the national standards referred to previously.

Following the merger of DNV and GL in 2013 to form DNVGL, separate standards have been published for design loads (DNVGL-ST-0437 2016) and for the design of individual components (e.g. DNVGL-ST-0376 2015, Rotor Blades for Wind Turbines). The standard for design loads covers both onshore and offshore wind turbines.

The following sub-section describes the scope of the IEC 61400-1 requirements in outline.

Table 5.1 Wind speed parameters for wind turbine classes. 

<table><tr><td></td><td>Class I</td><td>Class II</td><td>Class III</td></tr><tr><td>Reference wind speed,  $U_{ref}$  (m/s)</td><td>50</td><td>42.5</td><td>37.5</td></tr><tr><td>Reference wind speed for cyclones,  $U_{refT}$  (m/s)</td><td>57</td><td>57</td><td>57</td></tr><tr><td>Annual average wind speed,  $U_{ave}$  (m/s)</td><td>10</td><td>8.5</td><td>7.5</td></tr><tr><td>50 year return gust speed,  $1.4U_{ref}$  (m/s)</td><td>70</td><td>59.5</td><td>52.5</td></tr><tr><td>1 year return gust speed,  $1.12U_{ref}$  (m/s)</td><td>56</td><td>47.6</td><td>42</td></tr></table>

# 5.1.2 IEC 61400-1

IEC 61400-1 Wind Turbines – Part 1: Design Requirements identires three different classes of wind turbines to suit differing site wind conditions, with increasing class designation number corresponding to reducing average and extreme wind speeds. The wind speed parameters for each class are given in Table 5.1, where the reference wind speed is derned as the 10 minute mean wind speed at hub height with a 50 year return period. For some (but not all) areas subject to tropical cyclones. a higher reference wind speed, $U _ { r e f T } ,$ of 57 m/s is specired.

Rigorous procedures are laid down for demonstrating that the wind conditions at a particular wind turbine site conform to those of the designated wind turbine class. To allow for sites where conditions do not conform to any of these classes, a fourth class (Class S) is provided, in which the basic wind speed parameters are to be specired by the manufacturer.

The standard identires a total of 23 different load cases (18 ultimate, 5 fatigue), which, as a minimum, require consideration in the design of the turbine. Each load case is derned in terms of a different combination of wind conditions and machine state – for example, extreme wind shear (EWS) during power production. The standard does not extend to the prescription of particular methods of loading analysis.

Subsequent sections cover requirements for the control and protection systems, the various mechanical systems, the electrical system, installation, commissioning, operation, and maintenance. A rnal section details the requirements for turbines operating at temperatures below $- 2 0 ^ { \circ } \mathrm { C }$ or where there is a risk of icing.

# 5.2 Basis for design loads

# 5.2.1 Sources of loading

The sources of loading to be taken into account may be categorised as follows:

• Aerodynamic loads.   
• Gravitational loads.   
• Inertia loads (including centrifugal and gyroscopic effects).   
• Operational loads arising from actions of the control system (e.g. braking, yawing, blade pitch control, generator disconnection).

# 5.2.2 Ultimate loads

The load cases selected for ultimate load design must cover realistic combinations of a wide range of external wind conditions and machine states. It is common practice to distinguish between normal and extreme wind conditions on the one hand, and between normal machine states and fault states on the other. The load cases for design are then chosen from:

• Normal wind conditions in combination with normal machine states.   
• Extreme wind conditions in combination with normal machine states.   
• Machine fault states in combination with appropriate wind conditions.

Extreme wind conditions are generally derned in terms of the worst condition occurring with a 50 year return period. It is assumed that machine fault states arise infrequently and are uncorrelated with extreme wind conditions, so that the occurrence of a machine fault in combination with the 50 year return wind condition is an event with such a high return period that it need not be considered as a load case. However, IEC 61400-1 wisely stipulates that if there is some correlation between an extreme external condition and a fault state, then the combination should be considered as a design case.

# 5.2.3 Fatigue loads

A typical wind turbine is subjected to a severe fatigue loading regime. The rotor of a 2 MW machine will rotate some 108 times during a 20 year life, with each revolution causing a complete gravity stress reversal in the low-speed shaft and in each blade, together with a cycle of blade out-of-plane loading due to the combined effects of wind shear, yaw error, shaft tilt, tower shadow, and turbulence. It is therefore scarcely surprising that the design of many wind turbine components is often governed by fatigue rather than by ultimate load.

The design fatigue load spectrum should be representative of the loading cycles experienced during power production over the full operational wind speed range, with the numbers of cycles weighted in accordance with the proportion of time spent generating at each wind speed. For completeness, load cycles occurring at start-up and shut-down, and, if necessary, during shut-down, should also be included.

It is generally assumed that the extreme load cases occur so rarely that they will not have a signircant effect on fatigue life.

# 5.2.4 Partial safety factors

# Partial safety factors for loads

Limit state design requires characteristic loads to be multiplied by appropriate partial safety factors when calculating the design loads. Although traditionally, different partial safety factor values have been assigned to different kinds of load in static analyses, IEC 61400-1 edition 3 specires a single partial safety factor for aerodynamic, operational, gravity, and inertia loads for each class of load case. This avoids the pitfalls inherent in any attempt to formulate equations of motions for a dynamic analysis in which different terms have been distorted relative to one another by the application of different load factors.

Table 5.2 Partial safety factors for loads, IEC 61400-1 edition 4. 

<table><tr><td colspan="2">Unfavourable loads</td><td>Favourable loads</td></tr><tr><td colspan="2">Class of design load case</td><td></td></tr><tr><td>Normal</td><td>Abnormal</td><td></td></tr><tr><td>1.35*</td><td>1.1</td><td>0.9</td></tr></table>

a Exceptionally, the partial factor for design load case 1.1 (see Section 5.4.1) is set at 1.25, because, in this case, the loads are determined using statistical load extrapolation, and factors less than 1.35 apply for the fault design load cases 2.1 and 2.5.

Ultimate load cases are divided into three classes, normal, abnormal, and transport/erection, with a different partial safety factor for each, as set out in Table 5.2. Most load cases are assigned to the normal class, with the abnormal class reserved for the more unlikely fault conditions. The partial factor for fatigue loads is unity.

# Partial safety factors for the consequences of failure

In addition to the partial safety factors for loads and materials intrinsic to limit state design, IEC 61400-1 also specires the use of a partial safety factor for the consequences of failure, which varies according to the nature of the component under consideration. Three classes of component are identired, as follows:

• Component class 1 – used for ‘fail-safe’ structural components whose failure does not result in the failure of a major part of a wind turbine.   
• Component class 2 – used for ‘non fail-safe’ structural components whose failure may lead to the failure of a major part of a wind turbine.   
• Component class 3 – used for ‘non fail-safe’ mechanical components that link non-redundant actuators and brakes required for turbine protection to main structural components.

Recommended minimum values for the partial safety factor for the consequences of failure are given in Table 5.3.

Table 5.3 Partial safety factors for the consequences of failure, IEC 61400-1 edition 4. 

<table><tr><td>Type of strength assessment</td><td>Ultimate strength</td><td>Fatigue strength</td></tr><tr><td>Component class 1</td><td>0.9</td><td>0.9</td></tr><tr><td>Component class 2</td><td>1.0</td><td>1.0</td></tr><tr><td>Component class 3</td><td>1.2</td><td>1.2</td></tr></table>

IEC 61400-1 requires the partial safety factor for the consequences of failure to be introduced at the stage of assessing component design strength, but as it could equally well have been applied in the derivation of the design load, it is instructive to introduce the concept here.

# 5.2.5 Functions of the control and safety systems

A primary function of the control system is to maintain the machine operating parameters within their normal limits. The purpose of the safety system (referred to as ‘protection system’ in IEC 61400-1 editions 1–3) is to ensure that, should a critical operating parameter exceed its normal limit as a result of a fault or failure in the wind turbine or the control system, the machine is maintained in a safe condition. Normally the critical operating parameters are:

• Turbine rotational speed.   
• Power output.   
• Vibration level.   
• Twist of pendant cables running up into nacelle.

For each parameter it is necessary to set an activation level at which the safety system is triggered. This has to be set at a suitable margin above the normal operating limit to allow for overshooting by the control system but sufrciently far below the maximum safe value of the parameter to allow scope for the safety system to rein it in. The rotor speed at which the safety system is activated is a key input to the design load case involving rotor overspeed.

IEC 61400-1 edition 4 allows a separate safety system (termed secondary layer protection) to be dispensed with if it can be demonstrated that the actions of the control system are inherently safe.

# 5.3 Turbulence and wakes

Fluctuation of the wind speed about the short-term mean, or turbulence, naturally has a major impact on the design loadings, as it is the source of both the extreme gust loading and a large part of the blade fatigue loading. The latter is exacerbated by the gust slicing effect, in which a blade will slice through a localised gust repeatedly in the course of several revolutions.

The nature of free-stream turbulence and its mathematical description in statistical terms form the subject of section 2.6. IEC 61400-1 edition 4 addresses the variation in turbulence intensity from site to site arising from different terrain types by derning four turbulence categories, according to the expected value, $I _ { r e f } ,$ of the hub-height turbulence intensity at a reference mean wind speed, ${ \overline { { U } } } ,$ of 15 m/s. These are categories A+, A, B, and C for $I _ { r e f }$ values of 0.18, 0.16, 0.14, and 0.12, respectively.

Measurements have shown (see, for example, Risø paper R-1111 1999 by Larsen et al.) that there is signircant variability in turbulence intensity at a particular site, even at a particular mean wind speed. Accordingly, IEC 61400-1 edition 4 specires that the design value is to be taken as the 90% quantile (i.e. the value with a 10% exceedance probability), derned as

$$
I _ {u} = \sigma_ {u} / \overline {{{U}}} = I _ {r e f} (0. 7 5 + 5. 6 / \overline {{{U}}}) \tag {5.1}
$$

where $\sigma _ { u }$ is the standard deviation of the turbulent wind speed suctuations, $\overline { { U } }$ is the hub-height mean wind speed, and $I _ { r e f }$ is derned above. This relationship results in reducing turbulence intensity with increasing wind speed, as illustrated in Figure 5.1, and is termed the normal turbulence model (NTM). Note that $\sigma _ { u }$ does not vary with height, so $I _ { u }$ reduces with increasing height, because of wind shear.

There is also a requirement to consider the maximum turbulence expected to occur, in load case 1.3 – see Section 5.4.1. This is derned by the extreme turbulence model (ETM), in which the turbulence intensity is given by

$$
I _ {u} = \sigma_ {u} / \overline {{U}} = I _ {r e f} (0. 0 3 6 (U _ {a v e} + 6) (1 - 8 / \overline {{U}}) + 2 0 / \overline {{U}}) \tag {5.2}
$$

This relationship is shown by the dashed line on Figure 5.1.

For any particular candidate wind farm site, ambient turbulence levels have to be determined from site wind speed measurements and used to derive an estimate of the augmented turbulence levels including wake effects at each turbine location – e.g. using the method suggested in IEC 61400-1 edition 4 annex E. An appropriate design turbulence category (A+, A, B, or C) may then be identired by showing that the 90% quantile of the estimated turbulence intensity including wake effects is less than the 90% quantile value given by Eq. (5.1) for that category, for all wind speeds between the annual average wind speed, $U _ { a v e } ,$ and $2 U _ { a v e }$ .

![](images/afcf573c927e34c39fc48944e64f4d11a08f552c0d7be52ebc4be6a0a099dbbc.jpg)

<details>
<summary>line</summary>

| Hub-height mean wind speed m/s | Cat B - I_ref = 0.14; Class I | A+ : I_ref = 0.18 | A : I_ref = 0.16 | B : I_ref = 0.14 | C : I_ref = 0.12 | Normal turbulence model |
| ------------------------------ | ----------------------------- | ----------------- | ---------------- | ---------------- | ---------------- | ----------------------- |
| 5                              | 0.62                          | 0.38              | 0.35             | 0.32             | 0.29             | 0.25                    |
| 10                             | 0.45                          | 0.28              | 0.26             | 0.24             | 0.22             | 0.18                    |
| 15                             | 0.30                          | 0.22              | 0.20             | 0.19             | 0.18             | 0.15                    |
| 20                             | 0.20                          | 0.18              | 0.17             | 0.16             | 0.15             | 0.13                    |
| 25                             | 0.15                          | 0.16              | 0.15             | 0.14             | 0.13             | 0.12                    |
</details>

Figure 5.1 Variation of turbulence intensity with wind speed for the normal and extreme turbulence models.

Computer simulation of the turbulent wind reld also requires the dernition of the power spectra of the suctuations of the three orthogonal velocity components and their spatial correlation, which comprise the turbulence model. Edition 2 of the standard details two spectra – those due to von Karman (1948) and Kaimal (1972) – and their corresponding coherence functions (see Sections 2.6.4 and 2.6.7). However, the von Karman spectrum is omitted from editions 3 and 4 and replaced by the Mann (1994) uniform shear turbulence model (see Section 2.6.8).

Some recent simulations of turbulent sow past wind turbines have instead modelled the whole sow reld using large eddy simulation and this (computationally very expensive but higher rdelity approach) is starting to be given more consideration; see Section 4.7.8.

# 5.4 Extreme loads

# 5.4.1 Operational load cases

A variety of load cases have to be investigated in this category, so that the effects of extremes of gust loading, wind direction change, and wind shear – with or without faults – can be evaluated in turn. The IEC 61400-1 load cases can be divided into two distinct types, depending on whether the wind reld is specired in deterministic or stochastic terms. In the deterministic load cases, simple mathematical expressions are used to derne the wind speed variation over time, direction changes, and wind shears. In the stochastic load cases the statistical properties of the wind are derned and the cases have to be analysed using a minimum of six 10 minute time domain simulations of the wind reld incident on the rotor.

The deterministic load cases have the merit of simplicity but are open to the criticism that they fail to model the behaviour of the real wind accurately. Accordingly, the number of load cases derned by deterministic discrete gusts or sudden direction changes has been reduced in IEC 61400-1 editions 3 and 4 compared with earlier editions, in favour of greater reliance on cases requiring simulation of the turbulent wind reld. In the longer term it may be possible to eliminate more deterministic load cases in favour of stochastic ones, by constraining the turbulent wind simulations to model a particular gust prorle – see Section 5.4.4.

IEC 61400-1 edition 3 requires account to be taken of the following in all operational load cases:

• Wind shear according to the power law $U ( z ) \propto z ^ { 0 . 2 }$ , which is termed the normal wind proSle (NWP) model.   
• Tower shadow (described in Section 5.7.2).   
• Inclination of the mean air sow of up to $8 ^ { \circ }$ with respect to the horizontal plane.   
• Rotor aerodynamic imbalance (e.g. due to blade pitch and twist deviations) and rotor mass imbalance.   
• Yaw tracking errors.

Air density is to be taken as 1.225 kg/m3.

The individual ultimate load cases derned in edition 4 of IEC 61400-1 are described below in turn. Note that, except where indicated otherwise, the full range of mean wind speeds between cut-in and cut-out are to be investigated in each case. (The annotated acronyms in capitals are those used by the code to identify the different wind conditions.)

# Power production load cases – normal machine state

Load case 1.1: Operation in turbulent wind reld derned by the normal turbulence model (NTM) – see Section 5.3. Wind speeds between cut-in wind speed, $U _ { i } ,$ , and cut-out wind speed, $U _ { \mathrm { o } }$ , to be investigated. For this load case and others where a range of wind speeds are to be investigated, wind speed steps of 2 m/s are considered sufrcient, except close to rated wind speed. (The rated wind speed is derned as the uniform, steady wind speed at which the turbine’s rated power is reached.) Normal partial load factor (exceptionally 1.25).

A minimum of 15 10 minute simulations are required for each wind speed between 2 m/s below the rated wind speed, $U _ { \mathrm { r } }$ , and the cut-out wind speed. The characteristic load – i.e. that having a 50 year recurrence period – in each element of the structure is to be determined by statistical extrapolation of the extreme value distribution – see Section 5.14. Alternatively, as a simplircation, it is permitted to take the characteristic load as 1.2 times the 99% percentile of the 10 minute extremes determined for each wind speed or 1.35 times the 93.3% percentile.

[Load case 1.2 is a fatigue load case.]

Load case 1.3: Operation in turbulent wind reld derned by the extreme turbulence model (ETM). Wind speeds between cut-in wind speed and cut-out wind speed, $U _ { \mathrm { o } }$ , to be investigated. Normal partial load factor. As this load case is intended to capture the extreme loading arising from the maximum anticipated turbulence intensity, no extrapolation is required.

Load case 1.4: Extreme coherent gust with direction change (ECD). Hub-height wind speed equal to the rated wind speed, $U _ { \mathrm { r } } ,$ , ±2 m/s plus a 15 m/s rising gust, in conjunction with a simultaneous wind direction change of $7 2 0 ^ { \circ } / U _ { r } - \mathrm { i . e . } 6 0 ^ { \circ }$ for a rated wind speed of 12 m/s, for example. The gust rise time and the period over which the direction change takes place are both specired as 10 seconds. Normal partial load factor.

Load case 1.5: Extreme wind shear (EWS). Additional vertical or horizontal transient wind shear superimposed on the normal wind prorle (NWP) model. Normal partial load factor. The additional wind shears are specired as

$$
\left(\frac {z - z _ {\text { hub }}}{D}\right) \left(2. 5 + 0. 2 \beta \sigma_ {u} \left(\frac {D}{\Lambda_ {1}}\right) ^ {0. 2 5}\right) \left(1 - \cos \left(\frac {2 \pi t}{T}\right)\right) \mathrm{m/sfor} 0 <   \mathrm{t< T}, \text { for   vertical   shear } \tag {5.3a}
$$

$$
\left(\frac {y}{D}\right) \left(2. 5 + 0. 2 \beta \sigma_ {u} \left(\frac {D}{\Lambda_ {1}}\right) ^ {0. 2 5}\right) \left(1 - \cos \left(\frac {2 \pi t}{T}\right)\right) \mathrm{m/sfor} 0 <   \mathrm{t< T}, \text { for   horizontal   shear } \tag {5.3b}
$$

where

z is the height above ground

y is the lateral coordinate with respect to the hub

D is the rotor diameter

$$
\beta = 6. 4
$$

$\sigma _ { u }$ is as derned in Eq. (5.1)

$\Lambda _ { 1 }$ is the longitudinal turbulence scale parameter of $0 . 7 \mathrm { z } _ { \mathrm { h u b } }$ , or 42 m, whichever is the lesser, and

T is the duration of the transient wind shear, set at 12 seconds

The two shears are to be applied independently as separate cases, not simultaneously. In the case of a 60 m hub height, 80 m diameter machine operating in a 25 m/s wind speed, the resulting maximum additional wind speed at the tip of a blade is 8.36 m/s, assuming category A turbulence.

# Fault occurrence during power production

This group of load cases covers faults both internal and external to the machine, including grid loss. If the connection to the grid is lost, then the aerodynamic torque will no longer meet with any resistance from the generator – which therefore experiences ‘loss of load’ – and so the rotor will begin to accelerate until the braking systems are brought into action. Depending on the speed of braking response, grid loss may well result in critical rotor loadings. The fault cases are as follows:

Load case 2.1: Operation in turbulent wind reld derned by the normal turbulence model (NTM), together with ‘normal’ control system fault or loss of the electrical network. A ‘normal’ control system fault is derned as one having a return period of 50 years or less. Normal partial load factor (except that, for a ‘normal’ control system fault return period between 10 and 50 years, the factor tapers down to 1.1).

Twelve 10 minute simulations are to be carried out, with the characteristic load derned as the mean of the six largest 10 minute extremes.

Load case 2.2: Operation in turbulent wind reld derned by the NTM, together with abnormal control system fault or protection system fault. Faults jeopardising protection against overspeed, generator overload, blade pitch runaway, uncontrolled yawing, and excessive vibration are to be considered. These faults are considered to be rare events, so the abnormal partial load factor is applied. The characteristic load is to be calculated as for load case 2.1.

Load case 2.3: Extreme operating gust (EOG), superimposed on hub-height wind speed of $U _ { r } \pm 2 \mathrm { m / s }$ or the cut-out wind speed, $U _ { o } ,$ , in conjunction with external or internal electrical system fault, including loss of electrical network. The wind speed variation is derned as

$$
U (z, t) = \overline {{{U}}} (z) - \frac {1 . 2 2 1 \sigma_ {u}}{1 + 0 . 1 (D / \Lambda_ {1})} \sin (3 \pi t / T) [ 1 - \cos (2 \pi t / T) ] \tag {5.4}
$$

![](images/bc2739628eccf0bdf871980848ca1f2e08f33eb485316fee4720aacb77acfa36.jpg)

<details>
<summary>line</summary>

| Time (s) | Hub-height wind speed (m/s) |
| -------- | -------------------------- |
| 0        | 25                         |
| 2        | 22                         |
| 4        | 28                         |
| 6        | 33                         |
| 8        | 22                         |
| 10       | 25                         |
| 12       | 25                         |
</details>

Figure 5.2 IEC 61400-1 extreme rising and falling gust with 50 year return period for steady wind speed of 25 m/s and category A turbulence.

where t is the time elapsed since the onset of the gust and T is the gust duration, specired at 10.5 seconds. Although termed an EOG, the gust magnitude is only about 70% of the 1 year return EOG derned in IEC 61400-1 edition 2, so the return period of the current EOG is likely to be only a few days. The gust prorle, which incorporates a dip in the wind speed both before and after the main gust, is illustrated in Figure 5.2 for a hub-height wind speed of 25 m/s, Class A turbulence, a turbine diameter of 80 m, and a turbulence length scale of 42 m. The combination of the gust and the electrical system fault is considered to be a rare event, so the abnormal partial load factor is to be applied.

[Load case 2.4 is a fatigue load case.]

Load case 2.5: Operation in steady wind derned by NWP model together with a low voltage ride through (LVRT) event (see Section 11.5.4). The voltage drop and its duration are normally specired by the grid operator. LVRT is considered as normal, but a reduced partial load factor of 1.2 is specired.

# Start-up load cases

[Load case 3.1 is a fatigue load case.]

Load case 3.2: Extreme operating gust (EOG) (as derned for load case 2.3, above) during start-up, superimposed on hub-height wind speed of $U _ { i } , U _ { r } \pm 2$ m/s or $U _ { \mathrm { o } }$ . Normal partial load factor.

The magnitude of the gust has been chosen so that its recurrence period in conjunction with a start-up or shut-down is one in 50 years.

Load case 3.3: Extreme direction change (EDC) during start-up, for steady hub-height wind speed of $U _ { i } , U _ { r } \pm 2 \mathrm { m / s }$ or $U _ { o }$ . The direction change, $\theta _ { e } ,$ is derned as

$$
\theta_ {e} = \pm 4 \arctan \left(\frac {\sigma_ {u}}{U _ {h u b} [ 1 + 0 . 1 (D / \Lambda_ {1}) ]}\right) \tag {5.5a}
$$

with the direction varying over time according to the relation:

$$
\theta (t) = 0. 5 \theta_ {e} \{1 - \cos (\pi t / T) \} \text {   for   } 0 <   t <   T \tag {5.5b}
$$

The direction change takes place over a period T of 6 seconds. Normal partial load factor.

For a hub-height wind speed of 12 m/s, Class A turbulence, a turbine diameter of 80 m, and a turbulence length scale of 42 m, the direction change is $3 7 ^ { \circ }$ , with a lower value applying at the cut-out wind speed because of the reduced turbulence intensity.

# Shut-down load cases

[Load case 4.1 is a fatigue load case.]

Load case 4.2: Extreme operating gust (EOG) (as derned for load case 2.3, above) during shut-down, superimposed on hub-height wind speed of $U _ { r } \pm 2 \mathrm { m / s }$ or $U _ { o } .$ . Normal partial load factor.

Load case 5.1: Emergency shut-down during operation in turbulent wind reld derned by the NTM, for steady hub-height wind speed of $U _ { r } \pm 2$ m/s or $U _ { o }$ . Normal partial load factor. The characteristic load is to be calculated as for load case 2.1.

# 5.4.2 Non-operational load cases

# Normal machine state

When non-operational, a turbine is either stationary, i.e. ‘parked’, or idling. In this condition it is exposed to the full range of wind speeds and is therefore required to survive the extreme wind conditions derned for the applicable wind class. IEC 61400-1 permits these wind conditions to be described in terms of either a steady wind speed corresponding to the 3 second gust with a 50 year return period or a turbulent wind with a 10 minute mean equal to the 50 year return value (the ‘reference wind speed’) and a rxed turbulence intensity of 0.11. The 50 year return gust value is derned as 1.4 times the 50 year return 10 minute mean. Both gust and 10 minute mean are specired at hub height and are to be used in conjunction with a reduced wind shear exponent of 0.11.

The magnitude of the 50 year return gust depends on the gust duration chosen, which in turn should be based on the size of the loaded area. For example, CP3: chapter V, part 2 of the UK Code of Basic Data for the Design of Buildings: Wind Loading states that a 3 second gust can envelope areas up to 20 m but advises that for larger areas up to 50 m across, a 5 second gust is appropriate. However, IEC 61400-1 and the GL rules (Germanischer Lloyd 2010) specify the use of gust durations of 3 seconds regardless of the turbine size.

Recognising that the turbulent wind speed suctuations are likely to excite blade and tower natural frequencies, IEC 61400-1 requires turbine dynamic response to be accounted for, whether using the deterministic or turbulent extreme wind models.

It is worth noting that Eurocode 1, Part 1-4 (EN 1991-1-4:2005) bases extreme loads on the dynamic pressure resulting from the extreme 10 minute mean wind speed rather than a 3 second gust. The loads resulting from the extreme 10 minute mean wind speed are augmented by a factor that takes into account both wind gusting and the excitation of resonant oscillations thereby.

The IEC 61400-1 non-operational load cases in the absence of faults or grid loss cater for varying yaw misalignments and may be summarised as follows:

Load case 6.1: Extreme wind with 50 year return period $\mathrm { ( E W M _ { 5 0 } ) }$ . Yaw misalignment up $\mathrm { t o } \pm 1 5 ^ { \circ }$ using the steady wind model, or up $\tan \pm 8 ^ { \circ }$ using the turbulence model, provided resistance against yaw slippage can be guaranteed. Normal partial safety factor.

Load case 6.3: Extreme wind with one year return period $( \mathrm { E W M } _ { 1 } )$ and extreme yaw misalignment of up to $\pm 3 0 ^ { \circ }$ using the steady wind model, or up to $\pm 2 0 ^ { \circ }$ using the turbulence model. The extreme wind speed with a return period of 1 year is to be taken as 80% of the 50 year return value. Normal partial safety factor.

Loss of grid connection can prevent the yaw system tracking any subsequent changes in wind direction, unless back-up is provided for the operation of the yaw system. Accordingly, IEC 61400-1 specires loss of grid connection as a separate load case, which is summarised below. The use of the abnormal safety factor indicates that the combination of extreme wind and grid loss is considered rare.

Load case 6.2: $\mathrm { E W M } _ { 5 0 }$ and loss of grid connection. Yaw misalignment due to wind direction change up $\mathrm { t o } \pm 1 8 0 ^ { \circ }$ unless back-up power for yawing provided. Abnormal partial safety factor.

The consequences of yaw slippage should be investigated in all non-operational load cases, if this is a possibility.

[Load case 6.4 is a fatigue load case.]

# Machine fault state

Examples of faults in this category are ones involving the failure of the yaw or pitch mechanisms. On the assumption that there is no correlation between such a failure and extreme winds, the design wind condition for this load case is normally taken as the extreme wind condition with a return period of 1 year. The load case in this category is summarised below.

Load case $7 . I \colon \mathrm { E W M } _ { 1 }$ and machine fault. Yaw misalignment up to $\pm 1 8 0 ^ { \circ }$ in case of yaw system fault. Abnormal partial safety factor.

# 5.4.3 Blade/tower clearance

In addition to checking the acceptability of stresses arising from the above load cases, the designer is also required to check that none can result in a collision between the blade and the tower, even after multiplying the blade tip desection by the appropriate partial load factor and the partial safety factor for elasticity of the blade material. For load case 1.1, the characteristic blade tip desection is to be determined by extrapolation in the same manner as the characteristic load.

# 5.4.4 Constrained stochastic simulation of wind gusts

Although time-domain simulations of the turbulent wind reld are able to accurately model the behaviour of the wind, very long simulations indeed are required if the extreme events required for design purposes are to be encountered by chance. Rather than select the desired extreme event from an extremely long wind speed time series, it is clearly desirable to ‘precipitate’ the desired event by constraining the time series in such a way that the statistical properties of the time series are unaffected.

![](images/e97df342a0ee0081b97d9a3ba56ddc9a078fce9ef599e6720311906c6851f0ee.jpg)

<details>
<summary>line</summary>

| Time (secs) | Wind speed (m/sec) |
|-------------|---------------------|
| 30          | ~25                 |
| 35          | ~25                 |
| 40          | ~25                 |
| 45          | ~25                 |
| 50          | ~25                 |
| 55          | ~44.5               |
| 60          | ~25                 |
| 65          | ~25                 |
| 70          | ~25                 |
| 75          | ~25                 |
| 80          | ~25                 |
</details>

Figure 5.3 Simulated wind speed time series constrained to give a 44.5 m/s peak wind speed.

A method of constraining gusts in wind simulations has been set out by Bierbooms (2005). In its simplest form, it consists in superposing a gust prorle having the form of the wind speed auto-correlation function on a local maximum of the simulated wind time series. This is illustrated in Figure 5.3.

In this example, the gust magnitude of 19.5 m/s approximates to the 50 year return value for a Class 1A site, based on exposure to a 24–26 m/s wind speed for about 4 hours per annum. [The peak factor of 5 is calculated using Eq. (A5.42) in Appendix A5, taking $\nu = 0 . 2 5 \mathrm { H z } . ]$ The wind speed auto-correlation function, derived from the power spectrum, is multiplied by the desired peak wind speed increment and added to the initial simulated wind speed time series, with the peak of the auto-correlation function centred on the selected maximum of the initial time series.

There is no need for the timing of the peak of the constrained gust to coincide with a maximum of the initial time series. In the general case, the time series of the constrained gust, $u _ { \mathrm { c } } ( t )$ , can be obtained from the initial time series, u(t) as follows:

$$
u _ {c} (t) = u (t) + \kappa (t - t _ {0}) (A - u (t _ {0})) - \frac {\dot {\kappa} (t - t _ {0})}{\ddot {\kappa} (0)} \dot {u} (t _ {0}) \tag {5.6}
$$

where $k ( t - t _ { 0 } )$ is the wind speed auto-correlation function and A the desired peak wind speed at time $t = t _ { 0 }$ .

The method can also be extended to gusts constrained to rise by a prescribed amount within a certain time (Bierbooms 2005). Such gusts are important in relation to the design of pitch-controlled machines.

Although constrained stochastic stimulation appears to be a promising method of modelling extreme events, it is not, as yet, recognised by design standards.

# 5.5 Fatigue loading

# 5.5.1 Synthesis of fatigue load spectrum

The complete fatigue load spectrum for a particular wind turbine component has to be built up from separate load spectra derived for turbine operation at different wind speeds and from the load cycles experienced at start-up and normal shut-down and while the machine is parked or idling. Firstly, the cycle counts for each stress range for 1 hour’s operation in a particular wind speed band are calculated and scaled up by the predicted number of hours of operation in that band over the machine lifetime. This prediction can be based on the Weibull distribution (Section 2.4), with the annual mean wind speed set according to the turbine class (see Section 5.1.2). Finally, the lifetime cycle counts obtained for operation in the different wind speed bands are combined and added to those calculated for start-ups, shut-downs, and periods of non-operation.

# 5.6 Stationary blade loading

# 5.6.1 Lift and drag coefJcients

Maximum blade loadings are in the out-of-plane direction and occur when the wind direction is either approximately normal to the blade, giving maximum drag, or at an angle of between $1 2 ^ { \circ }$ and $1 6 ^ { \circ }$ to the plane of the blade when the angle of attack is such as to give maximum lift.

In the absence of data on drag coefrcients for air sow normal to the blade, designers formerly utilised the drag coefrcient for an inrnitely long sat plate of 2.0, with an adjustment downwards based on the aspect ratio. Thus, on a typical blade with a mean chord equal to 1/15th of the radius, the length to width ratio would be taken as 30, because free sow cannot take place around the inboard end of the blade. Following EN 1991-1-4:2005, Eurocode 1: Actions on Structures – Part 1-4: General Actions – Wind Actions, this would give a drag coefrcient of 1.64. However, reld measurements have shown that such an approach is unduly conservative, with drag coefrcients of 1.24 being reported for the LM 17.2 m blade (Rasmussen 1984) and 1.25 for the Howden HWP-300 blade (Jamieson and Hunter 1985). The 1992 edition of Danish Standard DS 472, Loads and Safety of Wind Turbine Construction, stipulated a minimum value of 1.3 for the drag coefrcient.

The choice of lift coefrcient value is more straightforward, because aerofoil data for low angles of attack is more generally available and is, in any case, required for assessing rotor performance. The maximum lift coefrcient rarely exceeds 1.6, but values down to as low as 1.1 will obtain on the thicker, inboard portion of the blade. The minimum value of lift coefrcient of 1.5 specired in the 1992 edition of DS 472 for the calculation of blade out-of-plane loads is therefore probably conservative.

# 5.6.2 Critical conJguration for different machine types

It was shown in the preceding section that the maximum lift coefrcient is likely to exceed the maximum drag coefrcient for a wind turbine blade, so consequently the maximum loading on a stationary blade will occur when the air sow is in a plane perpendicular to the blade axis and the angle of attack is such as to produce maximum lift. For a stall-regulated machine, this will be the case when the blade is vertical and the wind direction is $7 5 ^ { \circ } - 8 0 ^ { \circ }$ to the nacelle axis. In the case of a pitch-regulated machine, with the blade chords oriented perpendicular to the plane of the rotor (i.e. at full feather) at shut-down, the blade only needs to be approximately vertical with a wind direction at $1 0 ^ { \circ } - 2 0 ^ { \circ }$ to the nacelle axis to attract maximum load.

# 5.6.3 Dynamic response

# Tip displacement

Wind suctuations at frequencies close to the rrst sapwise mode blade natural frequency excite resonant blade oscillations and result in additional, inertial loadings over and above the quasi-static loads that would be experienced by a completely rigid blade. As the oscillations result from suctuations of the wind speed about the mean value, the standard deviation of resonant tip displacement can be expressed in terms of the wind turbulence intensity and the normalised power spectral density at the resonant frequency, ${ \cal R } _ { u } \left( n _ { l } \right)$ $= n . S _ { u } ( n _ { 1 } ) / \sigma _ { u } ^ { 2 }$ , as follows:

$$
\frac {\sigma_ {x 1}}{\overline {{{x}}} _ {1}} = 2 \frac {\sigma_ {u}}{\overline {{{U}}}} \frac {\pi}{\sqrt {2 \delta}} \sqrt {R _ {u} (n _ {1})} \sqrt {K _ {S x} (n _ {1})} \tag {5.7}
$$

Here $\overline { { x } } _ { 1 }$ is the rrst mode component of the steady tip displacement, $\overline { { U } }$ is the mean wind speed (usually averaged over 10 minutes), 훿 is the logarithmic decrement of damping, and $K _ { S x } ( n _ { 1 } ) \ –$ is a size reduction factor, which results from the lack of correlation of the wind along the blade at the relevant frequency. Note that the dynamic pressure, $\begin{array} { r } { \frac { 1 } { 2 } \rho U ^ { 2 } = } \end{array}$ $\begin{array} { r } { \frac { 1 } { \gamma } \rho ( \overline { { U } } + u ) ^ { 2 } = \frac { 1 } { \gamma } \rho ( \overline { { U } } ^ { 2 } + 2 \overline { { U } } u + u ^ { 2 } ) } \end{array}$ , is linearised to ${ \scriptstyle { \frac { 1 } { 2 } } } \rho { \overline { { U } } } ( { \overline { { U } } } + 2 u )$ to simplify the result. See Appendix A5.2-4 for the derivations of Eq. (5.7) and the expression for $K _ { S x } ( n _ { 1 } )$ .

# Damping

It is evident from Eq. (5.7) that a key determinant of resonant tip response is the level of damping present. Generally, the damping consists of two components, aerodynamic and structural. In the case of a vibrating blade sat on to the wind, the aerodynamic force per unit length is given by ${ \scriptstyle \frac { 1 } { \gamma } } \rho ( \overline { { U } } - \dot { x } ) ^ { 2 } \check { C } _ { D } . c ( r )$ , where ẋ is the blade satwise velocity, $\mathrm { C _ { D } }$ the drag coefrcient, and c(r) the local blade chord. Hence the aerodynamic damping per unit length, $\hat { c } _ { a } ( \boldsymbol { r } )$ , is $\rho \overline { { U } } C _ { D } c ( \boldsymbol { r } )$ , and the rrst mode aerodynamic damping ratio,

$$
\xi_ {a 1} = c _ {a 1} / 2 m _ {1} \omega_ {1} = \int_ {0} ^ {R} \hat {c} _ {a} (r) \mu_ {1} ^ {2} (r) d r / 2 m _ {1} \omega_ {1}
$$

is given by

$$
\xi_ {a 1} = \rho \overline {{U}} C _ {D} \int_ {0} ^ {R} \mu_ {1} ^ {2} (r) c (r) d r / 2 m _ {1} \omega_ {1}
$$

Here $\mu _ { 1 } ( \mathrm { r } )$ is the rrst mode shape,

$$
m _ {1} = \int_ {0} ^ {R} m (r) \mu_ {1} ^ {2} (r) d r
$$

is the generalised mass, and $\omega _ { 1 }$ is the rrst mode natural frequency in radians per second. The logarithmic decrement is obtained by multiplying the damping ratio by $2 \pi$ .

When the wind direction is angled to the blade so as to generate maximum lift, the blade will be approaching stall, with the result that the aerodynamic damping is effectively zero. In this situation, tip desections are limited only by the blade structural damping. Structural damping is discussed in Section 5.8.4, and values for typical blade materials given.

# Root bending moment

The standard deviation of tip displacement in combination with the blade mode shape yields an inertial loading distribution from which the standard deviation of the resulting bending moment at any position along the blade may be calculated. In particular, the standard deviation of the root bending moment may be expressed in terms of the mean root bending moment as follows:

$$
\frac {\sigma_ {M 1}}{\overline {{{M}}}} = 2 \frac {\sigma_ {u}}{\overline {{{U}}}} \frac {\pi}{\sqrt {2 \delta}} \sqrt {R _ {u} (n _ {1})} \sqrt {K _ {S x} (n _ {1})}. \lambda_ {M 1} = \frac {\sigma_ {x 1}}{\overline {{{x}}} _ {1}}. \lambda_ {M 1} \tag {5.8a}
$$

where

$$
\lambda_ {M 1} = \frac {\int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r}{m _ {1} . \int_ {0} ^ {R} c (r) r d r}. \int_ {0} ^ {R} c (r) \mu_ {1} (r) d r \tag {5.8b}
$$

See Appendix A5.5 for the derivation of the expression for $\lambda _ { M 1 }$

The standard deviation of the quasi-static root bending moment suctuation, or root bending moment background response, is expressed in terms of the mean root bending moment by

$$
\frac {\sigma_ {M B}}{\overline {{M}}} = 2 \frac {\sigma_ {u}}{\overline {{U}}} \sqrt {K _ {S M B}} \tag {5.9}
$$

where $K _ { S M B }$ is a size reduction factor to take account of lack of correlation of wind suctuations along the blade. As shown in Appendix A5.6, $K _ { S M B }$ is usually only slightly less than unity because the blade length is small compared with the integral length scale of longitudinal turbulence measured in the across wind direction.

The variance of the total root bending moment suctuations is equal to the sum of the resonant and background response variances – i.e.

$$
\sigma_ {M} ^ {2} = \sigma_ {M 1} ^ {2} + \sigma_ {M B} ^ {2}
$$

Hence

$$
\frac {\sigma_ {M}}{\overline {{M}}} = 2 \frac {\sigma_ {u}}{\overline {{U}}} \sqrt {K _ {S M B} + \frac {\pi^ {2}}{2 \delta} R _ {u} (n _ {1}) K _ {S x} (n _ {1}) . \lambda_ {M 1} ^ {2}} \tag {5.10}
$$

The design extreme root bending moment is typically calculated as that due to the 50 year return, 10 minute mean wind speed plus the number of standard deviations of the root bending moment suctuations corresponding to the likely peak excursion in a 10 minute period. Thus

$$
M _ {\max} = \overline {{M}} + g. \sigma_ {M} \tag {5.11}
$$

where g is known as the peak factor and depends on the number of cycles of root bending moment suctuations in 10 minutes, according to the formula

$$
g = \sqrt {2 \ln (6 0 0 \nu)} + \frac {0 . 5 7 7}{\sqrt {2 \ln (6 0 0 \nu)}} \tag {5.12}
$$

Here, 휈 is the mean zero-upcrossing frequency of the root bending moment suctuations, which will be intermediate between that of the quasi-static wind loading and the blade natural frequency, $n _ { \mathrm { 1 } } - \mathsf { s e e }$ Appendix A5.7. (Note that, as g varies relatively slowly with frequency, it is a reasonable approximation to set g at an upper limit of 3.9, which corresponds to a frequency of about 1.9 Hz.)

Substituting Eq. (5.10) into Eq. (5.11) yields

$$
M _ {\max} = \overline {{{{M}}}} \left[ 1 + g \frac {\sigma_ {M}}{\overline {{{{M}}}}} \right] = \overline {{{{M}}}} \left[ 1 + g \left(2 \frac {\sigma_ {u}}{\overline {{{{U}}}}}\right) \sqrt {K _ {S M B} + \frac {\pi^ {2}}{2 \delta} R _ {u} (n _ {1}) K _ {S x} (n _ {1}) . \lambda_ {M 1} ^ {2}} \right] \tag {5.13}
$$

The expression in square brackets is similar to the numerator of the structural factor, $c _ { s } c _ { d } .$ , in EN 1991-1-4:2005:

$$
c _ {s} c _ {d} = \frac {1 + 2 k _ {p} I _ {v} (z _ {s}) \sqrt {B ^ {2} + R ^ {2}}}{1 + 7 I _ {v} (z _ {s})} \tag {5.14}
$$

in which $k _ { p }$ is the peak factor, $I _ { \nu } ( z _ { s } )$ is the turbulence intensity at height $z _ { s }$ and $R ^ { 2 } =$ $\frac { \pi ^ { 2 } } { 2 \delta } R _ { u } ( n _ { 1 } ) K _ { S x } ( n _ { 1 } )$ 휋2 .

It is often necessary to express the maximum moment in terms of the quasi-static moment due to the 50 year return gust speed, $U _ { e 5 0 }$ . To do this, we equate the latter quantity to the quasi-static component of Eq. (5.13), obtaining

$$
C _ {f}. \frac {1}{2} \rho U _ {e 5 0} ^ {2} \int_ {0} ^ {R} c (r). r. d r = \overline {{M}} \left(1 + g _ {0}. 2 \frac {\sigma_ {u}}{\overline {{U}}} \sqrt {K _ {S M B}}\right) \tag {5.15}
$$

Here the peak factor, $g ,$ takes a lower value, $g _ { 0 }$ , corresponding to the lower frequency of the quasi-static root bending moment suctuations. Equation (5.15) can then be combined with Eq. (5.13) to yield

$$
M _ {\max} = C _ {f}. \frac {1}{2} \rho U _ {e 5 0} ^ {2} \int_ {0} ^ {R} c (r). r. d r. Q _ {D} \tag {5.16}
$$

where $Q _ { \mathrm { D } }$ is a dynamic factor given by

$$
Q _ {D} = \frac {1 + g \left(2 \frac {\sigma_ {u}}{\overline {{{U}}}}\right) \sqrt {K _ {S M B} + \frac {\pi^ {2}}{2 \delta} R _ {u} (n _ {1}) K _ {S x} (n _ {1}) . \lambda_ {M 1} ^ {2}}}{1 + g _ {0} \left(2 \frac {\sigma_ {u}}{\overline {{{U}}}}\right) \sqrt {K _ {S M B}}} \tag {5.17}
$$

The dynamic factor $Q _ { \mathrm { D } }$ equates to the EN 1991-1-4 dynamic factor, $c _ { d } , \mathrm { i f } \ g _ { 0 }$ is 3.5 and the ratio $\lambda _ { M 1 }$ is unity. The EN 1991-1-4 structural factor, $c _ { s } c _ { d } ,$ given in Eq. (5.14) is the product of the dynamic factor, $c _ { d } .$ , and the size factor, $c _ { s } ,$ , given by $c _ { s } = \frac { 1 + 7 . I _ { v } ( z _ { s } ) \sqrt { B ^ { 2 } } } { 1 + 7 . I _ { v } ( z _ { s } ) }$

There is considerable advantage in starting with the extreme gust speed and calculating the extreme root moment as the product of $\begin{array} { r } { C _ { f } . { } _ { \hat { \gamma } } \overset { 1 } { \rho } U _ { e 5 0 } ^ { 2 } \int _ { 0 } ^ { R } c ( r ) . r . d r } \end{array}$ 휌U2e50 ∫ R0 c( and $Q _ { \mathrm { D } }$ , because it eliminates most of the error associated with linearising the formula for dynamic pressure. For example, if the extreme gust is 1.4 times the extreme 10 minute mean wind speed, as postulated in IEC 61400-1 (which implies that the product $g _ { 0 . } \frac { \sigma _ { u } } { \overline { { U } } } \mathrm { i s } 0 . 4 )$ , then the dynamic pressure due to the gust will be $1 . 4 ^ { 2 } = 1 . 9 6$ times that due to the 10 minute mean, rather than 1.8 times as given by the formula $1 + g _ { 0 } \left( 2 \frac { \sigma _ { u } } { \overline { { U } } } \right)$

Example 5.1 Evaluate the dynamic factor, $Q _ { \mathrm { D } }$ , for the blade root bending moment for a 40 m long stationary blade under extreme loading.

Consider a trial 40 m long rbreglass blade design (designated blade SC40) utilising NACA 632XX aerofoil sections with the chord and thickness distributions shown in Figure 5.4a. The thickness distribution has a pronounced knee near mid-span to minimise the thickness to chord ratio in the outer half of the span.

The blade structure is assumed to consist of an aerodynamic shell strengthened by spar caps and linking shear webs, as illustrated in Figure 7.6. The spar cap thickness is required to be a maximum at the knee at 17 m radius and tapers down to zero between there and the root while varying as the blade chord in the outboard section. The thickness of the rbreglass skins of the foam sandwich panels forming the aerodynamic shell and their spacing vary as the chord except in the root region. [The blade structure chosen for the SC40 blade is intended to be more realistic (and structurally more efrcient) than the blade structure of the T40 blade used for this example in the rrst and second editions. In the latter, there were no spar caps, and the thickness of the rbreglass skins was uniform along the blade. The SC40 blade has a mass of 7.7 t, compared with the T40 blade mass of 16.3 t.]

The resulting mass and stiffness distributions are as shown in Figure 5.4b, and modal analysis as described in Section 5.8.2 yields the rrst and second mode shapes shown in Figure 5.4c. The rrst mode shape for a blade of constant cross-section (i.e. a uniform cantilever) is also shown for comparison purposes, and it is evident that the high stiffness of the inboard portion of the tapered blade results in dramatically reduced desections there as a proportion of tip desection. For a rbreglass blade, typical values of the Young’s modulus and material density would be 43 GPa and $1 . 9 \mathrm { t } / \mathrm { m } ^ { 3 }$ , respectively, resulting in a rrst mode natural frequency of 0.88 Hz and a second mode natural frequency of 2.73 Hz.

Values of the other parameters assumed are:

<table><tr><td>Blade height, z</td><td>70 m</td></tr><tr><td>50 year return 10 minute mean wind speed, $\overline{U}$ , at blade height</td><td>50 m/s</td></tr><tr><td>Eurocode 1 terrain category</td><td>I (Roughness length,  $z_{o} = 0.01$  m)</td></tr><tr><td>Turbulence intensity,  $I(z) = 1/\ln(z/z_{0})$ </td><td>0.113</td></tr></table>

![](images/ab2e1084ad21483aff34764c8fbe3fc7179ba5731ac7ceb4445135146b7ddc55.jpg)

<details>
<summary>line</summary>

| Blade radius, r (metres) | Blade chord (metres) | Blade thickness (metres) | Percentage thickness/chaord ratio |
| ------------------------ | -------------------- | ------------------------ | --------------------------------- |
| 0                        | 2.3                  | 2.3                      | 30%                               |
| 5                        | 3.5                  | 2.0                      | 50%                               |
| 10                       | 3.2                  | 1.5                      | 40%                               |
| 20                       | 2.8                  | 0.6                      | 20%                               |
| 40                       | 1.3                  | 0.1                      | 5%                                |
</details>

![](images/c9a65dc287e3b352f720f3e6492f5994c4222fb9d9808497a1a3a820cd9234fb.jpg)

<details>
<summary>line</summary>

| Blade radius, r (metres) | Mass per unit length (kg/m) | Second moment of area (m⁴) |
| ------------------------ | --------------------------- | --------------------------- |
| 0                        | 310                         | 0.05                        |
| 17                       | 240                         | 0.04                        |
| 21                       | 40                          | 0.01                        |
| 40                       | 70                          | 0                           |
</details>

![](images/3157fcde114d9f39df751278b44ffe1a0ee40c4ae8fbc23355413520fde9570a.jpg)

<details>
<summary>line</summary>

| Blade radius (metres) | First mode - blade of constant cross-section for comparison (dashed line) | First mode - tapered blade SC40 | Second mode - tapered blade SC40 |
| --------------------- | ------------------------------------------------------------------ | ------------------------------ | ------------------------------- |
| 0                     | 0.0                                                                | 0.0                            | 0.0                             |
| 5                     | ~0.1                                                               | ~-0.1                          | ~-0.1                           |
| 10                    | ~0.3                                                               | ~-0.2                          | ~-0.2                           |
| 15                    | ~0.5                                                               | ~-0.3                          | ~-0.3                           |
| 20                    | ~0.7                                                               | ~-0.4                          | ~-0.4                           |
| 25                    | ~0.8                                                               | ~-0.4                          | ~-0.4                           |
| 30                    | ~0.9                                                               | ~-0.3                          | ~-0.3                           |
| 35                    | ~1.0                                                               | ~0.0                           | ~0.0                            |
| 40                    | 1.0                                                                | 1.0                            | 1.0                             |
</details>

(c)   
Figure 5.4 (a) Blade SC40 chord and thickness distributions. (b) Blade SC40 mass and stiffness distribution. (c) Blade SC40 rrst and second mode shapes.

The corresponding integral length scale for longitudinal turbulence is 189 m according to EN 1991-1-4:2005.

The values of the parameters in Eq. (5.7) governing the resonant tip response are determined as follows:

1. The aerodynamic damping is assumed to be zero, so the damping logarithmic decrement is taken as 0.05, corresponding to the structural damping value for rbreglass.   
2. The non-dimensional power spectral density of longitudinal wind turbulence, $R _ { u } ( n ) = n . S _ { u } ( n _ { 1 } ) / \sigma _ { u } ^ { 2 } .$ , is calculated at the blade rrst mode natural frequency of 0.881 Hz according the Kaimal power spectrum derned in EN 1991-1-4 [Eq. (A5.8) in Appendix A5] as 0.0606.   
3. A value of 10 is taken for the non-dimensional decay constant, C, in the exponential expression for the normalised co-spectrum used in the derivation of the size reduction factor, $K _ { S x } ( n _ { 1 } )$ , in Eq. (A5.25).

The various stages in the derivation of the extreme root bending moment and the dynamic factor, $Q _ { D }$ , are set out below. The rgures in square brackets are the corresponding values obtained using the method of annex C of EN 1991-1-4:2005, which are included for comparison.

<table><tr><td>Size reduction factor for resonant response,  $K_{Sx}(n_1)$ </td><td>0.372</td><td>Eq. (A5.25)</td><td>[0.308]</td></tr><tr><td>Ratio of standard deviation of resonant tip displacement to the first mode component of steady tip displacement,</td><td></td><td></td><td></td></tr><tr><td> $\frac{\sigma_{y1}}{\overline{y}_1} = 2\frac{\sigma_u}{\overline{U}}\frac{\pi}{\sqrt{2\delta}}\sqrt{R_u(n_1)}\sqrt{K_{Sx}(n_1)}$ </td><td></td><td></td><td></td></tr><tr><td>= 2 × 0.113 × 9.935 ×  $\sqrt{0.0606}.\sqrt{0.372}$ </td><td></td><td></td><td></td></tr><tr><td>= 2 × 0.113 × 9.935 × 0.246 × 0.610 = 2 × 0.113 × 1.490</td><td>0.337</td><td>Eq. (5.7)</td><td>[N/A]</td></tr><tr><td>Root moment factor,  $\lambda_{M1}$ </td><td>0.683</td><td>Eq. (5.8b)</td><td>[N/A]</td></tr><tr><td>Ratio of standard deviation of resonant root moment to mean value,  $\frac{\sigma_{M1}}{\overline{M}} = \frac{\sigma_{x1}}{\overline{x}_1}. \lambda_{M1}$ </td><td>0.230</td><td>Eq. (5.8a)</td><td>[0.306]</td></tr><tr><td>Size reduction factor for quasi-static or background response,  $K_{SMB}$ </td><td>0.829</td><td>Eq. (A5.40)</td><td>[0.871]</td></tr><tr><td>Ratio of standard deviation of quasi-static root moment response to mean value,  $\frac{\sigma_{MB}}{\overline{M}} = 2\frac{\sigma_u}{\overline{U}}\sqrt{K_{SMB}} = 2 \times 0.113 \times 0.910$ </td><td>0.206</td><td>Eq. (5.9)</td><td>[0.197]</td></tr><tr><td>Ratio of standard deviation of total root moment response to mean value, $\frac{\sigma_M}{\overline{M}} = \sqrt{\left(\frac{\sigma_{MB}}{\overline{M}}\right)^2 + \left(\frac{\sigma_{M1}}{\overline{M}}\right)^2} = \sqrt{0.206^2 + 0.230^2}$ </td><td>0.308</td><td></td><td>[0.364]</td></tr><tr><td>Zero up-crossing frequency of quasi-static response,  $n_0$ </td><td>0.342 Hz</td><td>Eq. (A5.57)</td><td>[N/A]</td></tr><tr><td>Zero up-crossing frequency of total root moment response,  $\nu$ </td><td>0.695 Hz</td><td>Eq. (A5.54)</td><td>[N/A]</td></tr><tr><td>Peak factor, g, based on  $\nu$ </td><td>3.64</td><td>Eq. (5.12)</td><td>[3.66]</td></tr><tr><td>Ratio of extreme moment to mean value, $\frac{M_{\text{max}}}{\overline{M}} = 1 + g\left(\frac{\sigma_M}{\overline{M}}\right) = 1 + 3.64(0.308)$ </td><td>2.12</td><td>Eq. (5.13)</td><td>[2.33]</td></tr><tr><td>Peak factor,  $g_0$ , based on  $n_0$ </td><td>3.44</td><td></td><td>[3.5]</td></tr><tr><td>Ratio of quasi-static component of extreme moment to mean value $= 1 + g_0 \frac{\sigma_{MB}}{\overline{M}} = 1 + 3.44(0.206)$ </td><td>1.708</td><td>Eq. (5.15)</td><td>[1.79]</td></tr><tr><td>Dynamic factor,  $Q_D = 2.12/1.708$ </td><td>1.243</td><td>Eq. (5.17)</td><td>[1.30]</td></tr></table>

It is apparent that the EN 1991-1-4 method yields a larger value of the extreme root bending moment. However, the EN 1991-1-4 ratio of extreme to mean bending moment is intended to apply at all points along the blade, so a conservative value at the root is inescapable, as is shown in the next section, which examines the variation of bending moment along the blade.

# Spanwise variation of bending moment

The resonant and quasi-static components of bending moments at intermediate positions along the blade can be related to those at the root in a straightforward way.

As far as the quasi-static bending moment suctuations are concerned, the variation along the blade follows closely the bending moment variation due to the steady loading, although slight changes in the size reduction factor have a small effect. The bending moment diagram for the resonant oscillations is, however, of a very different shape, because of the dominance of the inertia loading on the tip. An expression for the resonant bending moment variation along the blade is given in Appendix A5.8, and it is plotted out for the example above in Figure 5.5a, with the quasi-static bending moment variation alongside for comparison. It is seen that the resonant bending moment diagram is closer to linear than the quasi-static one, which approximates to a parabola.

A consequence of the much slower decay of the resonant bending moment out towards the tip is an increase in the ratio of the resonant bending moment standard deviation to the local steady moment with radius. This results in an increase in the dynamic magnircation factor, $Q _ { \mathrm { D } }$ , from 1.24 at the root to 1.85 near the tip for the example above. See Figure 5.5b.

![](images/663b278b6c25658262635c5df495246977b71192cdf8dee2032a3714011f790a.jpg)  
Figure 5.5 (a) Spanwise variation of resonant and quasi-static moments – blade SC40. (b) Spanwise variation of (i) bending moment standard deviations in terms of local steady bending moment, and (ii) dynamic magnircation factor – for blade SC40.

# 5.7 Blade loads during operation

# 5.7.1 Deterministic and stochastic load components

It is normal to separate out the loads due to the steady wind on the rotating blade from those due to wind speed suctuations and analyse them in different ways. The periodic loading on the blade due to the steady spatial variation of wind speed over the rotor swept area is termed the deterministic load component, because it is uniquely determined by a limited number of parameters – i.e. the hub-height wind speed, the rotational speed, the wind shear, etc. On the other hand, the random loading on the blade due to wind speed suctuations (i.e. turbulence) has to be described probabilistically and is therefore termed the stochastic load component.

In addition to wind loading, the rotating blade is also acted on by gravity and inertial loadings. The gravity loading depends simply on blade azimuth and mass distribution and is thus deterministic, but the inertial loadings will be affected by turbulence – as, for example, in the case of a teetering rotor, or a sexing blade – and so will contain stochastic as well as deterministic components.

# 5.7.2 Deterministic aerodynamic loads

# Steady, uniform @ow perpendicular to plane of rotor

The application of momentum theory to a blade element, which is described in Section 3.5.3, enables the aerodynamic forces on the blade to be calculated at different radii. Eqs. (3.54a) and (3.55) are solved iteratively for the sow induction factors, a and a’, at each radius, enabling the sow angle, 휙, the angle of attack, 훼, and hence the lift and drag coefrcients to be determined.

For loadings on the outboard portion of the blade, allowance for tip-loss must be made, so Eqs. (3.54a) and (3.55) are replaced by Eqs. (3.54c) and (3.55a) in Section 3.9.6. These equations can be arranged to give the following expressions for the forces per unit length on an element perpendicular to the plane of rotation and in the direction of blade motion, known as the out-of-plane and in-plane forces, respectively.

Out-of-plane force per unit length:

$$
F _ {X} = C _ {x}. \frac {1}{2} \rho W ^ {2}. c = \frac {4 \pi r \rho}{B} U _ {\infty} ^ {2} (1 - a f) a f \tag {5.18}
$$

In-plane force per unit length:

$$
F _ {Y} = C _ {y}. \frac {1}{2} \rho W ^ {2}. c = \frac {4 \pi r ^ {2} \rho}{B} \Omega U _ {\infty} (1 - a f) a ^ {\prime} f \tag {5.19}
$$

The parameters in the expressions are as derned in Chapter 3. f is the tip-loss factor, and B is the number of blades.

The variation of the in-plane and out-of-plane forces with radius is shown in Figure 5.6 for a typical machine operating in uniform, steady winds of 8 and 10 m/s. The 80 m stall-regulated turbine considered in this example is rtted with three SC40 blades as described in Example 5.1 and rotates at 15 rpm. The blade twist distribution (Figure 5.6) is linear with respect to the reciprocal of the radius in line with Eq. (3.74) and selected to produce the maximum energy yield for an annual mean wind speed of 7.5 m/s. It is evident that the out-of-plane load per unit length increases approximately linearly with radius, in spite of the reducing blade chord, until the effects of tip-loss are felt beyond about 80% of tip radius. The tip-loss effect is relatively greater for a 10 m/s wind speed compared with 8 m/s due to the greater spacing of the vortex sheets (Section 3.9.3). Note that the form of the variation would be the same for any combination of rotational speed, wind speed, and tip radius yielding the same tip speed ratio, because it is the tip speed ratio that determines the radial distribution of sow angle 휙 and of the induction factors a and a’.

Integration of these forces along the blade then yields in-plane and out-of-plane aerodynamic blade bending moments. The variation of these moments with radius is shown in Figure 5.7 for the example above. The blade bending moments effectively decrease linearly with increasing radius over the inboard third of the blade because of the concentration of loading outboard.

![](images/1324b28b8941d2e4788d3dc3ec4d3236eea6298bd43c076adfa4ce428037f8cc.jpg)

<details>
<summary>line</summary>

| Radius (m) | Blade twist (radians) - Twist distribution | Blade twist (radians) - 10 m/s | Blade twist (radians) - 8 m/s | Blade twist (radians) - In-plane load per metre | Blade load per unit length (kN/m) - 10 m/s | Blade load per unit length (kN/m) - 8 m/s |
| ---------- | ------------------------------------------ | ------------------------------ | ----------------------------- | ----------------------------------------------- | ------------------------------------------ | ------------------------------------------ |
| 0          | 0.25                                       | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 5          | 0.2                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 10         | 0.1                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 15         | 0.05                                       | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 20         | 0.0                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 25         | 0.0                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 30         | 0.0                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 35         | 0.0                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
| 40         | 0.0                                        | 0.3                            | 0.2                           | 0.0                                             | 0.5                                        | 0.0                                        |
</details>

Figure 5.6 Distribution of blade in-plane and out-of-plane aerodynamic loads during operation of an example 80 m diameter machine in steady, uniform winds of 8 and 10 m/s.

The variation of the blade root out-of-plane bending moment with wind speed is illustrated in Figure 5.8 for the 80 m diameter example machine described above. As explained in Section 3.10, the phenomenon of stall delay results in signircantly increased values of the lift coefrcient at higher wind speeds on the inboard section of the rotating blade than predicted by static aerofoil data, such as that reproduced in Figure 3.43. Accordingly, Figure 5.8 and the other rgures referred to in this section have been derived using realistic aerofoil data for a rotating LM 19.0 blade reported in Petersen et al. (1998), which is based on an empirical modircation of static or two-dimensional (2-D) aerofoil data. The modired data is reproduced in Figure 5.9, and it displays signircantly higher lift coefrcients for the thicker, inboard blade sections at high angles of attack than for the thinner, outboard blade sections because of stall delay at the inboard sections.

Figure 5.8 shows the blade root out-of-plane bending moment increasing nearly linearly with wind speed at rrst and then levelling off, becoming almost constant for winds between 12 and 16 m/s, as the blade goes into stall. Thereafter the root moment increases again, but much more gently than before.

Also shown on Figure 5.8 is the variation of blade root out-of-plane bending moment with wind speed for the same machine with pitch regulation to limit the power output to 1700 kW. It is evident that the bending moment drops away rapidly at wind speeds above rated.

![](images/1686255b2ed58f22b1744f92a5362e71911f346077ca0fd521299ecc2f4e0b0b.jpg)

<details>
<summary>line</summary>

| Radius (m) | In-plane moment (kNm) | Out-of-plane moment (kNm) |
| ---------- | --------------------- | ------------------------- |
| 0          | 300                   | 2100                      |
| 10         | 150                   | 1400                      |
| 20         | 75                    | 800                       |
| 30         | 25                    | 300                       |
| 40         | 0                     | 0                         |
</details>

Figure 5.7 Distribution of blade in-plane and out-of-plane aerodynamic bending moments during operation of an example 80 m diameter machine in steady, uniform winds of 8 and 10 m/s.

![](images/aa0a874e28abe1e4d4a498b36ae5ed3a13d6340782a8dd2e94df369c0cfbe332.jpg)

<details>
<summary>line</summary>

| Mean wind speed (m/s) | Out-of-plane aerodynamic blade root bending moment (kNm) |
| --------------------- | ------------------------------------------------------ |
| 5                     | ~300                                                   |
| 10                    | ~2300                                                  |
| 15                    | ~2400                                                  |
| 20                    | ~2600                                                  |
| 25                    | ~2900                                                  |
| 30                    | ~3300                                                  |
</details>

Figure 5.8 Blade out-of-plane root bending moment during operation in steady, uniform wind – variation with wind speed for similar stall-regulated and pitch-regulated machines.

# Yawed @ow

The application of blade-element/momentum (BEM) theory to steady yawed sow is described in Section 4.2.8. This methodology has been used to derive Figure 5.10a, which shows the variation of the blade root out-of-plane and in-plane moments with azimuth for the 80 m diameter stall-regulated machine described above, operating at a steady yaw angle of $+ 2 0 ^ { \circ }$ . Note that the blade azimuth is measured in the direction of blade rotation, from a zero value at top dead centre, and the yaw angle is derned as positive when the lateral component of air sow with respect to the rotor disc is in the same direction as the blade movement at zero azimuth. [Note that in this and subsequent rgures, the blade root moments plotted are actually the values extrapolated to the shaft axis rather than those at the blade/hub interface.]

![](images/d6713787e1451e0462c57be8c85f1a0c1742f09762f55aaeb99e0857bfbb62ff.jpg)

<details>
<summary>line</summary>

| Angle of attack (degrees) | Lift (t/c = 24%) | Lift (t/c = 18%) | Lift (t/c = 15%) | Lift (t/c = 13%) | Drag (t/c = 13%, 15%, 18%) | Drag (t/c = 24%) |
| ------------------------- | ---------------- | ---------------- | ---------------- | ---------------- | --------------------------- | ---------------- |
| 0                         | 0.4              | 0.4              | 0.4              | 0.4              | 0.4                         | 0.4              |
| 5                         | 1.0              | 1.0              | 1.0              | 1.0              | 0.6                         | 0.6              |
| 10                        | 1.7              | 1.3              | 1.2              | 1.1              | 0.8                         | 0.8              |
| 15                        | 1.7              | 1.3              | 1.2              | 1.1              | 1.0                         | 1.0              |
| 20                        | 1.6              | 1.2              | 1.2              | 1.1              | 1.2                         | 1.2              |
| 25                        | 1.5              | 1.2              | 1.2              | 1.1              | 1.3                         | 1.3              |
| 30                        | 1.4              | 1.2              | 1.2              | 1.1              | 1.5                         | 1.5              |
</details>

Figure 5.9 Aerofoil data for LM 19.0 blade for various thickness/chord ratios. Source: From Petersen et al. (1998).

Figure 5.10a reveals a distinct difference between the behaviour at 10 m/s on the one hand and 15–20 m/s on the other. In the latter case, the bending moment variation is sinusoidal with a maximum value at $1 8 0 ^ { 0 }$ azimuth, indicating that the variation is dominated by the effect of the suctuation of the air velocity relative to the blade, W. At 10 m/s, however, the maximum out-of-plane bending moment occurs at about $2 2 5 ^ { 0 }$ azimuth, suggesting that the non-uniform component of induced velocity, $u _ { 1 }$ [Eq. (4.20)] is also signircant. As wind speed increases, of course, the induction factor, a, becomes small, reducing the impact of $u _ { 1 }$ .

For comparison, the variation in blade root bending moment with azimuth for an example 2 MW, 80 m diameter pitch-regulated, variable-speed machine operating at a steady $2 0 ^ { \circ }$ yaw is shown in Figure 5.10b – again for wind speeds of 10, 15, and 20 m/s. The turbine operates at a constant tip speed ratio of 8 up to a wind speed of 11 m/s, with the tip speed limited to 88 m/s thereafter, giving a maximum rotational speed of 21 rpm. The blade has the same plan-form and thickness prorle as the SC40 blade, but the blade twist distribution is optimised to maximise power output when the tip speed ratio is 8 (while remaining linear with respect to the reciprocal of the radius). It is seen that both the maximum out-of-plane root bending moment and its range of variation with azimuth are somewhat reduced at the higher wind speeds compared with the stall-regulated machine. However, at 10 m/s, these quantities are increased signircantly because of the increased rotational speed (19 rpm).

![](images/4f0314bfe1ebe1a4032fc21f9d9968aa95e8c538a6c5b321a6445b88ec225f4a.jpg)

<details>
<summary>line</summary>

| Azimuth (degrees) | Out-of-plane BMs (20 m/s) | Out-of-plane BMs (15 m/s) | Out-of-plane BMs (10 m/s) | In-plane BMs (20 m/s) | In-plane BMs (15 m/s) | In-plane BMs (10 m/s) |
| ----------------- | ------------------------ | ------------------------ | ------------------------ | --------------------- | --------------------- | --------------------- |
| 0                 | ~1950                    | ~1900                    | ~1850                    | ~300                  | ~350                  | ~400                  |
| 45                | ~2050                    | ~2000                    | ~1850                    | ~350                  | ~400                  | ~450                  |
| 90                | ~2400                    | ~2300                    | ~1850                    | ~450                  | ~450                  | ~500                  |
| 135               | ~2800                    | ~2600                    | ~1900                    | ~550                  | ~500                  | ~550                  |
| 180               | ~3100                    | ~2850                    | ~2100                    | ~650                  | ~550                  | ~600                  |
| 225               | ~3000                    | ~2700                    | ~2200                    | ~600                  | ~550                  | ~550                  |
| 270               | ~2700                    | ~2400                    | ~2150                    | ~500                  | ~450                  | ~450                  |
| 315               | ~2200                    | ~2100                    | ~2050                    | ~350                  | ~350                  | ~350                  |
| 360               | ~1950                    | ~1900                    | ~1900                    | ~300                  | ~350                  | ~350                  |
</details>

(a)

![](images/03413917d81b670a92abf2546a58055625cd5e330d4c084516406c0f375424a3.jpg)

<details>
<summary>line</summary>

| Azimuth (degrees) | In-plane BMs (10 m/s) | In-plane BMs (15 m/s) | In-plane BMs (20 m/s) | Out-of-plane BM (10 m/s) | Out-of-plane BM (15 m/s) | Out-of-plane BM (20 m/s) |
| ----------------- | --------------------- | --------------------- | --------------------- | ------------------------ | ------------------------ | ------------------------ |
| 0                 | ~300                  | ~300                  | ~750                  | ~2100                    | ~1200                    | ~2100                    |
| 45                | ~250                  | ~250                  | ~600                  | ~1900                    | ~1100                    | ~2000                    |
| 90                | ~200                  | ~200                  | ~400                  | ~1800                    | ~1000                    | ~1900                    |
| 135               | ~150                  | ~150                  | ~200                  | ~1700                    | ~900                     | ~1800                    |
| 180               | ~100                  | ~100                  | ~-200                 | ~1600                    | ~850                     | ~1700                    |
| 225               | ~200                  | ~200                  | ~-100                 | ~1500                    | ~950                     | ~1800                    |
| 270               | ~300                  | ~300                  | ~+100                 | ~1400                    | ~1100                    | ~2450                    |
| 315               | ~350                  | ~350                  | ~+200                 | ~1350                    | ~1250                    | ~2350                    |
| 360               | ~400                  | ~400                  | ~+300                 | ~1300                    | ~1250                    | ~2150                    |
</details>

(b)   
Figure 5.10 (a) Variation of blade root bending moment with azimuth, for an example 80 m diameter stall-regulated machine operating at 15 rpm at a steady $2 0 ^ { \circ }$ yaw. (b) Variation of blade root bending moment with azimuth, for an example 80 m diameter pitch-regulated, variable-speed machine operating at a steady $2 0 ^ { \circ }$ yaw with a tip speed ratio of 8 below 11 m/s and a maximum rotational speed of 2.2 rad/s (21 rpm).

# Shaft tilt

Upwind machines – that is, wind turbines with the rotor positioned between the tower and the oncoming wind – normally have the rotor shaft tilted upwards by several degrees to increase the clearance between the rotor and the tower. Thus, as for the case of yaw misalignment, the sow is inclined to the rotor shaft axis but tilted upwards rather than sideways, so the treatment of shaft tilt mirrors that of yawed sow.

# Wind shear

The increase of wind speed with height is known as wind shear. The theoretical logarithmic prorle, $U ( z )$ ∝ $\ln ( z / z _ { 0 } )$ , is usually approximated by the power law, $U ( z ) \propto ( z / z _ { r e f } ) ^ { \alpha }$ , for wind turbine design purposes. The appropriate value of the exponent 훼 increases with the surface roughness, $z _ { 0 } .$ , with a rgure of 0.14 typically quoted for level countryside, although the speed-up of air sow close to the ground over rounded hills usually results in a lower value at hill tops. As already noted, IEC 61400-1 specires a conservative value of 0.20.

In applying momentum theory to this case, the velocity component at right angles to the plane of rotation is expressed as U∞(1 + r cos 휓z 훼 $U _ { \infty } \bigg ( 1 + \frac { r \cos \psi } { z _ { h u b } } \bigg ) ^ { \alpha } ( 1 - a )$ and the momentum equations are solved for the induction factors at each azimuth and radius. The variation of blade root bending moments with azimuth due to wind shear is illustrated in Figure 5.11a for the example 80 m diameter stall-regulated machine, taking the exponent as 0.20 and the hub height as 60 m and considering hub-height wind speeds of 10, 15, and 20 m/s. In the 10 m/s case, the variation in out-of-plane moment due to wind shear is signircant, but in the 15 m/s case there is negligible variation, as the blade is in stall.

Figure 5.11b shows the variation of blade root bending moments with azimuth due to wind shear for the example 2 MW, 80 m diameter pitch-regulated, variable-speed machine. It is seen that the out-of-plane moment range increases with increasing hub-height wind speed because of the increased range of wind speeds encountered over a blade revolution.

# Tower shadow

Blocking of the air sow by the tower results in regions of reduced wind speed both upwind and downwind of the tower. This reduction is more severe for tubular towers than for lattice towers and, in the case of tubular towers, is larger on the downwind side because of sow separation. As a consequence, designers of downwind machines usually position the rotor plane well clear of the tower to minimise the interference effect.

The velocity dercits upwind of a tubular tower can be modelled using potential sow theory. The sow around a cylindrical tower is derived by superposing a doublet – that is, a source and sink at very close spacing – on a uniform sow, $U _ { \infty }$ , giving the stream function:

$$
\psi = U _ {\infty} y \left(1 - \frac {(D / 2) ^ {2}}{x ^ {2} + y ^ {2}}\right) \tag {5.20}
$$

where D is the tower diameter, and x and y are the longitudinal and lateral coordinates with respect to the tower centre – see Figure 5.12. Differentiation of 휓 with respect to y yields the following expression for the sow velocity in the x direction:

$$
U = U _ {\infty} \left(1 - \frac {(D / 2) ^ {2} (x ^ {2} - y ^ {2})}{(x ^ {2} + y ^ {2}) ^ {2}}\right) \tag {5.21}
$$

![](images/cfbe6a41edba9f14c371e2417ff6905b282f360463ef4b43e17ddac78e9fe47f.jpg)

<details>
<summary>line</summary>

| Azimuth (degrees) | Steady wind speed at hub ht (kNm) | 15 m/s (kNm) | 10 m/s (kNm) | In-plane moments (kNm) |
| ----------------- | ---------------------------------- | ------------ | ------------ | ---------------------- |
| 0                 | 2600                               | 2400         | 2300         | 500                    |
| 45                | 2600                               | 2400         | 2300         | 500                    |
| 90                | 2600                               | 2400         | 2300         | 500                    |
| 135               | 2600                               | 2400         | 2300         | 500                    |
| 180               | 2600                               | 2400         | 2300         | 500                    |
| 225               | 2600                               | 2400         | 2300         | 500                    |
| 270               | 2600                               | 2400         | 2300         | 500                    |
| 315               | 2600                               | 2400         | 2300         | 500                    |
| 360               | 2600                               | 2400         | 2300         | 500                    |
</details>

(a)

![](images/b57358b6915ec6df10614ea16ab094a276fc623e74f7db4408fc0ce44d113a71.jpg)

<details>
<summary>line</summary>

| Azimuth (degrees) | In-plane moments (kNm) | Out-of-plane moments (kNm) | 10 m/s (kNm) | 15 m/s (kNm) | 20 m/s (kNm) |
| ----------------- | ---------------------- | -------------------------- | ------------ | ------------ | ------------ |
| 0                 | ~500                   | ~1700                      | ~2500        | ~1700        | ~1700        |
| 45                | ~400                   | ~1500                      | ~2400        | ~1600        | ~1600        |
| 90                | ~300                   | ~1300                      | ~2300        | ~1500        | ~1500        |
| 135               | ~200                   | ~1000                      | ~2100        | ~1300        | ~1300        |
| 180               | ~100                   | ~800                       | ~1900        | ~1100        | ~1100        |
| 225               | ~200                   | ~1000                      | ~2100        | ~1300        | ~1300        |
| 270               | ~300                   | ~1300                      | ~2300        | ~1500        | ~1500        |
| 315               | ~400                   | ~1600                      | ~2400        | ~1600        | ~1600        |
| 360               | ~500                   | ~1700                      | ~2500        | ~1700        | ~1700        |
</details>

(b)   
Figure 5.11 (a) Variation of blade root bending moments with azimuth due to wind shear, for the example 80 m diameter stall-regulated machine operating in steady hub-height winds of 10, 15, and 20 m/s with 0.2 shear exponent. (b) Variation of blade root bending moments with azimuth due to wind shear, for the example 80 m diameter pitch-regulated, variable-speed machine operating in steady hub-height winds of 10, 15, and 20 m/s with 0.2 shear exponent. The machine operates at a tip speed ratio of 8 in winds below 11 m/s and at a limiting rotational speed of 2.2 rad/s (21 rpm) in higher winds.

![](images/fb338bfeaea5971730598a56d1e831bb6db56f160138d390771956dc4fe3de09.jpg)

<details>
<summary>text_image</summary>

Ω
d
J J
Tower radius = D/2
y x(d) x Section J - J Rotor plane
Velocity Profile at rotor plane
</details>

Figure 5.12 Tower shadow parameters.

The second term within the brackets, which is the velocity dercit as a proportion of the undisturbed wind speed, is plotted out against the lateral coordinate, y, divided by tower diameter, for a range of upwind distances, x, in Figure 5.13. The velocity dercit on the sow axis of symmetry is equal to $U _ { \infty } ( D / 2 x ) ^ { 2 }$ , and the total width of the dercit region is twice the upwind distance. Consequently, the velocity gradient encountered by a rotating blade decreases rapidly as the upwind distance, x, increases.

The effect of tower shadow on blade loading can be estimated by setting the local velocity component at right angles to the plane of rotation equal to U(1 − a) in place of $U _ { \infty } ( 1 - a )$ and applying blade element theory as usual. Results for blade root bending moments for the example 80 m diameter stall-regulated machine are given in Figure 5.14, assuming a tower diameter of 4 m and ignoring dynamic effects. The plots show the variation of in-plane and out-of-plane root moments with azimuth during operation in wind speeds of 10 and 20 m/s, for a blade–tower clearance equal to the tower radius – i.e. for x/D = 1. Note that the dip in out-of-plane bending moment is more severe at the lower wind speed. Also shown are 10 m/s plots for $x / D = 1 . 5 ,$ , which exhibit a much less severe disturbance.

![](images/6e1287fdd975324e0fa9298da59c6f604f1000b349e400f22072e3222a6311ed.jpg)

<details>
<summary>line</summary>

| Lateral distance from flow axis of symmetry through tower centreline, as a proportion of tower diameter | Distance, x, upwind of tower centreline (D=0.75D) | Distance, x, upwind of tower centreline (D=1.0D) | Distance, x, upwind of tower centreline (D=1.25D) | Distance, x, upwind of tower centreline (D=1.5D) | Distance, x, upwind of tower centreline (D=2.0D) |
| --- | --- | --- | --- | --- | --- |
| 0.0 | 0.45 | 0.25 | 0.16 | 0.11 | 0.07 |
| 0.5 | 0.15 | 0.10 | 0.08 | 0.06 | 0.04 |
| 1.0 | 0.05 | 0.03 | 0.02 | 0.01 | 0.01 |
| 1.5 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 |
| 2.0 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| 2.5 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
</details>

Figure 5.13 Prorles of velocity dercit due to tower shadow at different distances x upwind of tower centreline.

![](images/a35df9ca5f80e113c794b03f49d03cf42e764569e84d1a8beda6968344fd5abf.jpg)

<details>
<summary>line</summary>

| Azimuth (degrees) | Aerodynamic out-of-plane root bending moment (kNm) |
| ----------------- | ----------------------------------------------- |
| 90                | 2000                                            |
| 110               | 2000                                            |
| 130               | 2000                                            |
| 150               | 2000                                            |
| 170               | 2000                                            |
| 175               | 1400                                            |
| 180               | 1800                                            |
| 190               | 2000                                            |
| 210               | 2000                                            |
</details>

Figure 5.14 Variation of blade root out-of-plane bending moment with azimuth due to tower shadow, for typical 80 m diameter stall-regulated upwind machine operating in steady, uniform winds of 10 and 20 m/s.

In the case of downwind turbines, the sow separation and generation of eddies that take place are less amenable to analysis, so empirical methods are used to estimate the mean velocity dercit. Commonly, the prorle of the velocity dercit is assumed to be of cosine form, so that

$$
U = U _ {\infty} \left(1 - k \cos^ {2} \left(\frac {\pi y}{\delta}\right)\right) \tag {5.22}
$$

where 훿 is the total width of the dercit region. The slight enhancement of velocities beyond the dercit region is usually ignored. See also Section 6.13.2.

The sharp dip in blade loading caused by tower shadow is more prone to excite blade oscillations than the smooth variations in load due to wind shear, shaft tilt, and yaw, and this aspect is considered in the ‘Blade Dynamic Response’ section.

# Wake effects

Within a wind farm, it is common for one turbine to be operating wholly or partly in the wake of another. In the latter case, which is more severe, the downwind turbine is effectively subjected to horizontal wind shear, and the blade load suctuations can be analysed accordingly. Wake effects are described in detail in Chapter 9.

# 5.7.3 Gravity loads

Gravity loading on the blade results in a sinusoidally varying edgewise bending moment that reaches a maximum when the blade is horizontal and that changes sign from one horizontal position to the other. It is thus a major source of fatigue loading. For the blade SC40 (see Example 5.1), the maximum gravity moment, $\begin{array} { r } { \int _ { 0 } ^ { R } m ( r ) r d r , } \end{array}$ is 1260 kNm, so the edgewise bending moment range due to gravity is 2520 KNm. This signircantly exceeds the variations in edgewise moment due to yaw or wind shear, which are typically less than a tenth this value below rated and less than a sixth above. The spanwise distribution of gravity bending moment is shown in Figure 5.15 for blade SC40.

![](images/7f938f41140ec8feec9df0b015ec2cd16f933d8123e51ff473e1a827e3bbe9c5.jpg)

<details>
<summary>line</summary>

| Radius (m) | Edgewise bending moment due to gravity - horizontal blade (kNm) |
| ---------- | ------------------------------------------------------------- |
| 0          | 1250                                                          |
| 10         | 750                                                           |
| 20         | 250                                                           |
| 30         | 50                                                            |
| 40         | 0                                                             |
</details>

Figure 5.15 Blade SC40 gravity bending moment distribution.

# 5.7.4 Deterministic inertia loads

# Centrifugal loads

For a rigid blade rotating with its axis perpendicular to the axis of rotation, the centrifugal forces generate a simple tensile load in the blade that at radius $\mathrm { r } ^ { * }$ is given by the expression $\Omega ^ { 2 } \breve { \int } _ { r * } ^ { R } m ( r ) r d r$ R . As a result, the suctuating stresses in the blade arising from all loading sources always have a tensile bias during operation. For blade SC40 rotating at 15 rpm, the centrifugal force at the root amounts to 320 KN – approximately four times its weight.

Thrust loading causes sexible blades to desect downwind, with the result that the centrifugal forces generate blade out-of-plane moments in opposition to those due to the thrust. This reduction of the moment due to thrust loading is known as centrifugal relief. The phenomenon is non-linear, so iterative techniques are required to arrive at a solution. Greater centrifugal relief can be obtained by coning the rotor so that the blades are inclined downwind in the rrst place. A balance can be struck so that the maximum forward out-of-plane moment due to centrifugal loads in very low wind is approximately equal to the maximum rearward out-of-plane moment due to the thrust loading in combination with centrifugal loads during operation in rated wind.

# Gyroscopic loads

When an operating machine yaws, the blades experience gyroscopic loads perpendicular to the plane of rotation. Consider the point A on a rotor rotating clockwise at a speed of 훺 rad/sec, as illustrated in Figure 5.16. The instantaneous horizontal velocity component of point A due to rotor rotation is 훺z, where z is the height of the point above the hub. If the machine is yawing clockwise in plan at a speed of 훬 rad/sec, then it can be shown that point A accelerates at 2훺훬z towards the wind, assuming the rotor is rigid. Integrating the resulting inertial force over the blade length gives the following expression for the blade out-of-plane bending moment about the shaft axis:

$$
M _ {Y} = \int_ {0} ^ {R} 2 \Omega \Lambda z r. m (r) d r = 2 \Omega \Lambda \cos \psi \int_ {0} ^ {R} r ^ {2} m (r) d r = 2 \Omega \Lambda \cos \psi . I _ {B} \tag {5.23}
$$

where $I _ { \mathrm { B } }$ is the blade inertia about the shaft axis.

As an example, consider an 80 m diameter machine with SC40 blades yawing at one degree per second during operation at 15 rpm. The blade inertia about the shaft axis is 3000 Tm2 , so the maximum value of $M _ { Y }$ is $2 ( \pi / 2 ) ( 0 . 0 1 7 5 ) 3 0 0 0 = 1 6 4 \mathrm { K N m }$ . This is only about a 20th of the maximum out-of-plane moment due to aerodynamic loads.

# Braking loads

Rotor deceleration due to mechanical braking introduces edgewise blade bending moments that are additive to the gravity moments on a descending blade.

# Teeter loads

Blade out-of-plane root bending moments can be eliminated entirely by mounting each blade on a hinge so that it is free to rotate in the fore–aft direction. Although centrifugal forces are effective in controlling the cone angle of each blade at normal operating speeds, the need for alternative restraints during start-up and shut-down means that such hinges are rarely used. However, in the case of two bladed machines, it is convenient to mount the whole rotor on a single shaft hinge allowing fore–aft rotation or ‘teetering’, and this arrangement is frequently adopted to reduce out-of-plane bending moment suctuations at the blade root and to prevent the transmission of blade out-of-plane moments to the low-speed shaft. As teetering is essentially a dynamic phenomenon, consideration of teeter behaviour is deferred to Section 5.8.

# 5.7.5 Stochastic aerodynamic loads: analysis in the frequency domain

As noted in Section 5.7.1, the random loadings on the blade due to short-term wind speed suctuations are known as stochastic aerodynamic loads. The wind speed suctuations about the mean at a Sxed point in space are characterised by a probability distribution – which, for most purposes, can be assumed to be normal – and by a power spectrum that describes how the energy of the suctuations is distributed between different frequencies (see Sections 2.6.3 and 2.6.4).

![](images/107c047a3c4e2fa0ef8d23b5f116bb22bb3dd60cc6b22c6d84e1c919a5a211af.jpg)  
= Speed of rotor rotation   
= Speed of yawing

Figure 5.16 Gyroscopic acceleration of a point on a yawing blade.

The stochastic loads are most conveniently analysed in the frequency domain, but to facilitate this, it is usual to assume a linear relation between the suctuation, u, of the wind speed incident on the aerofoil and the resultant loadings. This is a reasonable assumption for an unstalled blade at high tip speed ratio, as will be shown. The suctuating aerodynamic lift per unit length, L, is $\scriptstyle { \frac { 1 } { 2 } } { \bar { \rho } } W ^ { 2 } C _ { L } c$ , where W is the air velocity relative to the blade, $C _ { L }$ is the lift coefrcient, and the drag term is ignored. See Figure 3.14. Because the sow angle, $\phi ,$ is small at high tip speed ratio, $\lambda ,$ , the relative air velocity, W, can be assumed to be changing much more slowly with the wind speed than $C _ { L }$ , so that dW/du can be ignored. As a result,

$$
\frac {d L}{d u} = \frac {1}{2} \rho W ^ {2} c \frac {d C _ {L}}{d \alpha} \frac {d \alpha}{d u} \text {   where   } \alpha , \text {   the   angle   of   attack   } = \phi - \beta \tag {5.24}
$$

If the blades are not pitching, then the local blade twist, $\beta ,$ is constant, so that $d \alpha / d u = d \phi / d u$ . To preserve linearity, it is necessary to assume that the rate of change of lift coefrcient with angle of attack, $d C _ { L } / d \alpha$ is constant, which is tenable only if the blade remains unstalled. Assuming for simplicity that the wake is frozen, i.e. that the induced velocity, ${ \overline { { U } } } a .$ , remains constant, despite the wind speed suctuations, u, we obtain

$$
\tan \phi \cong (\overline {{U}} (1 - a) + u) / \Omega r
$$

so that, for $\phi$ small,

$$
\frac {d \phi}{d u} \cong \frac {1}{\Omega r} \quad \text { and } W \cong \Omega r, \text { leading   to }
$$

$$
\Delta L = L - \overline {{L}} = u \frac {d L}{d u} = \frac {1}{2} \rho (\Omega r) ^ {2} c \frac {d C _ {L}}{d \alpha} \frac {u}{\Omega r} = \frac {1}{2} \rho \Omega r c \frac {d C _ {L}}{d \alpha} u \tag {5.25}
$$

Hence

$$
\sigma_ {L} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) r c \sigma_ {u}
$$

Theoretically the slope of the lift curve $\frac { d C _ { L } } { d \alpha }$ dCL is $2 \pi$ , but in practice it is about 6.0 – see Appendix A3.7.

If the turbulence integral length scale is large compared to the blade radius, then the expression for the standard deviation of the blade root fore–aft bending moment – assuming a completely rigid blade – approximates to

$$
\sigma_ {M} = \int_ {0} ^ {R} \sigma_ {L} r d r = \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \sigma_ {u} \int_ {0} ^ {R} c (r). r ^ {2} d r \tag {5.26}
$$

where $\sigma _ { u }$ is the standard deviation of the wind speed incident on the rotor disc, which, by virtue of the ‘frozen wake’ assumption (see Section 4.4.1), equates to the standard deviation of the wind speed in the undisturbed sow. Note that the expression for $\sigma _ { M }$ in Eq. (5.26) should include the cosine of the sow angle, $\phi ,$ but this is assumed to approximate to unity, as $\phi$ is small.

If, as will be the case in practice, the longitudinal wind suctuations are not perfectly correlated along the length of the blade, then

$$
\sigma_ {M} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \kappa_ {u} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}) r _ {1} ^ {2} r _ {2} ^ {2} d r _ {1} d r _ {2} \tag {5.27}
$$

where $\kappa _ { u } ( r _ { 1 } , r _ { 2 } , 0 )$ is the cross-correlation function $\kappa _ { u } ( r _ { 1 } , r _ { 2 } , \tau )$ between the wind suctuations at radii $r _ { 1 }$ and $r _ { 2 }$ with the time lag 휏 set equal to zero, i.e.

$$
\kappa_ {u} (r _ {1}, r _ {2}, 0) = \left[ \frac {1}{T} \int_ {0} ^ {T} u (r _ {1}, t) u (r _ {2}, t) d t \right] \tag {5.28}
$$

In reality, of course, the blade will not be completely rigid, so the random wind loading will excite the natural modes of blade vibration. To quantify these excitations, it is rrst necessary to know the energy content of the incident wind suctuations as seen by each point on the rotating blade at the blade natural frequencies – information that is provided by the ‘rotationally sampled spectrum’. This spectrum is signircantly different from the rxed-point spectrum, because a rotating blade will often slice through an individual gust (derned as a volume of air travelling at above average speed) several times, as the gust dimensions are frequently large compared with the distance travelled by the air in one turbine revolution. This phenomenon, known as gust slicing, considerably enhances the frequency content at the rotational frequency, and, to a lesser extent, at its harmonics also.

The method for deriving the rotational spectrum is described below. The dynamic response of a sexible blade to random wind loading is explored in Section 5.8.

# Rotationally sampled spectrum

The derivation of the power spectrum of the wind seen by a point on a rotating blade is based on the Fourier transform pairs:

$$
S _ {u} (n) = 4 \int_ {0} ^ {\infty} \kappa_ {u} (\tau) \cos 2 \pi n \tau d \tau \tag {5.29}
$$

$$
\kappa_ {u} (\tau) = \int_ {0} ^ {\infty} S _ {u} (n) \cos 2 \pi n \tau d n \tag {5.30}
$$

where $S _ { u } ( n ) \mathrm { i s }$ the single-sided spectrum of wind speed suctuations at a rxed point in terms of frequency in Hz. Firstly, the latter equation is used to obtain the auto-correlation function, $\kappa _ { u } ( \tau )$ , for the along-wind turbulent suctuations at a rxed point in space from the corresponding power spectrum. Secondly, $\kappa _ { u } ( \tau ) \mathrm { i s }$ s used to derive the related auto-correlation function, $\kappa _ { u } ^ { o } ( r , \tau )$ , for a point on the rotating blade at radius r. Finally this function is transformed using Eq. (5.29) to yield the rotationally sampled spectrum. The three steps are set out in more detail below. Note that three key simplifying assumptions are made – that the turbulence is homogeneous and isotropic, and that the sow is incompressible.

Step 1 – Derivation of the auto-correlation function at a Sxed point: The von Karman spectrum is chosen as the input spectrum, because it is isotropic and homogeneous and analytic expressions exist for the correlations. The power spectrum of the along-wind wind speed suctuations at a rxed point in space is given by Eq. (2.25):

$$
\frac {S _ {u} (n)}{\sigma_ {u} ^ {2}} = \frac {4 L / \overline {{U}}}{(1 + 7 0 . 8 (n L / \overline {{U}}) ^ {2}) ^ {\frac {5}{6}}} \tag {5.31}
$$

where L is the integral length scale of the longitudinal component of turbulence in the longitudinal direction (i.e. $L _ { 2 u }$ or $^ { x } L _ { u } ,$ as derned in Section 2.6.4). It can be shown that Eq. (5.30) yields the following expression for the corresponding auto-correlation function:

$$
\kappa_ {u} (\tau) = \frac {2 \sigma_ {u} ^ {2}}{\Gamma \left(\frac {1}{3}\right)} \left(\frac {\tau / 2}{T ^ {\prime}}\right) ^ {\frac {1}{3}} K _ {1 / 3} \left(\frac {\tau}{T ^ {\prime}}\right) \tag {5.32}
$$

where $T ^ { \prime }$ is related to the integral length scale, L, by the formula

$$
T ^ {\prime} = \frac {\Gamma \left(\frac {1}{3}\right)}{\Gamma \left(\frac {5}{6}\right) \sqrt {\pi}} \frac {L}{\overline {{U}}} \cong 1. 3 4 \frac {L}{\overline {{U}}} \tag {5.33}
$$

Γ() is the Gamma function and $K _ { 1 _ { / 3 } } ( x )$ is a modired Bessel function of the second kind and order $\upsilon = { ^ { 1 } / 3 }$ . See eqs. (13.5) and (13.6) in Harris and Deaves (1980), with the cross-correlation function converted to an auto-correlation function by setting the spatial separation, 휆, of the two points considered to zero. The general dernition of $K _ { \upsilon } ( x )$ is as follows:

$$
K _ {v} (x) = \frac {\pi}{2 \sin \pi v} \sum_ {m = 0} ^ {\infty} \frac {(x / 2) ^ {2 m}}{m !} \left[ \frac {(x / 2) ^ {- v}}{\Gamma (m - v + 1)} - \frac {(x / 2) ^ {v}}{\Gamma (m + v + 1)} \right] \tag {5.34}
$$

[Note: Better approximations for $K _ { \upsilon } ( x )$ exist – see Abramowitz and Stegun (1958). Also, Bessel functions are available as built-in functions in computer programmes such as MATLAB.]

Step 2 – Derivation of the auto-correlation function at a point on the rotating blade: This derivation makes use of Taylor’s ‘frozen turbulence’ hypothesis, by which the instantaneous wind speed at point C at time $t = \tau$ is assumed to be equal to that at a point B a distance $\overline { { U } } \tau$ upwind of C at time $t = 0$ , U being the mean wind speed. Thus, referring to Figure 5.17a, the auto-correlation function $\kappa _ { u } ^ { o } ( r , \tau )$ for the along-wind wind suctuations seen by a point Q at radius r on the rotating blade is equal to the cross-correlation function $\kappa _ { u } ( \vec { s } , 0 )$ between the simultaneous along-wind wind suctuations at points A and B. Here A and $\textrm { C }$ are the positions of point Q at the beginning and end of time interval $\tau ,$ respectively, B is $\overline { { U } } \tau$ upwind of $\mathrm { C } ,$ and $\vec { \mathbf { \nabla } } _ { \vec { S } } ^ { }$ is the vector BA. (Note that the superscript o denotes that the auto-correlation function relates to a point on a rotating blade rather than a rxed point. The same convention will be adopted in relation to power spectra.)

Batchelor (1953) has shown that, if the turbulence is assumed to be homogeneous and isotropic, the cross-correlation function, $\kappa _ { u } ( \vec { s } , 0 )$ , is given by

$$
\kappa_ {u} (\overrightarrow {s}, 0) = (\kappa_ {L} (s) - \kappa_ {T} (s)) \left(\frac {s _ {1}}{s}\right) ^ {2} + \kappa_ {T} (s) \tag {5.35}
$$

where $\kappa _ { L } ( s )$ is the cross-correlation function between velocity components at points A and B, s apart, in a direction parallel to AB $( v _ { L } ^ { A }$ and $v _ { L } ^ { B }$ in Figure 5.17a), and $ \kappa _ { T } ( s ) \mathrm { i s }$ the corresponding function for velocity components $( v _ { T } ^ { A }$ and $v _ { T } ^ { B } )$ in a direction perpendicular to AB. $s _ { 1 }$ is the separation of points A and B measured in the along-wind direction $\mathrm { ~ - ~ i . e . ~ } \overline { { U } } \tau$ . The variation of the cross-correlation functions 휅L(s)and $\kappa _ { T } ( s )$ )with separation distance, $s ,$ is shown in Figure 5.17b, with the separation distance normalised by the integral length scale of the longitudinal component of turbulence in the longitudinal direction, $L ( = ^ { x } L _ { u } )$ . Note that the integral length scale of the longitudinal component of turbulence in the transverse directions is 0.5 L.

As the distance between points A and C on the rotor disc is 2rsin(훺휏/2), we have

$$
s ^ {2} = \overline {{{U}}} ^ {2} \tau^ {2} + 4 r ^ {2} \sin^ {2} (\Omega \tau / 2) \tag {5.36}
$$

Hence

$$
\kappa_ {u} (\vec {s}, 0) = \kappa_ {L} (s) \left(\frac {\overline {{{U}}} \tau}{s}\right) ^ {2} + \kappa_ {T} (s) \left[ 1 - \left(\frac {\overline {{{U}}} \tau}{s}\right) ^ {2} \right] = \kappa_ {L} (s) \left(\frac {\overline {{{U}}} \tau}{s}\right) ^ {2} + \kappa_ {T} (s) \left(\frac {2 r \sin (\Omega \tau / 2)}{s}\right) ^ {2} \tag {5.37}
$$

For incompressible sow, it can also be shown (Batchelor 1953) that

$$
\kappa_ {T} (s) = \kappa_ {L} (s) + \frac {s}{2} \frac {d \kappa_ {L} (s)}{d s} \tag {5.38}
$$

Substitution of Eq. (5.38) in Eq. (5.37) gives

$$
\kappa_ {u} (\overrightarrow {s}, 0) = \kappa_ {L} (s) + \frac {s}{2} \frac {d \kappa_ {L} (s)}{d s} \left(\frac {2 r \sin (\Omega \tau / 2)}{s}\right) ^ {2} \tag {5.39}
$$

When the vector $\vec { s }$ is in the along-wind direction, $\kappa _ { L } ( s )$ translates to $\kappa _ { u } ( s _ { 1 } )$ , which, by Taylor’s ‘frozen turbulence’ hypothesis, equates to the auto-correlation function at a rxed point, $\kappa _ { u } ( \tau )$ [Eq. (5.32)], with $\tau = s _ { 1 } / \overline { { U } }$ . Thus,

$$
\kappa_ {L} (s _ {1}) = \frac {2 \sigma_ {u} ^ {2}}{\Gamma \left(\frac {1}{3}\right)} \left(\frac {s _ {1} / 2}{T ^ {\prime} \overline {{U}}}\right) ^ {\frac {1}{3}} K _ {1 / 3} \left(\frac {s _ {1}}{T ^ {\prime} \overline {{U}}}\right) \tag {5.40}
$$

Because the turbulence is assumed to be isotropic, $\kappa _ { L } ( s )$ is independent of the direction of the vector $\vec { \mathbf { \nabla } } _ { \vec { S } } ^ { }$ , so we can write, with the aid of Eq. (5.33):

$$
\kappa_ {L} (s) = \frac {2 \sigma_ {u} ^ {2}}{\Gamma \left(\frac {1}{3}\right)} \left(\frac {s / 2}{T ^ {\prime} \overline {{U}}}\right) ^ {\frac {1}{3}} K _ {1 / 3} \left(\frac {s}{T ^ {\prime} \overline {{U}}}\right) = \frac {2 \sigma_ {u} ^ {2}}{\Gamma \left(\frac {1}{3}\right)} \left(\frac {s / 2}{1 . 3 4 L}\right) ^ {\frac {1}{3}} K _ {1 / 3} \left(\frac {s}{1 . 3 4 L}\right) \tag {5.41}
$$

Noting that $\frac { d } { d x } [ x ^ { \upsilon } K _ { \upsilon } ( x ) ] = - x ^ { \upsilon } K _ { ( 1 - \upsilon ) } ( x )$ , the following expression for the auto-correlation function for the along-wind suctuations at a point at radius r on the rotating blade is obtained by substituting Eq. (5.41) in Eq. (5.39):

$$
\begin{array}{l} \kappa_ {u} ^ {o} (r, \tau) = \kappa_ {u} (\overrightarrow {s}, 0) = \frac {2 \sigma_ {u} ^ {2}}{\Gamma \left(\frac {1}{3}\right)} \bigg (\frac {s / 2}{1 . 3 4 L} \bigg) ^ {\frac {1}{3}} \\ \times \left[ K _ {1 / 3} \left(\frac {s}{1 . 3 4 L}\right) - \frac {s}{2 (1 . 3 4 L)} K _ {2 / 3} \left(\frac {s}{1 . 3 4 L}\right) \left(\frac {2 r \sin (\Omega \tau / 2)}{s}\right) ^ {2} \right] \tag {5.42} \\ \end{array}
$$

where s is derned in terms of 휏 by Eq. (5.36) above.

![](images/b3d10217039ffb85dd04af6df77e8defebcf020df03a488b32bdc715d404c6e3.jpg)  
Figure 5.17 (a) Geometry for the derivation of the velocity auto-correlation function for a point on a rotating blade. (b) Cross-correlation functions for velocity suctuations at points A and B – parallel and perpendicular to AB.

Step 3 – Derivation of the power spectrum seen by a point on the rotating blade: The rotationally sampled spectrum is obtained by taking the Fourier transform of $\kappa _ { u } ^ { o } ( r , \tau )$ （ from Eq. (5.42):

$$
S _ {u} ^ {0} (n) = 4 \int_ {0} ^ {\infty} \kappa_ {u} ^ {o} (r, \tau) \cos 2 \pi n \tau d \tau
$$

$$
= 2 \int_ {- \infty} ^ {\infty} \kappa_ {u} ^ {o} (r, \tau) \cos 2 \pi n \tau d \tau \text {   as   } \kappa_ {u} ^ {o} (r, \tau) = \kappa_ {u} ^ {o} (r, - \tau) \tag {5.43}
$$

As no analytical solution has been found for the integral, a solution has to be obtained numerically using a discrete Fourier transform (DFT). First the limits of integration are reduced $\mathrm { t o } - T / 2 , + T / 2$ , as $\kappa _ { \mathrm { u } } ^ { \mathrm { o } } ( r ,$ 휏) tends to zero for large 휏. Then the limits of integration are altered to 0, T with $\kappa _ { \mathrm { u } } ^ { \mathrm { o } } ( r , \ \tau )$ set equal to $\kappa _ { u } ^ { o } ( r , T - \tau )$ for $\tau > T / 2$ , as $\kappa _ { \mathrm { u } } ^ { \mathrm { o } } ( r , \ \tau )$ is now assumed to be periodic with period T. Thus,

$$
S _ {u} ^ {o} (n) = 2 \int_ {0} ^ {T} \kappa_ {u} ^ {* o} (r, \tau) \cos 2 \pi n \tau d \tau \tag {5.44}
$$

where the asterisk denotes that $\kappa _ { u } ^ { o } ( r , ~ \tau )$ is ‘resected’ for $\mathrm { T } > \mathrm { T } / 2$ . The DFT then becomes

$$
S _ {u} ^ {o} (n _ {k}) = 2 T \left[ \frac {1}{N} \sum_ {p = 0} ^ {N - 1} \kappa_ {u} ^ {* o} (r, p T) \cos {(2 \pi k p / N)} \right] \tag {5.45}
$$

Here, N is the number of points taken in the time series of $\kappa _ { u } ^ { \ast o } ( r , p T )$ , and the power spectral density is calculated at the frequencies $\mathrm { n _ { k } } = k / T$ for $k = 0 , 1 , 2 ~ \ldots ~ N - 1$ . The expression in square brackets can be evaluated using a standard fast Fourier transform (FFT), provided N is chosen equal to a power of 2. Clearly N should be as large as possible if a wide range of frequencies is to be covered at high resolution. Just as $\kappa _ { u } ^ { \ast o } ( r , \tau )$ is symmetrical about $T / 2 .$ , the values of $S _ { u } ^ { o } ( n _ { k }$ )obtained from the FFT are symmetrical about the mid-range frequency of $N / ( 2 T )$ , and the values above this frequency have no real meaning. Moreover, the values of power spectral density calculated by the DFT at frequencies approaching $N / ( 2 T )$ will be in error as a result of aliasing, because these are falsely distorted by frequency components above N/(2T) which contribute to the $\kappa _ { u } ^ { \ast o } ( r , p T )$ series. Assuming that the calculated spectral densities are valid up to a frequency of $N / ( 4 T )$ , then the selection of $T = 2 0 0$ seconds and $N = 4 0 9 6$ would enable the FFT to give useful results up to a frequency of about 5 Hz at a frequency interval of 0.005 Hz.

Example 5.2 As an illustration, results have been derived for points on a 40 m radius SC40 blade rotating at 15 rpm in a mean wind speed of 8 m/s. Following the recommendations for the use of the von Karman isotropic turbulence model in IEC 61400-1 edition 2 (1999), the isotropic integral length scale, L, is taken as 3.5 times the IEC 61400-1 turbulence scale parameter, $\varLambda _ { 1 }$ . However, $\varLambda _ { 1 }$ is taken as 42 m, as recommended in edition 3 (2005) and edition 4 (2019) for a hub height exceeding 60 m, giving $L = 1 4 7$ m. (These values compare with $A _ { 1 } = 2 1$ m and $L = 7 3 . 5$ m recommended in edition 2.) Figure 5.18 shows how the normalised auto-correlation function, $\rho _ { u } ^ { o } ( r , \tau ) \ ~ ( = \kappa _ { u } ^ { o } ( r , \tau ) / \sigma _ { u } ^ { 2 } )$ , for the longitudinal wind suctuations varies with the number of rotor revolutions at 40 m, 20 m, and 0 m radii. For $\mathrm { r } = 2 0 \mathrm { m }$ , and even more so for $r = 4 0 \mathrm { m }$ , these curves display pronounced peaks after each full revolution, when the blade may be thought of as encountering the initial gust or lull once more.

![](images/e616c7ea54cea962ca63034d9ca97908586463db5bb74bcfd13f565a59e14d60.jpg)

<details>
<summary>line</summary>

| Number of rotor revolutions | Normalised correlation functions (r = 0 m) | Normalised correlation functions (r = 20 m) | Normalised correlation functions (r = 40 m) | Normalised correlation functions (r = 73.5 m) |
| -------------------------- | ------------------------------------------ | ------------------------------------------- | ------------------------------------------- | --------------------------------------------- |
| 0                          | 1.0                                        | 1.0                                         | 1.0                                         | 1.0                                           |
| 0.5                        | ~0.85                                      | ~0.65                                       | ~0.35                                       | ~0.15                                         |
| 1.0                        | ~0.75                                      | ~0.7                                        | ~0.65                                       | ~0.2                                          |
| 1.5                        | ~0.7                                       | ~0.55                                       | ~0.3                                        | ~0.1                                          |
| 2.0                        | ~0.65                                      | ~0.55                                       | ~0.35                                       | ~0.1                                          |
| 2.5                        | ~0.6                                       | ~0.45                                       | ~0.25                                       | ~0.1                                          |
| 3.0                        | ~0.55                                      | ~0.45                                       | ~0.2                                        | ~0.1                                          |
| 3.5                        | ~0.5                                       | ~0.4                                        | ~0.15                                       | ~0.1                                          |
| 4.0                        | ~0.45                                      | ~0.35                                       | ~0.1                                        | ~0.1                                          |
| 4.5                        | ~0.4                                       | ~0.3                                        | ~0.1                                        | ~0.1                                          |
| 5.0                        | ~0.35                                      | ~0.3                                        | ~0.1                                        | ~0.1                                          |
</details>

Figure 5.18 Normalised auto-correlation and cross-correlation functions for alongwind wind suctuations as seen by points on a rotating blade at different radii.

Figure 5.19a shows the corresponding rotationally sampled power spectral density function, $R _ { u } ^ { o } ( r , n ) ~ ( = n S _ { u } ^ { o } ( r , n ) / \sigma _ { u } ^ { 2 } )$ , plotted out against frequency, n, using a logarithmic scale for the latter. It is clear that there is a substantial shift of the frequency content of the spectrum to the frequency of rotation and, to a lesser degree, to its harmonics, with the extent of the shift increasing with radius. Figure 5.19b is a repeat of Figure 5.19a, but with a logarithmic scale used on both axes.

It is instructive to consider how the various input parameters affect the shift of energy to the rotational frequency. As $\kappa _ { u } ^ { o } ( r , \tau ) = \kappa _ { u } ( \vec { s } , 0 )$ decreases monotonically with increasing s, Eq. (5.36) indicates that the depths of the troughs in this function – and hence the transfer of energy to the rotational frequency – increase roughly in proportion to the tip speed ratio, $\Omega r / \overline { { U } }$ , and will thus be most signircant for rxed-speed two bladed machines (which generally rotate faster than three bladed ones) in low wind speeds.

# Effect of reduced length scale

The effect of adopting a reduced isotropic integral length scale, L, of 73.5 m as opposed to 147 m on the auto-correlation function and the rotationally sampled power spectrum is illustrated for a radius of 40 m in Figures 5.18 and 5.20, respectively.

It is seen that, despite the more rapid attenuation of auto-correlation function, the reduction of length scale has negligible effect on the spectral peak at the rotational frequency.

# Rotationally sampled cross-spectra

The expressions for the spectra of blade bending moments and shears are normally functions of entities known as rotationally sampled cross-spectra for pairs of points along the

![](images/b21942c171daa612fcecb0796d2ac1642f00e3dc7c9b25050660340b3a7e3eb9.jpg)

<details>
<summary>line</summary>

| Frequency, n Hz, logarithmic scale | Rotationally sampled power spectral density R(r,n) for r=0 m | Rotationally sampled power spectral density R(r,n) for r=20 m (dashed line) | Rotationally sampled power spectral density R(r,n) for r=40 m |
| ---------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| 0.5                                | ~0.2                                                          | ~0.1                                                               | ~0.1                                                        |
| 0.5                                | ~0.1                                                          | ~0.1                                                               | ~0.1                                                        |
| 0.5                                | ~0.05                                                         | ~0.05                                                              | ~0.05                                                       |
| 0.5                                | ~0.03                                                         | ~0.03                                                              | ~0.03                                                       |
| 0.5                                | ~0.02                                                         | ~0.02                                                              | ~0.02                                                       |
| 0.5                                | ~0.01                                                         | ~0.01                                                              | ~0.01                                                       |
| 0.5                                | ~0.01                                                         | ~0.01                                                              | ~0.01                                                       |
| 0.5                                | ~0.01                                                         | ~0.01                                                              | ~0.01                                                       |
| 0.5                                | ~0.01                                                         | ~0.01                                                              | ~0.01                                                       |
| 0.5                                | ~0.01                                                         (final value)                                              | ~0.3                                                               | ~1.2                                                        |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.1                                                        |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.1                                                        |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.1                                                        |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.1                                                        |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.05                                                       |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.05                                                       |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.05                                                       |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~0.05                                                       |
| 10                                 | ~0.01                                                         | ~0.1                                                               | ~7.85                                                       |
Integrall length scale, L = 147 m, Mean wind speed = 8 m/s, Speed of rotation = 15 rpm, Tip speed ratio = 7.85
</details>

(a)

![](images/960366b1b3eb49dcfdf59ffaab2ca9716159c239f270c62336fb8bfba9d9c4ac.jpg)

<details>
<summary>line</summary>

| Frequency, n Hz | Rotationally sampled power spectral density R(r,n) (logarithmic scale) for r = 0 m | Rotationally sampled power spectral density R(r,n) (logarithmic scale) for r = 20 m | Rotationally sampled power spectral density R(r,n) (logarithmic scale) for r = 40 m |
| --------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 0.01            | ~0.3                                                                 | ~0.3                                                                             | ~0.3                                                                             |
| 0.1             | ~0.05                                                                 | ~0.05                                                                            | ~0.05                                                                            |
| 1               | ~0.01                                                                 | ~0.01                                                                            | ~0.01                                                                            |
| 10              | ~0.001                                                                 | ~0.001                                                                           | ~0.001                                                                           |
</details>

(b)   
Figure 5.19 (a) Rotationally sampled power spectra of longitudinal wind speed suctuations at different radii. (b) Rotationally sampled power spectra of longitudinal wind speed suctuations at different radii: log-log plot.

![](images/7252f0c6be8abcd75525c9332e37c3787223e363e6d1d7c5a4079288a479eb61.jpg)

<details>
<summary>line</summary>

| Frequency, n Hz | Rotationally sampled power spectral density R(r,n) (logarithmic scale) - L = 73.5 m (dotted line) | Rotationally sampled power spectral density R(u'(r,n)) = nS^o(u'(r,n))/σ^2_u (solid line) |
| --------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| 0.01            | ~0.1                                                                                      | ~0.1                                                                                       |
| 0.1             | ~0.01                                                                                     | ~0.01                                                                                      |
| 1               | ~0.1                                                                                      | ~0.1                                                                                       |
| 10              | ~0.01                                                                                     | ~0.01                                                                                      |
</details>

Figure 5.20 Comparison of rotationally sampled power spectra at 40 m radius for different integral length scales.

blade, which are analogous to the rotationally sampled ordinary spectra for single points described above. The cross-spectrum for a pair of points at radii $r _ { 1 }$ and $r _ { 2 }$ on a rotating blade is thus related to the corresponding cross-correlation function by the Fourier transform pair

$$
S _ {u} ^ {o} (r _ {1}, r _ {2}, n) = 4 \int_ {0} ^ {\infty} \kappa_ {u} ^ {o} (r _ {1}, r _ {2}, \tau) \cos 2 \pi n \tau d \tau \tag {5.46a}
$$

$$
\kappa_ {u} ^ {o} (r _ {1}, r _ {2}, \tau) = \int_ {0} ^ {\infty} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) \cos 2 \pi n \tau d n \tag {5.46b}
$$

Setting 휏 = 0 in Eq. (5.46b) gives

$$
\kappa_ {u} ^ {o} (r _ {1}, r _ {2}, 0) = \int_ {0} ^ {\infty} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) d n \tag {5.47}
$$

which, when substituted into the expression for the standard deviation of the blade root bending moment in Eq. (5.27), gives

$$
\sigma_ {M} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \left[ \int_ {0} ^ {\infty} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) d n \right] c (r _ {1}) c (r _ {2}) r _ {1} ^ {2} r _ {2} ^ {2} d r _ {1} d r _ {2} \tag {5.48}
$$

From this, it can be deduced that the power spectrum of the blade root bending moment is

$$
S _ {M} (n) = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) c (r _ {1}) c (r _ {2}) r _ {1} ^ {2} r _ {2} ^ {2} d r _ {1} d r _ {2} \tag {5.49}
$$

The derivation of the rotationally sampled cross-spectrum, $S _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , n )$ , exactly parallels the derivation of the rotationally sampled single-point spectrum given above, with the cross-correlation function $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , \tau )$ between the longitudinal wind suctuations at points at radii $r _ { 1 }$ and $r _ { 2 }$ on the rotating blade replacing the auto-correlation function in step 2. Here the expression for the separation distance, s, given in Eq. (5.36), is replaced by

$$
s ^ {2} = \overline {{U}} ^ {2} \tau^ {2} + r _ {1} ^ {2} + r _ {2} ^ {2} - 2 r _ {1} r _ {2} \cos \Omega \tau \tag {5.50}
$$

The expression for the cross-correlation function thus becomes:

$$
\begin{array}{l} \kappa_ {u} ^ {o} (r _ {1}, r _ {2}, \tau) = \frac {2 \sigma_ {u} ^ {2}}{\Gamma \left(\frac {1}{3}\right)} \left(\frac {s / 2}{1 . 3 4 L}\right) ^ {\frac {1}{3}} \\ \times \left[ K _ {1 / 3} \left(\frac {s}{1 . 3 4 L}\right) - \frac {s}{2 (1 . 3 4 L)} K _ {2 / 3} \left(\frac {s}{1 . 3 4 L}\right) \left(\frac {r _ {1} ^ {2} + r _ {2} ^ {2} - 2 r _ {1} r _ {2} \cos (\Omega \tau)}{s ^ {2}}\right) \right] \tag {5.51} \\ \end{array}
$$

with s derned by Eq. (5.50).

The form of the resulting normalised cross-correlation function, $\rho _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , \tau ) =$ $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , \tau ) / \sigma _ { u } ^ { 2 }$ , is illustrated in Figure 5.18 for the case considered in Example 5.2, taking $r _ { 1 } = 2 0$ m and $r _ { 2 } = 4 0 \mathrm { m }$ . In Figure 5.21, the rotationally sampled cross-spectrum for this case is compared with the rotationally sampled single-point spectra or ‘autospectra’ at these radii. It can be seen that the form of the cross-spectrum curve is similar to that of the autospectra, with a pronounced peak at the rotational frequency roughly midway between the peaks of the two autospectra. At higher frequencies, however, the cross-spectrum falls away much more rapidly.

The evaluation of the power spectrum of the blade root bending moment is, in practice, carried out using summations to approximate to the integrals in Eq. (5.49), as follows:

$$
S _ {M} (n) = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \sum_ {j} \sum_ {k} S _ {u} ^ {o} (r _ {j}, r _ {k}, n) c (r _ {j}) c (r _ {k})   r _ {j} ^ {2} r _ {k} ^ {2} (\Delta r) ^ {2} \tag {5.52}
$$

# Limitations of analysis in the frequency domain

As noted at the beginning of this section, analysis of stochastic aerodynamic loads in the frequency domain depends for its validity on a linear relationship between the incident wind speed and the blade loading. Thus the method becomes increasingly inaccurate for pitch-regulated machines as winds approach the cut-out value, and it breaks down completely for stall-regulated machines once the wind speed is high enough to cause stall. To avoid these limitations, it is necessary to carry out the analysis in the time domain.

# 5.7.6 Stochastic aerodynamic loads: analysis in the time domain

# Wind simulation

The analysis of stochastic aerodynamic loads in the time domain requires, as input, a simulated wind reld extending over the area of the rotor disc and over time. Typically, this is obtained by generating simultaneous time histories at points over the rotor disc, which have appropriate statistical properties both individually and in relation to each other. Thus, the power spectrum of each time history should conform to one of the standard power spectra (e.g. von Karman or Kaimal), and the normalised cross-spectrum (otherwise known as the coherence function) of the time histories at two different points should equate to the coherence function corresponding to the chosen power spectrum and the distance separating the points. For example, the coherence of the longitudinal component of turbulence corresponding to the Kaimal power spectrum for points j and k separated by a distance $\Delta s _ { \mathrm { j k } }$ perpendicular to the wind direction is

![](images/a3dee62f7721923346475d6f3f1fae8630c025e86d35aecfb1334dc140175532.jpg)

<details>
<summary>line</summary>

| Frequency, n Hz | Auto-spectrum for r = 40 m | Auto-spectrum for r = 20 m | Cross-spectrum for r₁ = 20 m and r₂ = 40 m (dashed line) |
| --------------- | -------------------------- | -------------------------- | -------------------------------------------------------- |
| 0.01            | ~0.2                       | ~0.2                       | ~0.2                                                     |
| 0.1             | ~0.01                      | ~0.01                      | ~0.01                                                    |
| 1               | ~0.1                       | ~0.1                       | ~0.1                                                     |
| 10              | ~0.05                      | ~0.05                      | ~0.05                                                    |
</details>

Figure 5.21 Rotationally sampled cross-spectrum of longitudinal wind speed suctuations at 20 and 40 m radii compared with auto-spectra: log-log plot.

$$
C _ {j k} (n) = C (\Delta s _ {j k}, n) = \frac {S _ {j k} (n)}{S _ {u} (n)} = \exp \left(- H. \Delta s _ {j k} \sqrt {\left(\frac {n}{U}\right) ^ {2} + \left(\frac {0 . 1 2}{L}\right) ^ {2}}\right) \tag {5.53}
$$

The constant H was specired as 8.8 in IEC 61400-1 edition 2 but increased to 12 in editions 3 and 4. The (0.12/L) term is negligible except at frequencies below 0.01 Hz. (Note that coherence is sometimes termed coherency, and that some authors derne coherence as the square of the normalised cross-spectrum.) See Section 2.6.7 for details of the coherence corresponding to the von Karman spectrum.

Three distinct approaches have been developed for generating simulation time histories as follows:

1. The transformational method, based on rltering Gaussian white noise signals.

2. The correlation method, in which the velocity of a small body of air at the end of a timestep is calculated as the sum of a velocity correlated with the velocity at the start of the timestep and a random, uncorrelated increment.   
3. The harmonic series method, involving the summation of a series of cosine waves at different frequencies with amplitudes weighted in accordance with the power spectrum.

This last method is probably now the one in widest use, and it is described in more detail below. The description is based on that given in Veers (1988).

# Wind simulation by the harmonic series method

The spectral properties of the wind speed suctuations at N points can be described by a spectral matrix, S, in which the diagonal terms are the double-sided single-point power spectral densities at each point, $S _ { k k } ( n )$ , and the off-diagonal terms are the cross-spectral densities, $S _ { j k } ( n )$ , also double-sided. This matrix is equated to the product of a triangular transformation matrix, H, and its transpose, $\mathbf { H } ^ { \mathrm { T } }$ , as follows:

$$
\left[ \begin{array}{c c c c} S _ {1 1} & S _ {2 1} & S _ {3 1} & \ldots \\ S _ {2 1} & S _ {2 2} & S _ {3 2} & \ldots \\ S _ {3 1} & S _ {3 2} & S _ {3 3} & \ldots \\ \ldots & \ldots & \ldots & S _ {N N} \end{array} \right] = \left[ \begin{array}{c c c c} H _ {1 1} & & & \\ H _ {2 1} & H _ {2 2} & & \\ H _ {3 1} & H _ {3 2} & H _ {3 3} & \\ \ldots & \ldots & \ldots & H _ {N N} \end{array} \right] \left[ \begin{array}{c c c c} H _ {1 1} & H _ {2 1} & H _ {3 1} & \ldots \\ & H _ {2 2} & H _ {3 2} & \ldots \\ & & H _ {3 3} & \ldots \\ & & & H _ {N N} \end{array} \right]
$$

resulting in a set of $N ( N + 1 ) / 2$ equations linking the elements of the S matrix to the elements of the H matrix as follows:

$$
S _ {1 1} = H _ {1 1} ^ {2} \qquad S _ {2 1} = H _ {2 1}. H _ {1 1} \qquad \qquad S _ {2 2} = H _ {2 1} ^ {2} + H _ {2 2} ^ {2} \qquad S _ {3 1} = H _ {3 1}. H _ {1 1}
$$

$$
S _ {3 2} = H _ {3 1}. H _ {2 1} + H _ {3 2}. H _ {2 2} \quad S _ {3 3} = H _ {3 1} ^ {2} + H _ {3 2} ^ {2} + H _ {3 3} ^ {2}
$$

$$
S _ {j k} = \sum_ {l = 1} ^ {k} H _ {j l}. H _ {k l} \quad S _ {k k} = \sum_ {l = 1} ^ {k} \sqrt {H _ {k l} ^ {2}} \tag {5.54}
$$

As with the elements of the S matrix, the elements of the H matrix are all double-sided functions of frequency n.

Noting that the expression for the power spectral density $S _ { k k }$ resembles that for the variance of the sum of group of k independent variables, it is apparent that the elements of the H matrix can be considered as the weighting factors for the linear combination of N independent, unit magnitude, white noise inputs to yield N correlated outputs with the correct spectral matrix. Thus the elements in the jth row of H are the weighting factors for the inputs contributing to the output at point j. The formula for the linear combination is

$$
u _ {j} (n) = \sum_ {k = 1} ^ {j} H _ {j k} (n). \Delta n. \exp (- i \theta_ {k} (n)) \tag {5.55}
$$

where $u _ { \mathrm { j } } ( n )$ is the complex coefrcient of the discretised frequency component at n Hz of the simulated wind speed at point j. The frequency bandwidth is 훥n. $\theta _ { k } ( n )$ is the phase angle associated with the n Hz frequency component at point k and is a random variable uniformly distributed over the interval 0–2휋.

The values of the weighting factors, $H _ { \mathrm { j k } }$ , which are $N ( N + 1 ) / 2$ , in number are derived from Eq. (5.54), giving:

$$
H _ {1 1} = \sqrt {S _ {1 1}} H _ {2 1} = S _ {2 1} / H _ {1 1} H _ {2 2} = \sqrt {S _ {2 2} - H _ {2 1} ^ {2}} H _ {3 1} = S _ {3 1} / H _ {1 1}, e t c. (5. 5 6)
$$

Hence

$$
u _ {1} (n) = \sqrt {S _ {1 1} (n)}. \Delta n. \exp (- i \theta_ {1} (n))
$$

$$
u _ {2} (n) = \sqrt {S _ {2 2} (n)}. \Delta n [ C _ {2 1} (n). \exp (- i \theta_ {1} (n)) + \sqrt {1 - C _ {2 1} ^ {2} (n)}. \exp (- i \theta_ {2} (n)) ], \mathrm{etc.} \tag {5.57}
$$

where $C _ { 2 1 } ( n )$ is the coherence, derned as $C _ { 2 1 } ( n ) = \frac { S _ { 2 1 } ( n ) } { \sqrt { S _ { 1 1 } ( n ) S _ { 2 2 } ( n ) } } .$

Time series for the wind speed suctuations are obtained by taking the inverse DFT of the coefrcients $u _ { \mathrm { j } } \left( n \right)$ at each point j. Lateral and vertical wind speed suctuations can also be simulated, if desired, using the same method. As an illustration, examples of time series derived by this method for two points 10 m apart are shown in Figure 5.22, based on the von Karman spectrum. The mean wind speed and integral length scale $^ x L _ { u } \mathrm { i n }$ this example are taken as 10 m/s and 73.5 m, respectively, giving an integral time scale, $x _ { L _ { u } / \overline { { U } } }$ , of 7.35 seconds.

In his 1988 paper, Veers pointed out that the computation time required can be reduced by arranging for the simulated wind speed to be calculated at each point only at those times when a blade is passing – i.e. at a frequency of 훺B/2휋, where B is the number of blades. This is achieved by applying a phase shift to each frequency component at each point of $\psi _ { j } . n . 2 \pi / \varOmega$ , where $\psi _ { j }$ is the azimuth angle of point j.

![](images/efe969793acd689011db965e4d91b62b5c566f9d547236598aac64ff62f8477c.jpg)

<details>
<summary>line</summary>

| Time (s) | Point 1 | Point 2 |
| -------- | ------- | ------- |
| 0        | 1.0     | 0.8     |
| 10       | -0.5    | -0.3    |
| 20       | 0.6     | -0.8    |
| 30       | -0.4    | -1.2    |
| 40       | -0.2    | -0.6    |
| 50       | -2.5    | -1.8    |
| 60       | 0.4     | -0.5    |
| 70       | 0.5     | 0.3     |
| 80       | -2.6    | -1.5    |
| 90       | 0.7     | -0.2    |
| 100      | -1.5    | -0.8    |
| 110      | 1.2     | 0.5     |
| 120      | 2.3     | 1.5     |
</details>

Figure 5.22 Simulated time series of wind speed suctuations at two points 10 m apart for mean wind speed of 10 m/s.

# Blade load time histories

Once the simulated wind speed time histories have been generated across the grid, the calculation of blade load histories at different radii can begin. If the wake is assumed to be ‘frozen’, then the axial induced velocity, aU, and the tangential induced velocity, a ’ Ω r, are taken as remaining constant over time, at each radius, at the values calculated for a steady wind speed of U. The instantaneous value of the sow angle, 휙, and, hence, the values of the lift and drag coefrcients, may then be calculated directly from the instantaneous value of the wind speed suctuation (including lateral and vertical components, if calculated) by means of the velocity diagram.

Alternatively, an equilibrium wake may be assumed. In this case, the induced velocities are taken to vary continuously so that the momentum equations are satisred at each blade element at all times. Obviously, this requires that these equations are solved afresh at each timestep, which is computationally much more demanding.

Neither the equilibrium wake model nor the frozen wake model provides an accurate description of wake behaviour. A better model is provided by unsteady sow theory, which assumes that there is some delay before induced velocities react to changes in the incident wind reld. See Section 4.4.

Note that, if desired, the spatial wind variations causing deterministic loading can be included in the simulated wind reld, enabling the combined deterministic and stochastic loading on the blade to be calculated in a single operation.

# 5.7.7 Extreme loads

The derivation of extreme loads should properly take into account dynamic effects, which form the subject of the next section. However, in the interests of clarity, this section will be restricted to the consideration of extreme loads in the absence of dynamic effects.

As described in Section 5.4.1, it was customary for wind turbine design codes to specify extreme operating load cases in terms of deterministic gusts. The extreme blade loadings are then evaluated at intervals over the duration of the gust, using blade element and momentum theory as described in Section 5.7.2.

Although deterministic gusts have the advantage of clarity of dernition, they are essentially arbitrary in nature. The alternative approach of employing a stochastic representation of the wind provides a much more realistic description of the wind itself, and it has been adopted to a greater extent in IEC 61400-1 editions 3 and 4. Although stochastic representation of the wind lends itself to analysis in the frequency domain, the solution is inevitably approximate because of the linearity assumptions [Eq. (5.24) et seq], so the standard specires analysis in the time domain using simulations. Nevertheless, analysis in the frequency domain can provide useful insights in the absence of stall and is considered further in the paragraphs that follow.

Normally the loading under investigation, for example, the blade root bending moment, will contain both periodic and random components. Although it is straightforward to predict the extreme values of each component independently, the prediction of the extreme value of the combined signal is quite involved. Madsen et al. (1984) have proposed the following simple, approximate approach and have demonstrated that it is reasonably accurate.

The periodic component, $z ( t )$ , is considered as an equivalent three-level square wave, in which the variable takes the maximum, mean $( \mu _ { \mathrm { z } } )$ , and minimum values of the original waveform, for proportions $\varepsilon _ { 1 } , \varepsilon _ { 2 }$ , and $\varepsilon _ { 3 }$ of the wave period, respectively. It is easy to show that

$$
\varepsilon_ {1} = \frac {\sigma_ {z} ^ {2}}{\left(z _ {\max} - \mu_ {z}\right) \left(z _ {\max} - z _ {\min}\right)}, \varepsilon_ {3} = \frac {\sigma_ {z} ^ {2}}{\left(\mu_ {z} - z _ {\min}\right) \left(z _ {\max} - z _ {\min}\right)} \tag {5.58}
$$

Extreme values of the combined signal are only assumed to occur during the proportion of the time, $\varepsilon _ { 1 }$ , for which the square wave representation of the periodic component is at the maximum value, zmax. $z _ { \mathrm { m a x } }$

Davenport (1964) gives the following formula for the extreme value of a random variable over a time interval T:

$$
\frac {x _ {\max}}{\sigma_ {x}} = \sqrt {2 \ln (\nu T)} + \frac {\gamma}{\sqrt {2 \ln (\nu T)}} \tag {5.59}
$$

where 휈 is the zero up-crossing frequency (i.e. the number of times per second the variable changes from negative to positive) given by Eq. (A5.46) and $\gamma = 0 . 5 7 7 2$ (Euler’s constant). Thus, the extreme value of the combined periodic and random components is taken to be

$$
z _ {\max} + x _ {\max} = z _ {\max} + \sigma_ {x} \left(\sqrt {2 \ln (\nu \varepsilon_ {1} T)} + \frac {\gamma}{\sqrt {2 \ln (\nu \varepsilon_ {1} T)}}\right) = z _ {\max} + g _ {1}. \sigma_ {x} \tag {5.60}
$$

where $g _ { 1 }$ is termed the peak factor.

The variation of $x _ { \mathrm { m a x } } / \sigma _ { x }$ with exposure time, T, is shown in Table 5.4 for a zero up-crossing frequency of 1 Hz. The periodic component is assumed to be a simple sinusoid, giving $\varepsilon _ { 1 } = 0 . 2 5$ .

The method for determining the extreme load described above has to be applied with caution when the wind suctuations exceed the rated wind speed. In the case of a stall-regulated machine, the linearity assumption breaks down completely, invalidating the method. With pitch-regulated machines, however, the blade pitch will respond to wind suctuations at frequencies below, say, half the rotor rotational frequency to limit power, causing a parallel reduction in blade loading. This will modify the spectrum of blade loading dramatically, effectively removing the frequency components below the pitch system cut-off frequency and consequently reducing the magnitude of $\sigma _ { \mathrm { x } }$ to be substituted in Eq. (5.60).

To illustrate the method, the procedure for calculating the extreme sapwise blade root bending moment of a pitch-regulated machine operating at rated wind speed is described as follows:

Table 5.4 Extreme values of random component for different exposure times. 

<table><tr><td>T</td><td>1 min</td><td>10 min</td><td>1 h</td><td>10 h</td><td>100 h</td><td>1000 h</td><td>1 yr</td></tr><tr><td>T (secs)</td><td>60</td><td>600</td><td>3600</td><td>36000</td><td>360000</td><td>3600,000</td><td>31536000</td></tr><tr><td> $\varepsilon_1$  T (secs)</td><td>15</td><td>150</td><td>900</td><td>9000</td><td>90000</td><td>900000</td><td>7884000</td></tr><tr><td> $x_{\text{max}}/\sigma_x$ </td><td>2.57</td><td>3.35</td><td>3.84</td><td>4.40</td><td>4.90</td><td>5.35</td><td>5.74</td></tr></table>

1. Eq. (5.48) for the standard deviation of the random component of blade root bending moment is rrst modired to eliminate the contribution of frequencies below half the rotational speed to account for the blade pitching response, and then discretised to give

$$
\sigma_ {M} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \sum_ {j = 1} ^ {m} \sum_ {k = 1} ^ {m} \left[ \int_ {\Omega / 2} ^ {\infty} S _ {u} ^ {o} (r _ {j}, r _ {k}, n) d n \right] c (r _ {j}) c (r _ {k}) r _ {j} ^ {2} r _ {k} ^ {2}. (\Delta r) ^ {2} \tag {5.61}
$$

Here the blade is assumed to be divided up into m sections of equal length $\Delta r = R / m$ .

2. After evaluation of the integrals of the $m ( m + 1 ) / 2$ different curtailed rotational spectra, the standard deviation of the blade root bending moment is obtained from Eq. (5.61).

3. The time, T, that the machine spends in a wind speed band centred on the rated wind speed is estimated using the Weibull curve and multiplied in turn by the factor $\varepsilon _ { 1 }$ appropriate to the waveform of the periodic component of blade root bending moment and by the zero up-crossing frequency of the random root bending moment suctuations, to give the effective number of peaks, $\nu \varepsilon _ { 1 } T .$ .

4. The predicted extreme value of the total moment is calculated by substituting the standard deviation of the blade root bending moment, $\sigma _ { \mathrm { M } } ( = \sigma _ { \mathrm { x } } )$ , the effective number of peaks, $\nu \varepsilon _ { 1 } T ,$ , and the extreme value of the periodic moment into Eq. (5.60).

In the case of a machine with a rated wind speed of 13 m/s operating at a site with an annual mean of 7 m/s, the expected proportion of the time spent operating within a 2 m/s wide band centred on the rated wind speed is 5.6%. Taking the machine lifetime as 20 years, a zero up-crossing frequency equal to the rotational speed of 15 rpm (0.25 Hz) and $\varepsilon _ { 1 } = 0 . 2 5$ , this results in a peak factor, $g _ { 1 }$ , of 5.5. For the 80 m diameter machine considered in Section 5.7.2, a turbulence intensity of 20%, and a turbulence isotropic length scale of 147 m, the standard deviation of the random component of blade root bending moment given by Eq. (5.60) is 315 kNm, resulting in a peak value of about 1730 KNm. This compares with the extreme value of the periodic component, including wind shear, of about 1830 KNm. It should be emphasised that the peak value of the random component quoted is a theoretical one – i.e. it assumes the linearity assumptions are maintained even for the large wind speed suctuation needed to generate this moment. In practice, a machine operating in a steady wind speed equal to rated is usually not all that far from stall, so the larger suctuations may induce stall. In this example, the square root of the weighted mean of the integrals of all of the curtailed rotational spectra is about $0 . 5 \sigma _ { u } ,$ so the idealised uniform wind speed suctuation equivalent to the extreme root moment is about $0 . 2 0 \times 1 3 \times 0 . 5 \times 5 . 5 = 7 . 2 \mathrm { m / s }$ .

The method outlined above has more validity at higher wind speeds, when the blades are pitched back and are operating further away from stall. However, it is important to note that the other linearity assumption used in deriving Eq. (5.26), namely, that $\phi$ is small, becomes increasingly in error.

It will be now be evident that the calculation of stochastic extreme loads is fraught with difrculties because non-linearities are likely to arise as the extremes are approached. In so far as lift forces ‘saturate’ due to stall, or even drop back, as wind speed increases, a crude and simple approach to extreme out-of-plane operational loads is to calculate an upper bound based on the maximum lift coefrcient for the local aerofoil section and the relative air velocity, W. The induction factors will be small and can be ignored.

The most sophisticated approach, however, is to analyse the loads generated by a simulated wind reld. As computing costs normally restrict the length of simulated ‘campaigns’ to a few hundred seconds or less, statistical methods have to be used to extrapolate from the extreme values of loadings calculated during the campaign to the extreme values to be expected over the machine design life.

One method, which is discussed by Thomsen and Madsen (1997), is to use Eq. (5.60) with T set equal to the appropriate exposure period over the machine design life, and values of $z _ { \mathrm { m a x } }$ and $\sigma _ { \mathrm { x } }$ abstracted from the simulation time history with the aid of azimuthal binning to separate the periodic and stochastic components. The danger of this approach with simulations of short duration is that the azimuthal binning process treats some load suctuations due to the slicing of low frequency gusts as periodic rather than stochastic, so that the standard deviation of the stochastic component, $\sigma _ { \mathrm { x } } ,$ is underestimated.

Extrapolation techniques are considered further in Section 5.14.

# 5.8 Blade dynamic response

# 5.8.1 Modal analysis

Although dynamic loads on the blades will, in general, also excite the tower dynamics, tower head motion will initially be excluded from consideration to focus on the blade dynamic behaviour itself. The treatment is further limited to the response of blades in unstalled sow because of the inherent difrculty in predicting stalled behaviour.

The equation of motion for a blade element at radius r subject to a time-varying load q(r,t) per unit length in the out-of-plane direction is

$$
m (r) \ddot {x} + \hat {c} (r) \dot {x} + \frac {\partial^ {2}}{\partial r ^ {2}} \left[ E I (r) \frac {\partial^ {2} x}{\partial r ^ {2}} \right] = q (r, t) \tag {5.62}
$$

where the terms on the left hand side are the loads on the element due to inertia, damping, and sexural stiffness, respectively. I(r) is the second moment of area of the blade cross-section about the weak principal axis (which for this purpose is assumed to lie in the plane of rotation), and x is the out-of-plane displacement. The expressions m(r) and ĉ(r) denote mass per unit length and damping per unit length, respectively.

The dynamic response of a cantilever blade to the suctuating aerodynamic loads upon it is most conveniently investigated by means of modal analysis, in which the excitations of the various different natural modes of vibration are computed separately and the results superposed, as follows:

$$
x (t, r) = \sum_ {j = 1} ^ {\infty} f _ {j} (t) \mu_ {j} (r) \tag {5.63}
$$

where $\mu _ { \mathrm { i } } \left( r \right)$ is the jth mode shape, arbitrarily assumed to have a value of unity at the tip, and $f _ { \mathrm { j } } \left( t \right)$ is the variation of jth mode tip displacement with time. Eq. (5.62) then becomes

$$
\sum_ {j = 1} ^ {\infty} \left\{m (r) \mu_ {j} (r) \ddot {f} _ {j} (t) + \hat {c} (r) \mu_ {j} (r) \dot {f} _ {j} (t) + \frac {d ^ {2}}{d r ^ {2}} \left[ E I (r) \frac {d ^ {2} \mu_ {j} (r)}{d r ^ {2}} \right] f _ {j} (t) \right\} = q (r, t) \tag {5.64}
$$

For low levels of damping, the beam natural frequencies are given by

$$
m (r) \omega_ {j} ^ {2} \mu_ {j} (r) = \frac {d ^ {2}}{d r ^ {2}} \left[ E I (r) \frac {d ^ {2} \mu_ {j} (r)}{d r ^ {2}} \right] \tag {5.65}
$$

so Eq. (5.64) becomes

$$
\sum_ {j = 1} ^ {\infty} \left\{m (r) \mu_ {j} (r) \ddot {f} _ {j} (t) + \hat {c} (r) \mu_ {j} (r) \dot {f} _ {j} (t) + m (r) \omega_ {j} ^ {2} \mu_ {j} (r) f _ {j} (t) \right\} = q (r, t) \tag {5.66}
$$

Multiplying both sides by $\mu _ { \mathrm { i } } ( r )$ and integrating over the length of the blade, R, gives:

$$
\begin{array}{l} \sum_ {j = 1} ^ {\infty} \left\{\int_ {0} ^ {R} m (r) \mu_ {i} (r) \mu_ {j} (r) \ddot {f} _ {j} (t) d r + \int_ {0} ^ {R} \hat {c} (r) \mu_ {i} (r) \mu_ {j} (r) \dot {f} _ {j} (t) d r + \int_ {0} ^ {R} m (r) \omega_ {j} ^ {2} \mu_ {i} (r) \mu_ {j} (r) f _ {j} (t) d r \right\} \\ = \int_ {0} ^ {R} \mu_ {i} (r) q (r, t) d r \tag {5.67} \\ \end{array}
$$

The undamped mode shapes are orthogonal as a result of Bettis’s law (Clough and Penzien 1993), so they satisfy the orthogonality condition:

$$
\int_ {0} ^ {R} m (r) \mu_ {i} (r) \mu_ {j} (r) d r = 0 \quad \text { for } i \neq j \tag {5.68}
$$

If we assume that the variation of the damping per unit length along the blade, ĉ (r), is proportional to the variation in mass per unit length, m(r), i.e. $\hat { c } ( r ) { = } \mathrm { a } . m ( r )$ , then

$$
\int_ {0} ^ {R} \hat {c} (r) \mu_ {i} (r) \mu_ {j} (r) d r = 0 \quad \text { for } i \neq j \tag {5.69}
$$

As a result, all the cross-terms on the left hand side of Eq. (5.67) drop out, and it reduces to

$$
m _ {i} \ddot {f} _ {i} (t) + c _ {i} \dot {f} _ {i} (t) + m _ {i} \omega_ {i} ^ {2} f _ {i} (t) = \int_ {0} ^ {R} \mu_ {i} (r) q (r, t) d r \tag {5.70}
$$

where $\begin{array} { r } { m _ { i } = \int _ { 0 } ^ { R } m ( r ) \mu _ { i } ^ { 2 } ( r ) d r } \end{array}$ and is known as the generalised mass, $\begin{array} { r } { c _ { i } = \int _ { 0 } ^ { R } \hat { c } ( r ) \mu _ { i } ^ { 2 } ( r ) d r } \end{array}$ , and $\begin{array} { r } { \int _ { 0 } ^ { R } \mu _ { i } ( r ) q ( r , t ) d r = Q _ { i } ( t ) } \end{array}$ is termed the generalised Tuctuating load with respect to the ith mode. Eq. (5.70) is the fundamental equation governing modal response to time-varying loading.

![](images/f011388fbb280cee2a963f349f53f232ff5abc833c30af982b2b4f4d6bd422ce.jpg)

<details>
<summary>text_image</summary>

Nacelle
Blade tip –
deflected position
Blade tip –
undeflected position
Blade section
with maximum twist
P
β
δ₁₂
δ₁₁
Weak principle axis
</details>

Figure 5.23 Desection of tip due to sapwise bending of twisted blade (viewed along blade axis).

Blade sexural vibrations occur in both the sapwise and edgewise directions (i.e. about the weak and strong principal axes, respectively). Blades are typically twisted some $1 5 ^ { 0 }$ , so the weak principal axis does not, in general, lie in the plane of rotation as assumed above. Consequently, blade sexure about one principal axis inevitably results in some blade movement perpendicular to the other. This is illustrated in Figure 5.23, in which the maximum blade twist near the root has been exaggerated for clarity. Point P represents the undesected position of the blade tip, point Q represents the desected position as a result of sexure about the weak principal axis, and the line between them is built up of the contributions to the tip desection made by sexure of each element along the blade, $M ( R - r ) \Delta r / E I$ .

The interaction between sexure about the two principal axes can be explored with the help of some simplifying assumptions. If M varies as $( R - r )$ for the rrst mode and I varies as $( R { - } r ) ^ { 2 }$ , then each of the tip desection contributions referred to above are equal, so that, for a linear twist distribution, the line PQ is the arc of a circle. If the twist varies between zero at the tip and a maximum value of $\beta$ towards the root, then the tip desection, $\delta _ { 1 2 }$ , in the direction of the weak principal axis, at the blade section with maximum twist, is $\beta / 2$ times the tip desection, $\delta _ { 1 1 }$ , perpendicular to this axis. Hence in the case of $\beta = 1 5 ^ { 0 }$ , the ratio $\delta _ { 1 2 } / \delta _ { 1 1 }$ approximates to 0.13, with the result that blade rrst mode sapwise oscillations will result in some relatively small simultaneous edgewise inertia loadings. These will not excite signircant edgewise oscillations, because the edgewise rrst mode natural frequency is typically about double the sapwise one.

It can be seen from the above that the effects of interaction between sapwise and edgewise oscillations are generally minor, so they will not be considered further.

Blades will also be subject to torsional vibrations. In the past, it has generally been possible to ignore these, both because the exciting loads were small and because the high torsional stiffness of a typical hollow blade placed the torsional natural frequencies well above the exciting frequencies. However, with the development of larger, more sexible blades, this is no longer always the case. Blade torsion, which can accompany sapwise bending due to offset of the cross-section centre of mass from the shear centre, for example, may signircantly alter the angle of attack in the tip region.

Finally, in the case of a blade hinged at the root, the whole blade will experience oscillations involving rigid body rotation about the hinge. This phenomenon is considered in the ‘Teeter Motion’ section.

# 5.8.2 Mode shapes and frequencies

The mode shape and frequency of the rrst mode can be derived by an iterative technique called the Stodola method after its originator. Briesy, this consists of assuming a plausible mode shape, calculating the inertia loads associated with it for an arbitrary frequency of one radian per second, and then computing the beam desected prorle resulting from these inertia loads. This prorle is then normalised, typically by dividing the desections by the tip desection, to obtain the input mode shape for the second iteration. The process is repeated until the mode shape converges. Then, in view of the fact that the inertia loads calculated for the input tip desection combined with a frequency of 1 rad per second must be the same as those calculated for the output tip desection combined with the actual frequency, the rrst mode natural frequency can be obtained from the following formula:

$$
\omega_ {1} = \sqrt {\frac {\text {Tip deflection input to last iteration}}{\text {Tip deflection output from last iteration}}}
$$

If the mode shapes are orthogonal, advantage can be taken of this property to simplify the derivation of the mode shapes and frequencies of the higher modes, provided this is carried out in ascending order. A trial mode shape is assumed as before, but before using it to calculate the inertia loadings, it is ‘purired’ so that it does not contain any lower mode content. For example, ‘purircation’ of a second mode trial mode shape, $\mu _ { 2 T } ( r )$ , of rrst mode content is achieved by subtracting

$$
\mu_ {2 C} (r) = \mu_ {1} (r) \frac {\int_ {0} ^ {R} \mu_ {1} (r) \mu_ {2 T} (r) m (r) d r}{\int_ {0} ^ {R} \mu_ {1} ^ {2} (r) m (r) d r} = \mu_ {1} (r) \frac {\int_ {0} ^ {R} \mu_ {1} (r) \mu_ {2 T} (r) m (r) d r}{m _ {1}} \tag {5.71}
$$

from it. The modired second mode trial mode shape, $\mu _ { 2 M } ( r ) = \mu _ { 2 T } ( r ) - \mu _ { 2 C } ( r )$ , then satisres the orthogonality condition

$$
\int_ {0} ^ {R} \mu_ {1} (r) \mu_ {2 M} (r) m (r) d r = 0
$$

After ‘purircation’ of the trial mode shape, the Stodola method can be applied exactly as before. Further ‘purircation’ before succeeding iterations should not be necessary if the lower mode shapes used for the initial ‘purircation’ are accurate enough. See Clough and Penzien (1993) for a rigorous treatment of the method.

The rrst mode frequency for out-of-plane oscillations of blade SC40 in the absence of centrifugal force is 0.881 Hz, compared with the corresponding frequency for in-plane oscillations of 1.183 Hz. The relatively small difference between the frequencies stems from the dominant contributions of the spar caps to the respective stiffnesses. In the absence of spar caps, the blade would be much stiffer in edgewise bending than in sapwise bending, and the frequency ratio would approach 2.

# 5.8.3 Centrifugal stiffening

When a rotating blade desects either in its plane of rotation or perpendicular to it, the centrifugal force on each blade element exerts a restoring force that has the effect of stiffening the blade and thereby increasing the natural frequency compared with the stationary value. The centrifugal forces act radially outwards perpendicular to the axis of rotation, so in the case of an out-of-plane blade desection, they are parallel to the undesected blade axis and act at greater lever arms to the inboard part of the blade than they do in the case of in-plane blade desection. This is illustrated in Figure 5.24.

In order to take account of the effects of centrifugal loads, the equation of motion for a blade element loaded in the out-of-plane direction is modired by the addition of an additional term to become

$$
m (r) \ddot {x} + \hat {c} (r) \dot {x} - \frac {\partial}{\partial r} [ N (r) \frac {\partial x}{\partial r} ] + \frac {\partial^ {2}}{\partial r ^ {2}} [ E I \frac {\partial^ {2} x}{\partial r ^ {2}} ] = q (r, t) \tag {5.72}
$$

where the centrifugal force at radius r, N(r), is the summation of the forces acting on each blade element outboard of radius r, that is, $\begin{array} { r } { N ( r ) = \sum _ { r = r } ^ { r = R } m ( r ) \Omega ^ { 2 } r . \Delta r } \end{array}$ .

![](images/309ae390a8df98432cdf2a1b607e5b309ebd8b8b948c30a2184148033218dcbb.jpg)

<details>
<summary>text_image</summary>

M_x(r*) = \int_R^R m(r) \Omega^2 r \left[ \frac{r^*}{r} y(r) - y(r^*) \right] \cdot \Delta r
\Omega
M_x
y(r)
m(r) \Omega^2 r \cdot \Delta r
r*
r
M_y(r*) = \int_R^R m(r) \Omega^2 r \left[ x(r) - x(r^*) \right] \cdot \Delta r
M_y
x(r)
m(r) \Omega^2 r \cdot \Delta r
r*
</details>

Figure 5.24 Restoring moments due to centrifugal force for in-plane and out-of-plane blade desections.

The Stodola method for deriving blade mode shapes and frequencies described in the preceding section can be modired to take account of centrifugal effects. In the case of out-of-plane modes, the procedure is as follows:

1. Assume plausible trial mode shape $\mu ( r )$ .   
2. ‘Purify’ trial mode shape of any lower mode content.   
3. Assume trial value for frequency, $\omega _ { j } ^ { 2 }$ .

4. Calculate bending moment distribution due to lateral inertia forces according to

$$
M _ {Y. L a t} (r ^ {*}) = \int_ {r ^ {*}} ^ {R} m (r) \omega_ {j} ^ {2} \mu (r) [ r - r ^ {*} ] d r \tag {5.73}
$$

5. Calculate bending moment distribution due to centrifugal forces according to

$$
M _ {Y.. C F} \left(r ^ {*}\right) = - \int_ {r ^ {*}} ^ {R} m (r) \Omega^ {2} r [ \mu (r) - \mu \left(r ^ {*}\right) ] d r \tag {5.74}
$$

6. Calculate combined bending moment distribution.

7. Calculate new desected prorle resulting from this bending moment distribution.

8. Calculate revised estimate of natural frequency from

$$
\omega_ {j} ^ {\prime} = \omega_ {j} \sqrt {\frac {\text {Trial tip deflection}}{\text {Tip deflection calculated for new deflected profile}}}
$$

9. Repeat steps 2–8 with revised mode shape and frequency until calculated mode shape converges.

It is important to note that the lateral loads and desections of a centrifugally loaded beam do not conform to Betti’s theorem, so, as a consequence, the mode shapes are not orthogonal. It is for this reason that the ‘purircation’ stage has been included in each cycle of iteration. When convergence of the calculated mode shape has occurred, it will be found that it differs signircantly from the ‘purired’ mode shape input into each iteration, indicating that a true solution has not been obtained. It is then necessary to use a trial and error approach to modify the magnitudes of the ‘purifying’ corrections applied until the output mode shape and input ‘purired’ mode shape match. A few further iterations will be required until the natural frequency settles down.

A quick estimate of the rrst mode frequency of a rotating blade can be derived using the Southwell formula for a uniform rotating beam reported by Putter and Manor (1978) as follows:

$$
\omega_ {1} = \sqrt {\omega_ {1 , 0} ^ {2} + \phi_ {1} \Omega^ {2}} \tag {5.75}
$$

in which $\omega _ { 1 , 0 }$ is the corresponding frequency for the non-rotating blade. The value of $\phi _ { 1 }$ depends on the blade mass and stiffness distribution, and Madsen et al. (1984) suggest the value 1.73 for wind turbine blade out-of-plane oscillations. In the case of blade SC40 rotating at 15 rpm, this yields a percentage increase in rrst mode frequency due to centrifugal stiffening of 6.7% compared to the correct value of 6.2%. Typically, centrifugal stiffening results in an increase of the rrst mode frequency for out-of-plane oscillations of between 5% and 10%. For higher modes, the magnitude of the centrifugal forces is less in proportion to the lateral inertia forces, so the percentage increase in frequency due to centrifugal stiffening becomes progressively less.

The procedure for deriving the blade rrst mode shape and frequency in the case of in-plane oscillations is the same as that described above for out-of-plane vibrations, except that the formula for the bending moment distribution due to the centrifugal forces has to be modired to

$$
M _ {X. C F} (r ^ {*}) = \int_ {r ^ {*}} ^ {R} m (r) \Omega^ {2} r \left[ \frac {r ^ {*}}{r} \mu (r) - \mu (r ^ {*}) \right] d r \tag {5.76}
$$

where $\mu ( r )$ is now the trial in-plane mode shape.

The smaller lever arms at which the centrifugal loads act in the case of in-plane oscillations (Figure 5.24) means that their effect on the in-plane natural frequency is much less than on the out-of-plane one. In the case of the SC40 blade, the increase in the rrst mode frequency for in-plane oscillations due to centrifugal force is only 0.8%.

# 5.8.4 Aerodynamic and structural damping

Blade motion is generally resisted by two forms of viscous damping, aerodynamic and structural, which are considered in turn.

An approximate expression for the aerodynamic damping per unit length in the sapwise direction can be derived by a method analogous to that used in Section 5.7.5 to derive the linear relation:

$$
q = \frac {1}{2} \rho \Omega r c (r) \frac {d C _ {L}}{d \alpha} u [ \mathrm{seeEq.(5.25)} ]
$$

between blade load suctuations per unit length, q, and suctuations in the incident wind, u. The wind speed suctuation, u, is simply replaced by the blade sapwise velocity, −ẋ , giving

$$
\hat {c} _ {a} (r) = \frac {q}{- \dot {x}} = \frac {1}{2} \rho \Omega r c (r) \frac {d C _ {L}}{d \alpha} \tag {5.77}
$$

The rate of change of lift coefrcient with angle of attack, $\frac { d C _ { L } } { d \alpha }$ , is constant and equal to 2π before the blade goes into stall but can become negative post-stall, leading to the risk of instability – see Section 7.1.15.

It can be seen that the aerodynamic damping per unit length, $\hat { c } _ { a } ( \boldsymbol { r } )$ , varies spanwise as the product of radius and blade chord and is therefore not very close to being proportional to the mass per unit length, as is required to satisfy the orthogonality condition. This will result in some aerodynamic coupling of modes, which is not accounted for in normal modal analysis.

The aerodynamic damping ratio for the ith mode is derned as

$$
\xi_ {a i} = c _ {a i} / 2 m _ {i} \omega_ {i} = \int_ {0} ^ {R} \hat {c} _ {a} (r) \mu_ {i} ^ {2} (r) d r / 2 m _ {i} \omega_ {i} \tag {5.78}
$$

Substituting the expression for $\hat { c } _ { a } ( \boldsymbol { r } )$ given in Eq. (5.77) leads to

$$
\xi_ {a i} = \frac {\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \int_ {0} ^ {R} r c (r) \mu_ {i} ^ {2} (r) d r}{2 \omega_ {i} \int_ {0} ^ {R} m (r) \mu_ {i} ^ {2} (r) d r} \tag {5.79}
$$

In the case of rbreglass blade SC40 described in Example 5.1, this yields values of 0.26 and 0.065 for the rrst and second modes, respectively. These high values are a consequence of the lightness of the blade in relation to its width in the vicinity of the tip, an area that dominates the integrals thanks to the mode shape weighting. The corresponding rrst mode logarithmic decrement $scriptstyle ( = 2 \pi \xi _ { a } )$ is thus 1.6.

It is evident from Eq. (5.79) that the damping ratio is inversely proportional to blade mass if the natural frequency remains constant. As the adoption of more accurate blade design techniques allows reduced safety factors to be used (see Table 7.10), the trend towards lighter blades will continue, resulting in increased aerodynamic damping ratios.

Structural damping arises from the conversion of mechanical energy to thermal energy during oscillatory motion, as a result of frictional resistance within the sexing material. Denoting the strain energy at peak displacement for the nth cycle as $S _ { \mathrm { n } }$ and the loss per cycle as $\Delta S _ { \mathrm { n } } ,$ it can be shown that

$$
\frac {\Delta S _ {n}}{S _ {n}} = \frac {2 \Delta \sigma_ {n}}{\sigma_ {n}} \tag {5.80}
$$

where $\sigma _ { \mathrm { n } }$ is the peak stress for the nth cycle, $\Delta \sigma _ { n } = \sigma _ { n } - \sigma _ { n + 1 }$ and $S _ { n } = \oint { \frac { \sigma _ { n } ^ { 2 } } { 2 E } }$ , with the integral taken over the whole volume of the beam. Hence the logarithmic decrement of damping, derned as the natural logarithm of the ratio of successive peak displacements in the same direction – i.e. as ln $( \sigma _ { n } / \sigma _ { n + 1 } )$ for elastic behaviour – approximates to $\Delta \sigma _ { n } / \sigma _ { n } = 0 . 5 ( \Delta S _ { n } / S _ { n } )$ .

Test results on rbreglass (see, for example, Gibson et al. 1982) indicate that the energy loss per cycle is unaffected by frequency. However, the percentage energy loss per cycle increases quite rapidly with stress range (Creed 1993), although it is usual to treat it as independent of stress range for analysis purposes.

Values for the structural damping logarithmic decrement, $\delta _ { \mathrm { s } } = 2 \pi \xi _ { s }$ at the fundamental natural (i.e. rrst mode) frequency were given in the 1992 edition of Danish Standard DS 472, Loads and Safety of Wind Turbine Construction, for several different materials, and these are reproduced in Table 5.5, together with corresponding values from EN 1991-1-4:2005. Equivalent values of the structural damping ratio are also shown. Note that the rrst mode structural damping ratio for a rbreglass blade is much smaller than the aerodynamic damping ratio for blade SC40 derived above.

Damping ratios for the rrst and second sapwise modes of the SC40 blade are presented in Table 5.6.

It is seen that the damping ratio for the second mode is less than a third of that for the rrst.

# 5.8.5 Response to deterministic loads: step-by-step dynamic analysis

As set out in Section 5.8.1, blade dynamic response to time-varying loading is best analysed in terms of the separate excitation of each blade mode of vibration, for which, under the assumptions of unstalled sow and mass-proportional aerodynamic damping, the governing equation is

$$
m _ {i} \ddot {f} _ {i} (t) + c _ {i} \dot {f} _ {i} (t) + m _ {i} \omega_ {i} ^ {2} f _ {i} (t) = \int_ {0} ^ {R} \mu_ {i} (r) q (r, t) d r = Q _ {i} (t) \quad [ \text { see   Eq. } (5. 7 0) ]
$$

Table 5.5 Values of rrst mode structural damping logarithmic decrements for different materials. 

<table><tr><td>Standard</td><td>DS 472 (1992)</td><td>EN 1991-1-4 (2005)</td><td>DS 472</td><td>EN 1991-1-4</td></tr><tr><td>Material</td><td>Logarithmic decrement,  $\delta_s$ </td><td>Logarithmic decrement,  $\delta_s$ </td><td>Structural damping ratio,  $\xi_s$ </td><td>Structural damping ratio,  $\xi_s$ </td></tr><tr><td>Concrete</td><td>0.05</td><td>0.03 (towers and chimneys)</td><td>0.008</td><td>0.005</td></tr><tr><td>Steel – welded</td><td>0.02</td><td>0.012 (chimney)</td><td>0.003</td><td>0.002</td></tr><tr><td>Steel – bolted</td><td>0.05</td><td>0.03 (high strength bolts)</td><td>0.008</td><td>0.005</td></tr><tr><td></td><td></td><td>0.05 (ordinary bolts)</td><td></td><td>0.008</td></tr><tr><td>Glass fibre reinforced plastic</td><td>0.05</td><td>0.04–0.08 (bridges)</td><td>0.008</td><td>0.006–0.012</td></tr><tr><td>Timber</td><td>0.05</td><td>0.06–0.12 (bridges)</td><td>0.008</td><td>0.01–0.02</td></tr></table>

Table 5.6 SC40 blade damping ratios for rrst two sapwise modes. 

<table><tr><td colspan="2"></td><td>First mode</td><td>Second mode</td></tr><tr><td colspan="2">Natural frequency including centrifugal stiffening</td><td>0.94 Hz</td><td>2.83 Hz</td></tr><tr><td colspan="2">Structural damping ratio</td><td>0.008</td><td>0.008</td></tr><tr><td rowspan="2">Blade SC40 weighing 7.7 t</td><td>Aerodynamic damping ratio</td><td>0.26</td><td>0.065</td></tr><tr><td>Combined damping ratio</td><td>0.27</td><td>0.073</td></tr></table>

where $f _ { \mathrm { i } } ( t )$ and $\mu _ { \mathrm { i } } ( r )$ are the tip displacement and mode shape for the ith mode, respectively. Starting with the initial tip displacement, velocity, and acceleration arbitrarily set at zero, this equation can be used to derive values for these quantities at successive timesteps over a complete blade revolution by numerical integration. The procedure is then repeated for several more revolutions until the cyclic blade response to the periodic loading becomes sensibly invariant from one revolution to the next.

# Linear acceleration method

The precise form of the equations linking the tip displacement, velocity, and acceleration at the end of a timestep to those at the beginning depends on how the acceleration is assumed to vary over the timestep. Newmark has classired alternative assumptions in terms of a parameter β, which measures the relative weightings placed on the initial and rnal accelerations in deriving the rnal displacement The simplest assumption is that the acceleration takes a constant value equal to the average of the initial and rnal values $( \beta = 1 / 4 )$ . Clough and Penzien (1993), however, recommend that the acceleration is assumed to vary linearly between the initial and rnal values, as this will be a closer approximation to the actual variation. Step-by-step integration with this assumption is known as either the linear acceleration method or the Newmark 훽 = 1/6 method.

Expressions for the tip displacement, velocity, and acceleration at the end of the rrst timestep $- f _ { i 1 } , \dot { f } _ { i 1 }$ , and $\ddot { f } _ { i 1 }$ , respectively – are derived in terms of the initial values $- f _ { i 0 } , \dot { f } _ { i 0 } .$ , and $\ddot { f } _ { i 0 } - \mathrm { a } \mathrm { { s } }$ follows. The acceleration at time t during the timestep of total duration h is

$$
\ddot {f} _ {i} (t) = \ddot {f} _ {i 0} + \left(\frac {\ddot {f} _ {i 1} - \ddot {f} _ {i 0}}{h}\right) t \tag {5.81}
$$

This can be integrated to give the velocity at the end of the timestep as

$$
\dot {f} _ {i 1} = \dot {f} _ {i 0} + \ddot {f} _ {i 0} h + (\ddot {f} _ {i 1} - \ddot {f} _ {i 0}) h / 2 \tag {5.82}
$$

Equation (5.81) can be integrated twice to give an expression for the displacement at the end of the timestep, which, after rearrangement, yields the following expression for the corresponding acceleration:

$$
\ddot {f} _ {i 1} = \frac {6}{h ^ {2}} (f _ {i 1} - f _ {i 0}) - \frac {6}{h} \dot {f} _ {i 0} - 2 \ddot {f} _ {i 0} \tag {5.83}
$$

Substituting Eq. (5.83) into Eq. (5.82) yields

$$
\dot {f} _ {i 1} = \frac {3}{h} (f _ {i 1} - f _ {i 0}) - 2 \dot {f} _ {i 0} - \ddot {f} _ {i 0} h / 2 \tag {5.84}
$$

Eq. (5.70) can be written as

$$
m _ {i} \ddot {f} _ {i n} + c _ {i} \dot {f} _ {i n} + m _ {i} \omega_ {i} ^ {2} f _ {i n} = \int_ {0} ^ {R} \mu_ {i} (r) q _ {n} (r) d r = Q _ {i n} \tag {5.85}
$$

where the sufrx n refers to the state at the end of the nth timestep. Substituting Eqs. (5.83) and (5.84) into Eq. (5.85) with n = 1 and collecting terms yields the displacement at the end of the rrst timestep as follows:

$$
f _ {i 1} = \frac {Q _ {i 1} + m _ {i} \left(\frac {6}{h ^ {2}} f _ {i 0} + \frac {6}{h} \dot {f} _ {i 0} + 2 \ddot {f} _ {i 0}\right) + c _ {i} \left(\frac {3}{h} f _ {i 0} + 2 \dot {f} _ {i 0} + \frac {h}{2} \ddot {f} _ {i 0}\right)}{m _ {i} \omega_ {i} ^ {2} + \frac {3 c _ {i}}{h} + \frac {6 m _ {i}}{h ^ {2}}} \tag {5.86}
$$

The velocity and acceleration at the end of the rrst timestep are then obtained by substituting $f _ { \mathrm { i l } }$ in Eqs. (5.84) and (5.85), respectively.

The full procedure for obtaining the blade dynamic response to a periodic loading using the Newmark $\beta = 1 / 6$ method (which is just one of many available) may be summarised as follows:

1. Calculate the blade mode shapes, $\mu _ { i } ( r )$ .   
2. Select the number of timesteps, N, per complete revolution. Then the timestep, $h = 2 \pi \ I N \varOmega$ .   
3. Calculate the blade element loads, $q ( r , \psi _ { n } ) = q _ { n } ( r )$ , at blade azimuth positions corresponding to each timestep (i.e. at 2휋/N intervals) using momentum theory. (Here, the sufrx n denotes the number of the timestep.)

4. Calculate the generalised load with respect to each mode, $\begin{array} { r } { Q _ { i n } = \int _ { 0 } ^ { R } \mu _ { i } ( r ) q _ { n } ( r ) d r } \end{array}$ for each timestep.   
5. Assume initial values of blade tip displacement, velocity, and acceleration.   
6. Calculate rrst mode blade tip displacement, velocity, and acceleration at end of rrst timestep, using Eqs. (5.86), (5.84), and (5.83), respectively (with i = 1).   
7. Repeat stage 6 for each successive timestep over several revolutions until convergence achieved.   
8. Calculate cyclic blade moment variation at radii of interest by multiplying the cyclic tip displacement variation by appropriate factors derived from the modal analysis.   
9. Repeat stages 6–8 for higher modes.   
10. Combine the responses from different modes to obtain the total response.

Figure 5.25 shows some results of the application of the above procedure to the derivation of the out-of-plane root bending moment response of a 40 m radius blade to tower shadow loading on a stall-regulated machine. The blade is similar to blade SC40 but has a reduced rrst mode damping ratio of 0.17. The case chosen is for a mean wind speed of 12 m/s, uniform across the rotor disc, and an x/D ratio of 1 (where x is the distance between the blade and the tower centreline, and D is the tower diameter), giving a maximum reduction in the blade root bending moment for a rigid blade of 600 KNm (see Figure 5.26). Centrifugal stiffening is included in the derivation of the mode shapes and frequencies. It is evident from Figure 5.25 that the tower shadow gives the blade a sharp ‘kick’ away from the tower, but the duration is too short in relation to the duration of the rrst mode half cycle for the blade to ‘feel’ the root bending moment reduction that would be experienced by a completely rigid blade. The blade oscillations have largely died away after a complete revolution because of aerodynamic damping.

The response of the blade out-of-plane root bending moment to tower shadow combined with wind shear is shown in Figure 5.26 for a hub-height wind speed of 12 m/s. Also plotted is the corresponding bending moment for a completely rigid blade.

The wind shear loading is approximately sinusoidal (see Figure 5.11), and, consequently, the response is also. However, it is worth noting that the amplitude of the dominating rrst mode response to wind shear is the result of two effects working against each other – in other words, the increase due to the dynamic magnircation factor of about 9% is largely cancelled out by the reduction due to centrifugal stiffening.

# Avoidance of resonance: the Campbell diagram

In the course of blade design, it is important to avoid the occurrence of a resonant condition, in which a blade natural frequency equates to the rotational frequency or a harmonic with a signircant forcing load. This is often done with the aid of a Campbell diagram, in which the blade natural frequencies are plotted out against rotational frequency together with rays from the origin representing integer multiples of the rotational frequency. Then any intersections of the rays with a blade natural frequency over

![](images/fa0e480dff38b868eea81d57daba059f54256a31035ce4ac3ff431417a943a6f.jpg)

<details>
<summary>line</summary>

| Blade azimuth (degrees) | Blade root bending moment relative to mean (kNm) |
| ------------------------ | ----------------------------------------------- |
| 0                        | ~30                                             |
| 90                       | ~0                                              |
| 180                      | ~-130                                           |
| 270                      | ~70                                             |
| 360                      | ~25                                             |
</details>

Figure 5.25 Blade out-of-plane root bending moment dynamic response to tower shadow.

![](images/287cb1a2ecc69946a6a2287aacfa70b5aed956ad0e2cdd68e5fc4876004d159c.jpg)

<details>
<summary>line</summary>

| Blade azimuth (degrees) | Blade root bending moment (kNm) |
| ----------------------- | ------------------------------- |
| 0                       | 2250                            |
| 90                      | 2100                            |
| 180                     | 1300                            |
| 270                     | 2150                            |
| 360                     | 2250                            |
</details>

Figure 5.26 Blade out-of-plane root bending moment dynamic response to tower shadow and wind shear.

![](images/90fa4a13ea71e052a8f1c809da53c0fa754b7b2f8995630d96b7c0dd389a7cf4.jpg)  
Figure 5.27 Campbell diagram for blade SC40.

the turbine rotational speed operating range represent possible resonances. An example of a Campbell diagram is shown in Figure 5.27.

Clearly blade periodic loading is dominated by the loading at rotational frequency from wind shear, yawed sow, and shaft tilt (Section 5.7.2), gravity (Section 5.7.3), and gust slicing (Section 5.7.5). However, the short-lived load relief resulting from tower shadow will be dominated by higher harmonics.

# 5.8.6 Response to stochastic loads

The analysis of stochastic loads in the frequency domain has already been described in Section 5.7.5 for a rigid blade, and this will now be extended to cover the dynamic response of the different vibration modes of a sexible blade using the governing equation,

Eq. (5.70). Note that the restriction to an unstalled blade operating at a relatively high tip speed ratio still applies.

# Power spectrum of generalised blade loading

The generalised suctuating load with respect to the ith mode is $\begin{array} { r } { Q _ { i } = \int _ { 0 } ^ { R } \mu _ { i } ( r ) q ( r ) d r } \end{array}$ , where

$$
q (r) = \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} u (r, t) c (r) r
$$

[see Eq.(5.25)]

Hence

$$
Q _ {i} = \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \int_ {0} ^ {R} \mu_ {i} (r) u (r, t) c (r) r d r \tag {5.87}
$$

An expression for the standard deviation of $Q _ { \mathrm { i } } , \sigma _ { O i }$ , can be derived by a method analogous to that given in Section A5.4 of Appendix A for a non-rotating blade, yielding

$$
\sigma_ {Q i} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \left[ \int_ {0} ^ {\infty} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) d n \right] \mu_ {i} (r _ {1}) \mu_ {i} (r _ {2}) c (r _ {1}) c (r _ {2}) r _ {1} r _ {2} d r _ {1} d r _ {2} \tag {5.88}
$$

Here $S _ { u } ^ { 0 } ( r _ { 1 } , r _ { 2 } , n )$ is the rotationally sampled cross-spectrum for a pair of points on the rotating blade at radii $r _ { 1 }$ and $r _ { 2 }$ . Eq. (5.88) is parallel to Eq. (A5.16) in Appendix A5 $\left( \frac { 1 } { 2 } \rho \varOmega \frac { d C _ { L } } { d \alpha } \right) ^ { 2 }$ dCL with r and $r '$ replaced by $r _ { 1 }$ and $r _ { 2 }$ and $( \rho \overline { { U } } C _ { F } ) ^ { 2 }$ replaced by . From this it can be deduced that the power spectrum of the generalised load with respect to the ith mode is

$$
S _ {Q i} (n) = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) \mu_ {i} (r _ {1}) \mu_ {i} (r _ {2}) c (r _ {1}) c (r _ {2}) r _ {1} r _ {2} d r _ {1} d r _ {2} \tag {5.89}
$$

In practice, this expression is evaluated using summations to approximate to the integrals.

# Power spectrum of tip de@ection

The expression for the amplitude of the ith mode blade tip response to excitation by a harmonically varying generalised load is given by Eq. (A5.4) in Appendix A5. Hence the power spectrum of the tip displacement is related to the power spectrum of the generalised load by

$$
S _ {x i} (n) = \frac {S _ {Q i} (n)}{k _ {i} ^ {2}} \frac {1}{[ (1 - n ^ {2} / n _ {i} ^ {2}) ^ {2} + 4 \xi_ {i} ^ {2} n ^ {2} / n _ {i} ^ {2} ]} \tag {5.90}
$$

This can be written $S _ { x i } ( n ) = \frac { S _ { Q i } ( n ) } { k _ { i } ^ { 2 } } [ D M R ] ^ { 2 }$ , where DMR stands for the dynamic magnircation ratio. $n _ { \mathrm { i } }$ is the ith mode natural frequency in Hz.

Figure 5.28 shows the power spectrum of rrst mode tip desection, $S _ { x 1 } ( n )$ , for blade SC40 operating at 15 rpm in a mean wind of 8 m/s. The turbulence intensity has been arbitrarily set at 12.5%, so that $\sigma _ { \mathrm { u } } = 1$ m/s. Also shown is the rrst mode tip desection spectrum ignoring dynamic magnircation, $S _ { Q 1 } ( n ) / k _ { i } ^ { 2 }$ , which, when multiplied by the square of the dynamic magnircation ratio (also plotted), yields the $S _ { x 1 } ( n )$ curve. The standard deviation of rrst mode tip desection, $\begin{array} { r } { \sigma _ { x 1 } = \int _ { 0 } ^ { \infty } S _ { x 1 } ( n ) d n . } \end{array}$ , comes to 122 mm. This is only 5% larger than the value without dynamic magnircation, resecting the large damping ratio and the large separation between the rotational and rrst out-of-plane vibration mode frequencies.

# Power spectrum of blade root bending moment

If the amplitude of tip desection due to excitation of the blade resonant frequency is derned as $x _ { \mathrm { R } } ( n _ { 1 } )$ , the amplitude of the corresponding blade root bending moment, $M _ { \mathrm { Y } } ( n _ { 1 } )$ is given by

$$
M _ {Y} (n _ {1}) = \omega_ {1} ^ {2} x _ {R} (n _ {1}) \int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r \tag {5.91a}
$$

Noting that $\omega _ { 1 } ^ { 2 } = k _ { 1 } / m _ { 1 }$ , this becomes

$$
\frac {M _ {Y} (n _ {1})}{x _ {R} (n _ {1})} = k _ {1} R \frac {\int_ {0} ^ {R} m (r) \mu_ {1} (r) (r / R) d r}{m _ {1}} = k _ {1} R \chi_ {M 1} \tag {5.91b}
$$

This relationship applies at all exciting frequencies, because the right hand side is essentially a function of mode shape. Hence the power spectrum of blade root bending moment due to excitation of the rrst mode is given by

$$
S _ {M y 1} (n) = (k _ {1} R \chi_ {M 1}) ^ {2}. S _ {x 1} (n) = (R \chi_ {M 1}) ^ {2}. S _ {Q 1} (n). \frac {1}{[ (1 - n ^ {2} / n _ {1} ^ {2}) ^ {2} + 4 \xi_ {1} ^ {2} n ^ {2} / n _ {1} ^ {2} ]} \tag {5.91c}
$$

For blade SC40, the ratio $\chi _ { \mathrm { M l } }$ takes a value of 1.41.

![](images/40644179626b89985faa20ee7cea811f9bb22115ea3171715c851c613f12fc91.jpg)

<details>
<summary>line</summary>

| Frequency in Hz (logarithmic scale) | nS_x1(n) (logarithmic scale) | Dynamic magnification ratio squared |
| ----------------------------------- | ---------------------------- | ----------------------------------- |
| 0.01                                | ~3000                        | ~1                                  |
| 0.1                                 | ~100                         | ~1                                  |
| 0.5                                 | ~10000                       | ~10                                 |
| 1.0                                 | ~5000                        | ~10                                 |
| 10.0                                | ~1                           | ~1                                  |
</details>

Figure 5.28 Power spectrum of blade SC40 rrst out-of-plane mode tip desection.

# 5.8.7 Response to simulated loads

The blade dynamic response to time-varying loading derived from wind simulation (Section 5.7.6) can be obtained by a step-by-step dynamic analysis such as that described for use with deterministic loads in Section 5.8.5. The procedure is essentially the same, except that it is more important to select realistic values for the initial blade tip displacement, velocity, and acceleration, unless the results from the rrst few rotation cycles are to be discarded.

# 5.8.8 Teeter motion

When the rotor is rigidly mounted on the shaft, out-of-plane aerodynamic loads on the blades result in suctuating bending moments in the low-speed shaft additional to those due to gravity. In the case of two bladed machines, the transfer of blade out-of-plane aerodynamic moments to the shaft can be eliminated and blade root bending moments reduced by mounting the rotor on a hinge with its axis perpendicular to both the low-speed shaft and the axis of the rotor. This allows the rotor to teeter to and fro in response to differential aerodynamic loads on each blade.

The restoring moment acting on a rotor rotating at a constant teeter angle is generated by the lateral components of the centrifugal force acting on each blade element (see Figure 5.29). For small teeter angles – up to, say 5 degrees – it may be approximated by

$$
M _ {R} = \int_ {0} ^ {R} r. m (r) \Omega^ {2} r. \zeta . d r = I \Omega^ {2} \zeta \tag {5.92}
$$

where $\zeta$ is the teeter angle, 훺 is the rotational speed and I is the rotor moment of inertia about its centre. The equation of motion for small free teeter oscillations thus becomes $I \ddot { \zeta } + I \Omega ^ { 2 } \zeta = 0$ (omitting the aerodynamic damping term for the moment), indicating that the natural frequency of the teeter motion with the teeter hinge perpendicular to the rotor axis is equal to the rotational frequency. Because both the deterministic and stochastic components of the exciting moment are dominated by this frequency, it is clear that the system operates at resonance, with aerodynamic damping alone controlling the magnitude of the teeter excursion. In the absence of stochastic wind loads, a teetering rotor can be thought of as rotating in a rxed plane at an angle $\zeta _ { \mathrm { o } }$ to the plane perpendicular to the shaft axis (with $\zeta _ { \mathrm { o } }$ equal to the maximum teeter angle), because the teetering frequency is equal to the rotational frequency.

The magnitude of teeter excursions would clearly be reduced if the teeter natural frequency were moved away from the rotational frequency. This can be done by rotating the teeter hinge axis relative to the rotor in the plane of rotation, as illustrated in Figure 5.29, so that teeter motion results in a change of blade pitch – positive in one blade and negative in the other – known as Delta 3 coupling. Consider the case of blade A slicing through a gust. The increased thrust on the blade will cause it to move in the downwind direction, by rotating about the teeter hinge. If the teeter angle, derned as the rotation of the blade in its own radial plane, is $\zeta ,$ , then the increase in blade A’s pitch angle will be $\zeta$ tan $\delta _ { 3 }$ ,where $\delta _ { 3 }$ is as derned in Figure 5.29. The increase in the pitch angle of blade A will reduce the angle of attack, $\alpha ,$ , and thereby reduce the thrust loading on it. The net result of this and a simultaneous increase in the thrust loading on blade B is to introduce an additional restoring moment which will further help to reduce the teeter motion.

![](images/681b470da2eee2d08bbd8225f5e695bdbffca7c73052653438c5a8596cb78921.jpg)

<details>
<summary>text_image</summary>

Teeter rotation
Blade A
δ₃
Axis of teeter hinge
Teeter angle ζ
r
Δr
Change in pitch angle
Δθ = ζ tan δ₃
Centrifugal force (at constant
teeter angle) m(r)Ω²rΔr
</details>

Figure 5.29 Teeter geometry.

The rrst stage for the exploration of teeter response to different loadings is the derivation of the complete equation of motion. It is assumed that the blades are unstalled and are operating at a relatively high tip speed, so that the linear relations adopted in the derivation of Eq. (5.25) in Section 5.7.5 can be retained. The various contributions to the change in the aerodynamic force on a blade element relative to the steady state situation are, therefore,

$$
\frac {1}{2} \rho \Omega r c \frac {d C _ {L}}{d \alpha} (u - \dot {\zeta} r) - \frac {1}{2} \rho (\Omega r) ^ {2} c \frac {d C _ {L}}{d \alpha}. \Delta \theta \tag {5.93}
$$

where the three terms result from the suctuation of the incident wind, teeter motion, and Delta 3 coupling, respectively. Multiplication of these terms by radius, integration over the length of the blade, and addition of the centrifugal and inertia hub moment terms yields the following equation of motion for the teeter response:

$$
\begin{array}{l} I \ddot {\zeta} + \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \left[ 2 \int_ {0} ^ {R} r ^ {3} c (r) d r \right]. \dot {\zeta} + \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \left[ 2 \int_ {0} ^ {R} r ^ {3} c (r) d r \right] \Omega \tan \delta_ {3} \zeta + I \Omega^ {2} \zeta \\ = \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \int_ {- R} ^ {R} u (r, t) c (r). r. | r | d r \tag {5.94} \\ \end{array}
$$

assuming a frozen wake. By dividing through by the moment of inertia and writing

$$
\eta = \frac {1}{2} \frac {\rho}{I} \frac {d C _ {L}}{d \alpha} \left[ 2 \int_ {0} ^ {R} r ^ {3} c (r) d r \right] \tag {5.95}
$$

this can be simplired to

$$
\ddot {\zeta} + \eta \Omega \dot {\zeta} + (1 + \eta \tan \delta_ {3}) \Omega^ {2} \zeta = \frac {1}{2} \rho \frac {\Omega}{I} \frac {d C _ {L}}{d \alpha} \int_ {- R} ^ {R} u (r, t) c (r). r. | r | d r \tag {5.96}
$$

휂 is a measure of the ratio of aerodynamic to inertial forces acting on the blade and is one eighth of the Lock number.

Delta 3 coupling thus raises the natural frequency, $\omega _ { n } \mathrm { . }$ , of the teeter motion from 훺 to $\Omega \sqrt { 1 + \eta \tan \delta _ { 3 } }$ . In the case of an 80 m diameter rotor consisting of two SC40 blades, the rotor inertia about the hub centre comes to about 5980 $\mathrm { T m } ^ { 2 }$ , giving 휂 = 1.46. When the rotor is mounted on a teeter hinge set at a $\delta _ { 3 }$ angle of $3 0 ^ { \circ }$ , tan $\delta _ { 3 } = 0 . 5 7 7$ , so the increase in natural frequency due to the $\delta _ { 3 }$ angle is $3 6 \%$ . The corresponding damping ratio, given by $\xi = \frac { \eta } { 2 \sqrt { 1 + \eta \tan \delta _ { 3 } } }$ , is quite high at 0.54.

# Teeter response to deterministic loads

The teeter response to deterministic loads can be found using the same step-by-step integration procedure set out in Section 5.8.5. However, as the loadings due to wind shear and yaw are both approximately sinusoidal, an estimate of the maximum teeter angle for these cases may be obtained by using the standard solution for forced oscillations. For a harmonically varying teeter moment, $M _ { \mathrm { T } } = M _ { \mathrm { T 0 } }$ cos 훺t due to wind shear, the teeter angle is given by

$$
\zeta = \frac {M _ {T O}}{I \omega_ {n} ^ {2}} \frac {\cos (\Omega t - \vartheta)}{\sqrt {(1 - (\Omega / \omega_ {n}) ^ {2}) ^ {2} + (2 \xi \Omega / \omega_ {n}) ^ {2}}} \tag {5.97a}
$$

where $\vartheta = \tan ^ { - 1 } \left( \frac { 2 \xi \varOmega / \omega _ { n } } { 1 - ( \varOmega / \omega _ { n } ) ^ { 2 } } \right) = 9 0 ^ { o } - \delta _ { 3 }$ is the phase lag with respect to the excitation. This reduces to

$$
\zeta = \frac {M _ {T O}}{\Omega^ {2} \rho \frac {d C _ {L}}{d \alpha} \int_ {0} ^ {R} r ^ {3} c (r) d r} \frac {\cos (\Omega t - \vartheta)}{\sqrt {1 + \tan^ {2} \delta_ {3}}} \tag {5.97b}
$$

which is independent of rotor inertia.

For the two bladed turbine described above, rotating at 15 rpm in a wind with a hub-height mean of 10 m/s and a shear exponent of 0.2, the teeter moment amplitude, $M _ { \mathrm { o } } ,$ is approximately 430 KNm (see Figure 5.11a, which gives the blade root bending moment variation with azimuth for a rxed hub machine, based on momentum theory). For the teetering rotor with two SC40 blades considered above, $\omega _ { n } = 1 . 3 6 \pi / 2$ rad/sec, the maximum teeter angle comes to $0 . 9 9 ^ { \circ }$ for $\delta _ { 3 } = 3 0 ^ { \circ }$ . This increases to $1 . 1 5 ^ { \circ }$ if the $\delta _ { 3 }$ angle is reduced to zero.

If the wind speed variation due to wind shear experienced by a vertical blade is assumed to be linear with height, i.e. $u = \overline { { U } } ( k r / R )$ , and the teeter moment is calculated from the expression on the right hand side of Eq. (5.94), which assumes a frozen wake instead of the equilibrium wake resulting from momentum theory, a very simple expression for the teeter angle results in the case of zero $\delta _ { 3 }$ angle. The teeter moment becomes

$$
M _ {T} = M _ {T O}. \cos \Omega t = \frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha} \frac {\overline {{{U}}} k}{R} \int_ {- R} ^ {R} c (r) r ^ {3} d r. \cos \Omega t \tag {5.98}
$$

Substitution of Eq. (5.98) in Eq. (5.97a), with $\omega _ { n }$ set equal to 훺 for the case of a zero $\delta _ { 3 }$ angle results in the following expression for the teeter angle:

$$
\zeta = \frac {\overline {{{U}}} k}{\Omega R} \cos (\Omega t - (\pi / 2)) \tag {5.99}
$$

Thus, the magnitude of the teeter excursion is simply equal to the velocity gradient divided by the rotational speed. For a hub height of 60 m, the equivalent uniform velocity gradient over the rotor disc for the case above is $0 . 1 5 2 \overline { { U } } / R = 0 . 0 3 8 1$ m/s per metre, giving a teeter excursion of 0.024 rad or 1.39∘ . This differs from the earlier value of $1 . 1 5 ^ { \circ }$ because of the frozen wake assumption.

# Teeter response to stochastic loads

As usual, it is convenient to analyse the response to the stochastic loads in the frequency domain. The teeter moment providing excitation is given by the right hand side of Eq. (5.94). By following a similar method to that used for the generalised load in Section 5.8.6, the following expression for the power spectrum of the teeter moment can be derived:

$$
S _ {M T} (n) = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} S _ {u} ^ {o} (r _ {1}, r _ {2}, n) c (r _ {1}) c (r _ {2}). r _ {1} r _ {2} | r _ {1} | | r _ {2} | d r _ {1} d r _ {2} \tag {5.100}
$$

where $S _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , n )$ is the rotationally sampled cross-spectrum. In practice, $S _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , n )$ is evaluated for a few discrete radius values and the integrals replaced by summations.

The power spectrum of the teeter angle response is related to the teeter moment power spectrum by a formula analogous to Eq. (5.90), as follows:

$$
S _ {\zeta} (n) = \frac {S _ {M T} (n)}{(I \omega_ {n} ^ {2}) ^ {2}} \frac {1}{[ (1 - (2 \pi n / \omega_ {n}) ^ {2}) ^ {2} + (2 \xi . 2 \pi n / \omega_ {n}) ^ {2} ]} \tag {5.101}
$$

This can be written $S _ { \zeta } ( n ) = \frac { S _ { M T } ( n ) } { ( I \omega _ { n } ^ { 2 } ) ^ { 2 } } [ D M R ] ^ { 2 }$ where DMR stands for the dynamic magnircation ratio.

Figure 5.30 shows the teeter angle power spectrum, $S _ { \zeta } ( n )$ , for a two bladed rotor with SC40 blades and zero $\delta _ { 3 }$ angle operating at 15 rpm in a mean wind of 8 m/s. The turbulence intensity is taken as 20.3%, for a Class B site, and the damping ratio, $\xi = \eta / 2$ , is 0.731, calculated from Eq. (5.95). Also shown in the rgure is the teeter angle power spectrum ignoring dynamic magnircation, $S _ { M T } ( n ) / ( I \omega _ { n } ^ { 2 } ) ^ { \bar { 2 } }$ , which, when multiplied by the square of the dynamic magnircation ratio (also plotted), yields the $S _ { \zeta }$ (n)curve. Note that the high damping ratio means that the dynamic magnircation ratio is less than unity across the whole frequency range. The resulting teeter angle standard deviation, obtained by taking the square root of the area under the power spectrum, is $0 . 7 7 ^ { \circ }$ .

![](images/a6d5cef61996c9b44d39e7e8a0ae5913e688e5bed57b11615a051b7f6085b792.jpg)

<details>
<summary>line</summary>

| Frequency (Hz) | Power spectrum of teeter angle, nSξ(n) | Dynamic magnification ratio squared |
| -------------- | ------------------------------------- | ------------------------------------ |
| 0.1            | ~9.5                                  | ~0.0                                 |
| 0.5            | ~18.5                                 | ~0.8                                 |
| 1.0            | ~0.5                                  | ~0.2                                 |
</details>

Figure 5.30 Teeter angle power spectrum for two bladed rotor with SC40 blades.

Having calculated the teeter angle standard deviation, the extreme value over any desired exposure period can be predicted from Eq. (5.59). As is evident from Figure 5.30, the teeter angle power spectrum is all concentrated about the rotational frequency, 훺, so the zero up-crossing frequency, 휈, can be set equal to it. Thus, for a machine operating at 15 rpm, a 1 hour exposure period gives $\nu T = 9 0 0$ and $\zeta _ { \mathrm { m a x } } / \sigma _ { \zeta } = 3 . 8 4$ . The predicted maximum teeter angle due to stochastic loading over a 1 hour period for the case above is thus $3 . 8 4 \times 0 . 7 7 ^ { \circ } = 3 . 0 ^ { \circ }$ . This reduces to $2 . 6 ^ { \circ }$ if a $\delta _ { 3 }$ angle of $3 0 ^ { \circ }$ is introduced.

As already mentioned, teetering relieves blade root bending moments as well as those in the low-speed shaft. The reduction of the stochastic component of root bending moment can be derived in terms of the standard deviations of blade root bending moment and hub teeter moment for a rigid hub two blade machine. Integration of Eq. (5.100) yields the following expression for the latter:

$$
\sigma_ {M T} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} \kappa_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}). r _ {1} r _ {2} | r _ {1} | | r _ {2} | d r _ {1} d r _ {2} \tag {5.102a}
$$

where, for convenience of notation, $r _ { 1 }$ and $r _ { 2 }$ take negative values on the second blade. $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 )$ is the cross-correlation function between the longitudinal wind suctuations between points at radii $r _ { 1 }$ and $r _ { 2 }$ on the rotating rotor and is given by the right hand side of Eq. (5.51), with $\varOmega \tau$ set equal to zero when $r _ { 1 }$ and $r _ { 2 }$ derne points on the same blade and replaced by $\pi$ when $r _ { 1 }$ and $r _ { 2 }$ derne points on different blades. Derning $\rho _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 )$ ) as the normalised cross-correlation function, $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 ) / \sigma _ { u } ^ { 2 }$ , Eq. (5.102a) can be rewritten

as

$$
\sigma_ {M T} ^ {2} = \sigma_ {u} ^ {2} \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} \rho_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}). r _ {1} r _ {2} | r _ {1} | | r _ {2} | d r _ {1} d r _ {2} \tag {5.102b}
$$

The corresponding expression for the standard deviation of the mean of the two blade root bending moments is

$$
\sigma_ {\overline {{M}}} ^ {2} = \frac {1}{4} \sigma_ {u} ^ {2} \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} \rho_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}). r _ {1} ^ {2} r _ {2} ^ {2} d r _ {1} d r _ {2} \tag {5.103}
$$

By inspection of the integrals, it is easily shown that

$$
\frac {1}{4} \sigma_ {M T} ^ {2} + \sigma_ {\overline {{M}}} ^ {2} = \sigma_ {u} ^ {2} \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \rho_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}). r _ {1} ^ {2} r _ {2} ^ {2} d r _ {1} d r _ {2} = \sigma_ {M} ^ {2} (5. 1 0 4)
$$

where $\sigma _ { M }$ is the standard deviation of root bending moment for a rigidly mounted blade. Thus, if the rotor is allowed to teeter, the standard deviation of the blade root bending moment will drop from $\sigma _ { M }$ to $\sigma _ { \overline { { M } } }$ where $\sigma _ { M }$ is given by the equation above. The extent of the reduction is driven primarily by the ratio of rotor diameter to the integral length scale of the wind turbulence. For a two bladed rotor with SC40 blades and an integral length scale of 147 m, the reduction is 11%.

# 5.8.9 Tower coupling

In the preceding sections, consideration of the dynamic behaviour of the blade has been based on the assumption that the nacelle is rxed in space – i.e. that the tower is rigid. In practice, of course, no tower is completely rigid, so suctuating loads on the rotor will result in fore–aft sexure of the tower, which, in turn, will affect the blade dynamics. This section explores the effect the coupling of the blade and tower motion has on blade response.

The application of standard modal analysis techniques to the dynamic behaviour of the system comprising the tower and rotating rotor treated as a single entity is complicated by the system’s continually changing geometry, which means that the mode shapes and frequencies of the structure taken as a whole would have to be re-evaluated at each succeeding rotor azimuth position.

An alternative approach is to base the analysis on the mode shapes and frequencies of the different elements of the structure considered separately, with the displacements arising from each set of modes superposed. Thus, the tower modes are calculated on the basis of a completely rigid rotor, and the blade modes are calculated as if the blades were cantilevered from a rigidly mounted shaft – i.e. in the same way as before. The blade modes are not orthogonal to the tower modes, so the equations of motion for the different modes are no longer independent of each other but contain coupled terms. Furthermore, the blade desections arising from excitation of the tower modes vary with blade azimuth, so a step-by-step solution is required. The treatment that follows is limited to the fundamental blade and tower modes but could be extended to encompass higher modes.

The equation of motion of the blade is given by Eq. (5.62). The blade desection for blade J may be written as

$$
x (r, t) = \mu (r). f _ {J} (t) + \mu_ {T J} (r). f _ {T} (t) \tag {5.105}
$$

![](images/dad00153cb2ea8f2741924ef5f6753cfe039b6fc1a244e475c4379e48d4e0fbf.jpg)

<details>
<summary>text_image</summary>

ψJ
μ(r)
μTJ(r)
r cos ψJ
μT(z)
L
z
</details>

Figure 5.31 Fundamental mode shapes of blade and tower.

where $\mu ( r )$ is the rrst blade mode shape for a rigid tower, and $\mu _ { T J } ( r )$ is the normalised rigid body desection of blade J resulting from excitation of the tower rrst mode. Assuming the normalisation is carried out with respect to hub desection,

$$
\mu_ {T J} (r) = 1 + \frac {r}{L} \cos \psi_ {J} \tag {5.106}
$$

where L is the depth below the hub of the intercept between the tangent to the top of the desected tower and the undesected tower axis, as illustrated in Figure 5.31.

Substitution of Eq. (5.105) into Eq. (5.62) yields, with the aid of Eq. (5.65),

$$
\begin{array}{l} m (r) \mu (r) \ddot {f} _ {J} (t) + \hat {c} (r) \mu (r) \dot {f} _ {J} (t) + m (r) \omega^ {2} \mu (r) f _ {J} (t) \\ = q (r, t) - m (r) \mu_ {T J} (r) \ddot {f} _ {T} (t) - \hat {c} (r) \mu_ {T J} (r) \dot {f} _ {T} (t) \tag {5.107} \\ \end{array}
$$

where the coupled terms have been transferred to the right hand side. Multiplying through by $\mu ( r )$ and integrating over the length of the blade gives

$$
\begin{array}{l} m _ {1} \ddot {f} _ {J} (t) + c _ {1} \dot {f} _ {J} (t) + m _ {1} \omega^ {2} f _ {J} (t) \\ = \int_ {0} ^ {R} \mu (r) q (r, t) d r - \int_ {0} ^ {R} m (r) \mu (r) \mu_ {T J} (r) d r. \ddot {f} _ {T} (t) - \int_ {0} ^ {R} \hat {c} (r) \mu (r) \mu_ {T J} (r) d r. \dot {f} _ {T} (t) \tag {5.108} \\ \end{array}
$$

By analogy with Eq. (5.70), the equation of motion of the tower is

$$
m _ {T 1} \ddot {f} _ {T} (t) + c _ {T 1} \dot {f} _ {T} (t) + m _ {T 1} \omega_ {T} ^ {2} f _ {T} (t) = \int_ {0} ^ {H} \mu_ {T} (z) q (z, t) d z \tag {5.109}
$$

Here $\mu _ { \mathrm { T } }$ is the tower rrst mode shape, and $m _ { \mathrm { T 1 } }$ is the generalised mass of the tower, nacelle, and rotor (including the contribution of rotor inertia), with respect to the rrst

mode, given by

$$
m _ {T 1} = \int_ {0} ^ {H} m _ {T} (z) \mu_ {T} ^ {2} (z) d z + m _ {N} + m _ {R} + I _ {R} / L ^ {2} \tag {5.110}
$$

Here $m _ { \mathrm { T } } ( z )$ is the mass per unit height of the tower, $m _ { \mathrm { N } }$ and $m _ { \mathrm { R } }$ are the nacelle and rotor masses, and $I _ { \mathrm { R } }$ is the inertia of the rotor about the horizontal axis in its plane, which is constant over time for a three bladed rotor. For a two bladed, rxed hub rotor it varies with rotor azimuth, and for a teetering rotor it is omitted altogether.

The major component of the loading on the tower, $q ( \boldsymbol { z } , t )$ , is the load fed in at hub height, H, from the blades. The inertia forces on the blades due to rigid body motion associated with the tower rrst mode have been accounted for by including rotor mass and inertia in $m _ { \mathrm { T 1 } }$ , and the corresponding damping forces can be accounted for in the calculation of the damping coefrcient, $c _ { T 1 }$ . However, the aerodynamic loads on the blades and the inertia and damping forces associated with blade sexure – all of which are transmitted to the tower top – have to be included in the right hand side of (5.109) as

$$
\mu_ {T} (H). F + \left(\frac {d \mu_ {T}}{d z}\right) _ {H}. M = F + M / L \tag {5.111}
$$

where

$$
F = \sum_ {B} \int_ {0} ^ {R} q _ {J} (r, t) d r - \sum_ {B} \int_ {0} ^ {R} m _ {1} (r) \mu (r) d r. \ddot {f} _ {J} (t) - \sum_ {B} \int_ {0} ^ {R} \hat {c} (r) \mu (r) d r. \dot {f} _ {J} (t) \tag {5.112}
$$

and

$$
\begin{array}{l} M = \sum_ {B} \int_ {0} ^ {R} r \cos \psi_ {J} q _ {J} (r, t) d r - \sum_ {B} \int_ {0} ^ {R} r \cos \psi_ {J} m _ {1} (r) \mu (r) d r. \ddot {f} _ {J} (t) \\ - \sum_ {B} \int_ {0} ^ {R} r \cos \psi_ {J} \hat {c} (r) \mu (r) d r. \dot {f} _ {J} (t) \tag {5.113} \\ \end{array}
$$

The sufrx J refers to the Jth blade, and B in the summations is the total number of blades.

Hence

$$
\begin{array}{l} F + M / L = \sum_ {B} \int_ {0} ^ {R} \mu_ {T J} q _ {J} (r, t) d r - \sum_ {B} \int_ {0} ^ {R} m _ {1} (r) \mu (r) \mu_ {T J} (r) d r. \ddot {f} _ {J} (t) \\ - \sum_ {B} \int_ {0} ^ {R} \hat {c} (r) \mu (r) \mu_ {T J} (r) d r. \dot {f} _ {J} (t) \\ \end{array}
$$

and Eq. (5.109) becomes

$$
m _ {T 1} \ddot {f} _ {T} (t) + c _ {T 1} \dot {f} _ {T} (t) + m _ {T 1} \omega_ {T} ^ {2} f _ {T} (t)
$$

$$
= \sum_ {B} \int_ {0} ^ {R} \mu_ {T J} q _ {J} (r, t) d r - \sum_ {B} \int_ {0} ^ {R} m _ {1} (r) \mu (r) \mu_ {T J} (r) d r. \ddot {f} _ {J} (t) - \sum_ {B} \int_ {0} ^ {R} \hat {c} (r) \mu (r) \mu_ {T J} (r) d r. \dot {f} _ {J} (t) \tag {5.114}
$$

omitting the term for loading on the tower itself.

Equations (5.108, 5.114) provide (B + 1) simultaneous equations of motion with periodic coefrcients 휇TJ corresponding to the (B + 1) degrees of freedom assumed. The procedure for the step-by-step dynamic analysis that is based on these equations may be summarised as follows:

1. Substitute the displacements, velocities, and aerodynamic loads at the beginning of the rrst timestep into Eqs. (5.108) and (5.114), and solve for the initial accelerations.   
2. Formulate the incremental equations of motion for the timestep, based on Eqs. (5.108) and (5.114), retaining the coupled terms on the right hand side – i.e. as pseudo forces.   
3. Assume initially that the coupled terms are constant over the duration of the timestep, so that they disappear from the incremental equations of motion altogether, rendering them uncoupled.   
4. Solve the uncoupled incremental equations of motion to obtain the increments of displacement and velocity over the timestep. Adopting the linear acceleration method (Section 5.8.5), the expressions for the displacement and velocity increments at the tip of blade J are as follows:

$$
\Delta f _ {J} = \frac {\Delta Q _ {J} + m _ {1} \left(\frac {6}{h} \dot {f} _ {J 0} + 3 \ddot {f} _ {J 0}\right) + c _ {1} \left(3 \dot {f} _ {J 0} + \frac {h}{2} \ddot {f} _ {J 0}\right)}{m _ {1} \omega^ {2} + \frac {3 c _ {1}}{h} + \frac {6 m _ {1}}{h ^ {2}}} \tag {5.115}
$$

$$
\Delta \dot {f} _ {J} = \frac {3}{h} \Delta f _ {J} - 3 \dot {f} _ {J 0} - \frac {h}{2} \ddot {f} _ {J 0} \tag {5.116}
$$

The derivation of these expressions parallels that for the absolute values of displacement and velocity at the end of the timestep, given in Section 5.8.5. Similar expressions obtain for the displacement and velocity increments at the hub due to tower sexure.

5. Solve Eqs. (5.108) and (5.114) for the accelerations at the end of the timestep.   
6. Solve the incremental equations of motion again – this time including the changes in the coupled terms on the right hand side over the timestep – to obtain revised increments of displacement and velocity over the timestep.   
7. Repeat step 5 and step 6 until the increments of displacement and velocity converge.   
8. Repeat steps 1–7 for the second and subsequent timesteps.

If the analysis is being carried out to obtain the response to deterministic loads, advantage may be taken of the fact that the behaviour of each blade mirrors that of its neighbours with an appropriate phase difference. This means that the number of equations of motion can be reduced to two and the analysis iterated over a number of revolutions until a steady state response is achieved. For example, in the case of a machine with three blades, A, B, and C, the values of blade B and blade C tip velocities and accelerations, which are required on the right hand side of Eq. (5.114), would be equated to the corresponding values for blade A occurring T/3 and 2T/3 earlier (T being the period of blade rotation).

Figure 5.32 shows the results from the application of the above procedure to the derivation of blade tip and hub displacements in response to tower shadow loading, considering only the blade and tower fundamental modes. The three bladed machine is stall regulated, and the parameters chosen are, as far as the rotor is concerned, generally the same as for the rigid tower example in Section 5.8.5 illustrated in Figure 5.25. The tower natural frequency is 0.58 Hz, and the tower damping ratio (which is dominated by the aerodynamic damping of the blades) is taken as 0.022. The wind speed is a uniform 12 m/s.

It can be seen that the tower response is sinusoidal at blade passing frequency, which is the forcing frequency. The amplitude is only about 1/50th of the maximum blade tip displacement of about 60 mm, resecting the large generalised mass associated with the tower mode relative to that associated with the blade mode. The tower shadow effect causes the blade to accelerate rapidly upwind as it passes the tower, with the maximum desection occurring at an azimuth of about 205∘ . Also plotted on Figure 5.32 is the desection that would occur if the nacelle were rxed, and it is seen from the comparison that one effect of tower sexibility is to slightly reduce the peak desection. However, a more signircant effect of the tower motion is the maintenance of the amplitude of the subsequent blade oscillations at a higher level prior to the next tower passing.

The modal analysis method outlined above forms the basis for a number of codes for wind turbine dynamic analysis, such as the Garrad Hassan Bladed code (DNVGL – Energy 2016, DNVGL 2020). Typically, these codes allow at least the rrst few blade modes, including sapwise, edgewise and torsional degrees of freedom, and several tower modes (fore-aft, side-to-side and torsional) to be represented together with drive train dynamics. See Section 5.13.

Rather than use modal analysis, the dynamic behaviour of coupled rotor/tower systems can also be investigated using rnite elements. Standard rnite element dynamics packages are, however, inappropriate to the task, because they are only designed to model the displacements of structures with rxed geometry. Lobitz (1984) has pioneered the application of the rnite element method to the dynamic analysis of wind turbines with two bladed, teetering rotors, and Garrad (1987) has extended it to three bladed, rxed hub machines. In both cases, equations of motion are developed in matrix form for the blade and tower displacement vectors and then amalgamated using a connecting matrix that is a function of blade azimuth and satisres the compatibility and equilibrium requirements at the tower/rotor interface. Solution of the equations is carried out by a step-by-step procedure. The rnite element method is more demanding of computing power, so the modal analysis method is generally preferred.

![](images/8150969137c6517b28ad6f7d05b4715a26ba5303ab2fae268a48b14b9c5b1d97.jpg)

<details>
<summary>line</summary>

| Blade azimuth (degrees) | Tower top deflection (x 10) | Blade tip deflection |
| ----------------------- | --------------------------- | ------------------- |
| 0                       | ~10                         | ~10                 |
| 30                      | ~-10                        | ~-10                |
| 60                      | ~0                          | ~0                  |
| 90                      | ~10                         | ~10                 |
| 120                     | ~-10                        | ~-10                |
| 150                     | ~0                          | ~0                  |
| 180                     | ~15                         | ~15                 |
| 210                     | ~-60                        | ~-60                |
| 240                     | ~35                         | ~35                 |
| 270                     | ~-20                        | ~-20                |
| 300                     | ~-20                        | ~-20                |
| 330                     | ~-10                        | ~-10                |
| 360                     | ~10                         | ~10                 |
</details>

Figure 5.32 Tower top and blade tip desections resulting from tower shadow, considering fundamental mode responses only.

# 5.8.10 Aeroelastic stability

Aeroelastic instability can arise when the change in aerodynamic loads resulting from a blade displacement is such as to exacerbate the displacement rather than diminish it, as is normally the case. A theoretical example would be a teetering rotor operating in stalled sow, where the rate of change of lift coefrcient with angle of attack is negative, so that the aerodynamic damping is negative likewise. In such circumstances, teeter excursions would be expected to grow until the limits of the negative damping band or of the teeter stops were reached. In practice, this phenomenon can be avoided if the blade is designed so that the blade root sapwise bending moment increases monotonically with wind speed over the full wind speed operational range (Armstrong and Hancock 1991).

A real instance of incipient aeroelastic instability was the development of an edgewise blade resonance under stalled conditions on some larger three bladed machines. A negative rate of change of lift coefrcient with angle of attack is believed to have been the prime cause – see Section 7.1.15.

Another potential instance of aeroelastic instability is classical sutter, encountered in the design of helicopter rotors, in which the blade structure is such that out-of-plane sexure in the downwind direction results in blade twisting, causing an increase in the angle of attack. During the development of some of the early large machines, the dangers of aeroelastic instability were considered to be a real concern, and much analysis work was directed to demonstrating that individual turbine designs would not be susceptible to it. However, partly no doubt because of the high torsional rigidity of the closed cell hollow structure adopted for most wind turbine blades, aeroelastic instability was not found to be critical in practice.

With the recent development of some very sexible blade designs for large machines, stability analyses are once again becoming important in the design process. Critical conditions include operation just below cut-out wind speed and standstill with extreme winds at yaw angles of 30 to 40 degrees.

# 5.9 Blade fatigue stresses

# 5.9.1 Methodology for blade fatigue design

The verircation of the adequacy of a blade design in fatigue requires knowledge of the fatigue loading cycles expected over the lifetime of the machine at different radii, derivation of the resultant stress cycles, and calculation of the corresponding fatigue damage number in relation to known fatigue properties of the material. The procedure is less or more complicated, depending upon whether blade loading in one or two planes is taken into account. If bending about only the weaker principal axis is taken into account, considering only aerodynamic lift forces, the steps involved are as follows:

1. Derive the individual fatigue load spectra for each mean wind speed and for each radius. This is a non-trivial task, because, unless wind simulation is used, the information on the periodic and stochastic load components is available in different forms, that is, as a time history and a power spectrum, respectively. Sections 5.9.2 and 5.9.3 consider methods of addressing this difrculty.   
2. Synthesise the complete fatigue load spectrum at each radius from the separate load spectra for each mean wind speed, including start-ups and shut-downs (see Section 5.5.1).   
3. Convert the fatigue load cycles (expressed as bending moments) to fatigue stresses by dividing by the appropriate section modulus. (The section modulus with respect to a particular principal axis is derned as second moment of area of the cross-section about that axis divided by the distance of the point under consideration from the axis).   
4. Sum the fatigue damage numbers, $n _ { i } / N _ { i } .$ , according to Miner’s rule, for each moment range ‘bin’ in the fatigue load spectrum, according to the appropriate S-N curve for the material. S-N curves for different blade materials are considered in Sections 7.1.8 and 7.1.9, together with the allowance necessary for mean stress.

Sections 5.9.2 and 5.9.3 are concerned with the rrst step of the preceding sequence. For a given mean wind speed, the periodic component of blade loading will be invariant over time, and the stochastic component will be stationary. As noted in Section 5.7.5, the stochastic component can be analysed either in the frequency domain (provided that a linear relationship between incident wind speed and blade loadings can be assumed) or in the time domain – i.e. by using wind simulation. Section 5.9.2 considers how the deterministic and stochastic components may be combined if the latter have been analysed in the frequency domain, and Section 5.9.3 looks in detail at the option of assessing fatigue damage completely in the frequency domain.

If the fatigue damage resulting from both in-plane and out-of-plane loading is to be computed, it is necessary to revise the ordering of the steps above to derive the periodic and stochastic components of the stress variation for each point under consideration and for each mean wind speed. For a chosen point, the procedure becomes:

A1 For a given mean wind speed, calculate the time histories of the bending moments about the principal axes resulting from the periodic load components over one blade rotation. The derivation of aerodynamic moments from blade element loads is illustrated in Figure 5.33.   
A2 Convert these bending moment time histories to stress time histories by dividing by the appropriate section modulus, and adding them together.

![](images/5bcd887c9e6bcfc9cfcbc4fb5171eb4e8831ec7cd25ea080e20ae401d9ca6091.jpg)

$$
M _ {x} = \int_ {r ^ {*}} ^ {R} (- F _ {y}) (r - r ^ {*}) d r
$$

$$
M _ {y} = \int_ {r ^ {*}} ^ {R} (F _ {x}) (r - r ^ {*}) d r
$$

$$
M _ {u u} = M _ {y} \cos \beta + M _ {x} \sin \beta
$$

$$
M _ {v v} = - M _ {y} \sin \beta + M _ {x} \cos \beta
$$

Figure 5.33 Derivation of blade bending stresses at radius r\* due to aerodynamic loads.

B For the same mean wind speed, convert the power spectrum of the stochastic bending moment component (which, because of the linearity assumption, arises from suctuating lift only) to a power spectrum of stress at the chosen point.   
C Calculate the fatigue damage resulting from the combined periodic and stochastic stress components, using the methods of Sections 5.9.2 and 5.9.3.   
D Repeat the above steps for the other mean wind speeds.   
E Add together the fatigue damages arising at each mean wind speed to obtain the total fatigue damage during normal running.

# 5.9.2 Combination of deterministic and stochastic components

Previous sections have shown how the deterministic (i.e. periodic) and stochastic components of blade bending moments can be characterised in terms of time histories and power spectra, respectively. Unfortunately, the spectral description of the stochastic loading is not in a suitable form to be combined with the time history of the periodic loading, but this difrculty can be resolved by one of two methods, as follows:

1. The power spectrum of the stochastic component can be transformed into a time history by inverse Fourier transform, which can then be added directly to the time history of the periodic component. Applications of this method have been reported by Garrad and Hassan (1986) and Warren et al. (1988). With the subsequent development of wind simulation techniques, this method is no longer commonly used because the use of transformations to generate time histories of wind speed rather than of wind loading avoids the need to assume that wind speed and wind loading are linearly related when deriving the power spectrum of the stochastic load component.   
2. A probability density function (PDF) for the load cycle ranges can be derived empirically, based on the spectral properties of the power spectrum of the stochastic and periodic components of loading combined.

The second approach is considered in the next section.

# 5.9.3 Fatigue prediction in the frequency domain

The probability density function (PDF) of peaks of a narrow band, Gaussian process are given by the well-known Rayleigh distribution. As each peak is associated with a trough of similar magnitude, the PDF of cycle ranges is Rayleigh likewise.

Wind turbine blade loading cannot be considered as narrow band, despite the concentration of energy at the rotational frequency by ‘gust slicing’ (Section 5.7.5), and neither can it be considered as Gaussian because of the presence of periodic components. Dirlik (1985) produced an empirical PDF of cycle ranges applicable to both wide and narrow band Gaussian processes, in terms of basic spectral properties determined from the power spectrum. This was done by considering 70 power spectra of various shapes, computing their rainsow cycle range distributions (see Section 5.9.5) and rtting a general expression for the cycle range PDF in terms of the rrst, second, and fourth spectral moments. Dirlik’s expression for the cycle range PDF is

$$
p (S) = \frac {\frac {D _ {1}}{Q} e ^ {- Z / Q} + \frac {D _ {2} Z}{R ^ {2}} e ^ {- (Z ^ {2} / 2 R ^ {2})} + D _ {3} Z e ^ {- (Z ^ {2} / 2)}}{2 \sqrt {m _ {o}}} \tag {5.117}
$$

where

$$
Z = \frac {S}{2 \sqrt {m _ {0}}},
$$

$$
D _ {1} = \frac {2 (x _ {m} - \gamma^ {2})}{1 + \gamma^ {2}}, D _ {2} = \frac {(1 - \gamma - D _ {1} + D _ {1} ^ {2})}{1 - R}, D _ {3} = 1 - D _ {1} - D _ {2}
$$

$$
Q = \frac {1 . 2 5 (\gamma - D _ {3} - D _ {2} R)}{D _ {1}} R = \frac {\gamma - x _ {m} - D _ {1} ^ {2}}{(1 - \gamma - D _ {1} + D _ {1} ^ {2})} x _ {m} = \frac {m _ {1}}{m _ {0}} \sqrt {\frac {m _ {2}}{m _ {4}}} \gamma = \frac {m _ {2}}{\sqrt {m _ {0} m _ {4}}}
$$

$$
m _ {i} = \int_ {0} ^ {\infty} n ^ {i} S _ {\sigma} (n) d n
$$

$S _ { \sigma } ( n )$ is the power spectrum of stress and S is the cycle stress range.

Although the Dirlik cycle range PDF was not intended to apply to signals containing periodic components, several investigations (Hoskin et al. 1989; Morgan and Tindal 1990; Bishop et al. 1991) have been carried out to determine its validity for wind turbine fatigue damage calculations, using monitored data for sapwise bending from the MS1 wind turbine on Orkney. Cycle range PDFs were calculated from power spectra of monitored strains using the Dirlik formula and fatigue damage rates derived from these PDFs compared with damage rates derived directly from the monitored signal by rainsow cycle counting. The ratio of damage calculated by the Dirlik method to damage calculated by the rainsow method ranged from 0.84 to 1.46, from 1.01 to 2.48, and from 0.73 to 2.34 in the three investigations listed, using a S/N curve exponent of 5 in each case, as the blade structure was of steel. In view of the fact that the calculated damage rates vary as the rfth power of the stress ranges, these results indicate that the Dirlik method is capable of giving quite accurate results, despite the presence of the periodic components.

There are two main drawbacks to the application of the Dirlik formula to power spectra containing periodic components. Firstly, the presence of large spikes in the spectra due to the periodic components renders them very different from the smooth distributions Dirlik originally considered, and secondly information about the relative phases of the periodic components is lost when they are transformed to the frequency domain. Morgan and Tindal (1990) illustrate the effect of varying phase angles by a comparison of plots of (cos휔t + 0.5cos3휔t) and (cos휔t – 0.5cos3휔t), which is reproduced in Figure 5.34. For a material with a S/N curve exponent of 5, stresses conforming to the rrst time history would result in 5.25 times as much fatigue damage as stresses conforming to the second.

![](images/d55b1b37eb6ac9b4cb2c1587d31cf24cbde02d56e16bb7a9ddd462cc61625f8b.jpg)

<details>
<summary>line</summary>

| Blade azimuth (degrees) | Combined signal (in phase) | Combined signal (out-of-phase) |
| ----------------------- | -------------------------- | ------------------------------ |
| 10                      | 1.5                        | 0.5                            |
| 20                      | 1.0                        | 0.7                            |
| 30                      | 0.5                        | 0.9                            |
| 40                      | 0.0                        | 1.0                            |
| 50                      | -0.5                       | 0.8                            |
| 60                      | -1.0                       | 0.5                            |
| 70                      | -1.5                       | 0.0                            |
| 80                      | -1.0                       | -0.5                           |
| 90                      | -0.5                       | -1.0                           |
| 100                     | 0.0                        | -1.5                           |
| 110                     | 0.5                        | -1.0                           |
| 120                     | 1.0                        | -0.5                           |
| 130                     | 1.5                        | 0.0                            |
| 140                     | 1.0                        | 0.5                            |
| 150                     | 0.5                        | 1.0                            |
| 160                     | 0.0                        | 1.5                            |
| 170                     | -0.5                       | 1.0                            |
| 180                     | -1.0                       | 0.5                            |
| 190                     | -1.5                       | 0.0                            |
| 200                     | -1.0                       | -0.5                           |
| 210                     | -0.5                       | -1.0                           |
| 220                     | 0.0                        | -1.5                           |
| 230                     | 0.5                        | -1.0                           |
| 240                     | 1.0                        | -0.5                           |
| 250                     | 1.5                        | 0.0                            |
| 260                     | 1.0                        | 0.5                            |
| 270                     | 0.5                        | 1.0                            |
| 280                     | 0.0                        | 1.5                            |
| 290                     | -0.5                       | 1.0                            |
| 300                     | -1.0                       | 0.5                            |
| 310                     | -1.5                       | 0.0                            |
| 320                     | -1.0                       | -0.5                           |
| 330                     | -0.5                       | -1.0                           |
| 340                     | 0.0                        | -1.5                           |
| 350                     | 0.5                        | -1.0                           |
| 360                     | 1.5                        | -0.5                           |
</details>

Figure 5.34 Effect of variation of phase angle between harmonics on combined signal.

Bishop, Wang, and Lack (1995) developed a modired form of the Dirlik formula to include a single periodic component, using a neural network approach to determine the different parameters in the formula from computer simulations.

Madsen et al. (1984) adopted a different approach to the problem of determining fatigue damage resulting from combined stochastic and periodic loading, involving the derivation of a single equivalent sinusoidal loading that would produce the same fatigue damage as the actual loading. The method applies a reduction factor, g, which is dependent on bandwidth, to account for the reduced cycle ranges implicit in a wide band as opposed to a narrow band process, and utilises Rice’s PDF for the peak value of a single sinusoid combined with a narrow band stochastic process, substituting half the maximum range of the periodic signal, including harmonics, for the amplitude of the sinusoid. A fuller summary is given in Hoskin et al. (1989). They concluded, along with Morgan and Tindal (1990), that the Madsen method yielded slightly less accurate fatigue damage values than the Dirlik method for the MS1 monitored data for sapwise bending referred to above.

Ragan and Manuel (2007) used about 2500 datasets of blade in-plane and out-of-plane bending moments from a 1.5 MW turbine in Colorado to compare fatigue damage equivalent loads calculated in the frequency domain by the Dirlik method with corresponding values calculated in the time domain. They concluded that the Dirlik method performed reasonably well for out-of-plane moments but very poorly for blade in-plane bending moments, which have a large periodic component.

# 5.9.4 Wind simulation

Wind simulation, which was introduced in Section 5.7.6, has two signircant advantages over the methods described above for fatigue damage evaluation. Firstly, it can handle non-linear relationships between wind speed suctuations and blade loadings in the calculation of stochastic loads, and secondly, it avoids the difrculty of deriving the fatigue stress ranges arising from combined periodic and stochastic load components. It is therefore currently the favoured method for detailed fatigue design. The procedure is essentially as follows:

1. Generate a three-dimensional (3-D) ‘run of wind’ for the chosen mean wind speed, with the desired shear prorle and tower shadow correction.   
2. Perform a step-by-step dynamic analysis on the turbine operating in this wind reld, to obtain in-plane and out-of-plane bending moment time histories at different radii.   
3. Convert these bending moment time histories to time histories of bending moments about the principal axes.

4. Compute stress time histories at chosen points on each cross-section.   
5. Derive the number of cycles in each stress range ‘bin’ by rainsow cycle counting (see Section 5.9.5).   
6. Scale up the cycle numbers in line with the predicted number of hours of operation at the chosen mean wind speed.   
7. Calculate corresponding fatigue damage numbers based on the applicable S-N curve.   
8. Repeat above steps for different mean wind speeds, and total the resulting fatigue damages at each point.

A computationally simpler alternative is to generate a one-dimensional ‘run of wind’ (in which only the longitudinal component of turbulence is modelled) and run a number of simulations at different, rxed yaw angles.

The duration of wind simulations is limited by available computing power, with a time history length of 600 seconds being frequently chosen. A consequence of this is that a single simulation will not provide an accurate picture of the infrequent high stress range fatigue cycles, which can have a disproportionate effect on fatigue damage for materials with high m value, such as those used for blades. However, this inaccuracy can be reduced (and quantired) by running several simulations with different random number seeds at each wind speed – see Thomsen (1998).

# 5.9.5 Fatigue cycle counting

As noted in Section 5.9.4, the dynamic analysis of turbine behaviour in a simulated wind reld yields time histories of loads or stresses that then need to be processed to abstract details of the fatigue cycles. There are two established methods of fatigue cycle counting: the reservoir method and the rainsow method, both of which yield the same result.

In the reservoir method, the load or stress history (with time axis horizontal) is imagined as the cross-section of a reservoir, which is successively drained from each low point, starting at the lowest and working up. Each draining operation then yields a load or stress cycle. See BS 5400 (British Standards Institution 1980) for a full description.

The rainsow method was rrst proposed by Matsuishi and Endo in 1968, and its title derives from the concept of water sowing down the ‘rooves’ formed when the time history is rotated so that the time axis is vertical. However, the following description not involving the rainsow analogy may be easier to understand.

The rrst step is to reduce the time history to a series of peaks and troughs, which are then termed extremes. Then, each group of four successive extremes is examined in turn to determine whether the values of the two intermediate extremes lie between the values of the initial and rnal extremes. If so, the two intermediate extremes are counted as derning a stress cycle, which is then included in the cycle count, and the two intermediate extremes are deleted from the time history. The process is continued until the complete series of extremes forming the time history has been processed in this way. Then the sequence remaining will consist simply of a diverging and a converging part from which the rnal group of stress ranges can be extracted. See ‘Fatigue Characteristics’ in the IEA series of Recommended Practices for Wind Turbine Testing and Evaluation (International Energy Agency Wind Technology Collaboration Programme 1990) for a full description of the method and for details of algorithms that can be used for automating the process.

Although, in principle, the fatigue cycles obtained from, say, a 600 second time history could be listed individually, it is normal to reduce the volume of data by allocating individual cycles to a series of equal load or stress ranges known as bins – e.g. 0–2, 2–4, 4–6 N/mm2 , etc. The fatigue spectrum is then presented in terms of the number of cycles falling into each ‘bin’.

# 5.10 Hub and low-speed shaft loading

# 5.10.1 Introduction

The loadings on the hub consist of the aerodynamic, gravity, and inertia loadings on the blades and the equal and opposite (discounting hub self-weight) reaction from the shaft. For rxed hub machines, the loading on the shaft will include a signircant moment arising from blade aerodynamic loads, but in the case of teetered two bladed rotors, this moment will be virtually eliminated. In either case, however, the cantilevered low-speed shaft will experience large suctuating moments due to rotor weight as it rotates. Figure 5.35 shows a low-speed shaft and front bearing in a factory prior to assembly.

The shaft moments due to out-of-plane loads on the blades can be expressed as moments about a pair of rotating axes, one perpendicular to blade 1 and the other parallel

![](images/e17371b329615ecfb44bc4302a30ff650d9649f3fa136717bdf822b7a124a50f.jpg)

<details>
<summary>natural_image</summary>

Factory worker operating machinery beside large industrial pipe fitting (no visible text or symbols)
</details>

Figure 5.35 Low-speed shaft and front bearing before assembly. The hub mounting sange at the right hand end is bolted to a temporary support to allow the bearing to be threaded on the shaft. Source: Reproduced by permission of NEG Micon.

![](images/e7e43065cdec1ae27aee2bc975c51ff99800994de31b42982613103a7f96a92c.jpg)

<details>
<summary>text_image</summary>

Blade 1
MZS
ψ1
MYS
O
MYS
MYS
Blade 2
MYS
Blade 3
MY1
MY2
MY2
O
</details>

Figure 5.36 Shaft bending moments with rotating axis system referred to blade 1.

to it. In the case of a three bladed rotor, these moments are, respectively, as follows:

$$
M _ {Y S} = \Delta M _ {Y 1} - \frac {1}{2} (\Delta M _ {Y 2} + \Delta M _ {Y 3}) \quad M _ {Z S} = \frac {\sqrt {3}}{2} (\Delta M _ {Y 3} - \Delta M _ {Y 2}) \tag {5.118}
$$

Here $\Delta M _ { \mathrm { Y } 1 } , \Delta M _ { \mathrm { Y } 2 }$ , and $\Delta M _ { \mathrm { Y } 3 }$ are the suctuations of the blade out-of-plane moments about the hub centre $( M _ { \mathrm { Y } 1 } , M _ { \mathrm { Y } 2 }$ , and $M _ { \mathrm { Y } 3 } )$ about the mean value. See Figure 5.36.

# 5.10.2 Deterministic aerodynamic loads

The deterministic aerodynamic loads on the rotor may be split up into a steady component, equal for each blade, and a periodic component, also equal for each blade, but with differing phase angles. The blade root out-of-plane bending moments due to the rrst component will be in equilibrium and will apply a ‘dishing’ moment to the hub that will result in tensile stresses in the front and compression stresses in the rear. These stresses will be uniaxial for a two bladed rotor and biaxial for a three bladed rotor.

The suctuations in out-of-plane blade root bending moment due to wind shear, shaft tilt, and yaw misalignment will often be approximately sinusoidal, with a frequency equal to the rotational frequency. Using Eq. (5.118), it is easily shown that, for a sinusoidally varying blade root bending moment with range 훥M, the range of the resulting shaft bending moment is 1.5훥M for a three bladed machine and 2훥M for a rigid hub two bladed machine.

![](images/de883869267609a2ac39a76107c4def9d6f4c9ee8b274c35ca5cb6b4877855e3.jpg)

<details>
<summary>line</summary>

| Azimuth at blade 1 (degrees) | Shaft BM for three-bladed machine (thick line) | Blade 1 out-of-plane root BM (thin line) | Shaft BM for two-bladed rigid hub machine (dashed line) |
| ---------------------------- | --------------------------------------------- | ---------------------------------------- | ---------------------------------------------------- |
| 0                            | 250                                           | -400                                     | 250                                                  |
| 30                           | 220                                           | -350                                     | 220                                                  |
| 60                           | 180                                           | -300                                     | 180                                                  |
| 90                           | 100                                           | -200                                     | 100                                                  |
| 120                          | -50                                           | -150                                     | -50                                                  |
| 150                          | -150                                          | -100                                     | -150                                                 |
| 180                          | -250                                          | -200                                     | -250                                                 |
| 210                          | -350                                          | -250                                     | -350                                                 |
| 240                          | -450                                          | -350                                     | -450                                                 |
| 270                          | -350                                          | -250                                     | -350                                                 |
| 300                          | -250                                          | -150                                     | -250                                                 |
| 330                          | -150                                          | -50                                      | -150                                                 |
| 360                          | -50                                           | 5                                        | -5                                                   |
</details>

Figure 5.37 Shaft bending moment suctuations due to wind shear.

In the case of wind shear conforming to a power law, the loading on a horizontal blade is always greater than the average of the loadings on blades pointing vertically upwards and downwards, so the loading departs signircantly from sinusoidal. The shaft bending moment suctuations due to wind shear with a 0.2 exponent are compared in Figure 5.37 for two and three bladed 80 m diameter, 60 m hub height rigid hub machines operating at 15 rpm in a hub-height wind speed of 10 m/s. The ratio of moment ranges is still close to 2:1.5.

# 5.10.3 Stochastic aerodynamic loads

The out-of-plane blade root bending moments arising from stochastic loads on the rotor will result in both a suctuating hub ‘dishing’ moment (see above) and suctuating shaft bending moments. For a two bladed, rigid hub rotor, the shaft moment is equal to the difference between the two out-of-plane blade root bending moments, or teeter moment, the standard deviation of which is given by Eq. (5.102a). Similarly, the standard deviation of the mean of these two moments (i.e. the ‘dishing’ moment) is given by Eq. (5.103).

The derivation of the standard deviation of the shaft moment for a three bladed machine is at rrst sight more complicated, as the integration has to be carried out over three blades instead of two. However, if the shaft moment about an axis parallel to one of the blades, $M _ { \mathrm { Z S } }$ (Figure 5.36), is chosen, the contribution of loading on that blade disappears, and the expression for the shaft moment standard deviation becomes

$$
\sigma_ {M z s} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} \kappa_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}) \frac {\sqrt {3}}{2} r _ {1} \frac {\sqrt {3}}{2} r _ {2} | r _ {1} | | r _ {2} | d r _ {1} d r _ {2} (5. 1 1 9 a)
$$

where the limits of the integrations refer to the other two blades. $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 )$ is given by Eq. (5.51), with $\varOmega \tau$ set equal to zero when $r _ { 1 }$ and $r _ { 2 }$ are radii to points on the same blade, and replaced by $2 \pi / 3$ when $r _ { 1 }$ and $r _ { 2 }$ are radii to points on different blades. Note that, compared with the two bladed case, the cross-correlation function, $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 )$ , will be increased when $r _ { 1 }$ and $r _ { 2 }$ relate to different blades, because of the reduced separation between the two blade elements resulting from the $1 2 0 ^ { \circ }$ angle between the blades. Eq. (5.119a) can be rewritten in terms of the normalised cross-correlation function, $\rho _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 ) = \kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 ) / \sigma _ { u } ^ { 2 }$ , as follows:

$$
\sigma_ {M z s} ^ {2} = \sigma_ {u} ^ {2} \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} \rho_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}) \frac {\sqrt {3}}{2} r _ {1} \frac {\sqrt {3}}{2} r _ {2} | r _ {1} | | r _ {2} | d r _ {1} d r _ {2} \tag {5.119b}
$$

In the case of 80 m diameter turbines with SC40 blades operating in wind with a turbulence length scale of 147 m, the standard deviation of shaft moment due to stochastic loading for a three bladed machine is 82% of that for a two bladed, rxed hub machine rotating at the same speed. This ratio would rise to ${ \sqrt { 3 } } / 2$ if the effect on the cross-correlation function of the 120∘ blade spacing were ignored.

It is worth noting that, for a three bladed machine, the standard deviation of the shaft moment $M _ { \mathrm { Y S } }$ due to stochastic loading is the same as that of $M _ { \mathrm { Z S } }$ (see Figure 5.36 for dernitions).

By analogy with the derivation of the shaft moment above, the standard deviation of the hub ‘dishing’ moment for a three bladed machine due to stochastic loading is given by

$$
\sigma_ {M h} ^ {2} = \frac {1}{4} \sigma_ {u} ^ {2} \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \int_ {- R} ^ {R} \int_ {- R} ^ {R} \rho_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}) \frac {\sqrt {3}}{2} r _ {1} ^ {2} \frac {\sqrt {3}}{2} r _ {2} ^ {2} d r _ {1} d r _ {2} \tag {5.120}
$$

where the integrations are carried out over two blades only, and the cross-correlation function is modired as before to account for the $1 2 0 ^ { 0 }$ angle between the blades.

It can be shown that

$$
\frac {1}{4} \sigma_ {\mathrm{Mzs}} ^ {2} + \sigma_ {\mathrm{Mh}} ^ {2} = \frac {3}{4} \sigma_ {\mathrm{Myl}} ^ {2} \tag {5.121}
$$

# 5.10.4 Gravity loading

An important component of shaft loading is the cyclic cantilever bending moment due to rotor weight, which usually has a dominant effect on shaft fatigue design. As an illustration, a rotor consisting of three SC40 blades weighing 7.7 t each, and a 25 t hub cantilevered 1.7 m beyond the shaft main bearing, will produce a shaft gravity moment range of about 1600 KNm. This compares with a shaft moment range due to wind shear of 630 KNm for a hub-height wind of 10 m/s and a shear exponent of 0.2, and a shaft moment standard deviation of 350 KNm due to turbulence, taking a turbulence intensity of 21% and the same hub-height mean wind speed. Note that the shaft moment due to wind shear relieves that due to gravity.

# 5.11 Nacelle loading

# 5.11.1 Loadings from rotor

The previous section considered the moments applied to the shaft by the rotor hub using an axis system rotating with the shaft. In addition to these moments, the shaft also experiences an axial load due to rotor thrust and radial forces arising from differential blade edgewise loadings and any out-of-balance centrifugal force.

![](images/261d1ff6f75fdd388f051a7f507e891cb8d80e2e8ece74996447b034920e2ace.jpg)

<details>
<summary>text_image</summary>

M_{Y1} sin \psi
M_{Y1} cos \psi
O_H
Shaft tilt \eta
O_N
z_N
x_N
M_{Y1} sin \psi
M_Y1 cos \psi
O_H
Blade 1
Blade 3
</details>

Figure 5.38 Components of blade 1 out-of-plane root bending moment about rxed set of axes.

To calculate loadings on the elements of the nacelle structure, it is rrst necessary to transform the shaft loads (or the constituent blade loads) derned in terms of the rotating axis system into nacelle loads expressed in terms of a rxed axis system. Here the conventional system in which the x axis is downwind, the y axis is horizontal to starboard, and the z axis is vertically upwards will be adopted. Thus the moments acting on the nacelle about the y and z axes as a result of the blade root out-of-plane bending moments are as follows for a three bladed machine with shaft tilt 휂:

$$
M _ {Y N} = M _ {Y 1} \cos \psi + M _ {Y 2} \cos (\psi - 1 2 0 ^ {0}) + M _ {Y 3} \cos (\psi - 2 4 0 ^ {0}) \tag {5.122}
$$

$$
M _ {Z N} = (M _ {Y 1} \sin \psi + M _ {Y 2} \sin (\psi - 1 2 0 ^ {0}) + M _ {Y 3} \sin (\psi - 2 4 0 ^ {0})) \cos \eta \tag {5.123}
$$

where 휓 is the azimuth of blade 1. See Figure 5.38.

It is instructive to compare the moments acting on the nacelle due to deterministic loading for three bladed and two bladed machines. The suctuations of out-of-plane root bending moment due to wind shear and yaw misalignment are approximately proportional to the cosine of blade azimuth for an unstalled blade. Substituting $M _ { Y 1 } = M _ { 0 }$ cos휓, $M _ { Y 2 } = M _ { 0 } \cos ( \psi - 2 \pi / B )$ , etc. into Eqs. (5.122) and (5.123) yields $M _ { Y N } = 1 . 5 M _ { 0 }$ and $M _ { Z N } = 0$ for a three bladed machine, whereas the corresponding results for a rigid hub two bladed machine are $M _ { Y N } = M _ { 0 } \left( 1 + \mathrm { c o s } 2 \psi \right)$ and $M _ { Z N } = M _ { 0 }$ sin2휓cos 휂. Thus, the moments on the nacelle are constant for a three bladed machine but continually suctuating with amplitude $M _ { 0 }$ for a rigid hub two bladed machine. Parallel results are obtained for $M _ { Y 1 } = M _ { 0 }$ sin휓, which approximates to the out-of-plane root bending moment due to shaft tilt – again for an unstalled blade. The full comparison is given in Table 5.7.

Table 5.7 Comparison between nacelle moments due to deterministic loads for two and three bladed machines. 

<table><tr><td rowspan="2"></td><td colspan="2">Nacelle moments resulting from out-of-plane blade root bending moment fluctuations due to wind shear and yaw misalignment approximated by  $M_{Y1} = M_0 \cos\psi$ ,  $M_{Y2} = M_0 \cos(\psi - 2\pi/B)$ , etc.</td><td colspan="2">Nacelle moments resulting from out-of-plane blade root bending moment fluctuations due to shaft tilt approximated by  $M_{Y1} = M_0 \sin\psi$ ,  $M_{Y2} = M_0 \sin(\psi - 2\pi/B)$ , etc.</td></tr><tr><td>Nacelle nodding moment,  $M_{YN}$ </td><td>Nacelle yaw moment,  $M_{ZN}$ </td><td>Nacelle nodding moment,  $M_{YN}$ </td><td>Nacelle yaw moment,  $M_{ZN}$ </td></tr><tr><td>Three bladed machine</td><td> $1.5 M_0$ </td><td>Zero</td><td>Zero</td><td> $1.5 M_0 \cos\eta$ </td></tr><tr><td>Two bladed, rigid hub machine</td><td> $M_0 (1 + \cos2\psi)$ </td><td> $M_0 \sin2\psi \cos\eta$ </td><td> $M_0 \sin2\psi$ </td><td> $M_0 (1 - \cos2\psi) \cos\eta$ </td></tr></table>

It is clear that the moments acting on the nacelle due to deterministic loading are much more benign for a three bladed rotor than for a two bladed rotor with rigid hub.

In the case of three bladed machines, the standard deviation of shaft bending moment due to stochastic rotor loading is independent of the rotating axis chosen (Section 5.10.3), so the standard deviation of the resulting moment on the nacelle will take the same value about both the nacelle y and z axes.

# 5.11.2 Nacelle wind loads

Except in the case of sideways wind loading, wind loads on the nacelle are not usually of great signircance. They may be calculated according to the rules given in standard wind loading codes. For sideways wind loading, a drag factor of 1.2 will generally be found to be conservative.

# 5.12 Tower loading

# 5.12.1 Extreme loads

It is customary to base the calculation of extreme loads on a non-operational turbine on the 50 year return 3 second gust. Several loading conrgurations may need to be considered, and the critical load case for the tower base will generally differ from that for the tower top. In addition, it is necessary to investigate the extreme operational load cases, as these can sometimes govern instead if the tip speed is high in relation to the design gust speed.

In the case of non-operational, stall-regulated machines, the critical case for the tower base occurs when the wind is blowing from the front and inducing maximum drag loading on the blades. By contrast, sideways wind loading to produce maximum lift on a blade pointing vertically upwards or rear wind loading on the rotor with one blade shielded by the tower will produce the maximum tower top bending moment.

One of the benerts of pitch regulation of three bladed machines is that blade feathering at shut-down considerably reduces non-operational rotor loading. The critical conrguration as far as tower base bending moment is concerned is sideways wind loading, with two of the blades inclined at $3 0 ^ { \circ }$ to the vertical. The horizontal component of the loading on these blades is $\cos ^ { 3 } 3 0 ^ { \circ }$ of the loading on a vertical blade, so that the total rotor loading is only $4 3 . 3 \% = 1 0 0 . { \sqrt { 3 } } / { 4 \% } )$ of the maximum experienced by a stall-regulated machine.

The cases of sideways wind loading on a wind turbine referred to previously can only arise if the yaw drive is disabled by grid loss for sufrcient time for a $9 0 ^ { \circ }$ wind direction change to take place, so IEC 61400-1 edition 3 treats this case (DLC 6.2) as an abnormal load case with a reduced load factor of 1.1 (in place of 1.35 for normal load cases). As a result of this, the load case causing extreme tower base overturning moment on pitch-regulated machines is not always clear cut. If the rotor is braked with one blade vertically upwards and the yaw angle is small (corresponding to IEC 61400-1 edition 3 DLC 6.1), the loading on the top blade could approach maximum lift. Loads on the other blades would be smaller, and their horizontal components would probably act in the opposite direction. The maximum loading on the top blade would be $( 0 . 5 \rho V ^ { 2 } ) 1 . 5 A _ { B } ,$ , ignoring wind shear, where $A _ { B }$ is the blade area. On the other hand, DLC 6.2 gives a drag loading of 2cos $^ 3 3 0 ^ { 0 } ( 0 . 5 \rho V ^ { 2 } ) \tilde { 1 . } 3 A _ { B } = ( 0 . 5 \rho V ^ { 2 } ) 1 . 6 9 A _ { B } .$ again ignoring wind shear, which becomes $( 0 . 5 \rho V ^ { 2 } ) 1 . 8 6 A _ { B }$ after inclusion of the load factor. This is somewhat less than the factored load on a vertical blade experiencing maximum lift of $2 . 0 2 5 ( 0 . 5 \rho V ^ { 2 } ) A _ { B }$ . However, the drag loading on the blades in DLC 6.2 acts in the same direction as the drag load on the tower, whereas the lift load on the vertical blade in DLC 6.1 acts at right angles to the drag loading on the tower.

Information on the drag factors appropriate for cylindrical and lattice towers is to be found in EN 1991-1-4:2005, Eurocode 1: Actions on Structures – Part 1-4: General Actions – Wind Actions, and in national codes such as BS 8100 (British Standards Institution 1984) or DS 410 (1983). The drag factor for a cylindrical tower is typically 0.6–0.7. Rotor loading is generally the dominating component of tower base moment for stall-regulated machines, but with pitch-regulated machines, the contributions of tower loading and rotor loading are often of similar magnitude.

# 5.12.2 Dynamic response to extreme loads

Just as in the case of the single, stationary cantilevered blade considered in Section 5.6.3, the quasi-static bending moments in the tower calculated for the extreme gust speed will be augmented by inertial moments resulting from the excitation of resonant tower oscillations by turbulence. As before, it is convenient to express this augmentation in terms of a dynamic factor, $Q _ { \mathrm { D } } ,$ , derned as the ratio of the peak moment over a 10 minute period, including resonant excitation of the tower, to the peak quasi-static moment over the same period. Thus

$$
M _ {M a x} = \frac {1}{2} \rho U _ {e 5 0} ^ {2} H \oint C _ {f} \left(\frac {z}{H}\right) ^ {1 + 2 \alpha} d A \cdot Q _ {D} \tag {5.124}
$$

where

$U _ { e 5 0 }$ is the 50 year return gust speed at hub height

z is height above ground

H is the hub height

$\mathrm { C } _ { f }$ is the force factor (lift or drag) for the element under consideration

훼 is the shear exponent, taken as 0.11 in IEC 61400-1

and

$$
Q _ {D} = \frac {1 + g \left(2 \frac {\sigma_ {u}}{\overline {{U}}}\right) \sqrt {K _ {S M B} + \frac {\pi^ {2}}{2 \delta} R _ {u} (n _ {1}) K _ {S x} (n _ {1}) . \lambda_ {M 1} ^ {2}}}{1 + g _ {0} \left(2 \frac {\sigma_ {u}}{\overline {{U}}}\right) \sqrt {K _ {S M B}}} [ \mathrm{seeEq.(5.17)} ]
$$

The integral sign $\boldsymbol { \oint }$ signires that the integral is to be undertaken over each blade, the nacelle, and the tower. The derivation of Eq. (5.17) is explained in Section 5.6.3 and Appendix A5 in relation to a cantilevered blade.

The essentially similar procedure for a tower supporting a braked rotor and nacelle is as follows:

1. Calculate the resonant size reduction factor, $K _ { S x } ( n _ { 1 } )$ , which resects the effect of the lack of correlation of the wind suctuations at the tower natural frequency along the blades and tower. Adopting an exponential expression for the normalised co-spectrum as before, Eq. (A5.25) becomes

$$
K _ {S x} (n _ {1}) = \frac {\oint \oint \exp [ - C s n _ {1} / \overline {{U}} ] C _ {f} ^ {2} c (r) c (r ^ {\prime}) \mu_ {1} (r) \mu_ {1} (r ^ {\prime}) d r d r ^ {\prime}}{(\oint C _ {f} c (r) \mu_ {1} (r) d r) ^ {2}} \tag {5.125}
$$

where

the integral sign $\boldsymbol { \oint }$ denotes integration over the blades and the tower

r and $r '$ denote radius in the case of the blades and depth below the hub in the case of the tower

s denotes the separation between the elements dr and $d \boldsymbol { r } ^ { \prime }$

$C _ { f }$ is the relevant force coefrcient

$c ( r )$ denotes chord in the case of the blades and diameter in the case of the tower $\mu _ { 1 } ( r )$ denotes the tower rrst mode shape

This expression can be considerably simplired by setting $\mu _ { 1 } ( r )$ to unity for the rotor and ignoring the tower loading contribution entirely. This is not unreasonable, as only loading near the top of the tower is of signircance, and this does not add much to the spatial extent of the loaded area.

2. Calculate the damping logarithmic decrement, 훿, for the tower rrst mode. The aerodynamic component is given by

$$
\delta_ {a} = 2 \pi \xi_ {a} = 2 \pi \frac {c _ {a 1}}{2 m _ {T 1} \omega_ {1}} = 2 \pi \frac {\oint \hat {c} _ {a} (r) \mu_ {1} ^ {2} (r) d r}{2 m _ {T 1} n _ {1}} \tag {5.126}
$$

where $m _ { T 1 }$ is the generalised mass of the tower, nacelle, and rotor (including the contribution of rotor inertia) with respect to the rrst mode given by Eq. (5.110), and $n _ { 1 }$ is the tower natural frequency in Hz. For a stall-regulated machine facing the wind, the rotor contribution to aerodynamic damping is simply $\rho \overline { { U } } C _ { D } A _ { R } / 2 m _ { T 1 } n _ { 1 }$ , where $A _ { R }$ is the rotor area.

3. Calculate the standard deviation of resonant nacelle displacement according to

$$
\frac {\sigma_ {x 1}}{\overline {{x}} _ {1}} = 2 \frac {\sigma_ {u}}{\overline {{U}}} \frac {\pi}{\sqrt {2 \delta}} \sqrt {R _ {u} (n _ {1})} \sqrt {K _ {S x} (n _ {1})} \quad [ \text { see   Eq. } (5. 7) ].
$$

4. Calculate the ratio $\lambda _ { \mathrm { M l } }$ , which relates the ratio of the standard deviation of resonant tower base moment to the mean value to the corresponding ratio for nacelle displacement as follows:

$$
\frac {\sigma_ {M 1}}{\overline {{M}}} = \lambda_ {M 1} \frac {\sigma_ {x 1}}{\overline {{x}} _ {1}} \quad [ \text { see   Eq. } (5. 8 a) ]
$$

$\operatorname { I f } \mu _ { 1 } ( r )$ is set to unity for the rotor, $\lambda _ { \mathrm { M l } }$ is given by

$$
\lambda_ {M 1} = \frac {\int_ {0} ^ {H} m (z) \mu_ {1} (z) . z d z \left\{C _ {D} A _ {R} + \int_ {0} ^ {H} C _ {f} \left[ \frac {U (z)}{\overline {{U}}} \right] ^ {2} d (z) \mu_ {1} (z) d z \right\}}{m _ {T 1} H \left\{C _ {D} A _ {R} + \int_ {0} ^ {H} C _ {f} \left[ \frac {U (z)}{\overline {{U}}} \right] ^ {2} d (z) \frac {z}{H} d z \right\}} \tag {5.127a}
$$

where z is the height up the tower measured from the base, $d ( z )$ is the tower diameter at height z and H is the hub height. If the loading on the tower is relatively small, this approximates to

$$
\lambda_ {M 1} = \frac {\int_ {0} ^ {H} m (z) \mu_ {1} (z) . z d z}{m _ {T 1} . H} \tag {5.127b}
$$

which is close to unity because the tower head mass dominates the integral.

5. Calculate the size reduction factor for the root bending moment quasi-static or background response, $K _ { S M B } ,$ , which resects the lack of correlation of the wind suctuations along the blades and tower. $K _ { S M B }$ may be derived from a similar expression to that for the resonant size reduction factor given in Eq. (5.125) but with the exponential function modired to $\exp [ - s / 0 . 3 L _ { u } ^ { x } ]$ .   
6. Calculate the peak factors for the combined (i.e. resonant plus quasi-static) and quasi-static responses in terms of the respective zero up-crossing frequencies. [In estimating the zero up-crossing frequency of the quasi-static response, the blade area should be replaced by the rotor area in Eq. (A5.57).]   
7. Substitute the parameter values derived in steps 1–6 into Eq. (5.17) to obtain the dynamic factor, $Q _ { D }$ .

In the case of a rotor that is allowed to idle when shut down, turbine geometry is continually changing as the rotor rotates to and fro in response to wind gusts, so the calculation of resonant tower excitation, should it occur, becomes a complex undertaking.

# 5.12.3 Operational loads due to steady wind (deterministic component)

Tower fore and aft bending moments result from rotor thrust loading and rotor moments. The moments acting on the nacelle due to deterministic rotor loads have already been described in Section 5.11.1. Although the thrust loads on individual blades vary considerably with azimuth as a result of yaw misalignment, shaft tilt, or wind shear, the suctuations on different blades balance each other, so that the total rotor thrust shows negligible azimuthal variation as a result of these effects. For example, on two bladed machines, a wind shear exponent of 0.2 results in a rotor thrust variation of about $\pm 1 \%$ .

Tower shadow loading results in a sinusoidal tower top displacement at blade passing frequency – see Figure 5.32.

Figure 5.39 illustrates the variation of rotor thrust with wind speed for stall- and pitch-regulated 80 m diameter three bladed machines.

# 5.12.4 Operational loads due to turbulence (stochastic component)

# Analysis in the frequency domain

Except near the top of the tower, the dominant source of fore–aft stochastic tower bending moments is rotor thrust. The standard deviation of rotor thrust can be expressed in terms of the turbulence intensity and the cross-correlation function between wind suctuations at different points on the rotor, following the method used for deriving the standard deviation of stochastic blade root bending moment in Section 5.7.5. As before, a linear relation between the wind suctuations and the resultant load suctuations is assumed, so that the perturbation of loading per unit length of blade, $q ,$ at radius $r$ is given by

$$
q = \frac {1}{2} \rho \Omega r c (r) \frac {d C _ {L}}{d \alpha} u \quad [ \text { see   Eq. } (5. 2 5) ]
$$

and the perturbation of rotor thrust by

$$
\Delta T = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) \oint u c (r) r d r \tag {5.128}
$$

where the integral sign $\boldsymbol { \oint }$ signires that the integration is carried out over the whole rotor. Hence the following expression for the variance of the rotor thrust is obtained:

$$
\sigma_ {T} ^ {2} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \sigma_ {u} ^ {2} \oint \oint \rho_ {u} ^ {o} (r _ {1}, r _ {2}, 0) c (r _ {1}) c (r _ {2}) r _ {1} r _ {2} d r _ {1} d r _ {2} \tag {5.129}
$$

where $\rho _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 )$ is the normalised cross-correlation function, $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 ) / \sigma _ { u } ^ { 2 }$ for points at radii $r _ { 1 }$ and $r _ { 2 }$ on the same or on different blades. $\kappa _ { u } ^ { o } ( r _ { 1 } , r _ { 2 } , 0 )$ is given by Eq. (5.51), with $\varOmega \tau$ replaced by the phase angle between the two blades on which are $r _ { 1 }$ and $r _ { 2 }$ measured. For a three bladed, 80 m diameter rotor and an integral length scale of 147 m, the reduction in the standard deviation of the stochastic rotor thrust suctuations is about 20% due to the lack of correlation of the wind speed variations over the rotor. If the machine is rotating at 15 rpm in an 8 m/s wind and the turbulence intensity is 20%, the rotor thrust standard deviation will be about 38 KN – i.e. 22% of the steady value.

![](images/f59e922f3c5cb669ae1906e396f040488656c554b268e0e816682d1c02099517.jpg)

<details>
<summary>line</summary>

| Mean wind speed (m/s) | 2 MW stall-regulated machine (kN) | Pitch-regulated machine with 1.7 MW power limit (kN) |
| --------------------- | ---------------------------------- | ---------------------------------------------------- |
| 5                     | ~30                                | ~30                                                  |
| 10                    | ~260                               | ~260                                                 |
| 15                    | ~280                               | ~150                                                 |
| 20                    | ~300                               | ~120                                                 |
| 25                    | ~350                               | ~100                                                 |
| 30                    | ~400                               | ~90                                                  |
</details>

Figure 5.39 Rotor thrust during operation in steady, uniform wind: variation with wind speed for similar stall-regulated and pitch-regulated machines.

The derivation of the expression for the power spectrum of rotor thrust parallels that for the power spectrum of blade root bending moment (Section 5.7.5), yielding

$$
S _ {T} (n) = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) ^ {2} \oint \oint S _ {u J, K} ^ {o} (r _ {1}, r _ {2}, n) c (r _ {1}) c (r _ {2}) r _ {1} r _ {2} d r _ {1} d r _ {2} \tag {5.130}
$$

where $S _ { u J . K } ^ { o } ( r _ { 1 } , r _ { 2 } , n )$ is the rotationally sampled cross-spectrum for points at radii $r _ { 1 }$ and $r _ { 2 }$ on blades J and K, respectively. Note that on a machine with three blades, $\mathbf { A } ,$ B, and $\mathbf { C } , S _ { u J , K } ^ { o } ( r _ { 1 } , r _ { 2 } , n )$ is complex when J and K are different, but $S _ { u A , B } ^ { o } ( r _ { 1 } , r _ { 2 } , n )$ a nd u J,K  u A,BS o u A,C(r1 , r2 , n) are complex conjugates, so the double integral in Eq. (5.130) is still real. $S _ { u A , C } ^ { o } ( r _ { 1 } , r _ { 2 } , \bar { n } )$ An example power spectrum of rotor thrust for an 80 m diameter three bladed machine is shown in Figure 5.40. It can be seen that there is some concentration of energy at the blade passing frequency of 0.75 Hz due to gust slicing, but that the effect is not large. The concentration effect is signircantly greater for two blade machines – see Figure 5.41. This shows the power spectrum of rotor thrust for a two bladed machine with the same blade plan-form but rotating 22.5% faster to give comparable performance.

In addition to thrust suctuations, longitudinal turbulence will also cause rotor torque suctuations and in-plane rotor loads due to differential loads on different blades, both of which will result in tower sideways bending moments. The expression for the in-plane component of aerodynamic lift per unit length, $\begin{array} { r } { - F _ { Y } ( r ) = \frac { 1 } { \gamma } \rho W ^ { \hat { 2 } } C _ { L } c ( r ) } \end{array}$ sin $\phi .$ , can be differentiated with respect to the wind suctuation as follows:

$$
\begin{array}{l} - \frac {d F _ {Y}}{d u} = \frac {1}{2} \rho c (r) \frac {d}{d u} [ W ^ {2} \sin \phi . C _ {L} ] \\ = \frac {1}{2} \rho c (r) \frac {d}{d u} [ W \{U _ {\infty} (1 - a) + u \} C _ {L} ] \cong \frac {1}{2} \rho c (r) W \left[ C _ {L} + \sin \phi \frac {d C _ {L}}{d \alpha} \right] \\ \end{array}
$$

so, approximately,

$$
- \frac {d F _ {Y}}{d u} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) c (r). r \left[ \frac {C _ {L}}{d C _ {L} / d \alpha} + \sin \phi \right] \tag {5.131a}
$$

Thus the standard deviation of rotor torque is approximately given by

$$
\sigma_ {Q} = \left(\frac {1}{2} \rho \Omega \frac {d C _ {L}}{d \alpha}\right) \sigma_ {u} \left\{\oint r ^ {2} c (r) \left[ \frac {C _ {L}}{d C _ {L} / d \alpha} + \sin \phi \right] d r \right\} \tag {5.131b}
$$

[which parallels Eq.(5.26)] provided the relationship between blade loading and wind speed suctuation remains linear and the turbulence length scale is large compared with rotor diameter. Eq. (5.131b) can be used to derive an expression for the variance of the rotor torque in the same way as for rotor thrust above. At the top of the tower the stochastic $M _ { \mathrm { X } }$ (i.e. side-to-side) moment due to rotor torque suctuations is typically of the same order of magnitude as the stochastic $M _ { \mathrm { Y } }$ (i.e. fore–aft) moment due to differential out-of-plane loads on the rotor, but at the tower base the dominant effect of

![](images/449629c146075bed6e1d6c1c2f869d0dbf4b29514ce28acc986f41a1a5745c13.jpg)

<details>
<summary>line</summary>

| Frequency, n (Hz) | Power spectral density of thrust, nSₜ(n) (kN²) |
| ----------------- | --------------------------------------------- |
| 0.01              | ~450                                          |
| 0.1               | ~50                                           |
| 1                 | ~2400                                         |
| 10                | ~50                                           |
</details>

Figure 5.40 Power spectra of rotor thrust and resultant tower base fore–aft bending moment for three bladed, 80 m diameter turbine.

![](images/402ddb2de9471d5d3011f635e347ed506ec3e8f838049881267984d72c26542f.jpg)

<details>
<summary>line</summary>

| Frequency, n (Hz) | Power spectral density of thrust, nS₁(n) (kN²) |
| ----------------- | --------------------------------------------- |
| 0.01              | ~250                                          |
| 0.1               | ~0                                            |
| 0.5               | ~2700                                         |
| 1                 | ~200                                          |
| 10                | ~0                                            |
</details>

Figure 5.41 Power spectra of rotor thrust and resultant tower base fore–aft bending moment for two bladed, 80 m diameter turbine.

rotor thrust loading means that the stochastic side-to-side moments are usually signircantly less than the stochastic fore–aft moments before the excitation of tower resonance is taken into account.

# Analysis in the time domain

As noted in Section 5.7.5, there are situations, such as operation in stalled sow, when the linear relationship between blade loading and wind speed suctuations required for analysis in the frequency domain does not apply. In these cases, recourse must be made to analysis in the time domain using wind simulation techniques such as described in Section 5.7.6.

# 5.12.5 Dynamic response to operational loads

The power spectrum of rotor thrust will usually contain some energy at the tower natural frequency, leading to dynamic magnircation of desections and hence of tower bending moments. The power spectrum of hub desection, $S _ { x 1 } \left( n \right)$ , resulting from the excitation of the tower rrst fore–aft sexural mode, is related to the power spectrum of rotor thrust by

$$
S _ {x 1} (n) = \frac {S _ {T} (n)}{k _ {1} ^ {2}} \frac {1}{[ (1 - n ^ {2} / n _ {1} ^ {2}) ^ {2} + 4 \xi_ {1} ^ {2} n ^ {2} / n _ {1} ^ {2} ]} \tag {5.132}
$$

This relation is analogous to Eq. (5.90) and derived in the same way.

The amplitude of tower base fore–aft moment at resonance in the rrst mode, $M _ { \mathrm { Y 1 } }$ , can be derived from the corresponding amplitude of hub desection, $x _ { H 1 }$ , as follows

$$
M _ {Y 1} = \omega_ {1} ^ {2} x _ {H 1} \int_ {0} ^ {H} m (z) \mu (z) z d z = \omega_ {1} ^ {2} x _ {H 1} m _ {T 1} H \frac {\int_ {0} ^ {H} m (z) \mu (z) z d z}{H \int_ {0} ^ {H} m (z) \mu^ {2} (z) d z} \tag {5.133}
$$

The quotient on the right hand side is close to unity because of the dominance of the tower head mass, so, substituting $k _ { 1 }$ for $\omega _ { 1 } ^ { 2 } m _ { T 1 }$ , the equation reduces to $M _ { Y 1 } = x _ { H 1 } k _ { 1 } H$ , which applies at any exciting frequency. Hence the power spectrum for the tower base fore–aft bending moment due to rotor thrust loading is given by

$$
S _ {M y 1} (n) = S _ {T} (n). H ^ {2} \frac {1}{[ (1 - n ^ {2} / n _ {1} ^ {2}) ^ {2} + 4 \xi^ {2} n ^ {2} / n _ {1} ^ {2} ]} \tag {5.134}
$$

The aerodynamic damping is almost entirely provided by the rotor, the damping ratio for the rrst tower mode being approximately

$$
\xi_ {a 1} = B \frac {\frac {1}{2} \rho \Omega \int_ {0} ^ {R} \frac {d C _ {l}}{d \alpha} r c (r) d r}{2 m _ {T 1} \omega_ {1}} \tag {5.135}
$$

where B is the number of blades (see Section 5.8.4). The overall damping ratio is obtained by adding this to the structural damping ratio for the tower (see Table 5.5) and is generally low compared to the blade rrst mode damping because of the large tower head mass. The effect of a low damping ratio is illustrated by the power spectrum of fore–aft tower bending moment shown in Figure 5.40, which has a very high peak at the tower natural frequency of 0.58 Hz, despite this frequency being somewhat removed from the blade passing frequency of 0.75 Hz. The damping ratio is calculated as 0.037, consisting of

0.035 due to aerodynamic damping (based on a tower head mass of 120 t) and 0.002 due to structural damping (for a welded steel tower).

In the example shown in Figure 5.40, the tower dynamic response increases the standard deviation of the tower base fore–aft bending moment by 9%. However, the effect of tower dynamic response results in a larger increase of 15% in the case of the two bladed machine featured in Figure 5.41, despite the reduction in tower natural frequency to maintain the same tower natural frequency to blade passing frequency ratio. The magnitude of the stochastic thrust loading at blade passing frequency in relation to the steady thrust is considered in Section 6.14.1.

It is important to note that the rotor provides negligible aerodynamic damping in the side-to-side direction, so that effectively the only damping present is the structural damping. This means that, even though the side-to-side loadings are small in relation to the fore–aft loads, the side-to-side tower moment suctuations can sometimes approach the fore–aft ones in magnitude.

# 5.12.6 Fatigue loads and stresses

The tower moments at height z are related to the hub-height loads as follows, omitting the tower inertial loads:

$$
M _ {Y} (z, t) = F _ {X} (H, t). (H - z) + M _ {Y} (H, t) \qquad M _ {X} (z, t) = - F _ {Y} (H, t). (H - z) + M _ {X} (H, t)
$$

$$
M _ {Z} (z, t) = M _ {Z} (H, t) \tag {5.136}
$$

For three bladed machines, the rve hub-height fatigue loads are almost entirely stochastic, because the deterministic load component is either constant (for a given mean wind speed) or negligible, and it is instructive to consider how they relate to one another. Recognising that the centre of any gust lying off the rotor centre will be located at a random azimuth, then it is clear that the rotor out-of-plane loads – that is, the moment about the horizontal axis, $M _ { Y } ( H , t )$ , the hub moment about the vertical axis, $M _ { Z } \left( H , t \right)$ , and the rotor thrust, $F _ { X } ( H , t )$ – will all be statistically independent of each other. The same will apply to the rotor in-plane loads – the rotor torque, $M _ { X } ( H , t )$ , and the sideways load, $F _ { Y } ( H , t )$ . However, as the out-of-plane and in-plane loads on a blade element are both assumed to be proportional to the local wind speed suctuation, $u ,$ it follows that the rotor torque suctuations will be in phase with the rotor thrust suctuations, and the rotor sideways load suctuations will be in phase with the suctuations of the hub moment about the horizontal axis, $M _ { Y } ( H , t )$ .

The preceding relationships have implications for the combination of fatigue loads. Clearly the power spectrum of the fore–aft tower moment at height z, $S _ { M \nu } ( z , n )$ , can be obtained by simply adding the power spectrum of the hub moment about the horizontal axis to $( H { - } z ) ^ { 2 }$ times the power spectrum of the rotor thrust. Similarly, the power spectrum of the side-to-side tower moment at height $z , S _ { M x } ( z , n )$ , can be obtained by adding the power spectrum of the rotor torque to $( H - z ) ^ { 2 }$ times the power spectrum of the rotor sideways load.

Having obtained power spectra for the $M _ { X } , M _ { Y }$ , and $M _ { Z }$ moments at height z, the corresponding fatigue load spectra can be derived with reasonable accuracy by means of the Dirlik method described in Section 5.9.3. As the tower stress ranges will be enhanced by tower resonance, the input power spectra should incorporate dynamic magnircation, as outlined in Section 5.12.5. Ragan and Manuel (2007) compared fatigue loads calculated in the frequency and time domains (see Section 5.9.3) and concluded that the Dirlik method performed very well in estimating tower fatigue bending moments for the case investigated.

Fatigue stress ranges due to bending about the two axes can easily be calculated separately from the $M _ { X } ( z )$ and $M _ { Y } ( z )$ fatigue spectra, but the stress ranges due to the two fatigue spectra combined cannot be calculated precisely because of lack of information about phase relationships. However, as noted above, the $M _ { X } ( H )$ component of the $M _ { X } ( z )$ （号 suctuations is in phase with the $F _ { X } ( H )$ component of the $M _ { Y } ( z )$ suctuations, and the $F _ { Y } ( H )$ component of the $M _ { X } ( z )$ suctuations is in phase with the $M _ { Y } ( H )$ component of the $M _ { Y } ( z )$ suctuations so the stress ranges due to the $M _ { X } ( z )$ and $M _ { Y } ( z )$ fatigue spectra combined can be conservatively calculated as if they were in phase too. Theoretically, this means pairing the largest $M _ { X } ( z )$ and $M _ { Y } ( z )$ loading cycles, the second largest, the third largest, and so on, right through the fatigue spectra, and calculating the stress range resulting from each pairing. In practice, of course, the $M _ { X } ( z )$ and $M _ { Y } ( z )$ load cycles are distributed between two sets of equal size ‘bins’, so they have to be reallocated to bins in a 2-D matrix of descending load ranges, as shown in the grossly simplired example given in Tables 5.8 and 5.9:

For a circular tower, the stress ranges would have to be computed at several points around the circumference to identify the location (with respect to the nacelle axis) where the fatigue damage was maximum.

A simpler but potentially cruder approach to the combination of the two fatigue spectra is to use the ‘damage equivalent load’ method. This involves the calculation of constant amplitude fatigue loadings, $M _ { X . D e l }$ and $M _ { Y . D e l } .$ , of, say $1 0 ^ { 7 }$ cycles each, that would, respectively, produce the same fatigue damages as the $M _ { X }$ and $M _ { Y }$ spectra, using the S-N curve appropriate to the fatigue detail under consideration. If the $M _ { \mathrm { X } }$ and $M _ { Y }$ suctuations are treated as being in-phase as before, the combined ‘damage equivalent load’ moment is $\sqrt { M _ { X . D e l } ^ { 2 } + M _ { Y . D e l } ^ { 2 } } .$ M2 l + M2Y .Del .

Table 5.8 Example $M _ { X }$ and $M _ { Y }$ fatigue spectra. 

<table><tr><td> $\Delta M_{Y}$  (KNm)</td><td>No. of  $\Delta M_{Y}$  cycles</td><td> $\Delta M_{X}$  (KNm)</td><td>No. of  $\Delta M_{X}$  cycles</td></tr><tr><td>200–300</td><td>5</td><td>100–150</td><td>10</td></tr><tr><td>100–200</td><td>15</td><td>50–100</td><td>40</td></tr><tr><td>0–100</td><td>80</td><td>0–50</td><td>50</td></tr></table>

Table 5.9 Joint $M _ { X }$ and $M _ { Y }$ cycle distribution. 

<table><tr><td></td><td colspan="4"> $\Delta M_{Y}$  (KNm)</td></tr><tr><td> $\Delta M_{X}$  (KNm)</td><td>200–300</td><td>100–200</td><td>0–100</td><td>Total no. of  $M_{X}$  cycles</td></tr><tr><td>100–150</td><td>5</td><td>5</td><td></td><td>10</td></tr><tr><td>50–100</td><td></td><td>10</td><td>30</td><td>40</td></tr><tr><td>0–50</td><td></td><td></td><td>50</td><td>50</td></tr><tr><td>Total no. of  $M_{Y}$  cycles</td><td>5</td><td>15</td><td>80</td><td></td></tr></table>

# 5.13 Wind turbine dynamic analysis codes

A large modern turbine is a complex structure. Relatively sophisticated methods are required to predict the detailed performance and loading of a wind turbine. These methods should take into account:

• The aerodynamics of the rotating blade, including induced sows (i.e. the modircation of the sow reld caused by the turbine itself), 3-D sow effects, and dynamic stall effects when appropriate.   
• Structural analysis of the blades, drive train, and tower, allowing their vibrational dynamics to be modelled.   
• Aeroelastic feedback, i.e. the modircation of the aerodynamic forces due to the vibrational velocities of the structure.   
• Dynamic response of subsystems such as the generator, yaw system, and blade pitch control system.   
• Control algorithms used during normal operation, start-up, and shut-down of the turbine.   
• Temporal and spatial variations of the wind reld impinging on the turbine, including the 3-D structure of the turbulence itself.

For offshore wind turbines, this should be extended to include:

• Hydrodynamic forces on the submerged structure.   
• Hydroelastic feedback, i.e. the modircation of the hydrodynamic forces due to the vibrational velocities of the structure.

Starting from a wind turbulence spectrum, it is possible to develop techniques in the frequency domain that account for many of these aspects, including rotational sampling of the turbulence by the blades, the response of the structure, and the control system. These techniques are set out in Sections 5.7.5, 5.8.6, 5.12.4, and elsewhere. However, although frequency-domain methods are elegant and computationally efrcient, they can only be applied to linear time-invariant systems and therefore cannot deal with some important aspects of wind turbine behaviour, such as

• Stall aerodynamics and hysteresis.   
• Non-linearities in sub-systems such as bearing friction and pitch rate limits.   
• Non-linear aspects of control algorithms.   
• Variable-speed operation.   
• Start-up and shut-down.

As a result, time-domain methods almost exclusively are now used for wind turbine design calculations. The ready availability of computing power means that the greater computational efrciency of frequency-domain methods is no longer such an important consideration.

A number of codes are available commercially for the calculation of wind turbine performance and loads using time-domain simulations. These simulations use numerical techniques to integrate the equations of motion over time, by subdividing the time into short timesteps as described in Section 5.8.5. In this way, all the non-linearities and non-stationary aspects of the system, such as those listed above, can be dealt with to any desired level of accuracy. A useful early comparative survey of such codes was given by Molenaar and Dijkstra (1999).

As explained in Section 5.8.5, there are a number of different algorithms or solvers for integrating the equations of motion. Some use a rxed timestep h (which has to be short enough to account for all modal frequencies that are considered important), while others use a variable timestep that is continually adjusted during the simulation, keeping it as long as possible to maximise simulation speed while still keeping all the integrated states within a certain error tolerance.

The use of variable timestep methods also allows accurate modelling of discontinuities, because close to a discontinuity the timestep can be adjusted to rnd the exact moment when the characteristics of the system change. Discontinuities can occur for many reasons: for example, stick-slip friction (of pitch and yaw bearings, shaft brake, slipping clutch, etc.), grid loss, faults, controller or safety system actions, etc. Note that the equations of motion and structural resonant frequencies change at the moment when a friction element like a brake changes from slipping to sticking.

On the other hand, these codes can provide a valuable way to test turbine controllers, linking the real controller to the simulation model, which acts as a ‘virtual turbine’, and in this case a rxed timestep may be more appropriate, to allow regular communication with the controller running in real time and to ensure that the calculations for each timestep are completed within that real-time interval. Necessarily this may mean a loss of accuracy in predicting the effect of higher frequency modes and discontinuities. As an example, the Bladed code mentioned below normally uses a variable timestep but also provides a rxed step option for real-time applications such as controller testing.

Two principal approaches to the modelling of structural dynamics are embodied in time-domain simulation packages. Some use a full rnite element representation of the structure, which is broken down into small elements. The equations of motion are solved for each element, with boundary conditions matched at the interfaces between elements. An example of such a code is Adams-WT (Hansen, 1998), which consists of a general purpose rnite element code (Adams) interfaced to an aerodynamic module.

The other main approach is the modal analysis method as described in Section 5.8.1, in which simple rnite element methods are used to predict just the rrst few modes of vibration of the main components, such as the rotor blades and the tower. These are typically modelled as beam elements, but it is important to include geometric stiffening effects so that, for example, the centrifugal stiffening of the blades is taken into account, i.e. the increase in apparent stiffness with rotational speed due to the effect of centrifugal force on the element mass. Additional degrees of freedom are added as required, for example, for the drive train rotation and torsion, pitch and yaw motion, etc. The equations of motion are then derived for the entire coupled system. Traditionally this can be done by constructing the Lagrangian for the system including all degrees of freedom. With full rotation of the yaw bearing on top of a sexible tower, and then full rotation of the rotor (also sexible) about the shaft axis, the coordinate transformations involved mean that the equations rapidly become very large, usually requiring some form of symbolic processing to derive them in an automated way. More recently, methods based on the approach of multi-body dynamics (see, for example, Shabana 1998) have been used. This provides a generalised way to link together the separate equations of motion of each rigid or sexible component by means of derned linking elements, including rigid links, revolute hinges, sliding joints, etc. This is a very powerful technique that is readily extended to structures of arbitrary complexity. Using a technique originally proposed by Craig and Bampton (1968), the mode shapes of each modal component can be derned in a way that is independent of any other component to which it is attached.

One example of a widely used commercial code based on the component mode approach is Bladed (DNVGL 2020) developed by Garrad Hassan. Originally built using a Lagrangian approach, this code has recently been converted to use a multi-body approach. Beam-element models for the blades and tower are combined with elements representing other components of the transmission system, the yaw and pitch actuators, etc. The control system, which has a major insuence on the performance as well as the loads, can be modelled in full detail. The code can also model the electrical generator and power converter, allowing detailed calculations of turbine response to network faults, generator short-circuit faults, etc. in a fully integrated way. Interfaces are provided to link in more detailed models of subcomponents, such as gearboxes. For most calculations this level of detail is not required, but where certain load cases are critical for the particular component, it may be useful to be able to run a more detailed model.

By using a limited number of modes, the modal approach results in rapid calculations, so that a complete set of design or certircation load cases, typically amounting to several hundred load cases each consisting of a 10 minute simulation, can be run in a few hours on a standard desktop computer. A small number of modes is generally adequate for predicting the loads: the higher frequency modes generally have little effect. However, to model the desections accurately it would be necessary to model more modes, because the modelled desection is a linear combination of the mode shapes used, and a small number of mode shapes may not be sufrcient to model the actual desected shape. Rather than using more modes, the static improvement technique can be used (Barltrop and Adams 1991): effectively the calculated loading is used as if it were a static load, and it is combined with the stiffness matrix to recalculate the desections.

The modal approach generally assumes that all desections of the sexible bodies remain small. More complex non-linear beam-element models are being developed to help increase accuracy in case of larger defections, such as may be found with very sexible blades. Alternatively, the non-linearity can be captured by modelling the blade as a number of shorter linear beam elements joined end to end.

For the aerodynamics, all of these codes generally use BEM theory as described in Chapter 3, as this is currently the only way to achieve rapid enough simulations for the standard sets of calculations that are normally needed. More advanced aerodynamic methods such as vortex wake and panel methods are starting to be used to examine specirc cases where BEM is not sufrciently accurate. This might include highly yawed sow, tip vanes, ducted rotors, or the need to understand the aerodynamic interaction between the blades and the nacelle, for instance. Ultimately, computational suid dynamics (CFD) methods based on direct solution of the Navier–Stokes equations could be used, and some general commercial CFD codes are now available, but these methods are still far too slow and cumbersome to be useful except perhaps to examine very special cases in detail.

![](images/a1df066a74f63a820cab5ae8d5c1a9b490d588d12c52d543a781e28fa9d170e3.jpg)

<details>
<summary>line</summary>

| Rotor azimuth angle (degrees) | Out-of-plane (kNm) | In-plane (kNm) |
| ----------------------------- | ------------------ | -------------- |
| 0                             | 165                | 35             |
| 60                            | 160                | 70             |
| 120                           | 150                | 60             |
| 180                           | 125                | 30             |
| 240                           | 150                | -15            |
| 300                           | 165                | -5             |
| 360                           | 165                | 35             |
</details>

Figure 5.42 Blade root bending moment in steady wind.

It is important to be able to simulate 3-D turbulent wind relds because the dynamic wind speed variations across the rotor are of major importance in determining the loads. The Veers method (Veers 1988) as described in Section 5.7.6 is a convenient way to do this: a random number sequence is rltered using a representation of the spectrum and spatial coherence of the turbulence to generate a 3-D wind reld that is consistent with the chosen spectral model. This method is used by the codes mentioned above. Bladed also incorporates a different technique due to Mann (1998), which generates a turbulence reld by means of a 3-D inverse FFT of the 3-D wavenumber spectrum (see Chapter 2). For offshore turbines, Bladed uses a related method to generate stochastic wave time histories impacting on the submerged part of the structure, in addition to the loading from water currents. As with aerodynamics, hydrodynamic forces opposing the vibrational velocities of structural members provide some damping. When the turbine is running, rotor aerodynamic damping dominates over the hydrodynamic damping for reducing fore-aft vibrations, but hydrodynamic damping can help in other situations, including when jacket brace members are excited by a harmonic of rotor rotational frequency.

Jamieson et al. (2000) have demonstrated that if wind and wave loading are treated in isolation from each other, an overconservative design is likely to result.

The use of sophisticated calculation methods such as those described above are now mandatory for the certircation of wind turbines, particularly at the larger sizes. A few illustrative examples of results obtained with Bladed are described below.

Figure 5.42 shows a Bladed simulation of the in- and out-of-plane bending moments at the root of one of the blades, during operation in steady, sheared wind. The in-plane moment is almost a sinusoidal function of azimuth, being dominated by the gravity loading due to the self-weight of the blade that, relative to the blade, changes direction once per revolution. The mean is offset from zero because of the mean positive aerodynamic torque developed by the blade. There is a slight distortion of the sinusoid, partly because of the variation of aerodynamic torque due to wind shear and the effect of tower shadow, and partly because of the effect of structural vibrations.

![](images/756cecad1b4eb8a977f3a46adf3a5865bcd71476943163250787bb60d8db436a.jpg)

<details>
<summary>line</summary>

| Time (s) | In-plane (kNm) | Out-of-plane (kNm) |
| -------- | -------------- | ------------------ |
| 0        | ~0             | ~200               |
| 10       | ~-50           | ~250               |
| 20       | ~-50           | ~200               |
| 30       | ~-50           | ~250               |
| 40       | ~-50           | ~100               |
| 50       | ~-50           | ~250               |
| 60       | ~-50           | ~200               |
| 70       | ~-50           | ~250               |
| 80       | ~-50           | ~150               |
| 90       | ~-50           | ~200               |
| 100      | ~-50           | ~150               |
| 110      | ~-50           | ~250               |
| 120      | ~-50           | ~150               |
</details>

Figure 5.43 Blade root bending moment in turbulent wind for a rxed rotational-speed machine.

The out-of-plane moment is always positive, the mean value being dominated by the aerodynamic thrust on the blade. There is a systematic variation with azimuth resulting from the wind shear, giving a lower load at $1 8 0 ^ { \circ }$ azimuth (bottom dead centre) than at 0∘. A sharp dip at $1 8 0 ^ { \circ }$ is also visible, and this is the effect of the tower shadow (the reduction in wind speed in the vicinity of the tower). The blade out-of-plane vibrational dynamics contribute a signircant higher frequency variation.

In turbulent wind, the loads take on a much more random appearance, as shown in Figure 5.43. The out-of-plane load in particular is varying with wind speed and, as this is a pitch-controlled machine, with pitch angle. The in-plane load is more regular, because it is always dominated by the reversing gravity load.

Spectral analysis provides a useful means of understanding these variations. Figure 5.44 shows auto-spectra of the blade root out-of-plane bending moment and the hub thrust force. The out-of-plane bending moment is dominated by peaks at all multiples of the rotational frequency of 0.8 Hz. These are caused mainly by the rotational sampling of turbulence by the blade as it sweeps around, repeatedly passing through turbulent eddies. Wind shear and tower shadow also contribute to these peaks. A small peak due to the rrst out-of-plane mode of vibration at about 3.7 Hz is just visible. There is also a signircant effect of the rrst tower fore–aft mode of vibration at about 0.4 Hz.

This tower effect is also visible in the spectrum of the hub thrust force. However, this force is the sum of the shear forces at the roots of the three blades. These forces are 120∘ out of phase with each other, with the result that the peak at the rotational frequency (1P) is eliminated, as are the peaks at multiples of this frequency such as 2P, 4P, etc. Only the peaks at multiples of 3P remain, because the loads on the three blades all have the same phase with respect to the 3P cycles.

This effect is even more signircant in the in-plane load spectra (Figure 5.45). Of the blade load peaks at multiples of 1P, only the relatively small peaks at 3P and 6P come

![](images/621111ef76da080ec12e5cc247e65fe70d30e59a0837a5882b448a09cec33e2d.jpg)

<details>
<summary>line</summary>

| Frequency (Hz) | Blade root moment | Hub thrust force |
| -------------- | ----------------- | ---------------- |
| 0.0            | ~1.0e+10          | ~1.0e+09         |
| 0.5            | ~1.0e+08          | ~1.0e+06         |
| 1.0            | ~1.0e+09          | ~1.0e+05         |
| 1.5            | ~1.0e+08          | ~1.0e+05         |
| 2.0            | ~1.0e+07          | ~1.0e+05         |
| 2.5            | ~1.0e+08          | ~1.0e+06         |
| 3.0            | ~1.0e+07          | ~1.0e+05         |
| 3.5            | ~1.0e+08          | ~1.0e+05         |
| 4.0            | ~1.0e+07          | ~1.0e+05         |
| 4.5            | ~1.0e+06          | ~1.0e+05         |
| 5.0            | ~1.0e+07          | ~1.0e+05         |
</details>

Figure 5.44 Spectra of out-of-plane loads in turbulent wind.

![](images/26e6eef7b8d0d28ae3fefd4d73ded4563d8aaff4a63afef35acd6f0c36707dc9.jpg)

<details>
<summary>line</summary>

| Frequency (Hz) | Auto spectral density (N²/Hz) |
| -------------- | ----------------------------- |
| 0.0            | ~1e+09                        |
| 0.5            | ~1e+07                        |
| 1.0            | ~1e+06                        |
| 1.5            | ~1e+07                        |
| 2.0            | ~1e+06                        |
| 2.5            | ~1e+07                        |
| 3.0            | ~1e+06                        |
| 3.5            | ~1e+05                        |
| 4.0            | ~1e+07                        |
| 4.5            | ~1e+09                        |
| 5.0            | ~1e+06                        |
</details>

Figure 5.45 Spectra of in-plane loads in turbulent wind.

through to the hub torque. The 1P peak in the blade load, which is dominated by gravity, is particularly large, but it is completely eliminated from the hub torque. The tower peak at 0.4 Hz is visible in both loads. A large blade load peak at the rrst in-plane blade vibrational mode at 4.4 Hz is also seen, but this is a mode that does not include any rotation at the hub and consequently is not seen in the hub torque. Some higher frequency blade modes (not shown) will be coupled with hub rotation.

# 5.14 Extrapolation of extreme loads from simulations

In the case of load case 1.1 (normal operation in a turbulent wind), IEC 61400-1 edition 4 requires the characteristic blade root out-of-plane and in-plane bending moments and the characteristic tip desection to be determined by statistical extrapolation of the extreme values of the load time series output from the simulations. For simulations of 10 minutes’ duration, the characteristic value is derned as that with a $3 . 8 \times 1 0 ^ { - 7 }$ probability of exceedance – i.e. the load with a return period of 50 years. This section considers ways in which the load exceedance probability distribution can be derived from the simulations and extrapolated to the $3 . { \overset { - } { 8 } } \times 1 0 ^ { - 7 }$ value. As it is more convenient to work with load non-exceedance probability distributions – otherwise known as cumulative distribution functions – the following discussion is in these terms, using the notation $P ( X \leq x ) = F ( x )$ .

There are two sequences that can be followed to assemble a single load probability distribution from simulation data from different wind speed bins:

• Derivation of load non-exceedance probability distributions for each wind speed bin followed by combination of these distributions in proportion to the operating time in each bin (‘rtting before aggregation’).   
• Aggregation of results from all wind speed bins, with the number of simulations per bin proportional to the hours of operation in each bin, followed by the derivation of a single load non-exceedance probability distribution (‘aggregation before rtting’).

It is also necessary to decide how many extreme values from each simulation are to be utilised. In the ‘global extremes’ method, only the largest extreme value in each 10 minute simulation – i.e. the global extreme – is used in the construction of the load non-exceedance probability distribution, but in the ‘local extremes’ method, all extreme values that can be considered independent are utilised. The local extremes method would appear to be more attractive, because it uses much more of the available data, but it throws up the problem of establishing a criterion for independence.

The various stages of the ‘rtting before aggregation’ sequence using the global extremes method are considered rrst.

# 5.14.1 Derivation of empirical cumulative distribution function of global extremes

Each 10 minute time series will yield a maximum value of the load under investigation, and, for n 10 minute simulations at a particular wind speed, there will be n such global extremes, which can be ranked $I , 2 , \ldots i , \ldots n _ { k }$ from smallest to largest. An empirical non-exceedance probability distribution for the 10 minute extreme load, $x _ { k }$ , at wind

speed $U _ { k }$ can then be constructed as

$$
F (x _ {k i} | U _ {k}) = \frac {i}{n _ {k} + 1}, i = 1, 2, \dots n _ {k} \tag {5.137}
$$

Harris (1996) has shown that, if $F ( x )$ is a known function of $x ,$ the mean of the L non-exceedance probabilities $F ( x _ { i } )$ for the ith extremes from L sets of n 10 minute simulations, derived from the $x _ { i }$ simulation results, tends to the value $\frac { i } { n + 1 }$ for L large.

# 5.14.2 Fitting an extreme value distribution to the empirical distribution

There are several extreme value distributions that can be rtted to the empirical probability distributions obtained from the simulations. These include the Gumbel distribution (also known as the Fisher–Tippett I distribution), which was introduced in the context of extreme wind speeds in Section 2.8, the log-normal distribution, the three parameter Weibull distribution, and the generalised extreme value (GEV) distribution, which are described in turn below.

# a) Gumbel distribution:

The probability that the variable X will not exceed the value x is given by

$$
P (X \leq x) = F (x) = \exp \left[ - \exp \left(- \frac {x - x _ {o}}{c}\right) \right] \tag {5.138}
$$

where $x _ { o }$ is the most likely extreme value or the mode of distribution, c is the dispersion, and $y = ( x - x _ { o } ) / c$ is termed the reduced variate.

This relationship is a straight line if $y = - \mathrm { l n } [ - \mathrm { l n } ( F ( x ) ) ]$ is plotted against x, so a Gumbel distribution can be rtted to the empirical distribution by the method of least squares and the parameters $x _ { o }$ and c thereby determined. However, Harris (1996) has pointed out two defects of the classical least squares method.

First of all, the mean of the function that is plotted, $- \mathrm { l n } [ - \mathrm { l n } ( F ( x _ { i } ) ) ]$ , is not the same as the double natural logarithm of the mean of $F ( x _ { i } ) )$ itself, given by Eq. (5.137). Harris provides a formula by which the mean of – $\ln [ - \ln ( F ( x _ { i } ) ) ] , 1 . { \mathsf e } . \overline { { y } } _ { i } ,$ , may be evaluated when the data should conform to a Gumbel distribution – as follows:

$$
\overline {{y}} _ {\nu} = \frac {N !}{(\nu - 1) ! (N - \nu) !} \int_ {0} ^ {1} - \ln [ - \ln (z) ] z ^ {N - \nu} (1 - z) ^ {\nu - 1} d z \tag {5.139}
$$

In this formula, N is the number of data points $( = n _ { k } )$ , and 휈 is the rank of data points with the largest rrst, so that $\nu = ( N + 1 ) - i$ and $z = F ( x _ { \nu } )$ .

Secondly, the classical least squares method assumes that the variability of each plotted ordinate is of similar magnitude, whereas, for extreme value data, the variability of the reduced variate, y, is much greater for the largest values than for the others. Accordingly, Harris proposes weighting the data points in inverse proportion to the variance of the y values, before the least squares rtting is carried out.

Values of $\overline { { y } } _ { \nu }$ and its standard deviation are given in Table 5.10 for the case of $N = 1 5 .$ , consistent with the IEC 61400-1 edition 3 requirement for at least 15 10 minute simulations for wind speeds above rated. Values of y calculated by the standard Gumbel method are also included for comparison, and it is seen that the differences are signircant for the largest of the extremes. The Harris weighting factor is included in Table 5.10 in the last column. It is seen that, in general, the Harris method will result in a steeper straight line that is less insuenced by the largest extremes.

An alternative method of rtting a straight line to the $- \mathrm { l n } [ - \mathrm { l n } ( F ( x ) ) ]$ plot is the method of statistical moments (Moriaty et al. 2004), in which the rrst two statistical moments of the data – derned as the mean and the variance, respectively – are equated to analytical expressions for these moments. Thus, for the standard Gumbel distribution, $F ( y ) = \exp [ - \exp ( - y ) ]$ , the PDF is $f ( y ) = \frac { d F ( y ) } { d y } = \exp [ - y - \exp ( - y ) ]$ dF(y) and the mean is

$$
\mu_ {y} = \int_ {- \infty} ^ {\infty} y. f (y) d y = \int_ {- \infty} ^ {\infty} y. \exp [ - y - \exp (- y) ] d y = \gamma = 0. 5 7 7 2 \tag {5.140}
$$

Similarly, the variance is

$$
\sigma_ {y} ^ {2} = \int_ {- \infty} ^ {\infty} (y - \mu_ {y}) ^ {2}. f (y) d y = \int_ {- \infty} ^ {\infty} (y - \mu_ {y}) ^ {2}. \exp [ - y - \exp (- y) ] d y = \frac {\pi^ {2}}{6} \tag {5.141}
$$

Denoting the mean and the standard deviation of the dataset of extreme values as $\mu _ { x }$ and $\sigma _ { x }$ , respectively, and noting that $y = ( x - x _ { o } ) / c$ , we obtain $\mu _ { \nu } = ( \mu _ { x } - x _ { o } ) / c = 0 . 5 7 7 2$ and $\sigma _ { \nu } = \sigma _ { x } / c = 1 . 2 8 2 5$ .

Hence $c = \sigma _ { x } / 1 . 2 8 2 5$ and $x _ { o } = \mu _ { x } - c \mu _ { y } = \mu _ { x } - 0 . 5 7 7 2 \frac { \sigma _ { x } } { 1 . 2 8 2 5 } = \mu _ { x } - 0 . 4 5 0 \sigma _ { x } .$ .

Figure 5.46 compares the three methods described above for rtting a straight line to empirical data on a Gumbel plot, for a dataset consisting of 15 global extremes of out-of-plane blade root bending moment, taken from 15 10 minute simulations of operation in a 12 m/s wind speed. Note that the straight lines derived using the Harris method and the method of moments appear less insuenced by the largest values than those based on the least squares method.

# b) Log-normal distribution:

In the log-normal distribution, the logarithm of the variable is normally distributed, so the probability distribution function of the variable x is

$$
f (x) = \frac {1}{\sqrt {2 \pi} \sigma_ {z} x} \exp \left[ - \frac {1}{2} \left(\frac {\ln (x) - \mu_ {z}}{\sigma_ {z}}\right) ^ {2} \right] \tag {5.142}
$$

where $\mu _ { z }$ and $\sigma _ { z }$ are the mean and standard deviation, respectively, of $z = \ln ( x )$ . The mean and standard deviation of the variable x itself, $\mu _ { x }$ and $\sigma _ { x } .$ , are given in terms of $\mu _ { z }$ and $\sigma _ { z }$ as follows:

$$
\mu_ {x} = \exp [ \mu_ {z} + \sigma_ {z} ^ {2} / 2 ] \quad \sigma_ {x} = \exp [ \mu_ {z} + \sigma_ {z} ^ {2} / 2 ] \sqrt {\exp (\sigma_ {z} ^ {2}) - 1} = \mu_ {x} \sqrt {\exp (\sigma_ {z} ^ {2}) - 1} \tag {5.143}
$$

The log-normal distribution parameters, $\mu _ { z }$ and $\sigma _ { z } ,$ , can again be rtted to the extreme value data by the method of statistical moments, using

$$
\sigma_ {z} = \sqrt {\ln (1 + (\sigma_ {x} / \mu_ {x}) ^ {2})} \text {   and   } \mu_ {z} = \ln (\mu_ {x}) - \sigma_ {z} ^ {2} / 2 \tag {5.144}
$$

derived from (5.143).

Table 5.10 Table of mean values of the reduced variate, $\mathrm { y } _ { \nu } = - \mathrm { l n } [ - \mathrm { l n } ( \mathrm { F } ( \mathrm { x } _ { \nu } ) ]$ , its standard deviation, and the Harris weighting factor, $w _ { \nu }$ . 

<table><tr><td>Rank,  $\nu$ (largest first)</td><td>Rank, i(smallest first)</td><td> $y_{\nu} = -\ln[-\ln((N+1\_ \nu)/(N+1))] = -\ln[-\ln(i/(N+1))]$ (Gumbel method)</td><td> $\overline{y}_{\nu}$ _Eq. (5.139)(Harris method)</td><td> $\sigma_{y}$ -standard deviation of  $\overline{y}_{\nu}$ </td><td>Harris weighting factor,  $w_{\nu}$ </td></tr><tr><td>1</td><td>15</td><td>2.7405</td><td>3.2853</td><td>1.2825</td><td>0.0064</td></tr><tr><td>2</td><td>14</td><td>2.0134</td><td>2.2504</td><td>0.8031</td><td>0.0164</td></tr><tr><td>3</td><td>13</td><td>1.572</td><td>1.7133</td><td>0.6291</td><td>0.0266</td></tr><tr><td>4</td><td>12</td><td>1.2459</td><td>1.3404</td><td>0.5341</td><td>0.037</td></tr><tr><td>5</td><td>11</td><td>0.9816</td><td>1.0478</td><td>0.4726</td><td>0.0472</td></tr><tr><td>6</td><td>10</td><td>0.755</td><td>0.8019</td><td>0.4291</td><td>0.0573</td></tr><tr><td>7</td><td>9</td><td>0.5528</td><td>0.5852</td><td>0.3965</td><td>0.0671</td></tr><tr><td>8</td><td>8</td><td>0.3665</td><td>0.3873</td><td>0.3714</td><td>0.0765</td></tr><tr><td>9</td><td>7</td><td>0.1903</td><td>0.201</td><td>0.3518</td><td>0.0852</td></tr><tr><td>10</td><td>6</td><td>0.0194</td><td>0.0206</td><td>0.3366</td><td>0.0931</td></tr><tr><td>11</td><td>5</td><td>-0.1511</td><td>-0.1595</td><td>0.3254</td><td>0.0996</td></tr><tr><td>12</td><td>4</td><td>-0.3266</td><td>-0.3458</td><td>0.3184</td><td>0.104</td></tr><tr><td>13</td><td>3</td><td>-0.5152</td><td>-0.5485</td><td>0.317</td><td>0.1049</td></tr><tr><td>14</td><td>2</td><td>-0.7321</td><td>-0.7884</td><td>0.3257</td><td>0.0994</td></tr><tr><td>15</td><td>1</td><td>-1.0198</td><td>-1.1326</td><td>0.3648</td><td>0.0793</td></tr></table>

![](images/efcfe1a5f8177636322749fc28db5842f00bd7d6f99f517b8a12921c64ea5278.jpg)

<details>
<summary>scatter</summary>

| x    | y      |
| ---- | ------ |
| 2.5  | -1.0   |
| 2.7  | -0.5   |
| 2.9  | 0.0    |
| 3.1  | 0.5    |
| 3.3  | 1.0    |
| 3.5  | 1.5    |
| 3.7  | 2.0    |
| 3.9  | 2.5    |
| 4.1  | 3.0    |
| 4.3  | 3.5    |
| 4.5  | 4.0    |
| 4.7  | 4.5    |
| 4.9  | 5.0    |
</details>

Figure 5.46 Comparison of techniques for rtting a straight line to empirical data on a Gumbel plot.

# c) Three parameter Weibull distribution:

The three parameter Weibull distribution is derned as $P ( Y \leq y ) = F ( y ) = 1 - \exp [ - y ^ { \alpha } ]$ , where $y = ( x - x _ { o } ) / c$ as before, and $F ( y )$ only applies to positive values of y. Hence the PDF, $f ( y )$ , is given by $\alpha y ^ { \alpha - 1 }$ exp[−y훼 ]. The three parameters, $x _ { o } , c ,$ and $\alpha ,$ can be rtted to the data by the method of statistical moments described above, but in this case using the rrst three moments instead of the rrst two.

Using the shorthand Gm(훼) = mΓ  $G _ { m } ( \alpha ) = \frac { m } { \alpha } \Gamma \left( \frac { m } { \alpha } \right)$ where Γ is the gamma function, the rrst 훼 훼three statistical moments are as follows:

$$
\mu_ {y} = G _ {1} (\alpha)
$$

$$
\sigma_ {y} ^ {2} = G _ {2} (\alpha) - G _ {1} ^ {2} (\alpha)
$$

$$
\eta_ {y} \sigma_ {y} ^ {3} = \int_ {- \infty} ^ {\infty} (y - \mu_ {y}) ^ {3} f (y) d y = G _ {3} (\alpha) - 3 G _ {2} (\alpha) G _ {1} (\alpha) + 2 G _ {1} ^ {3} (\alpha) \tag {5.145}
$$

Note that $\eta _ { \nu }$ , the skewness parameter, is the third statistical moment normalised by the cube of the standard deviation.

# d) Generalised extreme value (GEV) distribution:

The GEV distribution was introduced by Jenkinson in 1955 and is more versatile than the Gumbel distribution, because it allows the skewness of extreme value distributions to be modelled as well as their spread. It is derned as $P ( Y \leq y ) = F ( y ) = \exp [ - \{ 1 - k y \} ^ { 1 / k } ]$ , where $y ~ = ~ ( x - x _ { o } ) / c$ as before, and k is the shape parameter, which determines the curvature of the distribution when it is plotted as $- \mathrm { l n } [ - \mathrm { l n } ( F ( x ) ) ]$ against x. If k is positive, the curve is concave upwards and has an upper bound of $x _ { o } + c / k$ , whereas if k is negative, the curve is concave downwards and has a lower bound of $x _ { o } + c / k$ .

Hosking, Wallis, and Wood (1985) advocate the use of the method of probability weighted moments (PWMs) for rtting a GEV distribution to empirical data. For a probability distribution $F { = } F ( x )$ , with an inverse distribution function $x ( F )$ , PWMs $\beta _ { 0 } , \beta _ { 1 }$ , and $\beta _ { 2 }$ are derned by $\begin{array} { r } { \beta _ { r } = \int _ { 0 } ^ { 1 } x ( F ) F ^ { r } d F } \end{array}$ , and the parameters $x _ { o } , c ,$ , and k of the GEV are determined by equating the PWMs of the empirical data to the PWMs of the GEV. of

The PWMs of the GEV are given by the formula $\beta _ { r } = { \frac { 1 } { r + 1 } } \left[ x _ { 0 } + { \frac { c } { k } } \left\{ 1 - { \frac { \Gamma ( 1 + k ) } { ( r + 1 ) ^ { k } } } \right\} \right]$ for $\mathrm { k } > - 1$ , where Γ is the gamma function. This gives

$$
\beta_ {0} = x _ {0} + \frac {c}{k} \{1 - \Gamma (1 + k) \}, \quad 2 \beta_ {0} - \beta_ {1} = \frac {c}{k} \Gamma (1 + k) \left(1 - 2 ^ {- k}\right) \text { and } \frac {3 \beta_ {2} - \beta_ {0}}{2 \beta_ {1} - \beta_ {0}} = \frac {1 - 3 ^ {- k}}{1 - 2 ^ {- k}} \tag {5.146}
$$

Solution of the last equation requires iterative methods, but Hosking et al. (1985) have shown that a good approximation for k is $7 . 8 5 9 0 C + 2 . 9 5 5 4 C ^ { 2 }$ , where $C = \frac { 2 \beta _ { 1 } - \beta _ { 0 } } { 3 \beta _ { 2 } - \beta _ { 0 } } - \frac { \log 2 } { \log 3 }$ 1 This value of k can then be substituted in the rrst two . Eqs. (5.146) to obtain $x _ { 0 }$ and c.

The PWMs of the empirical data can be estimated from the formula

$$
\beta_ {r} [ p _ {i, n} ] = \frac {1}{n} \sum_ {i = 1} ^ {n} p _ {i, n} ^ {r} x _ {i} \tag {5.147}
$$

where $p _ { i , n }$ is the probability assigned to the ith global extreme, with ranking from smallest to largest. Hosking et al. propose two alternative expressions for use in estimating $p _ { i , n }$ as follows:

$$
p _ {i, n} = (i - a) / n, \quad 0 <   a <   0. 5
$$

$$
p _ {i, n} = (i - a) / (n + 1 - 2 a), \quad - 0. 5 <   a <   0. 5
$$

Another approach is to estimate the PWMs directly from the unbiased estimators $b _ { r }$ given by

$$
b _ {r} = \frac {1}{n} \sum_ {i = 1} ^ {n} \frac {(i - 1) (i - 2) \dots (i - r)}{(n - 1) (n - 2) \dots (n - r)} x _ {i} \tag {5.148}
$$

Figure 5.47 compares two GEV distributions rtted to the dataset of 15 global extremes described above and extrapolated to a 50 year return period. In one case unbiased estimators of the PWMs are used for the rtting, and, in the other, the formula $p _ { i , n } = ( i - a ) / n$ with $\mathrm { a } = 0 . 3 5$ was employed for the probabilities, as this was found to give the best overall results in a computer simulation by Hosking et al. Also shown for comparison is the Gumbel distribution rtted to the dataset using the method of statistical moments.

It is seen that there is poor agreement between the two GEV distributions. This is likely to be due – at least in part – to the small size of the dataset, which results in coarse estimates of the PWMs. It should also be noted that the use of different datasets for the same load case results in considerable variation in the shape parameter, suggesting that a dataset of 15 extreme values is not large enough to yield a meaningful result.

# 5.14.3 Comparison of extreme value distributions

Gumbel, three parameter Weibull, and log-normal distributions have been rtted to the dataset of 15 global extremes of out-of-plane blade root bending moment introduced above, using the method of statistical moments in each case, and compared on a Gumbel plot of –ln[−ln(F(x))] against the normalised bending moment excursion, x, in Figure 5.48.

Figure 5.48 shows the three extreme value distribution extrapolated to the 50 year return period exceedance probability of $3 . 8 \times 1 0 ^ { - 7 }$ (for which –ln[−ln(F(x))] is 14.78) to illustrate their behaviour. It is seen that there is a wide variation in the predicted value of the 50 year return load.

Although the loadings on wind turbine components are generally not narrow banded, it is instructive to investigate how well the above three extreme value distributions and the GEV distribution can be rtted to the distribution of global extremes arising from a narrow banded process. Consider a blade rotating at 15 rpm, which experiences 150 loading cycles in 10 minutes. Assuming that the extreme loads in adjacent three cycle blocks are independent of one another, there are 50 independent maxima in the 10 minute time interval, and the cumulative probability distribution of the global maximum is

$$
F (x) = \left\{1 - \exp \left[ - \frac {x ^ {2}}{2} \right] \right\} ^ {5 0} \tag {5.149}
$$

![](images/92c152326163eed11dbb3b2a1f7a71a9a719214218bda2a71b36a5d887d5c038.jpg)

<details>
<summary>line</summary>

| x | Non-exceedance probability associated with 50 year return period | Gumbel distribution - fitted by method of statistical moments (continuous line) | GEV distribution fitted using (j=0.35) upon n as probability measure: k = -0.067 (dotted line) | GEV distribution fitted using unbiased estimator: k = -0.17(dashed line) |
|---|---|---|---|---|
| 2 | 15 | -1.5 | -1.5 | -1.5 |
| 3 | 15 | 0.5 | 0.5 | 0.5 |
| 4 | 15 | 2.5 | 2.5 | 2.5 |
| 5 | 15 | 5.0 | 5.0 | 5.0 |
| 6 | 15 | 7.5 | 7.5 | 7.5 |
| 7 | 15 | 10.0 | 10.0 | 10.0 |
| 8 | 15 | 12.5 | 12.5 | 12.5 |
| 9 | 15 | 15.0 | 15.0 | 15.0 |
| 10 | 15 | 17.5 | 17.5 | 17.5 |
| 11 | 15 | 20.0 | 20.0 | 20.0 |
| 12 | 15 | 22.5 | 22.5 | 22.5 |
</details>

Figure 5.47 Comparison of GEV distributions rtted to empirical data on a Gumbel plot.

Gumbel, three parameter Weibull, log-normal, and GEV distributions have been rtted to this distribution using the method of statistical moments, and Gumbel plots of the rtted distributions are presented in Figure 5.49, together with their derning parameters.

It is seen that the log-normal and the three parameter Weibull distributions rt the distribution of global maxima of a narrow banded process better than the other two.

Freudenreich and Argyriadis (2008) compared extrapolations made using the above four extreme value distributions by reference to rve 1 year simulations for a 5 MW pitch-regulated turbine. Using the extreme values from 30 10 minute time histories per wind speed bin as input, they concluded that the extrapolations of blade sapwise root bending moment made with the three parameter Weibull and log-normal distributions were the most accurate, whereas the Gumbel extrapolation was signircantly conservative.

# 5.14.4 Combination of probability distributions

The procedure outlined above yields a family of load non-exceedance probability distributions conditional upon wind speed for the extreme load in the simulation period, $F ( x | U _ { k } )$ – one for each wind speed bin. These are combined to yield a single distribution for all operating wind speeds by weighting each one according to the number of hours of operation applicable to the wind speed bin and summing the results. Mathematically, the summation is expressed as follows:

$$
F _ {\text { Long - term }} (x) \approx \sum_ {k = 1} ^ {M} F (x \mid U _ {k}) p _ {k} \tag {5.150}
$$

![](images/9788a0084ddfba48e9a62da85470a9a494210f0af4a6de1c6f9f8234832a675a.jpg)

<details>
<summary>line</summary>

| x    | -LN(-LN(F(x))) |
| ---- | --------------- |
| 0    | 02.5            |
| 1    | 0.0             |
| 2    | 0.0             |
| 3    | 1.0             |
| 4    | 5.0             |
| 5    | 10.0            |
| 6    | 15.0            |
| 7    | 15.0            |
</details>

Figure 5.48 Gumbel plot comparison of three extreme value distributions rtted to empirical data.

![](images/377e3cf9d9798cf4da386150f6fd042a6eea8e46881f0448525cb54ab95e070c.jpg)

<details>
<summary>line</summary>

| Distribution Type | Slope (x) | Std Dev (y) |
| ----------------- | --------- | ----------- |
| Fitted GEV distribution (chain dotted line) | (x - 2.799)/0.355; k = 0.10 | |
| Fitted three parameter Weibull distribution (dotted line) | (x - 2.345)/0.697; Alpha = 1.553 | |
| Fitted Gumbel distribution (plain line) | (x - 2.786)/0.3213 | |
| CDF of largest of 50 Rayleigh distributed extremes (thick line) | 1.080 | 0.1380 |
</details>

Figure 5.49 Gumbel plot comparison of four extreme value distributions rtted to the distribution of the largest of 50 Rayleigh distributed extremes.

where $p _ { k }$ is the proportion of operating hours in the wind speed bin with mean wind speed $U _ { k }$ and the operating range of wind speeds is divided into M bins.

# 5.14.5 Extrapolation

The load with a 50 year return period is found by extrapolating $F _ { L o n g - t e r m } ( x )$ to the requisite non-exceedance probability – i.e. $( 1 { - } 3 . 8 \times 1 0 ^ { - 7 } )$ for a 10 minute simulation period. As $F _ { L o n g - t e r m } ( x )$ is the summation of several mathematically derned distributions, this is straightforward. Figure 5.48 illustrates how the extrapolation might look if a single wind speed bin dominated the extreme loads for the three extreme value distributions considered.

# 5.14.6 Fitting probability distribution after aggregation

With this sequence, the rrst step is to aggregate the data points from the simulations from all the wind speed bins. If the number of simulations from each wind speed bin is proportional to the number of hours of operation in that bin and there are m 10 minute simulations in all, then the m global extremes can be ranked $I , 2 , \ldots i , \ldots m$ from smallest to largest, and the long-term empirical load non-exceedance probability distribution for the 10 minute extreme load, x, can be constructed according to the formula

$$
F _ {L o m g - t e r m} (x _ {i}) = \frac {i}{m + 1} \qquad i = 1, 2, \ldots m
$$

In cases where the number of simulations in each wind speed bin is not proportional to the actual likelihood of that bin, then different weights need to be assigned to the global extremes in different bins, and the probability distribution becomes

$$
F _ {L o m g - t e r m} (x) = \sum_ {k = 1} ^ {b} \left(\sum_ {i = 1} ^ {n _ {k}} \frac {I [ x _ {i , k} \leq x ]}{m + 1}\right) w _ {k} = \sum_ {k = 1} ^ {b} \left(\sum_ {i = 1} ^ {n _ {k}} \frac {I [ x _ {i , k} \leq x ]}{m + 1}\right) \frac {m p _ {k}}{n _ {k}} \tag {5.151}
$$

where

$x _ { i , k }$ is the ith extreme in the kth wind speed bin

$\ I [ x _ { i . k } \leq x ] = 1$ if $x _ { i . k } \leq x$ and 0 otherwise

$n _ { k }$ is the number of simulations in the kth wind speed bin

b is the number of wind speed bins

$w _ { k }$ is the weighting factor for kth wind speed bin

$p _ { k }$ is the proportion of operating hours in the kth wind speed bin

The second step is the rtting of an extreme value distribution to the long-term empirical load distribution to permit extrapolation to the 50 year return load. Clearly, the ‘aggregation before rtting’ approach is simpler than the ‘rtting before aggregation’ approach in that only one rtting operation is required, although the inherent complexity of the long-term empirical distribution may make a close rt more difrcult to achieve.

# 5.14.7 Local extremes method

The local extremes method is the same as the global extremes method, except that several independent extreme values in each 10 minute simulation are utilised in constructing the empirical load non-exceedance probability distribution(s) instead of just the single largest value – i.e. the ‘global extreme’ – from each simulation.

If there are n independent extreme values in each 10 minute simulation, then the empirical non-exceedance probability distribution for the 10 minute extreme load, $x _ { k }$ , at wind speed $U _ { k }$ can be constructed from the non-exceedance probability distribution of the local extremes using

$$
F (x _ {k} | U _ {k}) = [ F _ {l o c a l} (x _ {k} | U _ {k}) ] ^ {n}
$$

To ensure independence of the local extremes, annex G of IEC 61400-1 edition 4 suggests that individual extremes should be separated by at least three response cycles. A less rigorous but computationally simpler approach is to divide the 10 minute simulation period into n segments or ‘blocks’ of equal duration and use the maximum value from each. This method of extracting the local extremes is illustrated in Figure 5.50 for a turbine rotating at 15 rpm with a block size of 12 seconds, corresponding to three cycles of rotation.

Fogle et al. (2008) have applied statistical tests for independence to block maxima obtained from 200 simulated load time histories for a 5 MW turbine model developed by the National Renewable Energy Laboratory (NREL) and concluded that a block duration of 30 seconds is required to ensure independence. However, they also found that the use of block durations as short as 5 seconds made negligible difference to the tail of the empirical probability distribution.

![](images/a9d70121a61fe4f2e644567caa3497a04bbf649378a6aef099a94887daafc5f3.jpg)

<details>
<summary>line</summary>

| Time (s) | Load time series, normalised by standard deviation |
| -------- | --------------------------------------------------- |
| 100      | 0.2                                                 |
| 110      | -1.5                                                |
| 120      | 0.5                                                 |
| 130      | -2.0                                                |
| 140      | 1.8                                                 |
| 150      | -3.0                                                |
| 160      | 0.7                                                 |
| 170      | 1.3                                                 |
| 180      | 2.4                                                 |
| 190      | -0.5                                                |
| 200      | 0.9                                                 |
| 210      | -1.2                                                |
| 220      | 0.8                                                 |
| 230      | -2.5                                                |
| 240      | 2.6                                                 |
</details>

Figure 5.50 Local extremes derived from blocks of 12 seconds’ duration.

# 5.14.8 Convergence requirements

IEC 61400-1 edition 4 imposes a limit on the uncertainty of extrapolated loads by requiring that sufrcient simulations are carried out so that the 90% conrdence interval on the 84% quantile load (that is, the extreme load in a 10 minute simulation likely to be exceeded 16% of the time) is less than 15% of that load. This requirement is expressed as

$$
\frac {\hat {S} _ {0 . 8 4 , 0 . 0 5} - \hat {S} _ {0 . 8 4 , 0 . 9 5}}{\hat {S} _ {0 . 8 4}} <   0. 1 5 \tag {5.152}
$$

where the conrdence bounds $\hat { S } _ { 0 . 8 4 , 0 . 0 5 }$ and $\hat { S } _ { 0 . 8 4 , 0 . 9 5 }$ are the empirical estimates of the 84% quantile load with a $5 \%$ and 95% probability of not being exceeded, respectively.

One approach to estimating the conrdence bounds utilises the binomial expansion to obtain the probability, C(j; m, 0.84), of j or fewer occurrences of the non-exceedance of the 84% quantile load in m simulations. This is given by

$$
C (j; m, 0. 8 4) = \sum_ {i = 0} ^ {j} \frac {m !}{i ! (m - i) !} 0. 8 4 ^ {i} 0. 1 6 ^ {m - i} \tag {5.153}
$$

As an example, this probability is plotted against j for the case of m = 15 simulations in Figure 5.51. It is seen that the 5% and 95% conrdence bounds on the number of trials in which the 84% quantile load is not exceeded are 9.5 and 14.3, respectively. The conrdence bounds on the 84% quantile load, $\hat { S } _ { 0 . 8 4 , 0 . 0 5 }$ and $\hat { S } _ { 0 . 8 4 , 0 . 9 5 }$ , required for the inequality (5.152) can then be derived by interpolating between the 9th and 10th and 14th and 15th ranked extremes, respectively. The ranking is from smallest to largest as usual.

![](images/9c66b7403e4b6b3b62c4d079b307ecadf95bf1bcaeafb9b913bb1f87e4bfde7d.jpg)

<details>
<summary>line</summary>

| Number of simulations, j | Probability of j or fewer occurrences of the non-exceedance of the 84% quantile load in a total of 15 simulations |
| ------------------------ | ---------------------------------------------------------------------------------- |
| 0                        | 0.0                                                                                |
| 1                        | 0.0                                                                                |
| 2                        | 0.0                                                                                |
| 3                        | 0.0                                                                                |
| 4                        | 0.0                                                                                |
| 5                        | 0.0                                                                                |
| 6                        | 0.0                                                                                |
| 7                        | 0.0                                                                                |
| 8                        | 0.0                                                                                |
| 9                        | 0.02                                                                               |
| 10                       | 0.06                                                                               |
| 11                       | 0.2                                                                                |
| 12                       | 0.4                                                                                |
| 13                       | 0.7                                                                                |
| 14                       | 0.9                                                                                |
| 15                       | 1.0                                                                                |
</details>

Figure 5.51 Probability of j or fewer occurrences of the non-exceedance of the 84% quantile load in a total of 15 simulations.

Table 5.11 Table of conrdence bounds on the number of simulations in which the 84% load is not exceeded for different numbers of simulations in total. 

<table><tr><td>Total number of simulations, m</td><td>Number of occurrences of the non-exceedance of the 84% quantile load with 5% probability of not being exceeded</td><td>Number of occurrences of the non-exceedance of the 84% quantile load with 95% probability of not being exceeded</td></tr><tr><td>15</td><td>9.5</td><td>14.32</td></tr><tr><td>20</td><td>13.35</td><td>18.83</td></tr><tr><td>25</td><td>17.23</td><td>23.39</td></tr><tr><td>30</td><td>21.18</td><td>27.83</td></tr><tr><td>35</td><td>25.13</td><td>32.32</td></tr></table>

Annex G of IEC 61400-1 edition 4 provides a table of 5% and 95% conrdence bounds on the number of simulations in which the 84% quantile load is not exceeded for each value of m, the total number of simulations, from 15 to 35. Selected values are given in Table 5.11.

# References

Abramowitz, M. and Stegun, I.A. (1965). Handbook of Mathematical Functions. New York: Dover. Armstrong JRC and Hancock M (1991). Feasibility study of teetered, stall-regulated rotors. ETSU Report No. WN 6022.

Barltrop, N.D.P. and Adams, A.J. (1991). Dynamics of Fixed Marine Structures, 3e. Butterworth-Heinemann.   
Batchelor, G.K. (1953). The Theory of Homogeneous Turbulence. Cambridge University Press.   
Bierbooms, W.A.A.M. (2005). Constrained stochastic simulation – generation of time series around some specirc event in a normal process. Extremes 8 (3).   
Bishop NWM, Zhihua H, and Sheratt F (1991). The analysis of non-Gaussian loadings from wind turbine blades using frequency domain techniques. Proceedings of the BWEA Conference, pp. 317–323.   
Bishop NWM, Wang R, and Lack L (1995). A frequency domain fatigue predictor for wind turbine blades including deterministic components. Proceedings of the BWEA Conference, pp. 53–58.   
British Standards Institution. (1980). BS 5400: Part 10: 1980 Steel, concrete and composite bridges – Code of practice for fatigue.   
British Standards Institution. (1986). BS 8100: Part 1: 1986 Lattice towers and masts – Code of practice for loading.   
Clough, R.W. and Penzien, J. (1993). Dynamics of Structures. McGraw-Hill.   
Craig, R.R. Jr. and Bampton, M.C.C. (1968). Coupling of substructures for dynamic analysis. AIAA J. 6 (7): 1313–1319.   
Creed, R.F. (1993) High cycle tensile fatigue of unidirectional rbreglass composite tested at high frequency. PhD thesis, Montana State University.   
Davenport, A.G. (1964). Note on the distribution of the largest value of a random function with application to gust loading. Proc. Inst. Civil Eng. 28: 187–196.   
Dirlik, T. (1985). Application of Computers in Fatigue Analysis. University of Warwick thesis.   
DNVGL (2020). Bladed. https://www.dnvgl.com/services/wind-turbine-design-softwarebladed-3775.   
DNVGL – Energy (2016). Bladed theory manual version 4.8.   
DNVGL-ST-0376 (2015). Rotor blades for wind turbines. Akershus, Norway: DNVGL.   
DNVGL-ST-0437 (2016). Loads and site conditions for wind turbines. Akershus, Norway: DNVGL.   
DS 410 (1983). Loads for the design of structures. Copenhagen: Danish Standards Foundation.   
DS 472 (1992). Loads and safety of wind turbine construction. Copenhagen: Danish Standards Foundation.   
EN 1991-1-4:2005 (2005). Eurocode 1: Actions on structures – Part 1-4: General actions – Wind actions. Brussels: European Committee for Standardization.   
Fogle, J., Agarwal, P., and Manuel, L. (2008). Towards an improved understanding of statistical extrapolation for wind turbine extreme loads. Wind Energy 11: 613–635. (Expanded version published by American Institute of Aeronautics and Astronautics).   
Freudenreich, K. and Argyriadis, K. (2008). Wind turbine load level based on extrapolation and simplired methods. Wind Energy 11: 589–600.   
Garrad AD (1987). The use of rnite element methods for wind turbine dynamics. Proceedings of the BWEA Conference, pp. 79–83.   
Garrad AD and Hassan U (1986). The dynamic response of wind turbines for fatigue life and extreme load predicition. Proceedings of the EWEA Conference, pp. 401–406.   
Germanischer Lloyd. (2010). Rules and guidelines: IV – Industrial services: Part 1 – Guideline for the certiScation of wind turbines.   
Gibson, R.F. et al. (1982). Vibration characteristics of automotive composite materials. In: Short Fibre Reinforced Composite Materials, 133–150. West Conshohocken, Pennsylvania, USA: ASTM.   
Hansen A C 1998. User’s guide to the wind turbine dynamics computer programs YawDyn and AeroDyn for Adams, version 11.0. University of Utah.   
Harris, R.I. (1996). Gumbel re-visited – a new look at extreme value statistics applied to wind speeds. J. Wind Eng. Ind. Aerodyn. 59: 1–22.   
Harris, R.I., Deaves, D.M., 1980. The structure of strong winds. Proceedings of the CIRIA conference ‘Wind Engineering in the Eighties’, London (12–13 November 1980).

Hoskin RE, Warren JG, and Draper J (1989). Prediction of fatigue damage in wind turbine rotors. Proceedings of the EWEC, pp. 389–394.   
Hosking, J.R.M., Wallis, J.R., and Wood, E.F. (1985). Estimation of the generalized extreme value distribution by the method of probability-weighted moments. Technometrics 27 (3): 251–261.   
IEC 1400-1 (1994). Wind turbine generator systems – Part 1: Safety requirements. Geneva, Switzerland: International Electrotechnical Commission.   
IEC 61400-1 (1999). Wind turbine generator systems – Part 1: Safety requirements (2nd edition). Geneva, Switzerland: International Electrotechnical Commission.   
IEC 61400-1 (2005). Wind turbines – Part 1: Design requirements (3rd edition). Geneva, Switzerland: International Electrotechnical Commission.   
IEC 61400-1 (2019). Wind energy generation systems – Part 1: Design requirements (4th edition). Geneva, Switzerland: International Electrotechnical Commission.   
International Energy Agency Wind Technology Collaboration Programme (1990). Recommended practice 3: Fatigue loads, 2nd edition (Task 11). https://community.ieawind.org/publications/rp.   
Jamieson P and Hunter C (1985). Analysis of data from Howden 300 kW wind turbine on Burgar Hill Orkney. Proceedings of the BWEA Conference, pp. 253–258.   
Jamieson P, Camp TR, and Quarton DC (2000). Wind turbine design for offshore. Proceedings of the Offshore Wind Energy in Mediterranean and European Seas, CEC/EWEA/IEA, Sicily, pp. 405–414.   
Jenkinson, A.F. (1955). The frequency distribution of the annual maximum (or minimum) of meteorological elements. Q. J. R. Meteorol. Soc. 81: 158–171.   
Kaimal, J.C. et al. (1972). Spectral characteristics of surface-layer turbulence. Quarterly Journal of the Meteorological Society, 98: 563–589.   
von Karman, T. (1948). Progress in the statistical theory of turbulence. In Proceedings of the National Academy of Sciences. vol. 34, pp. 530–539.   
Larsen, G.C., Ronold, K., Jorgensen, H.E., Argyriadis, K. and 2de Boer, J. (1999). Ultimate loading of wind turbines. Risø National Laboratory No. R-1111.   
Lobitz DWA (1984). NASTRAN based computer program for structural dynamic analysis of HAWTs. Proceedings of the EWEA conference.   
Madsen PH, Frandsen S, Holley WE, and Hansen JC (1984). Dynamics and fatigue damage of wind turbine rotors during steady operation. Risø National Laboratory No. R-512.   
Mann (1998, 1998). Wind reld simulation. J. Mann, Prob. Engng. Mech. 13 (4): 269–282.   
Matsuishi M and Endo T (1968). ‘Fatigue of metals subject to varying stress. Proceedings of the Japan Society of Mechanical Engineers.   
Molenaar, D.P. and Dijkstra, S. (1999). State-of-the-art of wind turbine design codes: main features overview for cost-effective generation. Wind Eng. 23 (5): 295–311.   
Morgan CA and Tindal AJ (1990). Further analysis of the Orkney MS-1 data. Proceedings of the BWEA Conference, pp. 325–330.   
Moriaty PJ, Holley WE and Butterreld SP (2004). Extrapolation of extreme and fatigue loads using probabilistic methods. NREL Report TP-500-34421.   
Petersen JT, Madsen HA, Björck A, Enevoldsen P, Øye S, Ganander H, and Winkelaar D (1998). Prediction of dynamic loads and induced vibrations in stall. Risø National Laboratory No. R-1045.   
Putter, S. and Manor, H. (1978). Natural frequencies of radial rotating beams. J. Sound Vib. 56 (2): 175–185.   
Ragan, P. and Manuel, L. (2007). Comparing estimates of wind turbine fatigue loads using time-domain and spectral methods. Wind Eng. 31 (2): 83–99.   
Rasmussen F. (1984). Aerodynamic performance of a new LM 17.2 m rotor. Risø National Laboratory No. 2432.   
Shabana, A.A. (1998). Dynamics of Multibody Systems, 2e. Cambridge: Cambridge University Press.

Thomsen K (1998). The statistical variation of wind turbine fatigue loads. Risø National Laboratory No. R-1063.

Thomsen K and Madsen PH (1997). Application of statistical methods to extreme loads for wind turbines. Proceedings of the EWEC, pp. 595–598.

Veers PS (1988). Three-dimensional wind simulation. Sandia Report SAND88–0152.

Warren JG, Quarton DC, Lack L, Draper J (1988). Prediction of fatigue damage in wind turbine rotors. Proceedings of the BWEA Conference.

# Appendix A5 Dynamic response of stationary blade in turbulent wind

# A5.1 Introduction

As described in Chapter 2, the turbulent wind contains wind speed suctuations over a wide range of frequencies, as described by the power spectrum. Although the bulk of the turbulent energy is normally at frequencies much lower than the blade rrst mode out-of-plane frequency, which is typically over 1 Hz, the fraction close to the rrst mode frequency will excite resonant blade oscillations. This appendix describes the method by which the resonant response may be determined. Working in the frequency domain, expressions for the standard deviations of both the tip displacement and root bending moment responses are derived, and then the method of deriving the peak value in a given period is described. Initially the wind is assumed to be perfectly correlated along the blade, but subsequently the treatment is extended to include the effect of spatial variation.

# A5.2 Frequency response function

# A5.2.1 Equation of motion

The dynamic response of a cantilever blade to the suctuating aerodynamic loads upon it is most conveniently investigated by means of modal analysis, in which the excitations of the various different natural modes of vibration are computed separately and the results superposed. Thus the desection x(r,t) at radius r is given by

$$
x (r, t) = \sum_ {i = 1} ^ {\infty} f _ {i} (t) \mu_ {i} (t)
$$

Normally, in the case of a stationary blade, the rrst mode dominates and higher modes do not need to be considered. The equation of motion for the ith mode, which is derived in Section 5.8.1, is as follows:

$$
m _ {i} \ddot {f} _ {i} (t) + c _ {i} \dot {f} _ {i} (t) + m _ {i} \omega_ {i} ^ {2} f _ {i} (t) = \int_ {0} ^ {R} \mu_ {i} (r) q (r, t) d r \tag {A5.1}
$$

where

q(r,t) is the applied loading

$f _ { i } ( t )$ is the tip displacement

$\mu _ { i } ( r )$ is the non-dimensional mode shape of the ith mode, normalised to give a tip displacement of unity

$\omega _ { i }$ is the natural frequency in radians per second

$m _ { i }$ is the generalised mass, $\begin{array} { l } { { \displaystyle \int _ { 0 } ^ { R } m ( r ) \mu _ { i } ^ { 2 } ( r ) d r } } \end{array}$

and $c _ { i }$ is the generalised damping, $\begin{array} { c } { { R } } \\ { { \int _ { 0 } { \hat { c } ( \boldsymbol { r } ) \mu _ { i } ^ { 2 } ( \boldsymbol { r } ) d \boldsymbol { r } } } } \end{array}$

# A5.2.2 Frequency response function

If q(r,t) varies harmonically, with frequency 휔 and amplitude $q _ { 0 } ( r )$ , then it can be shown that

$$
\begin{array}{l} f _ {i} (t) = \frac {1}{m _ {i}} \frac {\int_ {0} ^ {R} \mu_ {i} (r) q _ {0} (r) d r}{\sqrt {(\omega_ {i} ^ {2} - \omega^ {2}) ^ {2} + (c _ {i} / m _ {i}) ^ {2} \omega^ {2}}} \cos (\omega t + \phi_ {i}) \\ = \frac {1}{m _ {i} \omega_ {i} ^ {2}} \frac {\int_ {0} ^ {R} \mu_ {i} (r) q _ {0} (r) d r}{\sqrt {(1 - \omega^ {2} / \omega_ {i} ^ {2}) ^ {2} + (c _ {i} / m _ {i} \omega_ {i} ^ {2}) ^ {2} \omega^ {2}}} \cos (\omega t + \phi_ {i}) \tag {A5.2} \\ \end{array}
$$

Derning $k _ { i } = m _ { i } \omega _ { i } ^ { 2 }$ , and noting that the damping ratio $\xi _ { i } = c _ { i } / 2 m _ { i } \omega _ { i }$ , this becomes

$$
f _ {i} (t) = \frac {1}{k _ {i}} \frac {\int_ {0} ^ {R} \mu_ {i} (r) q _ {0} (r) d r}{\sqrt {(1 - \omega^ {2} / \omega_ {i} ^ {2}) ^ {2} + 4 \xi_ {i} ^ {2} \omega^ {2} / \omega_ {i} ^ {2}}} \cos (\omega t + \phi_ {i}) = A _ {i} \cos (\omega t + \phi_ {i}) \tag {A5.3}
$$

The numerator $\begin{array} { r } { \int _ { 0 } ^ { R } \mu _ { i } ( r ) q _ { 0 } ( r ) d r } \end{array}$ is the amplitude of the equivalent harmonic loading at the tip of the cantilever that would result in the same tip displacement as the loading $q ( r , t )$ , and is known as the generalised load with respect to the ith mode, $Q _ { \mathrm { i } } ( t )$ . Thus, the ratio between the tip displacement amplitude and the amplitude of the generalised load is

$$
\begin{array}{l} \frac {A _ {i}}{\int_ {0} ^ {R} \mu_ {i} (r) q _ {0} (r) d r} = \frac {1}{k _ {i} \sqrt {(1 - \omega^ {2} / \omega_ {i} ^ {2}) ^ {2} + 4 \xi_ {i} ^ {2} \omega^ {2} / \omega_ {i} ^ {2}}} \\ = \frac {1}{k _ {i} \sqrt {(1 - n ^ {2} / n _ {i} ^ {2}) ^ {2} + 4 \xi_ {i} ^ {2} n ^ {2} / n _ {i} ^ {2}}} = | H _ {i} (n) | \tag {A5.4} \\ \end{array}
$$

The ratio| $H _ { i } ( n ) |$ is the modulus of the complex frequency response function, $H _ { i } ( n )$ , and its square can be used to transform the power spectrum of the wind incident on the blade into the power spectrum of the ith mode tip displacement. Thus, in the case of the dominant rrst mode, the tip displacement in response to a harmonic generalised loading, $Q _ { 1 } ( t )$ , of frequency n is given by

$$
x _ {1} (R, t) = f _ {1} (t) = Q _ {1} (t). | H _ {1} (n) |
$$

and the power spectrum of the rrst mode tip desection is $S _ { 1 x } ( n ) = S _ { O 1 } ( n ) . | H _ { 1 } ( n ) | ^ { 2 }$

In what follows, the simplifying assumption is made initially that the wind is perfectly correlated along the blade.

# A5.3 Resonant displacement response ignoring wind variations along the blade

# A5.3.1 Linearisation of wind loading

For a suctuating wind speed $U ( t ) = \overline { { U } } + u ( t )$ , the wind load per unit length on the blade is $\begin{array} { r } { \frac { 1 } { 7 } C _ { f } \rho U ^ { 2 } ( t ) c ( r ) = \frac { 1 } { 7 } C _ { f } \rho \left[ \overline { { U } } ^ { 2 } + 2 \overline { { U } } u ( t ) + u ^ { 2 } ( t ) \right] c ( r ) } \end{array}$ , where $C _ { f }$ is the lift or drag coefrcient, as appropriate, and $c ( r )$ is the local blade chord dimension. In order to permit a linear treatment, the third term in the square brackets, which will normally be small compared to the rrst two, is ignored, so that the suctuating load $q ( r , t )$ becomes $C _ { f } \rho \overline { { U } } u ( t ) c ( r )$ .

# A5.3.2 First mode displacement response

Setting $q ( r , t ) = C _ { f } \rho \overline { { U } } u ( t ) c ( r )$ , the rrst mode tip displacement response to a sinusoidal wind suctuation of frequency $n \ ( = \omega / 2 \pi )$ and amplitude $u _ { \mathrm { o } } ( n )$ given by Eq. (A5.3) becomes

$$
\begin{array}{l} f _ {1} (t) = \int_ {0} ^ {R} \mu_ {1} (r) C _ {f} \rho \overline {{U}} c (r) d r. u _ {o} (n). | H _ {1} (n) |. \cos (2 \pi n t + \phi_ {1}) \\ = C _ {f} \rho \overline {{U}} \int_ {0} ^ {R} \mu_ {1} (r) c (r) d r. u _ {o} (n). | H _ {1} (n) |. \cos (2 \pi n t + \phi_ {1}) \tag {A5.5} \\ \end{array}
$$

Hence the power spectrum of rrst mode tip displacement is

$$
S _ {1 x} (n) = \left[ C _ {f} \rho \overline {{U}} \int_ {0} ^ {R} \mu_ {1} (r) c (r) d r \right] ^ {2}. S _ {u} (n). | H _ {1} (n) | ^ {2} \tag {A5.6}
$$

![](images/f779508359c0b4e61878b7adaee39d2210a65364cd4181f5b2ae2b9e3a91e7b9.jpg)

<details>
<summary>line</summary>

| Frequency (Hz) | Power Spectral Density |
| -------------- | ---------------------- |
| 0.0001         | ~0.00                  |
| 0.001          | ~0.02                  |
| 0.01           | ~0.15                  |
| 0.1            | ~0.22                  |
| 1              | ~0.25                  |
| 10             | ~0.01                  |
</details>

Figure A5.1 Power spectrum of wind turbulence and frequency response function.

where $S _ { \mathrm { u } } ( n )$ is the power spectrum for the along wind turbulence. Thus, the standard deviation of the rrst mode tip displacement is given by

$$
\sigma_ {1 x} ^ {2} = \left[ C _ {f} \rho \overline {{U}} \int_ {0} ^ {R} \mu_ {1} (r) c (r) d r \right] ^ {2} \int_ {0} ^ {\infty} S _ {u} (n). | H _ {1} (n) | ^ {2}. d n \tag {A5.7}
$$

# A5.3.3 Background and resonant response

Normally the bulk of the turbulent energy in the wind is at frequencies well below the frequency of the rrst out-of-plane blade mode. This is illustrated in Figure A5.1, where a typical power spectrum for wind turbulence is compared with the square, $| H _ { 1 } ( n ) | ^ { 2 }$ , of an example frequency response function for a 1 Hz resonant frequency.

The power spectrum is that due to Kaimal (and adopted in Eurocode 1 [EN 1991-1-4:2005]):

$$
n. S _ {u} (n) = \sigma_ {u} ^ {2} \frac {6 . 8 n L _ {u} ^ {x} / \overline {{U}}}{(1 + 1 0 . 2 . n . L _ {u} ^ {x} / \overline {{U}}) ^ {\frac {5}{3}}} \tag {A5.8}
$$

and is plotted as the non-dimensional power spectral density function, $\boldsymbol { R _ { u } } ( n ) =$ $n . S _ { u } ( n ) / \sigma _ { u } ^ { 2 } ,$ , against a logarithmic frequency scale. The timescale, $L _ { u } ^ { x } / \overline { { U } }$ , chosen is 4 seconds, based on a mean wind speed, ${ \overline { { U } } } ,$ , of 50 m/s and an integral length scale, $L _ { u } ^ { x }$ , of 200 m.

In view of the fact that the resonant response usually occurs over a narrow band of frequencies on the tail of the power spectrum, it is normal to treat it separately from the quasi-static response at lower frequencies and to ignore the variation in $n . S _ { \mathrm { u } } ( n )$ on either side of the resonant frequency, $n _ { 1 }$ . (See, for example, Wyatt 1980). The variance of total tip displacement then becomes

$$
\sigma_ {x} ^ {2} = \sigma_ {B} ^ {2} + \sigma_ {x 1} ^ {2}
$$

in which the variance of the rrst mode resonant response, $\sigma _ { x 1 }$ , is given by

$$
\sigma_ {x 1} ^ {2} = \left[ C _ {f} \rho \overline {{U}} \int_ {0} ^ {R} \mu_ {1} (r) c (r) d r \right] ^ {2}. S _ {u} (n _ {1}) \int_ {0} ^ {\infty} | H _ {1} (n) | ^ {2}. d n \tag {A5.9}
$$

and the resonant response of higher modes, $\sigma _ { x 2 } ^ { 2 } , ~ \sigma _ { x 3 } ^ { 2 }$ x2, etc. is ignored. The non-resonant response, $\sigma _ { \mathrm { B } } ,$ , is termed the background response and can be derived from simple static beam theory.

It has been shown by Newland (1984) that $\int _ { 0 } ^ { \infty } | H _ { 1 } ( n ) | ^ { 2 }$ .dn reduces to $\frac { \pi ^ { 2 } } { 2 \delta } . \frac { n _ { 1 } } { k _ { 1 } ^ { 2 } }$ , where $\delta$ is the logarithmic decrement of damping. The logarithmic decrement, $\delta ,$ is $2 \dot { \pi }$ times the damping ratio, $\xi _ { 1 }$ , derned as $\xi _ { 1 } = c _ { 1 } / 2 m _ { 1 } \omega _ { 1 }$ . Hence Eq. (A5.9) becomes

$$
\sigma_ {x 1} ^ {2} = \left[ C _ {f} \rho \overline {{U}} \int_ {0} ^ {R} \mu_ {1} (r) c (r) d r \right] ^ {2}. S _ {u} (n _ {1}) \frac {\pi^ {2}}{2 \delta} \frac {n _ {1}}{k _ {1} ^ {2}} \tag {A5.10}
$$

For comparison, the rrst mode component, $\overline { { x } } _ { 1 }$ , of the steady response is obtained by setting $\omega = 0$ and $\begin{array} { r } { q _ { 0 } ( r ) = \frac { 1 } { 2 } \rho \overline { { U } } ^ { 2 } C _ { f } c ( r ) } \end{array}$ in Eq. (A5.3), yielding

$$
\overline {{x}} _ {1} = \frac {1}{2} \rho \overline {{U}} ^ {2} C _ {f}. \frac {1}{k _ {1}}. \int_ {0} ^ {R} \mu_ {1} (r) c (r) d r \tag {A5.11}
$$

Hence, the ratio of the standard deviation of the rrst mode resonant response to the rrst mode component of the steady response is

$$
\frac {\sigma_ {x 1}}{\overline {{x}} _ {1}} = 2. \frac {\sigma_ {u}}{\overline {{U}}} \cdot \frac {\pi}{\sqrt {2 \delta}} \cdot \sqrt {\frac {n _ {1} S _ {u} (n _ {1})}{\sigma_ {u} ^ {2}}} = 2. \frac {\sigma_ {u}}{\overline {{U}}} \cdot \frac {\pi}{\sqrt {2 \delta}} \cdot \sqrt {R _ {u} (n _ {1})} \tag {A5.12}
$$

Note that towards the upper tail of the power spectrum of along wind turbulence, where $n _ { 1 }$ is likely to be located, $\sqrt { R _ { u } \left( n _ { 1 } \right) }$ tends to $\sqrt { 0 . 1 4 1 7 / ( n . L _ { u } ^ { x } / \overline { { U } } ) ^ { \frac { 2 } { 3 } } }$ .

# A5.4 Effect of across wind turbulence distribution on resonant displacement response

In the foregoing treatment, the wind was assumed to be perfectly correlated along the blade. The implications of removing this simplifying assumption will now be examined.

The suctuating load on the blade, $q ( r , t )$ , becomes $C _ { f } \rho \overline { { U } } u ( r , t ) c ( r )$ per unit length, and the generalised suctuating load with respect to the rrst mode becomes

$$
Q _ {1} (t) = \int_ {0} ^ {R} \mu_ {1} (r) q (r, t) d r = C _ {f} \rho \overline {{{U}}} \int_ {0} ^ {R} u (r, t). c (r). \mu_ {1} (r) d r \tag {A5.13}
$$

The standard deviation, $\sigma _ { \mathrm { Q 1 } }$ , of $Q _ { I } ( t )$ is given by

$$
\begin{array}{l} \sigma_ {Q 1} ^ {2} = \frac {1}{T} \int_ {0} ^ {T} Q _ {1} ^ {2} (t) d t = (\rho \overline {{U}} C _ {f}) ^ {2} \frac {1}{T} \int_ {0} ^ {T} \left[ \int_ {0} ^ {R} u (r, t). c (r). \mu_ {1} (r) d r \right] \left[ \int_ {0} ^ {R} u (r ^ {\prime}, t). c (r ^ {\prime}). \mu_ {1} (r ^ {\prime}) d r ^ {\prime} \right] d t \\ = (\rho \overline {{{U}}} C _ {f}) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \left[ \frac {1}{T} \int_ {0} ^ {T} u (r, t). u \left(r ^ {\prime}, t\right) d t \right] c (r). c (r ^ {\prime}). \mu_ {1} (r). \mu_ {1} (r ^ {\prime}). d r. d r ^ {\prime} \tag {A5.14} \\ \end{array}
$$

Now the expression within the square brackets is the cross-correlation function, $\kappa _ { u } ( r ,$ $r ^ { \prime } , \tau ) = E \{ u ( r , t ) u ( r ^ { \prime } , t + \tau ) \}$ , with 휏 set equal to zero. The cross-correlation function is related to the cross-spectrum, $\boldsymbol { S _ { u u } } ( \boldsymbol { r , r ^ { \prime } , n } )$ , as follows:

$$
\kappa_ {u} (r, r ^ {\prime}, \tau) = \frac {1}{2} \int_ {- \infty} ^ {\infty} S _ {u u} (r, r ^ {\prime}, n). \exp (i. 2 \pi n \tau) d n,
$$

giving

$$
\kappa_ {u} (r, r ^ {\prime}, 0) = \left[ \frac {1}{T} \int_ {0} ^ {T} u (r, t). u \left(r ^ {\prime}, t\right) d t \right] = \int_ {0} ^ {\infty} S _ {u u} (r, r ^ {\prime}, n) d n \text {   for   } \tau = 0 \tag {A5.15}
$$

Hence,

$$
\sigma_ {Q 1} ^ {2} = (\rho \overline {{{U}}} C _ {f}) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \left[ \int_ {0} ^ {\infty} S _ {u u} (r, r ^ {\prime}, n) d n \right] c (r). c (r ^ {\prime}). \mu_ {1} (r). \mu_ {1} (r ^ {\prime}). d r. d r ^ {\prime} \tag {A5.16}
$$

The normalised cross-spectrum is derned as $S _ { u u } ^ { N } ( r , r ^ { \prime } , n ) = \frac { S _ { u u } ( r , r ^ { \prime } , n ) } { S _ { u } ( n ) }$ , and like $S _ { u u } ( \boldsymbol { r } , \boldsymbol { r } ^ { \prime }$ , Su(n) n), is in general a complex quantity, because of phase differences between the wind speed suctuations at different heights. As only in-phase wind speed suctuations will affect the response, we consider only the real part of the normalised cross-spectrum, known as the normalised co-spectrum and denoted by $\psi _ { u u } ^ { N } ( \boldsymbol { r } , \boldsymbol { r } ^ { \prime } , n )$ . Substituting in Eq. (A5.16), we obtain

$$
\sigma_ {Q 1} ^ {2} = (\rho \overline {{U}} C _ {f}) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} \left[ \int_ {0} ^ {\infty} S _ {u} (n) \psi_ {u u} ^ {N} \left(r, r ^ {\prime}, n\right) d n \right] c (r). c (r ^ {\prime}). \mu_ {1} (r). \mu_ {1} (r ^ {\prime}). d r. d r ^ {\prime} \tag {A5.17}
$$

From this, it can be deduced that the power spectrum of the generalised load with respect to the rrst mode is

$$
S _ {Q 1} (n) = (\rho \overline {{U}} C _ {f}) ^ {2} \int_ {0} ^ {R} \int_ {0} ^ {R} S _ {u} (n) \psi_ {u u} ^ {N} (r, r ^ {\prime}, n) c (r). c (r ^ {\prime}). \mu_ {1} (r). \mu_ {1} (r ^ {\prime}). d r. d r ^ {\prime} \tag {A5.18}
$$

Note that the power spectrum for the along wind turbulence shows some variation with height, and so should strictly be written $S _ { \mathrm { u } } ( n , z )$ instead of $S _ { \mathrm { u } } ( n )$ . However, the variation along the length of a vertical blade is small and is ignored here.

As for the initial case when wind loadings along the blade were assumed to be perfectly correlated, the power spectrum for rrst mode tip displacement is equal to the product of the power spectrum of the generalised load (with respect to the rrst mode) and the square of the frequency response function, i.e.

$$
S _ {1 x} (n) = S _ {Q 1} (n). | H _ {1} (n) | ^ {2} \tag {A5.19}
$$

As before, $S _ { \mathrm { Q l } } ( n )$ is assumed constant over the narrow band of frequencies straddling the resonant frequency, and the standard deviation of resonant tip response becomes

$$
\sigma_ {x 1} ^ {2} = S _ {Q 1} (n _ {1}). \int_ {0} ^ {\infty} | H _ {1} (n) | ^ {2} d n = S _ {Q 1} (n _ {1}). \frac {\pi^ {2}}{2 \delta}. \frac {n _ {1}}{k _ {1} ^ {2}}. \tag {A5.20}
$$

# A5.4.1 Formula for normalised co-spectrum

It remains to evaluate $\begin{array} { r } { S _ { \mathcal { Q } 1 } ( n _ { 1 } ) = ( \rho \overline { { U } } C _ { f } ) ^ { 2 } . S _ { u } ( n _ { 1 } ) \int _ { 0 } ^ { R } \int _ { 0 } ^ { R } \psi _ { u u } ^ { N } ( r , r ^ { \prime } , n ) . c ( r ) . c ( r ^ { \prime } ) . \mu _ { 1 } ( r ) } \end{array}$ $\mu _ { 1 } ( r ^ { \prime } ) . d r . d r ^ { \prime }$ . The normalised co-spectrum, $\psi _ { u u } ^ { N } ( \boldsymbol { r } , \boldsymbol { r } ^ { \prime } , n )$ , must decrease as the spacing $\left| \boldsymbol { r } - \boldsymbol { r ^ { \prime } } \right|$ between the two points considered increases, and intuitively it is to be expected that the decrease would be more rapid for the higher frequency components of wind suctuation. On an empirical basis, Davenport (1962) has proposed an exponential expression for the normalised co-spectrum as follows:

$$
\psi_ {u u} ^ {N} (r, r ^ {\prime}, n) = \exp [ - C | r - r ^ {\prime} | n / \overline {{{U}}} ] \tag {A5.21}
$$

where C is a non-dimensional decay constant. Davenport noted that measurements by Cramer (1958) indicated values of C ranging from 7 in unstable conditions to 50 in stable conditions but recommended the use of the lower rgure as being the more conservative despite the likelihood of stable conditions in high winds. Dyrbye and Hansen (1997) quote Risø measurements reported by Mann (1994) that indicate a value of C of 9.4, and they recommend a value of 10 for use in design. A value of 11.5 is implicitly assumed in Eurocode 1.

There is an obvious inconsistency in the exponential expression for the normalised co-spectrum – when it is integrated up over the plane perpendicular to the wind direction, the result is positive instead of zero, as it should be. This has led to the development of more complex expressions by Harris (1971) and Krenk (1995). However, the Davenport formulation will be used here, giving

$$
\begin{array}{l} \sigma_ {x 1} ^ {2} = S _ {Q 1} (n _ {1}). \frac {\pi^ {2}}{2 \delta}. \frac {n _ {1}}{k _ {1} ^ {2}} \\ = (\rho \overline {{U}} C _ {f}) ^ {2}. S _ {u} (n _ {1}) \int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - C | r - r ^ {\prime} | n _ {1} / \overline {{U}} ]. c (r). c (r ^ {\prime}). \mu_ {1} (r). \mu_ {1} (r ^ {\prime}). d r. d r ^ {\prime} \left[ \frac {\pi^ {2}}{2 \delta} \frac {n _ {1}}{k _ {1} ^ {2}} \right] \tag {A5.22} \\ \end{array}
$$

The resonant response can be expressed in terms of the rrst mode component, $\overline { { x } } _ { 1 }$ , of the steady response, ${ \ L } _ { 2 } ^ { 1 } \rho \overline { { U } } ^ { 2 } C _ { f } \frac { 1 } { k _ { 1 } } \int _ { 0 } ^ { R } \mu _ { 1 } ( r ) . c ( r ) d r$ , from Eq. (A5.11), giving

$$
\frac {\sigma_ {x 1} ^ {2}}{\overline {{x}} _ {1} ^ {2}} = 4. \frac {\sigma_ {u} ^ {2}}{\overline {{U}} ^ {2}}. \frac {\pi^ {2}}{2 \delta}. R _ {u} (n _ {1}) \frac {\int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - C | r - r ^ {\prime} | n _ {1} / \overline {{U}} ] . c (r) . c (r ^ {\prime}) . \mu_ {1} (r) . \mu_ {1} (r ^ {\prime}) . d r . . d r ^ {\prime}}{\left(\int_ {0} ^ {R} c (r) . \mu_ {1} (r) . d r\right) ^ {2}} \tag {A5.23}
$$

Hence,

$$
\frac {\sigma_ {x 1}}{\overline {{x}} _ {1}} = 2. \frac {\sigma_ {u}}{\overline {{U}}}. \frac {\pi}{\sqrt {2 \delta}}. \sqrt {R _ {u} (n _ {1})}. \sqrt {\mathrm{K} _ {\mathrm{Sx}} (\mathrm{n} _ {1})} \tag {A5.24}
$$

where

$$
\mathrm{K} _ {\mathrm{Sx}} (\mathrm{n} _ {1}) = \frac {\int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - C | r - r ^ {\prime} | n _ {1} / \overline {{U}} ] . c (r) . c (r ^ {\prime}) . \mu_ {1} (r) . \mu_ {1} (r ^ {\prime}) . d r . d r ^ {\prime}}{\left(\int_ {0} ^ {R} c (r) . \mu_ {1} (r) . d r\right) ^ {2}} \tag {A5.25}
$$

is denoted the size reduction factor, which results from the lack of correlation of the wind along the blade. As an example, the size reduction factor, $\mathrm { K } _ { \mathrm { S x } } ( \mathrm { n } _ { 1 } )$ , is plotted out against frequency in Figure A5.2 for the case of a 40 m blade with chord $c ( r ) = 0 . 0 9 6 1 \mathrm { R } - 0 . 0 6 4 6 7 \mathrm { r }$ (Blade SC40), assuming a decay constant C of 10 and a mean wind speed $\overline { { U } }$ of 50 m/s. The mode shape taken is the same as for the example in Section 5.6.3 in edition 2 (see Figure 5.4). Also shown for comparison is the corresponding parameter for a uniform cantilever.

# A5.5 Resonant root bending moment

For design purposes, it is the augmentation of blade bending moments due to dynamic effects that is of principal signircance. The ratio of the standard deviation of the rrst mode resonant root bending moment to the steady root bending moment (allowing for the lack of correlation of wind suctuations along the blade) is derived below.

Derning $M _ { 1 } ( t )$ as the suctuating root bending moment due to wind excitation of the rrst mode, we have

$$
M _ {1} (t) = \int_ {0} ^ {R} m (r) \ddot {x} _ {1} (t, r) r d r = \int_ {0} ^ {R} m (r) \omega_ {1} ^ {2} x _ {1} (t, r) r d r = \omega_ {1} ^ {2} f _ {1} (t) \int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r (\mathrm{A5.26})
$$

Hence, the standard deviation of $M _ { 1 } ( t )$ ,

$$
\sigma_ {M 1} = \omega_ {1} ^ {2} \sigma_ {x 1} \int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r \tag {A5.27}
$$

![](images/b024b6b22db1c802170135d6cb56dd426f2d81072d01b85e197647b566872540.jpg)

<details>
<summary>line</summary>

| First mode natural frequency, n₁ (Hz) | Tapered blade | Blade of constant cross-section (dashed line) |
| ------------------------------------- | ------------- | --------------------------------------------- |
| 0                                     | 1.0           | 1.0                                           |
| 0.5                                   | ~0.6          | ~0.5                                          |
| 1.0                                   | ~0.4          | ~0.3                                          |
| 1.5                                   | ~0.3          | ~0.25                                         |
| 2.0                                   | ~0.25         | ~0.2                                          |
| 2.5                                   | ~0.2          | ~0.18                                         |
| 3.0                                   | ~0.18         | ~0.15                                         |
</details>

Figure A5.2 Size reduction factors for the rrst mode resonant response due to lack of correlation of wind loading along the blade: variation with frequency for 40 m blade.

The steady root bending moment,

$$
\overline {{M}} = \int_ {0} ^ {R} \frac {1}{2} \rho \overline {{U}} ^ {2} C _ {f}. c (r) r d r = \frac {1}{2} \rho \overline {{U}} ^ {2} C _ {f} \int_ {0} ^ {R} c (r) r d r \tag {A5.28}
$$

Hence, the ratio

$$
\frac {\sigma_ {M 1}}{\overline {{M}}} = \frac {\omega_ {1} ^ {2} \sigma_ {x 1} \int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r}{\frac {1}{2} \rho \overline {{U}} ^ {2} C _ {f} \int_ {0} ^ {R} c (r) r d r} \tag {A5.29}
$$

Substituting the expression for $\sigma _ { \mathrm { x l } }$ from Eq. (A5.22), we obtain

$$
\frac {\sigma_ {M 1}}{\overline {{M}}} = \frac {\omega_ {1} ^ {2} . \rho \overline {{U}} C _ {f} . \frac {\pi}{\sqrt {2 \delta}} \frac {\sqrt {n _ {1} S _ {u} (n _ {1})}}{k _ {1}} \int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r \sqrt {\int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - C | r - r ^ {\prime} | n _ {1} / \overline {{U}} ] . c (r) . c (r ^ {\prime}) . \mu_ {1} (r) . \mu_ {1} (r ^ {\prime}) . d r . d r ^ {\prime}}}{\frac {1}{2} \rho \overline {{U}} ^ {2} C _ {f} \int_ {0} ^ {R} c (r) r d r} \tag {A5.30}
$$

Noting that $R _ { u } ( n ) = n . S _ { u } ( n ) / \sigma _ { u } ^ { 2 }$ , and that $k _ { 1 } = m _ { 1 } \omega _ { 1 } ^ { 2 }$ , this simplires to

$$
\frac {\sigma_ {M 1}}{\overline {{M}}} = 2 \frac {\sigma_ {u}}{\overline {{U}}} \frac {\pi}{\sqrt {2 \delta}} \sqrt {R _ {u} (n)} \frac {\int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r}{m _ {1} . \int_ {0} ^ {R} c (r) r d r} \sqrt {\int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - C | r - r ^ {\prime} | n _ {1} / \overline {{U}} ] . c (r) . c (r ^ {\prime}) . \mu_ {1} (r) . \mu_ {1} (r ^ {\prime}) . d r . d r ^ {\prime}} \tag {A5.31}
$$

where $\begin{array} { r } { m _ { 1 } = \int _ { 0 } ^ { R } m ( r ) \mu _ { 1 } ^ { 2 } ( r ) d r } \end{array}$ is the generalised mass with respect to the rrst mode, and the exponential expression within the double integral allows for the lack of correlation of wind suctuations along the blade. Substituting $\begin{array} { r l } {  { ( \int _ { 0 } ^ { R } c ( r ) . \mu _ { 1 } ( r ) . d r ) . \sqrt { K _ { S x } ( n _ { 1 } ) } } \quad } & { { } } \end{array}$ for the square root of the double integral, using Eq. (A5.25), leads to

$$
\frac {\sigma_ {M 1}}{\overline {{M}}} = 2 \frac {\sigma_ {u}}{\overline {{U}}} \frac {\pi}{\sqrt {2 \delta}} \sqrt {R _ {u} (n)} \frac {\int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r}{m _ {1} . \int_ {0} ^ {R} c (r) r d r} \left(\int_ {0} ^ {R} c (r). \mu_ {1} (r). d r\right). \sqrt {K _ {S x} (n _ {1})} \tag {A5.32}
$$

Derning the ratio of the integrals,

$$
\frac {\int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r}{m _ {1} . \int_ {0} ^ {R} c (r) r d r} \left(\int_ {0} ^ {R} c (r). \mu_ {1} (r). d r\right) = \frac {\sigma_ {M 1}}{\overline {{M}}} / \frac {\sigma_ {x 1}}{\overline {{x}} _ {1}}, \text { as } \lambda_ {\mathrm{M1}} \tag {A5.33}
$$

we obtain

$$
\frac {\sigma_ {M 1}}{\overline {{M}}} = 2 \frac {\sigma_ {u}}{\overline {{U}}} \frac {\pi}{\sqrt {2 \delta}}. \sqrt {R _ {u} (n _ {1})}. \sqrt {K _ {S x} (n _ {1})}. \lambda_ {\mathrm{M} 1} \tag {A5.34}
$$

# A5.6 Root bending moment background response

The root bending moment background response can be expressed in terms of the standard deviation of the root bending moment excluding resonant effects. If the wind is perfectly correlated along the blade, this is given by

$$
\sigma_ {M B} = C _ {f} \rho \overline {{{U}}}. \sigma_ {u} \int_ {0} ^ {R} c (r) r d r \tag {A5.35}
$$

However, if the lack of correlation of wind suctuations along the blade is taken into account,

$$
\sigma_ {M B} = C _ {f} \rho \overline {{U}}. \sigma_ {u} \sqrt {\int_ {0} ^ {R} \int_ {0} ^ {R} \rho_ {u} (r - r ^ {\prime}) . c (r) . c (r ^ {\prime}) . r . r ^ {\prime} . d r . d r ^ {\prime}} \tag {A5.36}
$$

where $\rho _ { \mathrm { u } } \left( r - r ^ { \prime } \right)$ is the normalised cross-correlation function between simultaneous wind speed suctuations at two different blade radii and is derned as

$$
\rho_ {u} (r - r ^ {\prime}) = \frac {1}{\sigma_ {u} ^ {2}} E \{u (r, t). u (r ^ {\prime}, t + \tau) \} \tag {A5.37}
$$

with 휏 set equal to zero.

Measurements indicate that the normalised cross-correlation function decays exponentially, so it can be expressed as

$$
\rho_ {u} (r - r ^ {\prime}) = \exp [ - | r - r ^ {\prime} | / L _ {u} ^ {r} ] \tag {A5.38}
$$

where $L _ { u } ^ { r }$ is the integral length scale for the longitudinal turbulence component measured in the across wind direction along the blade and is thus derned as $\begin{array} { r l r } {  { \int _ { 0 } ^ { \infty } \rho _ { u } ( r - r ^ { \prime } ) . d ( r - } } \end{array}$ $r ^ { \prime } )$ . As the integral length scale for longitudinal turbulence measured vertically in the across wind direction $( L _ { u } ^ { z } )$ , is, if anything, less than that measured horizontally $( L _ { u } ^ { y } )$ , it is conservative to treat it as being equal to that measured horizontally, with the result that $L _ { u } ^ { r }$ can be taken as equal to $L _ { u } ^ { y }$ also. Typically, $L _ { u } ^ { y }$ is approximately equal to 30% of $L _ { u } ^ { x }$ , the integral length scale for longitudinal turbulence measured in the along wind direction. Observing that

$$
\overline {{M}} = \frac {1}{2} \rho \overline {{U}} ^ {2} C _ {f} \int_ {0} ^ {R} c (r). r. d r
$$

we can therefore write

$$
\frac {\sigma_ {M B}}{\overline {{M}}} = 2 \frac {\sigma_ {u}}{\overline {{U}}}. \sqrt {K _ {S M B}} \tag {A5.39}
$$

where $K _ { S M B } .$ , the size reduction factor for the root bending moment background response, is derned as

$$
K _ {S M B} = \frac {\int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - | r - r ^ {\prime} | / 0 . 3 L _ {u} ^ {x} ] . c (r) . c (r ^ {\prime}) . r . r ^ {\prime} . d r . d r ^ {\prime}}{\left(\int_ {0} ^ {R} c (r) . r d r\right) ^ {2}} \tag {A5.40}
$$

For a blade with a uniform chord, the integral is straightforward, giving

$$
K _ {S M B} = 4 \left[ \frac {2}{3 \phi} - \frac {1}{\phi^ {2}} + \frac {2}{\phi^ {4}} - \exp (- \phi) \{\frac {2}{\phi^ {3}} + \frac {2}{\phi^ {4}} \} \right] \quad \mathrm{where} \phi = \frac {R}{0 . 3 L _ {u} ^ {x}} \qquad (\mathrm{A5.41})
$$

As an example, $K _ { \mathrm { S M B } }$ comes to 0.837 for the case of R = 40 m and $L _ { u } ^ { x } = 1 8 9 \ m$ , indicating that the lack of correlation of the wind suctuations reduces the root bending moment appreciably.

For blades with a normal tapering chord, $K _ { \mathrm { S M B } }$ can be evaluated numerically. In the case of a blade with a tip chord equal to 33% of the maximum chord, $K _ { \mathrm { S M B } }$ is 0.829 for the same value of $\phi$ as before. It is seen that the taper has an almost negligible effect on the end result.

# A5.7 Peak response

One of the key parameters required in blade design is the extreme value of the out-of-plane bending moment. The 50 year return moment is derned as the expected maximum moment occurring during the mean wind averaging period when the mean takes the 50 year return value. Treating the moment as a Gaussian process, Davenport (1964) has shown that the expected value of the maximum departure from the mean is the standard deviation multiplied by the peak factor, g, where

$$
g = \sqrt {2 \ln (\nu T)} + \frac {0 . 5 7 7 2}{\sqrt {2 \ln (\nu T)}} \tag {A5.42}
$$

In this formula, 휈 is the mean zero up-crossing frequency of the root moment suctuations, and T is the mean wind speed averaging period. The variance of the root bending moment is, in the same way as for the tip displacement, equal to the sum of the variances of the background and resonant root bending moment responses, i.e.

$$
\sigma_ {M} ^ {2} = \sigma_ {M B} ^ {2} + \sigma_ {M 1} ^ {2} \tag {A5.43}
$$

Hence, from Eqs. (A5.39) and (A5.34), we obtain

$$
\sigma_ {M} ^ {2} = \sigma_ {M B} ^ {2} + \sigma_ {M 1} ^ {2} = 4 \overline {{M}} ^ {2} \frac {\sigma_ {u} ^ {2}}{\overline {{U}} ^ {2}} \left[ K _ {S M B} + \frac {\pi^ {2}}{2 \delta} R _ {u} (n _ {1}). K _ {S x} (n _ {1}). \lambda_ {M 1} ^ {2} \right] \tag {A5.44}
$$

Thus,

$$
M _ {\max} = \overline {{M}} + g. \sigma_ {M} = \overline {{M}} \left(1 + 2 g \frac {\sigma_ {u}}{\overline {{U}}} \sqrt {K _ {S M B} + \frac {\pi^ {2}}{2 \delta} R _ {u} (n _ {1}) . K _ {S x} (n _ {1}) . \lambda_ {M 1} ^ {2}}\right) \tag {A5.45}
$$

The mean zero up-crossing frequency of the root moment suctuations, 휈, is derned as

$$
\nu = \sqrt {\frac {\int_ {0} ^ {\infty} n ^ {2} S _ {M} (n) d n}{\int_ {0} ^ {\infty} S _ {M} (n) d n}} \tag {A5.46}
$$

where $S _ { \mathrm { M } } ( n )$ is the power spectrum of the root moment suctuations. If we separate the power spectrum of the background response from the rrst mode resonant response at frequency $n _ { 1 }$ , then the above expression can be written

$$
\nu = \sqrt {\frac {\left(\int_ {0} ^ {\infty} n ^ {2} S _ {M B} (n) d n\right) + n _ {1} ^ {2} \sigma_ {M 1} ^ {2}}{\sigma_ {M B} ^ {2} + \sigma_ {M 1} ^ {2}}} \tag {A5.47}
$$

Now

$$
S _ {M B} (n) = (C _ {f} \rho \overline {{U}}) ^ {2}. S _ {u} (n). \int_ {0} ^ {R} \int_ {0} ^ {R} \psi_ {u u} ^ {N} (r, r ^ {\prime}, n). c (r). c (r ^ {\prime}). r. r ^ {\prime}. d r. d r ^ {\prime} \tag {A5.48}
$$

and

$$
\overline {{M}} = C _ {f}. \frac {1}{2} \rho \overline {{U}} ^ {2}. \int_ {0} ^ {R} c (r). r. d r \tag {A5.49}
$$

giving

$$
C _ {f} \rho \overline {{U}} = 2 \frac {\overline {{M}}}{\overline {{U}}} \frac {1}{\int_ {0} ^ {R} c (r) r d r}
$$

so

$$
S _ {M B} (n) = 4 \frac {\overline {{{M}}} ^ {2}}{\overline {{{U}}} ^ {2}} \frac {. S _ {u} (n) . \int_ {0} ^ {R} \int_ {0} ^ {R} \psi_ {u u} ^ {N} (r , r ^ {\prime} , n) . c (r) . c (r ^ {\prime}) . r . r ^ {\prime} . d r . d r ^ {\prime}}{\left(\int_ {0} ^ {R} c (r) . r . d r\right) ^ {2}} \tag {A5.50}
$$

Derning

$$
K _ {S M B} (n) = \frac {\int_ {0} ^ {R} \int_ {0} ^ {R} \psi_ {u u} ^ {N} (r , r ^ {\prime} , n) . c (r) . c (r ^ {\prime}) . r . r ^ {\prime} . d r . d r ^ {\prime}}{\left(\int_ {0} ^ {R} c (r) . r . d r\right) ^ {2}} \tag {A5.51}
$$

we obtain

$$
S _ {M B} (n) = 4 \frac {\overline {{{M}}} ^ {2}}{\overline {{{U}}} ^ {2}}. S _ {u} (n). K _ {S M B} (n) \tag {A5.52}
$$

Substituting into Eq. (A5.47) gives

$$
\nu = \sqrt {\frac {4 \frac {\overline {{M}} ^ {2}}{\overline {{U}} ^ {2}} \left(\int_ {0} ^ {\infty} n ^ {2} S _ {u} (n) . K _ {S M B} (n) . d n\right) + n _ {1} ^ {2} \sigma_ {M 1} ^ {2}}{\sigma_ {M B} ^ {2} + \sigma_ {M 1} ^ {2}}} \tag {A5.53}
$$

Noting from Eq. (A5.52) that $\sigma _ { M B } ^ { 2 } = 4 \frac { \overline { { { M } } } ^ { 2 } } { \overline { { { U } } } ^ { 2 } } \int _ { 0 } ^ { \infty } S _ { u } ( n ) K _ { S M B } ( n ) d n$ , the expression for 휈 becomes

$$
\nu = \sqrt {\frac {n _ {0} ^ {2} \sigma_ {M B} ^ {2} + n _ {1} ^ {2} \sigma_ {M 1} ^ {2}}{\sigma_ {M B} ^ {2} + \sigma_ {M 1} ^ {2}}} \tag {A5.54}
$$

where

$$
n _ {0} ^ {2} = \frac {\int_ {0} ^ {\infty} n ^ {2} S _ {u} (n) . K _ {S M B} (n) . d n}{\int_ {0} ^ {\infty} S _ {u} (n) . K _ {S M B} (n) . d n} \tag {A5.55}
$$

Substituting $\psi _ { u u } ^ { N } ( r , r ^ { \prime } , n ) = \exp [ - C ( r - r ^ { \prime } ) n / \overline { { U } } ]$ into the expression for $K _ { \mathrm { S M B } } ( n )$ in the numerator of Eq. (A5.55) gives

$$
\int_ {0} ^ {\infty} n ^ {2} S _ {u} (n). K _ {S M B} (n). d n = \int_ {0} ^ {\infty} n ^ {2} S _ {u} (n). \frac {\int_ {0} ^ {R} \int_ {0} ^ {R} \exp [ - C (r - r ^ {\prime}) n / \overline {{{U}}} ] . c (r) . c (r ^ {\prime}) . r . r ^ {\prime} . d r . d r ^ {\prime}}{\left(\int_ {0} ^ {R} c (r) . r . d r\right) ^ {2}}. d n \tag {A5.56}
$$

For high frequencies, the double integral is, in the limit, inversely proportional to frequency, so the integrand $n ^ { 2 } S _ { u } ( n ) . K _ { S M B } ( n )$ is proportional to $n ^ { 2 } n ^ { - \frac { 5 } { 3 } } n ^ { - 1 } = n ^ { - \frac { 2 } { 3 } }$ and th e integral does not converge. Consequently, it is necessary to take account of the chordwise lack of correlation of wind suctuation at high frequencies, and if this is done, it is found that, in the limit, the integrand is proportional to $n ^ { - \frac { 5 } { 3 } }$ for which the integral is rnite. The evaluation of the integral $\begin{array} { r } { \int _ { 0 } ^ { \infty } \hat { n } ^ { 2 } \hat { S _ { u } } ( n ) . K _ { S M B } ( n ) } \end{array}$ .dn taking chordwise lack of correlation into account is a formidable task, so the use of an approximate formula for the frequency, $n _ { 0 } .$ , is preferable, especially as the insuence of $n _ { 0 }$ on the peak factor, $^ { g , }$ is slight. Dyrbye and Hansen (1997) give an approximate formula for a uniform cantilever as follows:

$$
n _ {0} = 0. 3 \frac {\overline {{U}}}{\sqrt {L _ {u} ^ {x} \sqrt {R c}}} \tag {A5.57}
$$

Here R is the blade tip radius and c is the blade chord, assumed constant. For a tapering chord, the mean chord, ${ \overline { { c } } } ,$ can be substituted.

# A5.8 Bending moments at intermediate blade positions

# A5.8.1 Background response

Denoting the standard deviation of the quasi-static or background bending moment suctuations at radius $r ^ { * }$ as $\sigma _ { \mathrm { M B } } ( r ^ { * } )$ , it is apparent that

$$
\frac {\sigma_ {M B} (r ^ {*})}{\sigma_ {M B} (0)} = \sqrt {\frac {K _ {S M B} (r ^ {*})}{K _ {S M B} (0)}} \frac {\int_ {r ^ {*}} ^ {R} c (r) [ r - r ^ {*} ] d r}{\int_ {0} ^ {R} c (r) r d r} \tag {A5.58}
$$

The ratio of the steady moment at radius $r ^ { * }$ to that at the root is $\frac { \int _ { r ^ { * } } ^ { R } c ( r ) [ r - r ^ { * } ] d r } { \int _ { 0 } ^ { R } c ( r ) r d r }$ , so the 0ratio of the standard deviation of the quasi-static suctuations at radius $r ^ { * }$ to the steady value there is

$$
\frac {\sigma_ {M B} (r ^ {*})}{\overline {{M}} (r ^ {*})} = \frac {\sigma_ {M B} (r ^ {*})}{\sigma_ {M B} (0)} \frac {\sigma_ {M B} (0)}{\overline {{M}} (0)} \frac {\overline {{M}} (0)}{\overline {{M}} (r ^ {*})} = \frac {\sigma_ {M B} (0)}{\overline {{M}} (0)} \sqrt {\frac {K _ {S M B} (r ^ {*})}{K _ {S M B} (0)}} \tag {A5.59}
$$

Generally, the square root will be close to unity, so $\frac { \sigma _ { M B } ( r ^ { * } ) } { \overline { { M } } ( r ^ { * } ) }$ will be nearly constant.

# A5.8.2 Resonant response

In Section A5.5, it was shown that the standard deviation of the rrst mode resonant root bending moment is equal to $\begin{array} { r } { \omega _ { 1 } ^ { 2 } \sigma _ { x 1 } \int _ { 0 } ^ { R } m ( r ) \mu _ { 1 } ( r ) r \ d r } \end{array}$ dr (Eq. A5.27). The corresponding quantity at other radii can be derived similarly, giving

$$
\sigma_ {M 1} (r ^ {*}) = \omega_ {1} ^ {2} \sigma_ {x 1} \int_ {r ^ {*}} ^ {R} m (r) \mu_ {1} (r) [ r - r ^ {*} ] d r \tag {A5.60}
$$

Hence, the ratio of the standard deviation of the rrst mode resonant root bending moment at radius $r ^ { * }$ to the steady value there is

$$
\frac {\sigma_ {M 1} (r ^ {*})}{\overline {{M}} (r ^ {*})} = \frac {\sigma_ {M 1} (r ^ {*})}{\sigma_ {M 1} (0)} \frac {\sigma_ {M 1} (0)}{\overline {{M}} (0)} \frac {\overline {{M}} (0)}{\overline {{M}} (r ^ {*})} = \frac {\int_ {r ^ {*}} ^ {R} m (r) \mu_ {1} (r) [ r - r ^ {*} ] d r}{\int_ {0} ^ {R} m (r) \mu_ {1} (r) r d r} \frac {\int_ {0} ^ {R} c (r) r d r}{\int_ {r ^ {*}} ^ {R} c (r) [ r - r ^ {*} ] d r} \frac {\sigma_ {M 1} (0)}{\overline {{M}} (0)} \tag {A5.61}
$$

# References

Cramer, H.E. (1958). Use of power spectra and scales of turbulence in estimating wind loads. Proceedings of the Second National Conference on Applied Meteorology, Ann Arbor, Michigan, USA.   
Davenport, A.G. (1962). The response of slender, line-like structures to a gusty wind. Proc. Inst. Civ. Eng. 23: 389–408.   
Davenport, A.G. (1964). Note on the distribution of the largest value of a random function with application to gust loading. Proc. Inst. Civil Eng. 28: 187–196.   
Dyrbye, C. and Hansen, S.O. (1997). Wind Loads on Structures. Wiley.   
EN 1991-1-4:2005 (2005). Eurocode 1: Actions on structures – Part 1-4: General actions – Wind actions. Brussels: European Committee for Standardization.   
Harris, R.I. (1971). The nature of the wind. Proceedings of the CIRIA Conference, pp 29–55.   
Krenk, S. (1995). Wind reld coherence and dynamic wind forces. Proceedings of the Symposium on the Advances in Non-linear Stochastic Mechanics.   
Mann, J. (1994). The spatial structure of neutral atmospheric surface-layer turbulence. J. Ind. Aerodyn. 1: 167–175.   
Newland, D.E. (1984). Random Vibration and Spectral Analysis. UK: Longman.   
Wyatt, T.A. (1980). The dynamic behaviour of structures subject to gust loading. Proceedings of the CIRIA Conference Wind Engineering in the Eighties, pp. 6-1–6-22.