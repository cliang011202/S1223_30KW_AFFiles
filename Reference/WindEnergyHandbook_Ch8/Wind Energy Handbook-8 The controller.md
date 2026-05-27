# The controller

In the most general sense, the wind turbine control system consists of a number of sensors, a number of actuators, and a system consisting of hardware and software that processes the input signals from the sensors and generates output signals for the actuators.

The sensors might include, for example,

• An anemometer.   
• A wind vane.   
• At least one rotor speed sensor.   
• An electrical power sensor.   
• Accelerometers.   
• Load sensors.   
• A pitch position sensor.   
• Various limit switches.   
• Vibration sensors.   
• Temperature and oil level indicators.   
• Hydraulic pressure sensors.   
• Operator switches, push buttons, etc.

The actuators might include hydraulic or electric pitch actuators, the electrical generator, which can be considered to be a torque actuator, generator contactors, switches for activating shaft brakes, yaw motors, etc.

The system that processes the inputs to generate outputs usually consists of a computer or microprocessor based controller that carries out the normal control functions needed to operate the turbine, supplemented by a highly reliable hard-wired safety system. The safety system must be capable of overriding the normal controller to bring the turbine to a safe state if a serious problem occurs.

# 8.1 Functions of the wind turbine controller

# 8.1.1 Supervisory control

Supervisory control can be considered as the means whereby the turbine is brought from one operational state to another. The operational states might, for example, include the following:

• Standby, when the turbine is available to run if external conditions permit.   
• Start-up.   
• Power production.   
• Shut-down.   
• Stopped with fault.

It is possible to envisage other states, or it may be useful to further subdivide some of these states. As well as deciding when to initiate a switch from one state to another, the supervisory controller will carry out the sequence control required. As an example, the start-up control for a pitch-regulated wind turbine might consist of a sequence of steps such as the following:

• Power up the pitch actuators and other subsystems.   
• Release the shaft brake.   
• Ramp the pitch position demand at a rxed rate to some starting pitch.   
• Wait until the rotor speed exceeds a certain small value.   
• Engage the closed-loop pitch control of speed.   
• Ramp the speed demand up to the generator minimum speed.   
• Wait until the speed has been close to the target speed for a specired time.   
• Close the generator contactors.   
• Engage power or torque controller.   
• Ramp the power/torque/speed set-points up to the rated level.

The supervisory controller must check that each stage is successfully completed before moving on to the next. If any stage is not completed within a certain time, or if any faults are detected, the supervisory controller should change to shut-down mode.

# 8.1.2 Closed-loop control

The closed-loop controller is usually a software based system that automatically adjusts the operational state of the turbine to keep it on some pre-derned operating curve or characteristic. Some examples of such control loops are

Control of blade pitch to regulate the power output or rotational speed of the turbine to a rxed or slowly varying set-point (for example, the rated level in above rated wind speeds, or a predetermined speed ramp during start-up or shut-down of the turbine).   
• Control of generator torque to regulate the rotational speed of a variable-speed turbine.   
• Control of yaw motors to minimise the yaw tracking error.

Some of these control loops may require very fast response to prevent the turbine wandering far from its correct operating curve. Such controllers may need to be designed very carefully if good performance is to be achieved without detrimental effects on other aspects of the turbine’s operation. Others, such as yaw control, are typically rather slow acting, and careful design is then much less critical.

This chapter examines the main issues behind closed-loop controller design and presents some of the techniques that can be used to effect a successful design.

# 8.1.3 The safety system

It is helpful to consider the safety system as quite distinct from the main or ‘normal’ control system of the turbine. Its function is to bring the turbine to a safe condition in the event of a serious or potentially serious problem. This usually means bringing the turbine to rest or to a slow idling speed with the blades feathered and the generator switched off.

The normal wind turbine supervisory controller should be capable of starting and stopping the turbine safely in all foreseeable ‘normal’ conditions, including extreme winds, loss of the electrical network, and most fault conditions that are detected by the controller. The safety system acts as a backup to the main control system, and takes over if the main system appears to be failing to do this. It may also be activated by an operator-controlled emergency stop button.

Thus, the safety system must be independent from the main control system as far as possible, and must be designed to be fail-safe and highly reliable. Rather than utilising any form of computer or microprocessor based logic, the safety system would normally consist of a hard-wired fail-safe circuit linking a number of normally open relay contacts that are held closed when all is healthy. Then if any one of those contacts is lost, the safety system trips, causing the appropriate fail-safe actions to operate. This might include disconnecting all electrical systems from the supply and allowing fail-safe pitching to the feather position, for example.

![](images/4933609b0faf064e4eac09acb2649f8941b5bdded86c063ececfbba3ac1f9391.jpg)

<details>
<summary>natural_image</summary>

Interior view of an industrial machine with visible gears and wiring (no text or symbols)
</details>

Figure 8.1 Low-speed shaft sensing system. Three proximity sensors mounted on a bracket attached to the front of the (integrated) gearbox register the passage of the teeth on the shaft circumference and provide an independent speed signal for the control and safety systems. The sange onto which the hub is bolted is immediately to the left of the teeth

The safety system might, for example, be tripped by any one of the following:

• Rotor overspeed, that is, reaching the hardware overspeed limit. This is set higher than the software overspeed limit, which would cause the normal supervisory controller to initiate a shut-down. Figure 8.1 shows a typical arrangement of rotor speed sensing equipment on the low-speed shaft.   
• Vibration sensor trip, which might indicate that a major structural failure has occurred.   
• Controller watchdog timer expired: the controller should have a watchdog timer that it resets every controller timestep. If it is not reset within this time, this indicates that the controller is faulty and the safety system should shut down the turbine.

• Emergency stop button pressed by an operator.   
• Other faults indicating that the main controller might not be able to control the turbine.

In some cases, the safety system may involve more than one circuit. For example, any safety system trip would normally cause the blades to pitch, but it may be feasible for the relay that disconnects the generator system to be on a different circuit that omits certain sensors, so that in the event of certain faults unrelated to the electrical system the braking action of the generator can be maintained to assist the shut-down.

# 8.2 Closed-loop control: issues and objectives

# 8.2.1 Pitch control

Pitch control (see also Sections 3.14 and 6.7.2) is the most common means of controlling the aerodynamic power generated by the turbine rotor. Pitch control also has a major effect on all of the aerodynamic loads generated by the rotor.

Below rated wind speed, the turbine should simply be trying to produce as much power as possible, so there is generally no need to vary the pitch angle because the optimum pitch angle does not change much with wind speed. The aerodynamic loads below rated wind speed are generally lower than above rated, so again there is no need to modulate these using pitch control, although some pitch action to reduce fatigue loads is possible as explained below. However, for turbines operating below rated at constant speed, the optimum pitch angle for aerodynamic efrciency varies slightly with tip speed ratio, and therefore with wind speed. In this case the pitch angle can be varied slowly (by no more than a few degrees) to maintain optimum power production as the mean wind speed changes. This applies also to variable-speed turbines when operating on a constant-speed portion of the operating curve. However, if minimisation of thrust-related loads is important, small gains in energy capture may be traded off and the pitch increased slightly instead to reduce thrust in the region of rated wind speed where the mean thrust is at its highest – so-called ‘thrust clipping’.

Above rated wind speed, pitch control provides a very effective means of regulating the aerodynamic power and loads produced by the rotor so that design limits are not exceeded. To achieve good regulation, however, the pitch control needs to respond very rapidly to changing conditions. This highly active control action needs very careful design as it interacts strongly with the turbine dynamics.

One of the strongest interactions is with the tower dynamics. As the blades pitch to regulate the aerodynamic torque, the aerodynamic thrust on the rotor also changes substantially, and this feeds into the tower vibration. As the wind increases above rated, the pitch angle increases to maintain constant torque, but the rotor thrust decreases. This allows the downwind tower desection to decrease, and as the tower top moves upwind the relative wind speed seen by the rotor increases. The aerodynamic torque increases further, causing more pitch action. Clearly if the pitch controller gain is too high this positive feedback can result in instability. It is therefore vital to take the tower dynamics into account when designing a pitch controller.

Below rated wind speed, the pitch setting should be at its optimum value to give maximum power. It follows that when the wind speed rises above rated, either an increase or a decrease in pitch angle will result in a reduction in torque. An increase in pitch angle, derned as turning the leading edge into wind, reduces the torque by decreasing the angle of attack and hence the lift. This is known as pitching towards feather. A decrease in pitch, that is, turning the leading edge downwind, reduces the torque by increasing the angle of attack towards stall, where the lift starts to decrease and the drag increases. This is known as pitching towards stall.

Although pitching towards feather is the more common strategy, some turbines pitch towards stall. This is commonly known as active stall or assisted stall (see Section 6.7.4). Pitching to feather requires much more dynamic pitch activity than pitching to stall: once a large part of the blade is in stall, very small pitch movements sufrce to control the torque. Pitching to stall results in signircantly greater thrust loads because of the increased drag. However, the thrust is much more constant once the blade is stalled, so thrust-driven fatigue loads may well be smaller.

A further problem with pitching to stall is that the lift curve slope at the start of the stalled region is negative, i.e. the lift coefrcient decreases with increasing angle of attack. This results in negative aerodynamic damping, which can result in instability of the blade bending modes, both in-plane and out-of-plane. This can be a problem also with rxed pitch stall-regulated turbines.

Most pitch-controlled turbines use full-span pitch control, in which the pitch bearing is close to the hub. It is also possible, though not common, to achieve aerodynamic control by pitching only the blade tips, or by using ailerons, saps, air-jets or other devices to modify the aerodynamic properties. These strategies will result in most of the blade being stalled in high winds. If only the blade tips are pitched, it may be difrcult to rt a suitable actuator into the outboard portion of the blade, and accessibility for maintenance is problematic.

# 8.2.2 Stall control

Many smaller and older turbines are stall-regulated, which means that the blades are designed to stall in high winds without any pitch action being required. This means that pitch actuators are not required, although some means of aerodynamic braking is likely to be required, if only for emergencies (see Section 6.8.2).

To achieve stall regulation at reasonable wind speeds, the turbine must operate closer to stall than its pitch-regulated counterpart, resulting in lower aerodynamic efrciency below rated. This disadvantage may be mitigated in a variable-speed turbine, when the rotor speed can be varied below rated to maintain peak power coefrcient.

In order for the turbine to stall rather than accelerate in high winds, the rotor speed must be restrained. In a rxed-speed turbine the rotor speed is restrained by the generator, which is governed by the network frequency, as long as the torque remains below the pull-out torque. In a variable-speed turbine, the speed is maintained by ensuring that the generator torque is varied to match the aerodynamic torque. A variable-speed turbine offers the possibility to slow the rotor down in high winds to bring it into stall. This means that the turbine can operate further from the stall point in low winds, resulting in higher aerodynamic efrciency. However, this strategy means that when a gust hits the turbine, the load torque not only has to rise to match the wind torque but also has to increase further to slow the rotor down into stall. This removes one of the main advantages of variable-speed operation, namely that it allows very smooth control of torque and power above rated.

The benerts of pitch control as a means of braking mean that stall control is now rarely used for large commercial turbines.

# 8.2.3 Generator torque control

The torque developed by a rxed-speed (i.e. directly connected) induction generator is determined purely by the slip speed (see also Sections 6.9 and 7.5). As the aerodynamic torque varies, the rotor speed varies by a very small amount such that the generator torque changes to match the aerodynamic torque. The generator torque cannot therefore be actively controlled.

However, if a frequency converter is interposed between the generator and the network, the generator speed will be able to vary. The frequency converter can be actively controlled to maintain constant generator torque or power output above rated wind speed. Below rated, the torque can be controlled to any desired value – for example, with the aim of varying the rotor speed to maintain maximum aerodynamic efrciency.

There are two principal means of achieving variable-speed operation. One is to connect the generator stator to the network through a frequency converter, which must then be rated for the full power output of the turbine. An alternative arrangement is the doubly fed induction generator, a wound-rotor machine in which the stator is connected directly to the network and the rotor is connected to the network through slip rings and a frequency converter. This means that the frequency converter need only be rated to handle a fraction of the total power, although the larger this fraction, the larger the achievable speed range will be. This arrangement has been very widely used in recent years, but the fully rated converter is more advantageous from the network point of view, and is becoming the favoured option as wind penetration increases.

A special case is the variable-slip induction generator, where active control of a resistance in series with the rotor windings allows the torque/speed relationship to be modired. By means of closed-loop control based on measured currents, it is possible to maintain constant torque above rated, effectively allowing variable-speed operation in this region. Below rated it behaves just like a normal induction generator (Bossanyi and Gamble 1991; Pedersen 1995).

# 8.2.4 Yaw control

Turbines, whether upwind or downwind, can be designed to be stable in yaw (Section 3.10), in the sense that if the nacelle is free to yaw, the turbine will naturally remain pointing into the wind. However, it may not point exactly into wind, in which case some active control of the nacelle angle may be needed to maximise the energy capture. Because a yaw drive is usually required anyway – for example, for start-up and for unwinding the pendant cable – it may as well be used for active yaw tracking. Free yaw has the advantage that it does not generate any yaw moments at the yaw bearing. However, it is usually necessary to have at least some yaw damping, in which case there will be a yaw moment at the bearing.

In practice, almost all turbines now use active yaw control. A yaw error signal from the nacelle-mounted wind vane is then used to calculate a demand signal for the yaw actuator. Frequently the demand signal will simply be a command to yaw at a slow rxed rate in one or the other direction. The yaw vane signal must be heavily averaged, especially for upwind turbines where the vane is behind the rotor. Because of the slow response of the yaw control system, a simple dead-band controller is often sufrcient. The yaw motor is switched on when the averaged yaw error exceeds a certain value, and switched off again after a certain time or when the nacelle has moved through a certain angle. A yaw brake is usually applied when the turbine is not yawing, and often even while yawing to prevent frequent load reversals at the yaw pinion due to the highly variable nature of the yawing moments.

More complex control algorithms are sometimes used, but the control is always slow-acting, and does not demand any special closed-loop design analysis; in fact rapid yawing is unnecessary, and can generate large gyroscopic loads. Because of this, yaw control is often classed as part of the supervisory controller; also because it remains active in standby mode to keep the turbine pointing into wind (except in very low winds when the wind direction becomes too variable).

Active yaw control can be used to regulate aerodynamic power in high winds, as on the experimental variable-speed Gamma 60 turbine referred to in Section 6.7.5. This clearly requires very rapid yaw rates, and results in large yaw loads and gyroscopic and asymmetric aerodynamic loads on the rotor. This method of power regulation would be too slow for a rxed-speed turbine, and even on the Gamma 60 the speed excursions during above rated operation were quite large. This approach has not found commercial application.

Instead of a yaw actuator, it is possible to use individual pitch control to generate a yawing moment – see Section 8.3.14.

A typical yaw control algorithm might be conrgured as follows: when a heavily low-pass-rltered yaw error signal from the nacelle wind vane becomes greater than a given threshold, the turbine yaws at a rxed rated (typically below 1∘ /s) to bring the averaged yaw error back to 0∘ . Yaw algorithm parameters, such as rlter time constants and yaw error thresholds, are often rxed by experience based on trial and error, so that yaw misalignments are kept small and yawing manoeuvres do not occur more frequently than, say, every few minutes. Optimum settings – for example, to achieve a suitable trade-off between the frequency of yawing operations and loss of energy production due to yaw misalignment – are difrcult to derne theoretically as they depend on the low-frequency variability of wind direction, which can be very site-specirc. Long-term simulation modelling based on site wind data can be used for this (Bossanyi et al. 2013). In a wind farm, sharing of information about wind direction between adjacent turbines can also be helpful (Bossanyi 2019).

# 8.2.5 InKuence of the controller on loads

As well as regulating the turbine power in high winds and optimising it in low winds, it is clear that the action of the control system can have a major impact on the loads experienced by the turbine. The design of the controller must take into account the effect on loads, and at least ensure that excessive loads will not result from the control action. It is possible to go further than this, and explicitly design the controller with the reduction of certain loads as an additional objective.

The reduction of certain loads is clearly compatible with the primary objective of limiting power in high winds. For example, the limitation of power output is clearly compatible with limitation of gearbox torque. In other cases however, there may be a consict, in which case the controller design is bound to be a compromise involving a trade-off between competing goals. For example, there is a clear trade-off between good control of power output and pitch actuator loads. The more actuator activity can be tolerated, the better the power control can be. Of course it is always possible to reduce loads by reducing energy capture (after all of the loads are minimised with the turbine switched off), but economic optimisation generally implies that reduced capital cost due to reduced loading is often only justired if it causes very little or no loss of energy production.

The interaction between pitch control and tower vibration referred to in Section 8.2.1 is another important example, because the amount of tower vibration has a major effect on tower base loads. The tighter the control of rotor speed by means of pitch control, the greater the tower vibration is likely to be. Blade, hub, and other structural loads will also be insuenced by pitch control activity. Generator torque control can have a major impact on gearbox loads, as described below.

# 8.2.6 DeJning controller objectives

The primary objective of the closed-loop controller can usually be stated fairly simply. For example, the primary objective of the pitch controller may be to limit power or rotor speed in high winds. There may be more than one ‘primary’ objective, as in the case where the pitch controller is also used to optimise energy capture in low winds.

However, because the controller can also have a major effect on structural loads and vibrations, it is vital to consider these when designing the control algorithm. Thus a fuller description of the pitch controller objectives might be

• To optimise power production in below rated wind speeds.   
• To regulate or limit aerodynamic torque in above rated wind speeds.   
• To minimise peaks in gearbox torque.   
• To avoid excessive pitch activity.   
• To minimise tower base loads as far as possible by controlling tower vibration.   
• To avoid exacerbating hub and blade root loads.

Especially with individual pitch control (Section 8.3.12), the last of these should be replaced by a much more positive objective:

• To actively reduce the loading on the rotor and the rest of the system.

Clearly some of these objectives may consict with others, so the control design process will inevitably involve some degree of trade-off or optimisation. To do this, it is necessary to be able to quantify the different objectives. It is usually almost impossible to do this with any precision, because the various loads may affect not only the costs of different components (sometimes in complex ways) but also their reliability. Even the trade-off between energy capture and component cost is not straightforward, as it will depend on the wind regime, the discount rate, and knowledge of future prices for the sale of electricity. Therefore, some degree of judgement will always be required in arriving at an acceptable controller design.

# 8.2.7 PI and PID controllers

A brief general description is given here of proportional and integral (PI) and proportional–integral–derivative (PID) controllers, because they will be referred to a number of times in the subsequent sections.

The PI controller is an algorithm that is very widely used for controlling all kinds of equipment and processes. The control action is calculated as the sum of two terms, one proportional to the control error, which is the difference between the desired and actual values of the quantity to be controlled, and one proportional to the integral of the control error. The integral term ensures that in the steady state the control error tends to zero, because if it did not, the control action would continue to increase indernitely. The proportional term makes the algorithm more responsive to rapid changes in the quantity being controlled.

A differential term is often added, which gives a contribution to the control action proportional to the rate of change of the control error. This is then known as a PID controller. In terms of the Laplace operator s, which can usefully be thought of as a differentiation operator, the PID controller from measured signal x to control signal y can be written as follows:

$$
y = \left(K _ {p} + \frac {K _ {i}}{s} + \frac {K _ {d} s}{1 + s T _ {d}}\right) x \tag {8.1}
$$

where $K _ { p } , K _ { i } ,$ , and $K _ { d }$ are the proportional, integral, and derivative gains, respectively. The denominator of the differential term is essentially a low-pass rlter, and is needed to ensure that the gain of the algorithm does not increase indernitely with frequency, which would make the algorithm very sensitive to signal noise. Setting $K _ { d } = 0$ results in a PI controller.

It is often the case that the control action is subject to limits. For example, if the control action represents the blade pitch used to control power above rated, then when the power drops below rated the pitch will be limited to the rne pitch setting and will not be allowed to drop further. In this situation the integral term of the PI or PID controller will grow more and more negative as the power remains below rated. Then when the wind speed rises again and the power rises above rated, the integral term will start to grow again towards zero, but until it gets close to zero it can dominate over the proportional and derivative terms. Therefore the pitch may remain ‘stuck’ at rne pitch for a considerable time, depending on how long the power has been below rated, until the integral term has come back close to zero. This is known as integrator wind-up, and clearly it must be prevented. This is done in effect by disabling the integrator when the pitch is on the limit. This is known as integrator desaturation, which is described more fully in Section 8.6.

The design of PI and PID controllers, including the choice of gains, is described in more detail in Section 8.4.

# 8.3 Closed-loop control: general techniques

This section outlines the principles behind many of the types of closed-loop controllers to be found in wind turbines. Mathematical methods for designing the closed-loop algorithms are covered in Section 8.4.

# 8.3.1 Control of Jxed-speed, pitch-regulated turbines

A rxed-speed pitch-regulated turbine usually means a turbine that has an induction generator connected directly to the ac network and that therefore rotates at a nearly constant speed. As the wind speed varies, the power produced will vary roughly as the cube of the wind speed. At rated wind speed, the electrical power generated becomes equal to the rating of the turbine, and the blades are then pitched to reduce the aerodynamic efrciency of the rotor and limit the power to the rated value. The usual strategy is to pitch the blades in response to the power error, derned as the difference between the rated power and the actual power being generated, as measured by a power transducer. The primary objective is then to devise a dynamic pitch control algorithm that minimises the power error, although as explained above, this may not be the only objective.

The main elements of the control loop are shown in Figure 8.2. A PI or PID algorithm is often used for the controller.

When the power falls below rated, the pitch demand saturates at the rne pitch limit, maximising the aerodynamic efrciency of the rotor. Because the optimum pitch angle depends on the tip speed ratio, it is possible to increase energy capture below rated by a small percentage if the rne pitch limit is varied in response to the wind speed. The measured power itself is the best available measure of wind speed over the whole turbine (effectively using the whole turbine as an anemometer). However, the rne pitch limit should be varied relatively slowly compared to the control loop dynamics. Good performance can be obtained by changing the rne pitch limit in response to a moving average of the measured power, using the calculated steady-state relationship between power output and optimum pitch angle at each wind speed. The moving average time constant can be quite long because the underlying wind speed (averaged over the rotor swept area) varies relatively slowly. Of course, it should be signircantly slower than the blade passing frequency and the lowest structural frequency (generally the rrst tower mode) to avoid unnecessary pitch activity below rated.

![](images/82979f9456ef7ed2c681b8acb314b000554eb3d795f575826462cf13a2db830a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Wind"] --> B["Turbine"]
    B -->|Electric power| C["Power transducer"]
    C -->|Measured power| D["Controller"]
    D --> E["Power set-point"]
    D --> F["Pitch actuator"]
    F -->|Pitch demand| F
    F -->|Blade pitch| B
```
</details>

Figure 8.2 Main control loop for a rxed-speed pitch-regulated turbine

# 8.3.2 Control of variable-speed, pitch-regulated turbines

A variable-speed generator is decoupled from the grid frequency by a power converter, which can control the load torque at the generator directly, so that the speed of the turbine rotor can be allowed to vary between certain limits. An often-quoted advantage of variable-speed operation is that below rated wind speed, the rotor speed can be adjusted in proportion to the wind speed so that the optimum tip speed ratio is maintained. At this tip speed ratio the power coefrcient, $C _ { p }$ , is a maximum, which means that the aerodynamic power captured by the rotor is maximised. This is often used to suggest that a variable-speed turbine can capture much more energy than a rxed-speed turbine of the same diameter. In practice it may not be possible to realise all of this gain, partly because of losses in the power converter and partly because it is not possible to track optimum $C _ { p }$ perfectly.

Maximum aerodynamic efrciency is achieved at the optimum tip speed ratio $\lambda = \lambda _ { \mathrm { o p t } } ,$ at which the power coefrcient $C _ { p }$ has its maximum value $C _ { p ( \mathrm { { m a x } ) } }$ . Because the rotor speed $\varOmega$ is then proportional to wind speed $U ,$ the power increases with $U ^ { 3 }$ and $\varOmega ^ { 3 }$ , and the torque with $\bar { U ^ { 2 } }$ and $\varOmega ^ { 2 }$ . The aerodynamic torque is given by

$$
Q _ {a} = \frac {1}{2} \rho A C _ {q} U ^ {2} R = \frac {1}{2} \rho \pi R ^ {3} \frac {C _ {p}}{\lambda} U ^ {2} \tag {8.2}
$$

Since $U = \varOmega R / \lambda$ we have

$$
Q _ {a} = \frac {1}{2} \rho \pi R ^ {5} \frac {C _ {p}}{\lambda^ {3}} \Omega^ {2} \tag {8.3}
$$

In the steady state therefore, the optimum tip speed ratio can be maintained by setting the load torque at the generator, $Q _ { g }$ , to balance the aerodynamic torque, that is,

$$
Q _ {g} = \frac {1}{2} \frac {\pi \rho R ^ {5} C _ {p}}{\lambda^ {3} G ^ {3}} \omega_ {g} ^ {2} - Q _ {L} \tag {8.4}
$$

Here $Q _ { L }$ represents the mechanical torque loss in the drive train (which may itself be a function of rotational speed and torque), referred to the high-speed shaft. The generator speed is $\omega _ { \mathrm { g } } = G \varOmega$ , where G is the gearbox ratio.

This torque-speed relationship is shown schematically in Figure 8.3 as the curve B1–C1. Although it represents the steady-state solution for optimum $C _ { p } ,$ , it can also be used dynamically to control generator torque demand as a function of measured generator speed. In many cases, this is a very benign and satisfactory way of controlling generator torque below rated wind speed.

For tracking peak $C _ { p }$ below rated in a variable-speed turbine, the quadratic algorithm of Eq. (8.4) works well and gives smooth, stable control. However, in turbulent winds, the large rotor inertia prevents it from changing speed fast enough to follow the wind, so rather than staying on the peak of the $C _ { p }$ curve it will constantly fall off either side, resulting in a lower mean $C _ { p }$ . This problem is clearly worse for heavy rotors, and also if the $C _ { p } - \lambda$ curve has a sharp peak. Thus, in optimising a blade design for variable-speed operation, it is not only important to try to maximise the peak $C _ { p } .$ , but also to ensure that the $C _ { p } - \lambda$ curve is reasonably sat-topped.

It is possible to manipulate the generator torque to cause the rotor speed to change faster when required, so staying closer to the peak of the $C _ { p }$ curve. One way to do this is to modify the torque demand by a term proportional to rotor acceleration (Bossanyi 1994):

![](images/b8a601b1b9b421172958ae29b5250bd1fbeafe759f5da613b7a92dca83c48673.jpg)

<details>
<summary>line</summary>

| Point | Generator speed (m/s) | Generator torque (m/s) |
|-------|------------------------|-------------------------|
| A     | ~0.5                   | ~0                      |
| B     | ~1.0                   | ~2                      |
| C     | ~1.5                   | ~4                      |
| D     | ~2.0                   | ~6                      |
| E     | ~2.5                   | ~8                      |
| F     | ~3.0                   | ~10                     |
| G     | ~3.5                   | ~12                     |
| H     | ~4.0                   | ~14                     |
| I     | ~4.5                   | ~16                     |
| J     | ~5.0                   | ~18                     |
| K     | ~5.5                   | ~14                     |
| L     | ~6.0                   | ~10                     |
| M     | ~6.5                   | ~8                      |
| N     | ~7.0                   | ~6                      |
| O     | ~7.5                   | ~4                      |
| P     | ~8.0                   | ~2                      |
| Q     | ~8.5                   | ~0                      |
| R     | ~9.0                   | ~0                      |
| S     | ~9.5                   | ~0                      |
| T     | ~10.0                  | ~0                      |
| U     | ~10.5                  | ~0                      |
| V     | ~11.0                  | ~0                      |
| W     | ~11.5                  | ~0                      |
| X     | ~12.0                  | ~0                      |
| Y     | ~12.5                  | ~0                      |
| Z     | ~13.0                  | ~0                      |
| AA    | ~13.5                  | ~0                      |
| AB    | ~14.0                  | ~0                      |
| AC    | ~14.5                  | ~0                      |
| AD    | ~15.0                  | ~0                      |
| AE    | ~15.5                  | ~0                      |
| AF    | ~16.0                  | ~0                      |
| AG    | ~16.5                  | ~0                      |
| AH    | ~17.0                  | ~0                      |
| AI    | ~17.5                  | ~0                      |
| AJ    | ~18.0                  | ~0                      |
| AK    | ~18.5                  | ~0                      |
| AL    | ~19.0                  | ~0                      |
| AM    | ~19.5                  | ~0                      |
| AN    | ~20.0                  | ~0                      |
| AO    | ~20.5                  | ~0                      |
| AP    | ~21.0                  | ~0                      |
| AQ    | ~21.5                  | ~0                      |
| AR    | ~22.0                  | ~0                      |
| AS    | ~22.5                  | ~0                      |
| AT    | ~23.0                  | ~0                      |
| AU    | ~23.5                  | ~0                      |
| AV    | ~24.0                  | ~0                      |
| AW    | ~24.5                  | ~0                      |
| AX    | ~25.0                  | ~0                      |
| AY    | ~25.5                  | ~0                      |
| AZ    | ~26.0                  | ~0                      |
| BA    | ~26.5                  | ~0                      |
| BB    | ~27.0                  | ~0                      |
| BC    | ~27.5                  | ~0                      |
| BD    | ~28.0                  | ~0                      |
| BE    | ~28.5                  | ~0                      |
| BF    | ~29.0                  | ~0                      |
| BG    | ~29.5                  | ~0                      |
| BH    | ~30.0                  | ~0                      |
| BI    | ~30.5                  | ~0                      |
| BJ    | ~31.0                  | ~0                      |
| BK    | ~31.5                  | ~0                      |
| BL    | ~32.0                  | ~0                      |
| BM    | ~32.5                  | ~0                      |
| BN    | ~33.0                  | ~0                      |
| BO    | ~33.5                  | ~0                      |
| BP    | ~34.0                  | ~0                      |
| BPB   | ~34.5                  | ~0                      |
| BPB+Q  | 4.5                    | 4                       |
| BPB+Q+Q  | 4.5                    | 6                       |
| BPB+Q+Q  | 4.5                    | 8                       |
| BPB+Q+Q  | 4.5                    | 10                      |
| BPB+Q+Q  | 4.5                    | 12                      |
| BPB+Q+Q  | 4.5                    | 14                      |
| BPB+Q+Q  | 4.5                    | 16                      |
| BPB+Q+Q  | 4.5                    | 18                      |
| BPB+Q+Q  | 4.5                    | 20                      |
| BPB+Q+Q  | 4.5                    | 22                      |
| BPB+Q+Q  | 4.5                    | 24                      |
| BPB+Q+Q  | 4.5                    | 26                      |
| BPB+Q+Q  | 4.5                    | 28                      |
| BPB+Q+Q  | 4.5                    | 30                      |
| BPB+Q+Q  | 4.5                    | 32                      |
| BPB+Q+Q  | 4.5                    | 34                      |
| BPB+Q+Q  | 4.5                    | 36                      |
| BPB+Q+Q  | 4.5                    | 38                      |
| BPB+Q+Q  | 4.5                    | 40                      |
| BPB+Q+Q  | 4.5                    | 42                      |
| BPB+Q+Q  | 4.5                    | 44                      |
| BPB+Q+Q  | 4.5                    | 46                      |
| BPB+Q+Q  | 4.5                    | 48                      |
| BPB+Q+Q  | 4.5                    | 50                      |
| BPB+Q+Q  | 4.5                    | 52                      |
| BPB+Q+Q  | 4.5                    | 54                      |
| BPB+Q+Q  | 4.5                    | 56                      |
| BPB+Q+Q  | 4.5                    | 58                      |
| BPB+Q+Q  | 4.5                    | 60                      |
| BPB+Q+Q  | 4.5                    | 62                      |
| BPB+Q+Q  | 4.5                    | 64                      |
| BPB+Q+Q  | 4.5                    | 66                      |
| BPB+Q+Q  | 4.5                    | 68                      |
| BPB+Q+Q  | 4.5                    | 70                      |
| BPB+Q+Q  | 4.5                    | 72                      |
| BPB+Q+Q  | 4.5                    | 74                      |
| BPB+Q+Q  | 4.5                    | 76                      |
| BPB+Q+Q  | 4.5                    | 78                      |
| BPB+Q+Q  | 4.5                    | 80                      |
| BPB+Q+Q  | 4.5                    | 82                      |
| BPB+Q+Q  | 4.5                    | 84                      |
| BPB+Q+Q  | 4.5                    | 86                      |
| BPB+Q+Q  | 4.5                    | 88                      |
| BPB+Q+Q  | 4.5                    | 90                      |
| BPB+Q+Q  | 4.5                    | 92                      |
| BPB+Q+Q  | 4.5                    | 94                      |
| BPB+Q+Q  | 4.5                    | 96                      |
| BPB+Q+Q  | 4.5                    | 98                      |
| BPB+Q+Q  | 4.5                    | >10                     |
The chart is a schematic representation of the generator torque versus generator speed.
</details>

Figure 8.3 Schematic torque-speed curve for a variable-speed pitch-regulated turbine

$$
Q _ {g} = \frac {1}{2} \frac {\pi \rho R ^ {5} C _ {p}}{\lambda^ {3} G ^ {3}} \omega_ {g} ^ {2} - Q _ {L} - B \dot {\omega} _ {g} \tag {8.5}
$$

where B is a gain that determines the amount of inertia compensation. For a stiff drive train, and ignoring frequency converter dynamics, the torque balance gives

$$
I \dot {\Omega} = Q _ {a} - G Q _ {g} \tag {8.6}
$$

where I is the total inertia (of rotor, drive train and generator, referred to the low-speed shaft) and $\varOmega$ is the rotational speed of the rotor. Hence

$$
(I - G ^ {2} B) \dot {\Omega} = Q _ {a} - \frac {1}{2} \frac {\pi \rho R ^ {5} C _ {p}}{\lambda^ {3} G ^ {2}} \omega_ {g} ^ {2} + G Q _ {L} \tag {8.7}
$$

Thus, the effective inertia is reduced from I to $I - G ^ { 2 } B ,$ , allowing the rotor speed to respond more rapidly to changes in wind speed. The gain B should remain signircantly smaller than $I / \bar { G ^ { 2 } }$ otherwise the effective inertia will approach zero, requiring huge power swings to force the rotor speed to track closely the changes in wind speed.

Another possible method is to use available measurements to make an estimate of the wind speed, calculate the rotor speed required for optimum $C _ { p } ,$ , and then use the generator torque to achieve that speed as rapidly as possible. The aerodynamic torque can be expressed as

$$
Q _ {a} = \frac {1}{2} \rho A C _ {q} R U ^ {2} = \frac {1}{2} \rho \pi R ^ {5} \Omega^ {2} C _ {q} / \lambda^ {2} \tag {8.8}
$$

where R is the turbine radius, 훺 the rotational speed, and $C _ { q }$ the torque coefrcient. If drive train torsional sexibility is ignored, a simple estimator for the aerodynamic torque is

$$
Q _ {a} ^ {*} = G Q _ {g} + I \dot {\Omega} = G Q _ {g} + I \dot {\omega} _ {g} / G \tag {8.9}
$$

where I is the total inertia. A more sophisticated estimator could take into account drive train torsion, etc. From this it is possible to estimate the value of the function $F ( \lambda ) = C _ { q } ( \lambda ) / \lambda ^ { 2 }$ as

$$
F ^ {*} (\lambda) = \frac {Q _ {a} ^ {*}}{\frac {1}{2} \rho \pi R ^ {5} \left(\omega_ {g} / G\right) ^ {2}} \tag {8.10}
$$

Knowing the function F(휆) from steady state aerodynamic analysis, one can then deduce the current estimated tip speed ratio $\lambda ^ { * }$ (see also Section 8.3.16 for a better estimation method). The desired generator speed for optimum tip speed ratio can then be calculated as

$$
\omega_ {d} = \omega_ {g} \widehat {\lambda} / \lambda^ {*} \tag {8.11}
$$

where $\widehat { \lambda }$ is the optimum tip speed ratio to be tracked. A simple PI controller can then be used, acting on the speed error $\omega _ { \mathrm { g } } - \omega _ { \mathrm { d } }$ , to calculate a generator torque demand that will track $\omega _ { \mathrm { d } }$ . The higher the gain of PI controller, the better will be the $C _ { p }$ tracking, but at the expense of larger power variations. Simulations for a particular turbine showed that a below rated energy gain of almost 1% could be achieved, with large but not unacceptable power variations.

Holley et al. (1999) demonstrated similar results with a more sophisticated scheme, and also showed that a perfect $C _ { p }$ tracker could capture 3% more energy below rated, but only by demanding huge power swings of plus and minus three to four times rated power, which is totally unacceptable.

Because such large torque variations are required to achieve only a modest increase in power output, it is usual to use the simple quadratic law, possibly augmented by some inertia compensation as in Eq. (8.5) if the rotor inertia is large enough to justify it.

As turbine diameters increase in relation to the lateral and vertical length scales of turbulence, it becomes more difrcult to achieve peak $C _ { p }$ anyway because of the non-uniformity of the wind speed over the rotor swept area. Thus if one part of a blade is at its optimum angle of attack at some instant, other parts will not be.

In most cases, it is actually not practical to maintain peak $C _ { p }$ from cut-in all of the way to rated wind speed. Although some variable-speed systems can operate all of the way down to zero rotational speed, this is not the case with limited range variable-speed systems based on the widely used doubly fed induction generators. These systems only need a power converter rated to handle a fraction of the turbine power, which is a major cost saving. This means that in low wind speeds, just above cut-in, it may be necessary to operate at an essentially constant rotational speed, with the tip speed ratio above the optimum value.

At the other end of the range, it is usual to limit the rotational speed to some level, usually determined by aerodynamic noise constraints or blade leading-edge erosion, which is reached at a wind speed that is still some way below rated. It is then cost-effective to increase to torque demand further, at essentially constant rotational speed, until rated power is reached. Figure 8.3 illustrates some typical torque-speed trajectories, which are explained in more detail below. Turbines designed for noise-insensitive sites may be designed to operate along the optimum $C _ { p }$ trajectory all of the way until rated power is reached. The higher rotational speed implies lower torque and in-plane loads, but higher out-of-plane loads, for the same rated power. This strategy might be of interest for offshore wind turbines.

# 8.3.3 Pitch control for variable-speed turbines

Once the rated torque has been reached, no further increase in load torque can occur, so the turbine will start to speed up. Pitch control is then used to regulate the rotor speed, with the load torque held constant. A PI or PID controller is often satisfactory for this application. In some situations, it may be useful to include notch rlters on the speed error to prevent excessive pitch action at, for example, the blade passing frequency or signircant structural resonant frequencies, such as the drive train torsional frequency.

Rather than maintain a constant torque demand while the pitch control is regulating the rotational speed, it is possible to vary the torque demand in inverse proportion to the measured speed to keep the power output, rather than the torque, at a constant level. Provided the pitch controller is able to maintain the speed close to the set-point, there will be little difference between these two approaches. The reduction of load torque with increasing speed has a slight destabilising effect on the pitch controller, but this is often not serious, and provided the gearbox torque and rotor speed variations are not greatly affected, the constant power approach is attractive from the perspective of power quality.

# 8.3.4 Switching between torque and pitch control

In practice, acoustic noise, loads or other design constraints usually mean that the maximum allowable rotor speed is reached at a relatively low wind speed. As the wind speed increases further, it is desirable to increase the torque and power without any further speed increase, to capture more energy from the wind. The simplest strategy is to implement a torque-speed ramp: line CD in Figure 8.3. Once rated power or torque is reached, pitch control is used to maintain the rotor speed at its rated value. To prevent the torque and pitch controllers from interfering with one another, the speed set-point for the pitch controller is set a little higher, at point E in Figure 8.3. If the speed set-point were at D then there would constantly be power dips in above rated winds, whenever the speed fell transiently below D. Furthermore the pitch controller would act below rated, as the pitch and torque controllers would both be trying to control the speed.

It would be an improvement if the torque-speed trajectory A-B-C-D-E in Figure 8.3 could be changed to A-B1-C1-E. The turbine would then stay close to optimum $C _ { p }$ over a wider range of wind speeds, giving slightly higher energy capture for the same maximum operating speed (Bossanyi 1994). The vertical sections A-B1 and C1-E can be achieved by using a PI controller for the torque demand, in response to the generator speed error with the set-point at A or C1. Transitions between constant speed and optimum $C _ { p }$ operation are conveniently handled by using the optimum $C _ { p }$ curve as the upper torque limit of the PI controller when operating at A, or the lower limit when at C1. The set-point sips between A and C1 when the measured speed crosses the mid-point between A and C1. Despite this step change in set-point the transition is completely smooth because the controller will be saturated on the optimum $C _ { p }$ limit curve both before and after the transition.

This logic can easily be extended to implement ‘speed exclusion zones’ to avoid speeds at which blade passing frequency would excite, for example, the tower resonance, by introducing additional speed set-points and some logic for switching between them – see lines FG, HJ in Figure 8.3. When the torque demand exceeds G for a certain time, the set-point ramps smoothly from F to H. Then if it falls below J, the set-point ramps back again.

Another advantage of PI control of the torque is that the ‘compliance’ of the system can be controlled. Controlling to a steep ramp (CD in Figure 8.3) can be quite harsh in that the torque demand will be varying rapidly up and down the slope. A PI controller, however, can be tuned to achieve a desired level of ‘softness’. With high gain, the speed will be tightly controlled to the set-point, requiring large torque variations. Lower gains will result in more benign torque variations, while the speed is allowed to vary more around the set-point.

To use point C1 as the speed set-point for both the torque and the pitch controllers, it is necessary to decouple the two. One technique is to arrange some switching logic that ensures that only one of the control loops is active at any one time. Thus below rated the torque controller is active and the pitch demand is rxed at rne pitch, while above rated the pitch controller is active and the torque demand is rxed at the rated value. This can be done with fairly simple logic, although there will always be occasions when the controller is caught briesy in the ‘wrong’ mode. For example, if the wind is just below rated but rising rapidly, it might be useful to start pitching the blades a little before the torque demand reaches rated. If the pitch does not start moving until the torque reaches rated, it then has to move some way before it starts to control the acceleration, and a small overspeed may result.

A more satisfactory approach is to run both control loops together but to couple them together with terms that drive one or the other loop into saturation when far above or below the rated wind speed. Thus most of the time only one of the controllers is active, but they can be made to interact constructively when close to the rated point.

A useful method is to include a torque error term in the pitch PID in addition to the speed error. Above rated, because the torque demand saturates at rated, the torque error will be zero, but below rated it will be negative. An integral term will bias the pitch demand towards rne pitch, preventing the pitch controller from acting in low winds, while a proportional term may help to start the pitch moving a little before the torque reaches rated if the wind speed is rising rapidly.

It is also necessary to prevent the torque demand from dropping when operating well above rated wind speed. Here a useful strategy is a ‘ratchet’ which prevents the torque demand from falling while the pitch is not at rne. This can also smooth over brief lulls in the wind around rated, using the rotor kinetic energy to avoid transient power drops.

An alternative approach is to introduce separate bias terms to the speed errors for the two control loops, effectively modifying the set-points of both loops, which remain active throughout. When the torque is below rated, the pitch controller sees a higher speed set-point, forcing the pitch towards rne. As the torque approaches rated, the set-point is reduced to the nominal value so that the pitch control gradually takes over. As the pitch rises above rne, the torque controller set-point is pushed down, forcing the torque up to the rated power limit. As the pitch comes down again the torque controller set-point rises back to the nominal value, allowing the torque controller to resume its duties by the time rne pitch is reached, and as the torque falls further the pitch controller set-point rises again to keep the pitch at the rne limit. The movement of the set-points is decoupled from the control loop dynamics by introducing rrst order lags with appropriate time constants. Shorter time constants are appropriate for rising set-points than for falling set-points. This helps prevent overspeeds and also prevents the pitch angle from falling too sharply during a temporary wind lull that could cause unnecessary tower vibration.

A further development of this approach is to use a wind speed estimator, as in Section 8.3.16. A transition zone is derned around the rated wind speed, and the estimated wind speed then dernes the fractional position through this transition zone. The torque bias is ramped from zero at the lower end of the transition zone to maximum at the upper end, and vice-versa for the pitch bias. This is likely to give a cleaner response, and there are no time constants to tune.

# 8.3.5 Control of tower vibration

For both rxed and variable-speed machines the insuence of the pitch controller on tower vibration and loading, described in Section 8.2.1, is one of the major constraints on the design of the control algorithm. The rrst tower fore–aft vibrational mode is essentially very lightly damped, exhibiting a strong resonant response that can be maintained at quite a high level even by a small amount of excitation, which is naturally present in the wind. The strength of the response depends critically on the small amount of damping that is present, mostly aerodynamic damping from the rotor. The pitch control action modires the effective damping of that mode. In designing the pitch controller, it is therefore important to avoid further reducing the already small level of damping, and if possible to increase it.

The design of control algorithms is covered in Section 8.4. This includes the choice of PID gains, as well as the addition of further terms to the controller that modify the overall dynamics in such a way as to help increase the tower damping. The use of modern control methods such as optimal state feedback is also discussed. This technique can help to achieve a suitable compromise between the competing objectives of speed or power control (achieved by regulating the in-plane loading) and tower vibration control (which depends on modifying the out-of-plane loading).

There is, however, only a certain amount of information in the measured speed or power signal. State estimators such as Kalman rlters (Section 8.4.5) can be used to try to distinguish between the effects of wind speed changes and tower motion on the measured signal. However, it is also possible to enhance the information available to the controller by using an accelerometer mounted in the nacelle, which provides a very direct measure of tower fore–aft motion. By using this extra signal, it is in fact possible to reduce tower loads signircantly without adversely affecting the quality of speed or power regulation.

The tower dynamics can be modelled approximately as a second order system exhibiting damped simple harmonic motion, that is,

$$
M \ddot {x} + D \dot {x} + K x = F + \Delta F \tag {8.12}
$$

where x is tower displacement and F is the applied force, which in this case is predominantly the rotor thrust. $\Delta F$ is the additional thrust caused by pitch action. We can equate M with the tower modal mass and K with the modal stiffness, such that the tower frequency is $\sqrt { K / M }$ rad/s. The damping term D is small. The effective damping can clearly be increased if $\Delta F$ is proportional to −ẋ . Clearly it is easier to measure acceleration than velocity, so the tower acceleration would have to be integrated to provide a measure of ẋ . A suitable gain for $\Delta F$ can be estimated from the partial derivative from pitch to thrust, 휕F/휕훽 where $\beta$ is the pitch angle, to achieve any particular additional damping $D _ { \mathfrak { p } } \mathrm { { : } }$ :

$$
\delta F = \frac {\partial F}{\partial \beta} \delta \beta = - D _ {p} \dot {x}
$$

$$
\delta \beta = \frac {- D _ {p}}{\partial F / \partial \beta} \dot {x} \tag {8.13}
$$

It may sometimes be necessary to place a notch rlter in series with this feedback term to prevent unwanted feedback from other components of tower acceleration, for example, at blade passing frequency. Lead-lag or other loop-shaping rlters may also help to adjust the phase of the feedback to ensure maximum damping, taking into account the full dynamics of the system that are actually more complex than Eq. (8.13). For example, the dynamic response of the pitch actuator should be taken into account, as well as other modes of vibration that couple to the tower dynamics. Figure 8.4 shows the results of a simulation with and without such an acceleration feedback term, in combination with a PID controller to control rotational speed. The simulations were driven with a realistic three-dimensional turbulent wind input. The speed control was hardly affected, and although there is a signircant increase in pitch actuator activity, the additional pitch rates required are modest. Clearly this technique is capable of increasing the tower damping substantially, almost eliminating the resonant response and signircantly reducing tower base loads. Although it requires an accelerometer, this is usually present anyway to trigger a shut-down in the event of excessive vibration. Accelerometers are also relatively cheap, robust, and reliable devices.

![](images/92fb2f1e1626cf43d6bc706b875b7ac894a6b85aef3b5edd33da9fbc8f3202a1.jpg)

<details>
<summary>line</summary>

| Time (s) | Nacelle fore-aft displacement (m) - Tower damping OFF | Nacelle fore-aft displacement (m) - Tower damping ON | Pitch rate (deg/s) - Tower damping OFF | Pitch rate (deg/s) - Tower damping ON |
| -------- | -------------------------------------------------- | ------------------------------------------------- | ------------------------------------- | ------------------------------------ |
| 120      | ~0.05                                              | ~0.03                                             | ~0                                    | ~0                                   |
| 125      | ~0.08                                              | ~0.06                                             | ~5                                    | ~10                                  |
| 130      | ~0.1                                               | ~0.08                                             | ~0                                    | ~5                                   |
| 135      | ~0.12                                              | ~0.1                                              | ~-15                                  | ~-10                                 |
| 140      | ~0.15                                              | ~0.12                                             | ~18                                   | ~15                                  |
| 145      | ~0.08                                              | ~0.06                                             | ~-5                                   | ~-5                                  |
| 150      | ~0.1                                               | ~0.08                                             | ~-10                                  | ~-10                                 |
| 155      | ~0.12                                              | ~0.1                                              | ~-15                                  | ~-15                                 |
| 160      | ~0.1                                               | ~0.08                                             | ~-20                                  | ~-20                                 |
</details>

Figure 8.4 Use of a tower accelerometer to help control tower vibration

Field test results demonstrating the effectiveness of this tower damping action have been published by Rossetti and Bossanyi (2004) and Bossanyi et al. (2010).

Because rotor thrust varies rapidly with pitch angle close to rne pitch, a common cause of fore–aft tower excitation is the case of a short-lived lull in wind speed starting a little above rated wind speed. The pitch responds by falling rapidly towards rne pitch, causing a rapid thrust reduction and large consequent tower vibration. This can be avoided by preventing the rapid decrease in pitch: if the wind picks up again quickly, as is often the case, little energy is lost. Various algorithms can be used for this. Simply limiting the negative pitch rate when close to rne pitch is a possibility, although this will generally reduce the effectiveness of speed regulation in this region, and the asymmetrical rate limits will result in loss of energy (restoring symmetry by similarly decreasing the positive rate limit is not advisable, as transient overspeeds will result). These disadvantages can be mitigated to some extent by limiting the downward pitch rate only after a large negative rate has already been sustained for a short time. However, a particularly effective technique is to use a dynamically varying rne pitch angle: whenever the pitch angle is above rne pitch, the rne pitch limit is increased, but always staying below the actual pitch by at least a certain margin, so that it is always well below the actual pitch in high winds. The dynamic rne pitch is allowed to decrease only slowly, so during a wind lull the pitch may decrease to the level of the dynamic rne pitch, which then continues to fall slowly to ensure that the true rne pitch is reached if the lull is prolonged. The generator torque control can act while the pitch is on the dynamic rne pitch limit, preventing any signircant reduction in rotor speed during a short wind lull.

Tower loading is generally dominated by the fore–aft vibration, but side–side vibration can be signircant in some situations – for example, in offshore turbines operating during periods of wind-wave misalignment. The side–side vibration is even more lightly damped than fore–aft, because there is even less aerodynamic damping from the rotor in this direction. When the principal wave direction is coming from the side therefore, the excitation of the side–side vibrations can be considerable, and may even become more signircant than the fore–aft vibration at such times. In principle, the damping of the side–side vibration can be increased by appropriate control of the generator torque, adding a component of torque demand derived from the measured side–side acceleration, in addition to the torsional damping described in the next section (Markou and Larsen 2009; Fischer et al. 2010).

In the special case of soating wind turbines, particular attention must be paid to the interaction of pitch control and tower motion. Depending somewhat on the type of moorings, there is likely to be a very low-frequency rigid-body oscillatory mode where the entire structure rocks backwards and forwards with a period that can be tens of seconds or even more, and can be signircantly excited by wave frequencies. More seriously however, an instability can arise: as the nacelle moves forward, the relative wind speed increases, causing the rotor speed to increase. The pitch increase needed to counteract this results in signircantly reduced rotor thrust, which can allow the motion to accelerate, resulting in an increasing amplitude of oscillation that could ultimately be catastrophic. Fortunately, the motion can be stabilised by suitable design of the controller. This can be addressed by multivariable controller design, but Vanni et al. (2015) compare two different stabilisation methods that use an additional single input, single output feedback loop based on measured nacelle acceleration, generating a modircation either to the pitch demand or to the generator torque demand. The former results in somewhat higher rotor speed deviations, while the latter increases electrical power variations. A compromise might be found by tuning both loops to run in parallel.

# 8.3.6 Control of drive train torsional vibration

A typical drive train can be considered to consist of a large rotor inertia and a (smaller) high-speed shaft inertia (mainly the generator and brake disc), separated by a torsional spring that represents twisting of shafts and couplings, bending of gear teeth and desection of any soft mountings. It is important to consider also the coupling of the torsional mode of vibration with the rrst rotor in-plane collective mode, in which case the drive train can be approximated by three inertias and two torsional springs (Ramtharan et al. 2007). In some cases the coupling to the second tower side-to-side mode, which has a lot of rotation at the tower top, is also important.

In a rxed-speed turbine, the induction generator slip curve (Section 7.5) essentially acts like a strong damper, with the torque increasing rapidly with speed – see Figure 7.53. Therefore, the torsional mode of the drive train is well damped and generally does not cause a problem. In a variable-speed turbine operating at constant generator torque however, there is very little damping for this mode, because the torque no longer varies with generator speed. The aerodynamic damping due to the rotor is small because the blades are vibrating in the in-plane direction. There is a small amount of structural damping in shafts and couplings, and some damping from the gearbox, but these effects contribute typically only a small fraction of 1% of critical damping. The very low damping can lead to large torque oscillations at the gearbox, effectively negating one of the principal advantages of variable-speed operation, the ability to control the torque.

Although it may be possible to provide some further damping mechanically – for example, by means of appropriately designed rubber mounts or couplings – it is difrcult to provide enough damping and there is a cost associated with this. A widely used solution, which has been successfully adopted on many variable-speed turbines, is to modify the generator torque control to provide some damping. Instead of demanding a constant generator torque above rated (or a torque varying slightly in inverse proportion to speed in the case of the constant power algorithm described in Section 8.3.3), a small ripple at the drive train frequency is added on to this basic torque demand, with the phase adjusted to counteract the effect of the resonance and effectively increase the damping. A band-pass rlter of the form

$$
G \frac {2 \zeta \omega s (1 + s \tau)}{s ^ {2} + 2 \zeta \omega s + \omega^ {2}} \tag {8.14}
$$

(where G is a gain) acting on the measured generator speed can be used to generate this additional ripple. The frequency 휔 must be close to the resonant frequency that is to be damped. The time constant 휏 modires the phase and contributes more of a high-pass rlter characteristic, and can sometimes be used to compensate for time lags or other dynamics in the system. A root locus plot (Section 8.4) is very useful for tuning the rlter parameters.

![](images/fa35db6aea84940f95dad4de8fa3c8d1660bbfc649d5eb47cf5043a7d8eaada6.jpg)

<details>
<summary>line</summary>

| Time (s) | Electrical power (kW) |
| -------- | --------------------- |
| 0        | 600                   |
| 5        | 600                   |
| 10       | 600                   |
| 15       | 600                   |
| 20       | 600                   |
| 25       | 300                   |
| 30       | 650                   |
</details>

![](images/741e6cd6bd01dcdd5feabff813e6fc38666fc6491830eb46da7922af72d14ef0.jpg)

<details>
<summary>line</summary>

| Time (s) | Electrical power (kw) | Gear box torque (kNm) |
| -------- | --------------------- | --------------------- |
| 0        | 620                   | 230                   |
| 5        | 620                   | 230                   |
| 10       | 620                   | 230                   |
| 15       | 620                   | 230                   |
| 20       | 620                   | 230                   |
| 25       | 400                   | 150                   |
| 30       | 620                   | 230                   |
</details>

Figure 8.5 Effect of a drive train damping rlter

Although a very effective rlter can be made by tuning it to give a frequency response with a very broad peak (large 휁), this may be detrimental to the overall performance in that more low frequency variations in torque and power are then introduced. Even with a narrow peak, there can be sufrcient response at multiples of blade passing frequency such as 3P or 6P to disturb the system, in which case a notch rlter (Section 8.4) can be cascaded with the rlter of Eq. (8.14). Of course if the resonant frequency nearly coincides with an excitation frequency such as 6P then the resonance will be very difrcult to control because it will be strongly excited.

Figure 8.5 shows some simulation results for a variable-speed turbine operating in simulated three-dimensional turbulence. A large drive train resonance can be seen to be building up. Although the power and generator torque are smooth, the gearbox would be very badly affected. The effect of introducing a damping rlter as described above is also shown. It almost completely damps out the resonance without increasing the electrical power variations. This is because the torque ripple needed to damp the resonance is actually very small, because the amount of excitation is small.

In many cases the drive train damping can be further improved by using an input signal representative of the ‘twisting speed’ rather than just the generator speed: the twisting speed is just the difference between the generator speed and the rotor speed (scaled by gearbox ratio). However, this requires two speed measurements, and the low-speed shaft sensor in particular sometimes has insufrcient resolution and may need to be upgraded. Care is needed to ensure that the required difference between the two signals is not too susceptible to noise on the signals.

These torsional vibrations are typically much less of a problem on direct drive systems, where in some cases a damping rlter of this sort may not even be required at all.

# 8.3.7 Variable-speed stall regulation

Figure 8.6 shows two power curves for the same rotor, one running as a 600 kW rxedspeed pitch-regulated turbine and one adjusted to run as a rxed-speed stall-regulated turbine with the same rating. The rotational speed of the stall-regulated turbine has been reduced to limit the power to the same rated level. Therefore, although the stall-regulated turbine generates slightly more energy at very low wind speeds, as the blades approach stall above 8 m/s there is a large loss of output compared to the pitch-regulated machine. (In practice of course, if the turbine was designed to operate in stall, the blade design, solidity, and rotor speed could be re-optimised, reducing this difference.)

![](images/160ac80f285b486e90223179a8462c0d4e206b45c340442b4bdb07a26ebf6e52.jpg)

<details>
<summary>line</summary>

| Wind speed (m/s) | Pitch | Stall |
| ---------------- | ----- | ----- |
| 5                | 40    | 40    |
| 6                | 80    | 80    |
| 7                | 140   | 140   |
| 8                | 220   | 220   |
| 9                | 320   | 320   |
| 10               | 450   | 420   |
| 11               | 620   | 520   |
| 12               | 620   | 580   |
| 13               | 620   | 600   |
| 14               | 620   | 610   |
| 15               | 620   | 610   |
</details>

Figure 8.6 Comparison of pitch and stall control

By making use of variable speed, it is quite possible to correct this loss of energy by operating either turbine at the optimum tip speed ratio up to rated, or until the maximum rpm is reached. At rated power, it is then possible to reduce the speed of the rotor to bring it into stall, although this has rarely been done to date on commercial machines. This can be done by closed-loop control of the generator torque in response to power error, allowing the turbine to follow exactly the same power curve as the pitch-regulated turbine. Thus, the variable-speed stall-regulated turbine can achieve the same energy output as the variable-speed pitch-regulated turbine, but without the need for an active pitch mechanism. As explained in Section 8.2.2 however, signircant torque and power transients will result from this strategy. The smooth torque and power, which are one of the main advantages of variable-speed systems, will therefore not be realised.

One simple and effective control algorithm for this case is illustrated in Figure 8.7. It consists of two nested loops, an outer power loop that demands a generator speed and an inner speed loop that demands a generator torque. As in Section 8.3.4, a PI controller can be used for the inner loop. This is the same controller as for sections A-B1 and C1-E of Figure 8.3, making it particularly easy to arrange the transition between control modes at the rated point because the inner loop is always active.

![](images/15a4e847c89de10c132ef6c61aed164564c00283b1e2d04c8444a2b14a9ea1fa.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Power set-point"] --> B["PI controller"]
    B --> C["Speed demand"]
    C --> D["PI controller"]
    D --> E["Turbine"]
    E --> F["Generator torque demand"]
    F --> G["Inner loop"]
    G --> H["Measured speed"]
    H --> I["Outer loop"]
    I --> J["Measured power (or measured speed multiplied by torque demand)"]
    J --> B
```
</details>

Figure 8.7 A simple control algorithm for variable-speed stall regulation

# 8.3.8 Control of variable-slip turbines

The operating envelope for a variable-slip generator is shown in Figure 8.8. Note that the slip speed represents the increase in speed above synchronous (conventionally for motors this would be a negative slip). Below rated, the generator acts just like a conventional induction machine, with the torque related to the slip speed according to the slip curve AB. Once point B is reached, a resistor in series with the rotor circuit, previously short-circuited by a semiconductor switch, is progressively brought into play by switching the semiconductor switch on and off at several kilohertz, and varying the mark-space ratio to change the average resistance. As the average resistance increases, the generator slip curve changes so that its slope varies inversely with the total resistance of the rotor circuit. Figure 8.8 shows a typical example in which the rotor resistance can increase by a factor 10, changing the slip curve from AB to AD. By controlling the resistance therefore, the generator can operate anywhere within the shaded region. The resistance is usually varied by a closed-loop algorithm that seeks to regulate the torque to any desired value. For example, this might be PI algorithm with torque error input and the mark-space ratio of the switch as output.

In practice, it is usual to keep the torque demand at the rated value. Then the generator will simply act as a conventional induction generator following the slip curve AB until rated torque is reached, at which point it will accelerate along the constant torque line BCD just like a variable-speed system. If the speed increases beyond D the torque is forced to increase again. Pitch control is used to regulate the speed to a chosen set-point such as point C. The higher the speed C, the higher the mechanical power input for the same output power. Thus, the power dissipated in the rotor circuit corresponds exactly to the slip. Therefore, C should be chosen as low as possible to minimise the cooling requirements (as well as turbine loads that increase with speed). However, if C is too close to B then the torque will occasionally dip down the slope AB as the speed varies around the set-point, causing power dips even when operating well above rated wind speed. How small the interval between B and C can be made depends on the rotor inertia and the responsiveness of the pitch control algorithm. As for a variable-speed system, the latter can be a PI or PID algorithm. It is possible to change the rate limits of the PID to force the pitch towards rne at maximum rate if the speed gets too close to B, or to feather at maximum rate if it gets too close to D.

![](images/e06eee5ee3a7e62d54af27354f46b5fdf353b8335640a766841c942176493d94.jpg)

<details>
<summary>line</summary>

| Slip speed | Torque (Rated torque) | Rotor resistance (R) | Rotor resistance (5R) | Rotor resistance (10R) |
| ---------- | ---------------------- | --------------------- | ---------------------- | ----------------------- |
| 0%         | 0                      | A                     | A                      | A                       |
| 1%         | ~1.5                   | B                     | B                      | B                       |
| 5%         | ~3.5                   | C                     | C                      | C                       |
| 10%        | ~5.5                   | D                     | D                      | D                       |
</details>

Figure 8.8 Operating envelope for a variable-slip generator

As with a variable-speed system, it may be desirable to modify the torque demand as in Section 8.3.6 to control drive train torsional vibrations. However, to do this, it is necessary to be able to update the torque demand at relatively high frequency, at least rve and preferably 10 times the drive train frequency, which is typically of the order of 3–5 Hz.

# 8.3.9 Individual pitch control

Large pitch-regulated turbines invariably have a separate pitch actuator for each blade, because these can be used to provide effectively independent aerodynamic braking systems on the rotor. This means that no shaft brake is required, other than a small parking brake, because if one pitch actuator fails, the remaining actuator(s) should still be capable of stopping the rotor. Given that each blade has its own independent actuator, it is possible to send different pitch demands to each blade, and this can be used to reduce the asymmetrical aerodynamic loadings across the rotor, which are responsible for a signircant contribution to fatigue loads (Donham and Heimbold 1979; Caselitz et al. 1997; Bossanyi 2004).

The simplest concept is cyclic pitch control based on the rotor azimuth. There are a number of effects that cause a systematic azimuthal variation of loading on each blade, in particular the wind speed variations caused by wind shear and tower shadow, and changes in angle of attack due to yaw misalignment, shaft tilt, and upsow. In principle it should be possible to impose an azimuth-dependent change to the demanded pitch for each blade to compensate for these effects.

The tower shadow is very systematic and predictable, but to have any effect would require a very rapid and short-lived ‘blip’ in pitch demand as each blade passed the tower, which could have other adverse consequences. The effect of shaft tilt is also very predictable, and possibly upsow too in some situations, but these will affect only the angle of attack and not the local wind speed. Yaw misalignment also affects just the angle of attack, and to compensate for it would require an additional sensor to measure it, because the magnitude and direction of the misalignment will vary continuously. Wind shear does cause a signircant difference in wind speed across the rotor, and therefore causes large blade load variations at the rotational frequency (1P), but again it is not a constant effect and would require one or more additional sensors to detect it. Furthermore, the wind shear can only be regarded as a mean effect, and because of turbulence the instantaneous variation in wind speed across the rotor may be very different: in fact the highest wind speed could occur instantaneously anywhere on the rotor disc, not always at the top.

Indeed, it is the turbulent variations in wind speed across a large wind turbine rotor that usually dominate the asymmetrical loading, because the size of a large rotor is comparable to the scale of turbulent eddies. Therefore azimuth-dependent cyclic pitch control tends not to be very successful: while on average some reduction in loading ought to be achievable by compensating for the mean wind shear, this is insignircant compared to the stochastic effects of turbulence. An exception might be for a turbine operating in highly stratired sow with low turbulence.

Normally though, to achieve any signircant reduction in these asymmetrical loads requires some additional measurement of the instantaneous turbulence, so that the individual pitch angles can be adjusted to compensate for these effects.

One possibility is actually to measure the incident wind sow just in front of each blade – for example, using a set of pitot tubes along the blades – or to use pressure taps at appropriate locations, and then to adjust the pitch of each blade in response to the measurements on that blade. Such sensors have also been proposed to control ‘smart’ blades, which have actuators distributed along the span of the blade to alter its aerodynamic properties locally, such as saps or ailerons, deformable trailing edges, or possibly air jets to modify the boundary layer sow. Such ideas are the subject of ongoing research and are currently a long way from any commercial deployment.

A more realistic possibility is to use load sensors to measure the blade bending moments at the root, or possibly at various points along the blade. It makes some sense to measure the very loads that we wish to reduce. With full-span pitch control, it would seem to make sense to measure the blade root loads on each blade and use the measurements to adjust the pitch of each blade in a feedback loop. Such a scheme could be called independent pitch control, although there is no dernite consensus on nomenclature.

The possibility then arises to use the load measurement on each blade root as a predictor of the load that will be seen by the next blade when it sweeps past that position. This provides a degree of anticipation that should allow a further improvement in the control of each blade, and it works because turbulent eddies tend to be large enough so that as they pass through the rotor, each blade will slice through the same turbulence structure, perhaps even several times, before it has passed. Because the pitch of each blade is now calculated from the load measurements on all of the blades, this can no longer be called ‘independent’ pitch control, and the term individual pitch control may be more appropriate.

Individual pitch control is described in more detail in Section 8.3.11.

# 8.3.10 Multivariable control – decoupling the wind turbine control loops

The wind turbine controller is now a multivariable controller, with a number of inputs and outputs:

Inputs (measured signals):

• Generator speed (for speed regulation and drive train damping).   
• Two tower accelerations (for tower damping).   
• Three blade root loads (for a three bladed turbine).

Outputs (demanded signals):

Generator torque.   
• Three pitch angles or rates (for a three bladed turbine).

There are modern control methods that are appropriate to the design of controllers for such MIMO (multiple input, multiple output) systems – see Section 8.4.5. However, a MIMO system can sometimes be ‘diagonalised’ or transformed into a set of independent SISO (single input, single output) systems, in which case the controller for each SISO system can be optimised in isolation from the others. In fact, this is possible to some extent for a wind turbine controller, and so all of the control loops previously mentioned can be designed using classical SISO design methods (Section 8.4.1). Actually the SISO loops are not quite independent, but the dynamic coupling between them can be small enough to make this a very successful approach in many cases.

It is relatively straightforward to decouple the pitch control from the torque control, as implied in the discussions above. In fact it is also possible to decouple the individual pitch control from the collective pitch control – the latter provides a collective pitch demand for speed regulation and tower damping, while the individual pitch control generates a separate pitch demand increment for each blade for minimising asymmetrical rotor loads. The pitch demand increments are all zero-mean, in such a way that the collective pitch control is not affected.

The main independent turbine control loops can now be summarised as follows:

1. Speed regulation loop using torque (using generator speed error to calculate the torque demand).   
2. Drive train damping loop (using generator speed to calculate a modircation to the torque demand).   
3. Side–side tower damping loop (using side–side nacelle acceleration to calculate a further modircation to the torque demand).   
4. Speed regulation loop (using generator speed error to calculate the collective pitch demand).   
5. Fore–aft tower damping loop (using fore–aft nacelle acceleration to calculate a modircation to the collective pitch demand).   
6. Individual pitch loop (using blade root loads to calculate individual pitch demand increments).

Loop 3 is not generally used but may become more interesting for offshore turbines that can be excited by wave action when this is misaligned with the wind direction.

There is actually some interaction between some of these loops; for example, loops 1 and 4 sometimes require notch rlters tuned to the drive train resonant frequency to suppress coupling that would otherwise arise through the control action itself. Also loops 4 and 5 must be coupled in principle, because any change in pitch angle affects both the torque and the thrust; but because loop 5 acts only in a restricted frequency range close to the rrst tower frequency, it is usually possible to tune the loops independently. However, a better result can be obtained with one or two iterations: one of the loops is tuned rrst using the open-loop plant model, then the plant is rederned by closing this loop while the other loop is tuned, and so on.

Loop 6 is still a MIMO loop, with as many inputs and outputs as there are blades. However, this can also be decoupled as explained in the next section, by exploiting the symmetry that exists between the blades.

# 8.3.11 Two axis decoupling for individual pitch control

To rrst order, the asymmetrical wind reld across the rotor swept area can be linearised and described by two orthogonal components, for example, as wind speed shear gradients in the horizontal vertical directions. Blade loading is closely related to wind speed, so this representation can also be used for a ‘blade load reld’ (the ‘blade load reld’ can be considered to include the effects of all three components of the local wind speed on the blade load). This description is independent of the number of blades or their speed of rotation, and the actual load seen by a blade at any instant can be thought of as the value of that reld as sampled by the blade at its instantaneous position.

Furthermore, the pitch action needed to compensate for this variation in loading can also be described by a ‘reld’ covering the swept area, and at any instant the pitch required by each blade is obtained by sampling that reld at the instantaneous position of the blade.

Because each reld is described by just two orthogonal components, a two-input, two-output controller is required to generate the pitch action ‘reld’ from the load ‘reld’. Again this is independent of the number of blades.

Thus for a three bladed rotor, the three measured blade root loads can be used to calculate the two components of the ‘load reld’ at that instant. These are used to calculate the two components of the ‘pitch reld’, from which the three individual pitch increments are calculated. The transformation between the three rotating blades and the two (non-rotating) reld components is identical to Park’s transformation for three-phase electrical machines (Park 1929), which relates the currents or voltages in each phase winding to two notional orthogonal currents or voltages in the ‘direct’ and ‘quadrature’ axes. For this reason it is known as the $d { - } q$ axis transformation. The same concept has also been used for helicopter rotors, where it is known as the Coleman transformation (Coleman and Feingold 1957). The transformation from three rotating blade root loads $L _ { I }$ , $L _ { 2 } , L _ { 3 }$ to the non-rotating d and q axes can be written as follows:

$$
\left[ \begin{array}{l} L _ {d} \\ L _ {q} \end{array} \right] = \frac {2}{3} \left[ \begin{array}{c c c} \cos (\varphi) & \cos (\varphi + 2 \pi / 3) & \cos (\varphi + 4 \pi / 3) \\ \sin (\varphi) & \sin (\varphi + 2 \pi / 3) & \sin (\varphi + 4 \pi / 3) \end{array} \right] \left[ \begin{array}{l} L _ {1} \\ L _ {2} \\ L _ {3} \end{array} \right] \tag {8.15}
$$

where φ is the azimuth angle. The reverse transformation is

$$
\left[ \begin{array}{l} \theta_ {1} \\ \theta_ {2} \\ \theta_ {3} \end{array} \right] = \left[ \begin{array}{c c} \cos (\varphi) & \sin (\varphi) \\ \cos (\varphi + 2 \pi / 3) & \sin (\varphi + 2 \pi / 3) \\ \cos (\varphi + 4 \pi / 3) & \sin (\varphi + 4 \pi / 3) \end{array} \right] \left[ \begin{array}{l} \theta_ {\mathrm{d}} \\ \theta_ {\mathrm{q}} \end{array} \right] \tag {8.16}
$$

where 휃 would represent pitch angle in this case. This can be extended to any number of blades B, as follows:

$$
\left[ \begin{array}{l} L _ {d} \\ L _ {q} \end{array} \right] = \frac {2}{B} \left[ \begin{array}{c c c c} \cos (\varphi) & \cos (\varphi + 2 \pi / B) & \cos (\varphi + 4 \pi / B) & ... \\ \sin (\varphi) & \sin (\varphi + 2 \pi / B) & \sin (\varphi + 4 \pi / B) & ... \end{array} \right] \left[ \begin{array}{l} L _ {1} \\ L _ {2} \\ L _ {3} \\ ... \end{array} \right] \tag {8.17}
$$

$$
\left[ \begin{array}{c} \theta_ {1} \\ \theta_ {2} \\ \theta_ {3} \\ \dots \end{array} \right] = \left[ \begin{array}{c c} \cos (\varphi) & \sin (\varphi) \\ \cos (\varphi + 2 \pi / B) & \sin (\varphi + 2 \pi / B) \\ \cos (\varphi + 4 \pi / B) & \sin (\varphi + 4 \pi / B) \\ \dots & \dots \end{array} \right] \left[ \begin{array}{c} \theta_ {\mathrm{d}} \\ \theta_ {\mathrm{q}} \end{array} \right] \tag {8.18}
$$

For a two bladed machine this reduces simply to

$$
L _ {d} = \left(L _ {1} - L _ {2}\right) \cos (\varphi)
$$

$$
L _ {q} = (L _ {1} - L _ {2}) \sin (\varphi) \tag {8.19}
$$

and

$$
\theta_ {1} = - \theta_ {2} = \theta_ {\mathrm{d}} \cos (\varphi) + \theta_ {\mathrm{q}} \sin (\varphi) \tag {8.20}
$$

In practice it is important to introduce an azimuthal phase shift into the reverse d-q axis transformation, by adding an offset to the rotor azimuth angle to account for the fact that a pure d axis pitch action generates both d and q axis loading, as a consequence of the aerodynamic properties of the rotating rotor; for example, an increase in pitch angle when a blade is at the top of its sweep will reduce the rotor tilt moment, but will also generate some yaw moment. The azimuthal phase shift can also compensate for the controller timestep and any other time delays in the control loop – in other words, the pitch angle is calculated for the azimuth angle, which will be reached by the time the pitch demand has been fully realised.

All that remains is to design a two-input, two-output controller [C] to calculate the d-q axis pitch demands from the d-q axis loads:

$$
\left[ \begin{array}{l} \theta_ {\mathrm{d}} \\ \theta_ {\mathrm{q}} \end{array} \right] = [ C ] \left[ \begin{array}{l} L _ {\mathrm{d}} \\ L _ {\mathrm{q}} \end{array} \right] \tag {8.21}
$$

In the steady state there is clearly a one-to-one correspondence between the load and the pitch angle needed to compensate for it, once the azimuthal phase shift described above has been taken into account. It seems logical therefore to suppose that [C] can be diagonal matrix, and furthermore because the rotor is rotationally symmetrical, the two diagonal terms should be identical. The design of the controller therefore boils down to designing a single SISO controller, and using two independent instances of it for the d and q axes. Because the wind reld in the non-rotating frame varies relatively slowly, a straightforward, fairly low-bandwidth PI controller can be used for this.

Taking into account the dynamics, rotational sampling at the blade passing frequency means that there will be a certain speed variation at that frequency, resulting in corresponding variations in $L _ { \mathrm { d } }$ and $L _ { \mathrm { q } }$ . A notch rlter at the blade passing frequency is therefore added in series with each PI controller. As for other PI loops, further notch or loop-shaping rlters can be added if required.

Once the dynamics are taken into account, the rotor is no longer symmetrical because of its interaction with the tower dynamics. In principle this could lead to some asymmetry between the d and q axes, and possibly also a small amount of dynamic coupling. Therefore, in principle there might be some advantage in designing in a coupled 2-input, 2-output controller (Bossanyi 2003). In practice however, any advantage is likely to be small, and two independent and identical SISO controllers have been found to work extremely well. Furthermore, these simple controllers have been found to be very robust: they tend to be rather insensitive to the turbine dynamics, and also to load sensor calibration errors or drift.

The inverse d-q transformation converts the relatively slowly varying d-q pitch demands into near-sinusoidal individual pitch demand increments for each blade. The near-sinusoids are of frequency 1P and phase-shifted between the blades, for example, by $1 2 0 ^ { \circ }$ for a three bladed turbine. This form of control is therefore sometimes referred to as cyclic pitch control, but this is not strictly correct: the controller is responding dynamically to the changing loads, so the pitch action is not actually sinusoidal, although it could be interpreted as sinusoidal with constantly changing amplitudes and phases. With PI controllers it is easy to limit the controller output to a maximum level, which corresponds to an upper limit on the amplitude of the sinusoids, and given the frequency (1P), this also determines the maximum additional pitch rate that would be demanded. This upper limit can be ramped down to zero in low winds, preventing any individual pitch action when the loads are small enough to contribute little to lifetime fatigue damage, so that the additional pitch action would not be worthwhile. It can also be used to ensure that the pitch demand does not fall below any physical pitch limit if this is close to the collective pitch demand in low winds. Another use is to prevent individual pitch action when it is more important to use the available pitch rates for collective pitch control – for example, if the rotor is accelerating rapidly towards an overspeed trip (Savini and Bossanyi 2010).

# 8.3.12 Load reduction with individual pitch control

The main effect of the once-per-revolution (1P) individual pitch control is to reduce the 1P out-of-plane loading on the blades, and hence also the rotating hub or shaft moments. Figure 8.9 shows spectra of the blade root out-of-plane and shaft bending moments in simulations with and without individual pitch control. In fact the spectral peak in these loads at the 1P frequency is virtually eliminated, an effect that has been conrrmed also in reld tests on an actual turbine (Bossanyi et al. 2012a). Since the 1P load component dominates the fatigue, signircant fatigue load reductions are obtained: typically of the order of 20% for blade root out-of-plane bending moment, and more for shaft bending moments (30–40%) because the low frequency variations cancel out between the blades so the 1P peak is even more signircant.

On a two bladed turbine therefore, the use of individual pitch control represents a good alternative to the use of a teetered hub (Bossanyi and Wright 2009). Although it does not eliminate the teetering moment completely, a teetered hub often needs some kind of teeter restraint, which re-introduces a moment, and it is almost certainly necessary to consider the possibility of a teeter end-stop impact that can generate huge loads.

![](images/2a6590efd802c70e9aa0d15cc9b77484dc249eccbf4e7a9707b959a06a513724.jpg)

<details>
<summary>line</summary>

| Frequency [1/s] | Simulation, 15 m/s, 20% turbulence OFF | Simulation, 15 m/s, 20% turbulence ON |
| --------------- | ---------------------------------------- | -------------------------------------- |
| 0.0             | ~1.0e+10                                 | ~1.0e+09                               |
| 0.5             | ~1.0e+09                                 | ~1.0e+10                               |
| 1.0             | ~1.0e+10                                 | ~1.0e+10                               |
| 1.5             | ~1.0e+09                                 | ~1.0e+10                               |
| 2.0             | ~1.0e+09                                 | ~1.0e+10                               |
| 2.5             | ~1.0e+09                                 | ~1.0e+10                               |
| 3.0             | ~1.0e+08                                 | ~1.0e+09                               |
| 3.5             | ~1.0e+08                                 | ~1.0e+09                               |
| 4.0             | ~1.0e+08                                 | ~1.0e+09                               |
| 4.5             | ~1.0e+08                                 | ~1.0e+09                               |
| 5.0             | ~1.0e+08                                 | ~1.0e+09                               |
</details>

Figure 8.9 Effect of individual pitch control on rotating out-of-plane loads: blade root out-of-plane moment (left) and shaft bending moment (right)

![](images/6a8ff37c45ff4208d0740f5dfa1a2a2ef47ffacfd32dd62ad71d490a3696acc8.jpg)

<details>
<summary>line</summary>

| Time [s] | kNm     |
| -------- | ------- |
| 0        | -5000   |
| 10       | 8000    |
| 20       | -3000   |
| 30       | -2000   |
| 40       | -8000   |
| 50       | 2000    |
| 60       | -1000   |
| 70       | 3000    |
| 80       | -6000   |
| 90       | 7000    |
| 100      | 6000    |
</details>

![](images/82fd1039ff1b45257953a4824189fdc8da5473acebf42dfb4de94baf426f1b11.jpg)

<details>
<summary>line</summary>

| Time [s] | kNm     |
| -------- | ------- |
| 0        | 7000    |
| 10       | -3000   |
| 20       | 4000    |
| 30       | -5000   |
| 40       | 3000    |
| 50       | -2000   |
| 60       | 2000    |
| 70       | -1000   |
| 80       | 5000    |
| 90       | -4000   |
| 100      | -6000   |
</details>

Figure 8.10 Effect of individual pitch control on yaw moment. Top: without individual pitch control; bottom: with individual pitch control

The 1P loading component on the rotor, when transformed to the non-rotating reference frame, results in loading contributions at 0P and 2P, so it is these load components that are reduced by individual pitch control. Hence the low frequency variation of nacelle nodding and yawing moments is removed, resulting in a reduction in peak loading – Figure 8.10 shows the effect on yaw moment, which may be of signircant benert in reducing the required yaw motor rating and duty. The nodding moment is reduced in a very similar way.

On a three bladed turbine, there is no signircant 2P component in the non-rotating loads, so only the low frequency load reduction is important here – the dominant source of fatigue loading on the non-rotating components is at 3P, and so is largely unaffected by the individual pitch control. However, for a two bladed turbine, where this fatigue loading is dominated by 2P, the individual pitch control does signircantly reduce the non-rotating fatigue loading. Again this has been conrrmed in reld tests (Bossanyi et al. 2012a) – by ‘toggling’ the individual pitch control on and off every few minutes, the improvement in loading is clearly demonstrated.

However, even for a three bladed turbine it is possible to reduce these non-rotating fatigue loads by making use of second-harmonic individual pitch control. Taking 1P as the rrst harmonic, second-harmonic individual pitch control is achieved in exactly the same way but with the arguments to the sine and cosine functions in the rotational transformations multiplied by two, or by n for the nth harmonic (although it may not be worthwhile to use more than the second harmonic in practice). Second-harmonic control results in 2P pitch action, hence any 2P loading in the rotating components is reduced, but also the 1P and 3P loading in the non-rotating components (van Engelen and van der Hooft 2005; Bossanyi and Wright 2009). On a three bladed turbine therefore, the dominant 3P non-rotating fatigue loads are reduced by this means, as shown in Figure 8.11.

![](images/ea5361bb57f79830af662be031034c59f4e326cfc57f08056756601d1bae28f3.jpg)

<details>
<summary>line</summary>

| Normalised frequency (P) | IPC off | IPC: 1P only | IPC: 1P & 2P |
| ------------------------ | ------- | ------------ | ------------ |
| 0.0                      | 26.0    | 42.0         | 1.0          |
| 0.5                      | 10.0    | 7.0          | 6.0          |
| 1.0                      | 3.0     | 4.0          | 3.0          |
| 1.5                      | 0.0     | 0.0          | 0.0          |
| 2.0                      | 0.0     | 0.0          | 0.0          |
| 2.5                      | 5.0     | 6.0          | 3.0          |
| 3.0                      | 16.0    | 17.0         | 6.0          |
| 3.5                      | 5.0     | 6.0          | 7.0          |
| 4.0                      | 1.0     | 1.0          | 1.0          |
| 4.5                      | 0.0     | 0.0          | 0.0          |
| 5.0                      | 4.0     | 4.0          | 4.0          |
</details>

Figure 8.11 Effect of 1P and 2P individual pitch control on non-rotating loads

![](images/b76318e2f16ee9ef89fc99cbc1f862c1d008810fd9fa4fae25f07709d3ea5207.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Load measurements (3 blades)"] --> B["Rotational transformation (1P)"]
    A --> C["Rotational transformation (2P)"]
    B --> D["D-axis control"]
    B --> E["Q-axis control"]
    C --> F["D-axis control"]
    C --> G["Q-axis control"]
    D --> H["Rotational transformation (1P)"]
    E --> I["Rotational transformation (2P)"]
    F --> J["Rotational transformation (2P)"]
    H --> K["Pitch demands (3 blades)"]
    I --> K
```
</details>

Figure 8.12 Adding higher harmonic individual pitch control loops

Any number of harmonics may be used together as shown in Figure 8.12, simply by using parallel control loops.

# 8.3.13 Individual pitch control implementation

Individual pitch control requires additional sensors, so it is important to ensure that these are very reliable, otherwise the overall reliability of the turbine would be compromised. Conventional strain gauges are notoriously unreliable, although they certainly can last well if very carefully installed. However, strain sensors based on rbre Bragg gratings are now available that have the potential to be sufrciently reliable for this application.

Pulses of laser light are directed along an optical rbre, and a rne grating ‘burnt’ into the rbre at a certain location resects light of the same wavelength as the grating. The frequency of the resected light is detected, and gives a direct measure of the strain at the position of the grating. Many gratings can be burnt into the same rbre, so strains at multiple locations can be measured at little extra cost: the time delay between sending the pulse and detecting the resected signal determines the position of each grating. The components required are based on communications technology and therefore becoming readily available. Furthermore, the special optical rbres can easily be included as part of the glass reinforced plastic (GRP) layup during construction of a wind turbine blade.

Individual pitch control could equally be implemented using shaft bending sensors or even other sensors in the nacelle or tower top (Bossanyi 2003), but it may be difrcult to rnd suitable sensor locations. However, if blade root sensors are used, they can also provide a measure of hub torque and rotor thrust. Although not currently used in this way, they might be useful as additional or alternative inputs to the other control loops described above; for example, for damping tower fore–aft or drive train torsional vibrations.

If there is any failure of the strain sensors, there is the potential for individual pitch control to increase rather than reduce loading, which could be serious. Some failures are readily detected in a well-designed sensor system, but it is always possible that some types of failure may be hard to detect without some analysis of the signals by the controller – for example, by comparing the sensor signals between different blades. If any failure is detected or suspected, the individual pitch control (being completely decoupled from the other control loops) can simply be switched off without the necessity to shut down the turbine, at least for a limited period or at a reduced power level until the fault can be rectired.

Below rated, the individual pitch control would normally be phased out because the loads are already smaller and so the additional pitch activity may not be justired. Also in principle there should be a small loss of energy output because the pitch angles are constantly moving either side of the optimum, although in practice this loss of output is usually very small. Above rated there is no loss of output, as the pitch angles are already well away from the optimum, and the collective pitch control loop ensures that rated output is maintained.

Clearly individual pitch control results in additional pitch actuator duty. The additional pitch action is concentrated around the 1P frequency. As turbines grow larger, the pitch rates required will diminish, because the rotational frequency will decrease as rotor diameter increases. If higher harmonic individual pitch control is used – for example, at 2P – then there will also be additional pitch action at that frequency. Because the pitch action is near-sinusoidal, the maximum pitch rate required can be estimated as the product of the maximum amplitude limit and the frequency; this should be multiplied by √2 in case the d and q axis demands are simultaneously at the limit. The required actuator torque is no greater than normal (and may even be slightly reduced because the lower blade root bending moment implies lower bearing friction), but the actuators will be working harder because of the increased pitch rates. This will have implications for the thermal rating of the actuators.

The total lifetime pitch travel will increase, typically by a factor of around 3 (Bossanyi 2003), which must be taken into account in the design of the pitch bearings.

Although fatigue loads can be signircantly reduced by individual pitch control, there remains the possibility of increased extreme loads in the event of a forced shut-down by the safety system: if the pitch angles are all different by several degrees and that difference is maintained as the pitch angles are ramped to feather, large asymmetrical loads, sometimes design-driving, can be generated. Where possible the individual pitch control is ramped out during the shut-down, but the safety system is unlikely to be allowed the sophistication required to do this. However, by reducing the individual pitch control amplitude as a function of rotor acceleration, this situation can effectively be avoided because the pitch angles are then likely to be much closer together when a safety system trip occurs (Savini and Bossanyi 2010). The fatigue load reduction is hardly affected because these situations occur only rarely.

# 8.3.14 Further extensions to individual pitch control

Another theoretical possibility for individual pitch control is for actually generating yawing loads in response to measured yaw misalignment, to keep the turbine pointing into the wind without the use of a yaw motor. A yaw moment can easily be generated, simply by setting a non-zero set-point for one of the PI controllers. However, it is unlikely that the yaw motor can be dispensed with completely, as it will probably be needed to yaw the nacelle while the rotor is not turning, and also for cable unwinds, etc., so it may be better simply to use the individual pitch control with zero set-point to minimise the yaw moment that the yaw actuator has to overcome.

It is also possible that the d-q axis loads could help to infer rotor averaged yaw misalignment, conceivably leading to better yaw control than just using the wind vane.

Nodding moments can be generated in the same way as yaw moments by setting a non-zero set-point: this could possibly be used for damping of higher fore–aft tower modes, or to help stabilise soating turbines (Namik and Stol 2010). Some damping of side–side tower vibration is also possible by means of azimuth-dependent individual pitch control responding to side–side acceleration (Fischer et al. 2010). Any of these applications would of course compromise the reduction of blade fatigue loads.

# 8.3.15 Commercial use of individual pitch control

Although the benerts of individual pitch control have been clear for some time, the small but repetitive motion required of the pitch bearings is unusual; although it can help to prevent some types of bearing wear such as brinelling, uncertainty about its long-term effect on bearing life was a factor in the slow initial uptake of individual pitch control by some wind turbine manufacturers. While it makes little sense as an add-on to an existing design, new commercial designs benert from the reduced loads in two main ways:

• Some existing designs have been uprated or the rotor diameter increased, with individual pitch control being added at the same time to keep the loads within the existing design envelope, resulting in higher energy capture with minimal redesign of components and hence minimal change in capital cost.   
• Some completely new turbines are now designed with individual pitch control from the start, leading to lower component costs. The signircant change in the loading regime gives scope to re-optimise the whole design.

Also, now that older wind farms are approaching the end of their design lives, there may be a case for retrortting individual pitch control to the turbines as a way to extend their lifetime.

Individual pitch control may also rnd a place in wind farm control, to mitigate any additional loading caused by yawing turbines for wake steering control (see Chapter 9).

# 8.3.16 Estimation of rotor average wind speed

Wind turbines usually have a nacelle-mounted anemometer, but while knowledge of the wind speed might seem useful for the controller, the control schemes described above do not make use of the anemometer, because it provides a point measurement rather than a rotor average, and because it is located in highly disturbed sow behind the rotor. It is used for supervisory control actions, especially when the turbine is not operating, such as for deciding whether the wind speed is within range for initiating a turbine start-up, or too low for yaw control to be useful (because the wind direction becomes extremely variable in very low winds). When the turbine is operating, the rotor itself makes a better anemometer. The pitch and torque control schemes described above use the rotor speed as input, and high wind shut-down, for example, can be triggered on the basis of the pitch angle, which makes a useful proxy for the wind speed in that situation. Nevertheless, a direct estimate of rotor average wind speed can be useful in some situations: one of these is for the bias terms described in Section 8.3.4. Another is for delta control, where the power production of the turbine is reduced to suit grid system requirements (Section 9.4.1); an estimate of the wind speed is useful for knowing how much power the turbine would have been producing if operating normally.

A simple way to estimate wind speed using the known function $F ( \lambda ) = C _ { q } ( \lambda ) / \lambda ^ { 2 }$ is outlined in Section 8.3.2 for below rated conditions. This can be extended to work at any pitch angle $\beta$ using $F ( \lambda , \beta ) = C _ { q } ( \lambda , \beta ) / \lambda ^ { 2 }$ . However, a given value of F may yield more than one possible value for the tip speed ratio 휆, making the method less straightforward to implement. A useful estimator can be constructed instead using a Luenberger observer of the form

$$
U _ {k} ^ {*} = U _ {k - 1} ^ {*} + K (\dot {\Omega} _ {k} - \dot {\Omega} _ {k} ^ {*}) \tag {8.22}
$$

at timestep k, where U denotes wind speed, $\dot { \varOmega }$ is the rotor acceleration (obtained by differentiating the measured rotor speed with some rltering to prevent noise), and \* denotes an estimate. Using the same notation as in Section 8.3.2, and omitting subscript k, we can combine Eqs. (8.2) and (8.6) to give

$$
\dot {\Omega} = \left(^ {1} / _ {2} \rho \pi R ^ {3} C _ {q} U ^ {2} - G Q _ {g}\right) / I \tag {8.23}
$$

Differentiating with respect to U gives $\Delta \dot { \varOmega } = C \Delta U$ where the factor C is given by

$$
C = \rho \pi R ^ {3} (2 C _ {q} U + U ^ {2} d C _ {q} / d U) / 2 I \tag {8.24}
$$

C can be calculated at each step from the latest estimated values, i.e. $\boldsymbol { U } ^ { * } , \boldsymbol { \lambda } ^ { * } = \boldsymbol { \varOmega } \boldsymbol { R } / \boldsymbol { U } ^ { * }$ and $C _ { q } ( \lambda ^ { * } , \beta )$ , and the derivative can be approximated numerically. Then the prediction error $e \overset { \cdot } { = } U - U ^ { * }$ will obey

$$
\Delta e _ {k} = (1 - K C) \Delta e _ {k - 1} \tag {8.25}
$$

If we aim for a response with time constant 휏 (of the order of a second, say, depending on the application), then integrating over one time step of length T gives $1 - K C = e ^ { - T / \tau }$ . From this we obtain the Kalman gain $K = ( 1 - e ^ { - T / \tau } ) / C$ . This is evaluated at each time step, and used together with $\dot { \varOmega } ^ { * }$ (using Eq. (8.23) with latest estimated values) to update the estimate of U using Eq. (8.22). However, C may become positive or negative, and if it gets close to zero, the estimator becomes unstable. A pragmatic solution is to multiply K by a function like $( C / C _ { 0 } ) ^ { 2 }$ whenever $C < C _ { 0 } .$ , to ensure that it crosses zero smoothly, where $C _ { 0 }$ is a small value chosen such that |C| is almost always greater than $C _ { 0 }$ .

# 8.3.17 LiDAR-assisted control

In recent years, the development of LiDAR (light detection and ranging) systems for laser Doppler anemometry has reached the point where these devices can be used effectively for wind speed measurements at a distance. A laser beam is emitted by the unit, and resections returned from small particles or aerosol droplets carried in the air are detected. The Doppler shift in frequency between the outgoing beam and the resected signal allows the speed of the resecting particle, and hence the wind speed, to be determined quite accurately. By means of a scanning laser beam, a signircant volume of space can be sampled, and the changing beam angle can help in estimating the wind vector rather than just its component in the beam direction. Alternatively, multiple beams can be used.

Ground based LiDARs are now being used as an alternative to meteorological masts for site wind speed assessment, and soating LiDARs are especially useful offshore where met mast installation is very expensive. A forward-pointing LiDAR on the turbine nacelle has a number of advantages for power curve measurements compared to a rxed mast. The possibility to use a nacelle-mounted LiDAR to scan the approaching wind reld in front of the turbine for the purposes of improving the control has been suggested many times over the years, and is now a possibility. The cost of these devices is still substantial, but LiDAR-assisted control may be worthwhile if sufrcient gains can be demonstrated, especially for large turbines where the cost of the LiDAR is a smaller proportion of the total. This section considers the possibilities of LiDAR-assisted wind turbine control.

A continuous-wave LiDAR focusses its beam on a sampling volume a certain distance away, with the length of the sampling volume determined by the lens area. Simley et al. (2011) consider how this may be used for wind turbine control. In contrast, a pulsed LiDAR sends out short pulses, allowing it to measure the time before the resected signal is received, from which the distance to the resecting particle is calculated; by analysing the Doppler shift for different ‘range gates’, the wind speed can be measured simultaneously at a number of distances along the beam. With either type, to sample the approaching wind over the rotor swept area requires either scanning or multiple beams. A wind turbine simulation model that includes turbulence and a detailed representation of any particular LiDAR characteristics can be used to investigate the effectiveness of different LiDAR conrgurations for various possible control applications (Bossanyi et al. 2012b). Good coverage of the rotor swept area is clearly important, whether this is achieved by one scanning beam or by multiple rxed beams. Multiple sampling distances along the angled beam(s) also help improve coverage. However, there is inevitably some trade-off between the number of points sampled and the time taken to sample them all. A sharply focussed measurement is not necessarily advantageous, perhaps because a more distributed sample along an angled beam is representative of more of the swept area, even though the resolution in terms of look-ahead time will be less precise. An accelerometer can be used to correct the measurement for the effect of tower motion. Different mounting options are possible, with generally similar performance. A spinner-mounted LiDAR has the advantage of avoiding beam blockage by the rotating blades, and correcting the measurements for shaft tilt and rotor azimuth is not difrcult. Even rxed blade-mounted beams at about two-thirds span, with a slow circular scan from the rotor rotation, can be effective despite the changing blade pitch angle.

![](images/dc15927b786603ed7b67a10a4ee6af06e6d2698d4b3ee65ed1ec1077f3811e90.jpg)

<details>
<summary>scatter</summary>

| x    | y    |
| ---- | ---- |
| -50  | -20  |
| 0    | -10  |
| 50   | 0    |
| 100  | 10   |
| 150  | 20   |
</details>

Figure 8.13 Possible LiDAR scanning pattern: a rve-lobed cycloidal scan is shown, with 40 sampling points per scan at three measurement distances

Figure 8.13 illustrates a possible scanning pattern for a nacelle- or spinner-mounter LiDAR. Note that the coverage of rotor area decreases for measurement points closer to the rotor. Current commercially available conrgurations currently include a circular scan with 50 points per scan or four rxed beams, although much more complex scan patterns are sometimes used for research purposes.

LiDAR measurements can be much more representative of the wind that the rotor experiences than the conventional nacelle-mounted anemometer and wind vane, because they can sample much more of the rotor swept area, and because they measure the ‘clean’ incoming wind reld. In contrast, the conventional instruments measure at a single point that is behind the rotor, and thus highly disturbed by the passage of the rotating blades and by the hub and nacelle. In addition, the LiDAR measurement provides a preview of the approaching wind speed before it reaches the turbine, potentially allowing the controller to anticipate gusts rather than reacting once the effect of the gust has already been felt; but the further ahead the measurement is, the more the wind will have changed by the time it reaches the turbine. Measurements closer to the turbine will need greater beam angles to cover the rotor area, leading to poorer estimation of the longitudinal wind component, but better estimation of transverse components and hence wind direction.

Four main ways in which these LiDAR characteristics could potentially improve wind turbine control have been investigated, as described in the following paragraphs.

Collective pitch control: Above rated, LiDAR preview of approaching wind speed changes can improve collective pitch control, by avoiding the delays caused by rrst having to measure the change in rotor speed and by the response time of the pitch system. This has clear potential to reduce particularly the thrust-related loads. A very simple feed-forward scheme can be used in which a pitch rate demand, calculated to move the pitch to the steady-state angle corresponding to the preview wind speed by the time this reaches the turbine, is simply added on to the normal pitch rate demand from the closed-loop feedback controller (Section 8.3.3). This can signircantly improve the speed regulation, with rotor speed variations reduced by a factor of 2 or more. This may be of some benert in itself, but more importantly, the gain of the feedback controller can then be reduced, so as to leave the tightness of the speed control unchanged, but allowing the amount of pitch activity to reduced, with a consequent reduction in fore–aft tower vibration. This has the potential to reduce tower base fatigue loading by around 20%, and out-of-plane blade root fatigue by about 5%. For a fatigue-driven design, this could signircantly reduce capital cost, particularly of the tower.

Individual pitch control: LiDAR measurement of wind shear gradients can be used as a feed-forward input to an individual pitch controller instead of using strain gauges. Good coverage of the rotor swept area is important. In this case, the preview shows no clear benert, however, and the control action may be no better than using conventional feedback control with blade root strain gauges, for example, which have the advantage of directly measuring the loads that are to be controlled. Using LiDAR and strain gauges in combination can give slightly better load alleviation, but the improvement may be too small to justify the additional expense and complexity of the LiDAR, unless it is already there for other reasons.

Optimum $C _ { P }$ tracking: Below rated, the torque control, which is attempting to maintain the optimum tip speed ratio, can anticipate changes by planning a rotor speed trajectory that maximises energy capture, taking into account the effect of the large rotor inertia on the rate of acceleration and deceleration. As with other methods of tighter $C _ { \mathfrak { p } }$ tracking, a very slight increase in energy capture is probably achievable, but only at the expense of prohibitive increases in the variation of power and drive-train torque needed to accelerate and decelerate the rotor.

Yaw control: For the reasons described above, the LiDAR provides a cleaner and more representative measurement of the wind direction relative to the nacelle, and may avoid the calibration errors and drift and the need for heavy averaging when a wind vane is used. However, yaw control has to be slow to prevent excessive yaw system duty, so if the wind vane is well calibrated, the advantage of using LiDAR may not be great, and the preview of a few seconds is of little value. Nevertheless, it is not easy to calibrate a wind vane to the required accuracy, especially as the calibration should depend on rotor speed and pitch angle (Kragh et al. 2013), so the use of LiDAR might be worthwhile, especially if it is installed anyway for other reasons, such as pitch control. A spinner anemometer (Friis Pedersen and Arranz 2018), consisting of a triple sonic anemometer mounted on the spinner, might provide a better compromise between cost and effectiveness. Of course, a LiDAR could be used temporarily for initial wind vane calibration, but a suitable mounting would be needed, and the wind vane calibration can easily drift afterwards, or change due to unintentional movement.

Depending on site conditions, the LiDAR signal may not always be available or reliable enough. This can happen if the air is so clean that there are not enough particles to give a sufrcient resected signal, or if thick fog or heavy precipitation disrupts the signal. In this situation, the control must switch back to standard or ‘safe’ mode, not using the LiDAR. The implications for fatigue load reduction are straightforward to assess: the fatigue load reduction can simply be factored by the proportion of time for which the LiDAR signal is expected to be available, in each wind condition. If used for yaw control, the controller would switch back to using the wind vane.

LiDAR-assisted control can reduce fatigue loads and hence the cost of components whose design is fatigue load driven, but for a component whose design is driven by extreme operational gust loads, the cost can only be reduced by LiDAR-assisted control if it can be relied upon to respond appropriately to the specirc extreme gust. However, it is not possible to know the exact characteristics of the extreme gust that a turbine will see. Some extreme coherent gusts are derned in the International Electrotechnical Commission (IEC) standards, but these are not physically realistic, and do not specify how the gust might advect and evolve between being measured by the LiDAR and arriving at the rotor. It is even possible that the LiDAR-assisted controller, with its reduced feedback gains, might exacerbate the extreme load if it fails to detect the gust properly – for example, if the gust is not advecting with the mean sow.

If extreme loads are calculated by statistical extrapolation, the probable effect of the LiDAR on the extreme load can be assessed by comparing extrapolations from simulations with and without LiDAR (Bossanyi et al. 2012b).

It is also necessary to take into account the possibility that the LiDAR signal is not available at the moment of the extreme gust. If this is due to a LiDAR fault, a gust with a lower return period can be used, but if it is due to atmospheric conditions, either thick fog or clean air providing very little resected signal, the controller would have switched to its standard or ‘safe’ mode where no load reduction is possible.

# 8.3.18 LiDAR signal processing

A LiDAR beam only measures the component of wind speed along the beam direction. With a scanning beam or a LiDAR with multiple rxed beams, the beam angle at each measurement point is different. Therefore, if an assumption is made that the sow reld over the whole rotor can be characterised by a given set of parameters – for example, mean wind speed, direction, and a vertical wind shear prorle – then these parameters can be estimated by combining the measurements from each point, as long as there are at least as many points as parameters to estimate. If the number of points equals the number of parameters, a set of simultaneous equations can be solved to give the parameters. If there are more measurement points, a least squares rt can be used. Five parameters are often considered to characterise the sow: speed (for collective pitch control), direction (for yaw control), vertical and horizontal shear gradients (for individual pitch control), and possibly the upsow angle. Assuming these parameters are the same over all of the measurement points, the component of wind speed along the beam can be calculated for each measurement point, as a function of these parameters. The parameters values that minimise the root-mean-square differences between the calculated and measured velocities can then be calculated.

However, with a single LiDAR source, it is not possible to directly distinguish between direction and horizontal shear, or between vertical shear and upsow (the so-called ‘cyclops dilemma’), unless further assumptions are made (for example, that the direction changes more slowly than the horizontal shear, or that the upsow angle is known from the terrain). More complex approaches take account of time variation or measurements at multiple distances, and may make further assumptions about mass conservation or compliance with simplired Navier–Stokes equations.

By using three LiDAR beams emanating from different points and controlled to converge at a single measurement point, all three components of velocity at that point can be calculated. This measurement point can be caused to scan around by scanning the three beams in a coordinated fashion, as, for example, with the DTU Windscanner (Vasiljevic´ et al. 2017).

# 8.4 Closed-loop control: analytical design methods

Clearly the choice of controller gains is crucial to the performance of the controller. With too little overall gain, the turbine will wander around the set-point, while too much gain can make the system completely unstable. Inappropriate combinations of gains can cause structural responses to become excited. This section outlines some of the techniques that have been found useful in designing closed-loop control algorithms for wind turbines, such as the gains of a PI or PID controller, for example. Clearly it is only appropriate here to give some useful hints and pointers. There are many standard texts on control theory and controller design methods to which the reader should refer for more detailed information, for example, D’Azzo and Houpis (1981), Anderson and Moore (1979), and Astrom and Wittenmark (1990).

# 8.4.1 Classical design methods

A linearised model of the turbine dynamics is an essential starting point for controller design. This allows various techniques to be used for rapidly evaluating the performance and stability of the control algorithm. Detailed non-linear simulations using a three-dimensional turbulent wind input should then be used to verify the design before it is implemented on the real turbine.

For a variable-speed turbine below rated wind speed, a PI speed controller using demanded torque can be quite slow and gentle, and the linearised model can be very simple. It must include the rotational dynamics of the drive train, but other dynamics are not usually important. For pitch control however, the aerodynamics of the rotor and some of the structural dynamics can be critical. The linearised model for pitch controller design should contain at least the following dynamics:

• Rotor and generator rotation.   
• Tower fore–aft vibration.   
• Power or speed transducer response.   
• Pitch actuator response.

The generator characteristics are also necessary for rxed-speed systems, and drive train torsion is particularly important for variable-speed turbines. In all cases a linearised description of the aerodynamics of the rotor is required – for example, as a set of partial derivatives of torque and thrust with respect to pitch angle, wind speed, and rotor speed. The thrust is important because it affects the tower dynamics, which couple strongly with pitch control.

![](images/7d7aee97d74709eb0aa9fa5f861e9fe0da98df79dbb615868c6e44aa54ff7397.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Wind"] --> B["Aerodynamic partial derivatives"]
    B --> C["Tower"]
    C --> D["Thrust"]
    B --> E["Drive train"]
    E --> F["Generator"]
    F --> G["Transducer"]
    G --> H["Set-point"]
    H --> I["Error"]
    I --> J["Control algorithm"]
    J --> K["Pitch demand"]
    K --> L["Pitch actuator"]
    L --> M["Pitch angle"]
    M --> B
    E --> N["Torque speed"]
    N --> E
    E --> O["Torque demand (variable speed)"]
    O --> J
    style A fill:#f9f,stroke:#333
    style H fill:#ccf,stroke:#333
```
</details>

Figure 8.14 Typical linearised turbine model

![](images/7292820923487f36a169d802a926c1c9563de97cec77615a698bbf2bc2ee9e86.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Set-point"] --> B["+"]
    B --> C["k.C(s)"]
    C --> D["G(s)"]
    D --> E["Measured output"]
    E --> F["Feedback Loop"]
    F --> B
```
</details>

Figure 8.15 Simplired general model of plant and controller

A typical linear model is shown in Figure 8.14. With such a linear model, it is then possible to vary the gains and other parameters, and then rapidly carry out a number of tests that help to evaluate the performance of the controller with those gain settings. Some of these tests are open-loop tests, which means they are applied to the open-loop system obtained by breaking the feedback loop; for example, at the symbol X in Figure 8.14. Other tests are carried out on the closed-loop system. Before describing some of these tests, some basic theory on open and closed-loop dynamics is outlined.

Figure 8.15 shows a simplired general model in which the turbine (i.e. from pitch actuator to transducer in Figure 8.14) is represented by the ‘plant model’ with transfer function $\mathrm { G } ( \mathrm { s } )$ , and the control algorithm is represented by the controller transfer function $\operatorname { k } . \mathrm { C } ( \operatorname { s } )$ , where s is the Laplace variable and k an overall controller gain.

Now the open-loop system can be represented by the transfer function k. $\mathrm { C ( s ) . G ( s ) = H ( s ) }$ . If the input to the transfer function is denoted x and the output is y, then $\mathrm { Y ( s ) = H ( s ) . X ( s ) }$ , where $\mathbf { X } ( \mathbf { s } )$ and $\mathrm { Y } ( \mathrm { s } )$ are the Laplace transforms of x and y. When the loop is closed at X the closed-loop dynamics can be derived as

$$
\mathrm{Y} ^ {\prime} (\mathrm{s}) = \mathrm{H} (\mathrm{s}) (\mathrm{X} (\mathrm{s}) - \mathrm{Y} (\mathrm{s})) \tag {8.26}
$$

where $\mathrm { Y ^ { \prime } } ( \mathrm { s } )$ is the Laplace transform of the closed-loop output y’. This can be rewritten as

$$
\mathrm{Y} ^ {\prime} (\mathrm{s}) = \frac {\mathrm{H} (\mathrm{s})}{1 + \mathrm{H} (\mathrm{s})} \mathrm{X} (\mathrm{s}) \tag {8.27}
$$

In other words, if the open-loop system is H(s), the closed-loop system will have dynamics represented by $\mathrm { H ^ { \prime } ( s ) } = \mathrm { H ( s ) } / \left( 1 + \mathrm { H ( s ) } \right)$ .

Now a linear transfer function can be expressed as the ratio of two polynomials in s. Thus, for the open-loop system, $\mathrm { \bf A ( s ) } \mathrm { \bf Y ( s ) } = \mathrm { \bf B ( s ) } \mathrm { \bf X ( s ) }$ , and so $\mathrm { H } ( \mathrm { s } ) = \mathrm { B } ( \mathrm { s } ) / \mathrm { A } ( \mathrm { s } )$ , where $\mathbf { A } ( \mathbf { s } )$ and B(s) are polynomials in s. The roots of the polynomial $\mathbf { A } ( \mathbf { s } )$ give important information about the system response. Consider, for example, a rrst order system

$$
\tau \dot {y} _ {1} = x - y _ {1} \tag {8.28}
$$

representing a rrst order lagged response of ${ \mathrm { y } } _ { 1 }$ with respect to x. This system can be represented by the transfer function

$$
\mathrm{H} (\mathrm{s}) = \frac {\mathrm{B} (\mathrm{s})}{\mathrm{A} (\mathrm{s})}, \text { where } \mathrm{B} (\mathrm{s}) = 1 \text { and } \mathrm{A} (\mathrm{s}) = 1 + \tau s \tag {8.29}
$$

The single root of A(s) is given by $\sigma = - 1 / \tau$ , while Eq. (8.28) has solutions of the form $y = a + b e ^ { \sigma t }$ , with $\sigma = - 1 / \tau$ again. These solutions are stable if 휏 is positive – in other words, if the root of A(s) is negative. A second order system will have solutions of the form $y = a + b e ^ { \sigma _ { 1 } t } + c e ^ { \sigma _ { 2 } t }$ , where once again $\sigma _ { 1 }$ and $\sigma _ { 2 }$ are the roots of the second order polynomial that forms the denominator of the transfer function. Now $\sigma _ { 1 }$ and $\sigma _ { 2 }$ may be real numbers or they may form a complex conjugate pair ${ \sigma \pm \mathrm { j } \omega }$ . The solutions are stable if $\sigma _ { 1 }$ and $\sigma _ { 2 }$ are both negative, or if 휎 is negative. In general, it can be stated that a linear system is stable if all of the roots of the denominator polynomial have negative real parts. These roots are known as the poles of the system, and they represent values of the Laplace variable that make the transfer function inrnite. The roots of the numerator polynomial are known as the zeros of the system, because the transfer function is zero at these points.

Now let us rewrite Eq. (8.27) in terms of the polynomials A and B:

$$
\mathrm{Y} (\mathrm{s}) = \frac {\mathrm{B} (\mathrm{s})}{\mathrm{A} (\mathrm{s}) + \mathrm{B} (\mathrm{s})} \mathrm{X} (\mathrm{s}) = \frac {\mathrm{k.B} ^ {\prime} (\mathrm{s})}{\mathrm{A} (\mathrm{s}) + \mathrm{k.B} ^ {\prime} (\mathrm{s})} \mathrm{X} (\mathrm{s}) \tag {8.30}
$$

where we have reintroduced the overall controller gain k such that $\mathbf { B } ( \mathrm { s } ) = \mathrm { k } . \mathbf { B } ^ { \prime } \left( \mathrm { s } \right)$ . Clearly when the gain k is small, the closed-loop transfer function tends towards the open-loop transfer function k.B′ /A. However, when the gain is large, A can be neglected and so the poles will tend towards the roots of $\mathbf { B ^ { \prime } }$ . In other words, as the gain increases from zero to inrnity, the poles of the closed-loop system move from the open-loop poles and end up at the open-loop zeros. They move along complicated trajectories in the complex plane. A plot of these trajectories is known as a root locus plot, and is very useful for helping to select the feedback gain k. The gain is selected such that all of the closed-loop poles are in the left half-plane, making the system stable, and preferably as well damped as possible. The damping factor for a pole pair at $\sigma \pm \mathrm { j } \omega = \mathrm { r e } ^ { \mathrm { j } \theta }$ is given by $- \mathrm { c o s } ( \theta ) = - \sigma / \mathrm { r } ,$ as shown in Figure 8.16.

Figure 8.17 shows an example of a root locus plot for a variable-speed pitch controller. As the gain increases, the closed-loop poles (+) move from the open-loop poles (x), corresponding to zero feedback gain, to the open-loop zeros (O). (Actually there are usually more poles than zeros; the ‘missing’ zeros can be considered to be equally spaced around a circle of inrnite radius.) In this example, the gain has been chosen to maximise the damping of the lightly damped tower poles (B). Any further increase in gain would exacerbate tower vibration, eventually leading to instability as the poles cross the imaginary axis. At the chosen gain, the controller poles (A) are well damped. The poles at (C) result from the pitch actuator dynamics. They remain sufrciently well damped, although again, excessive gain would drive them to instability.

![](images/ccfd5066c24d4b3396a0247b3c8a70a586d30f3f1fda25901273b83f112a5bca.jpg)

<details>
<summary>text_image</summary>

r
ω
-σ
θ
</details>

Figure 8.16 Damping ratio for a complex pole pair

![](images/e60b0134d6eabdcf5d407bc98d26a3a7ef0cf75addce8f4d6a72bb8beab88fce.jpg)

<details>
<summary>scatter</summary>

| Point | Real axis | Imaginary axis |
|-------|-----------|----------------|
| A     | -0.5      | 0.2            |
| B     | -0.2      | 1.5            |
| C     | -1.2      | 2.3            |
| A     | -0.8      | 0.3            |
| B     | -0.1      | -1.5           |
| C     | -1.0      | -2.2           |
</details>

Figure 8.17 Example root locus plot for a variable-speed pitch controller

Although a root locus plot is useful for helping to select the overall controller gain, this can only be done once the other parameters derning the controller have been rxed. A PI controller (Eq. 8.1 with $\mathrm { k _ { d } } = 0 )$ is characterised by only two parameters, $K _ { p }$ and $K _ { i } .$ . It can be re-written as

$$
y = K _ {p} \left(1 + \frac {1}{s T _ {i}}\right) x \tag {8.31}
$$

where $T _ { i } = K _ { p } / K _ { i }$ is known as the integral time constant. The root locus plot can be used to select $K _ { p }$ once $T _ { i }$ has been derned, but the shape of the loci will change with different $T _ { i }$ . However, it is relatively straightforward to iterate on the value of $T _ { i }$ , using the root locus plot each time to select $K _ { p } ,$ , until a suitable overall performance is achieved, using criteria such as those listed below. In the case of PID and more complex controllers, where more than two parameters must be selected, other ways must be found to select the parameters, although it is always possible to use a root locus plot for the rnal choice of the overall gain.

The choice of parameters will usually be an iterative process, often using a certain amount of trial and error, and on each iteration the performance of the resulting controller must be assessed. Useful measures of performance include:

Gain and phase margins: These are calculated from the open-loop frequency response, and give an indication of how close the system is to instability. If the margins are too narrow, the system may tend to become unstable. The system will be unstable if the open-loop system displays a $1 8 0 ^ { \circ }$ phase lag with unity gain. The phase margin represents the difference between the actual phase lag and $1 8 0 ^ { \circ }$ at the point where the open-loop gain crosses unity. A phase margin of at least $4 5 ^ { \circ }$ is usually recommended, although there is no rrm rule. Similarly, the gain margin represents the amount by which the open-loop gain is less than unity where the open-loop phase lag crosses 180∘ . A gain margin of at least a few decibels is recommended.   
• The cross-over frequency, which is the frequency at which the open-loop gain crosses unity, gives a useful measure of the responsiveness of the controller.   
• The positions of the closed-loop poles of the system indicate how well various resonances will be damped.   
• Closed-loop step responses – for example, the response of the system to a step change in wind speed– give a useful indication of the effectiveness of the controller. For example, in tuning a pitch controller, the rotor speed and power excursions should return rapidly and smoothly to zero, the tower vibration should damp out reasonably fast, and the pitch angle should change smoothly to its new value, without too much overshoot and without too much oscillation.   
• Frequency responses of the closed-loop system also give some very useful indications. For example, in the case of pitch controller: (i) The frequency response from wind speed to rotor speed or electrical power should die away at low frequencies, as the low frequency wind variations are controlled away. (ii) The frequency response from wind speed to pitch angle must die away at high frequencies and must not be too great at critical disturbance frequencies such as the blade passing frequency, or the drive train resonant frequency in variable-speed systems. (iii) The frequency response from wind speed to tower velocity should not have too large a peak at the tower resonant frequency, and so forth.

With experience, it is possible, by examining measures such as these, to converge rapidly on a controller tuning that will work well in practice.

# 8.4.2 Gain scheduling for pitch controllers

Close to rated wind speed, because the rne pitch angle is selected to maximise power, it follows that the sensitivity of aerodynamic torque to pitch angle is very small. Thus, a much larger controller gain is required here than at higher wind speeds, where small change in pitch can have a large effect on torque. Frequently the torque sensitivity changes almost linearly with pitch angle, and so can be compensated for by varying the overall gain of the controller linearly in inverse proportion to the pitch angle. Such a modircation of gain with operating point is termed a gain schedule. However, the sensitivity of thrust to pitch angle varies in a different way, and because of its effect on tower dynamics, which couples strongly with the pitch controller, it may be necessary to modify the gain schedule further to ensure good performance in all winds. In some cases just varying the overall gain may not be sufrcient to achieve satisfactory response at all operating points, in which case it may be necessary to change the proportional an integral gains separately, each as a different function of pitch angle.

It is therefore important to generate linearised models of the system corresponding to several different operating points between rated and cut-out wind speed, and to choose a gain schedule that ensures that the above performance measures are satisfactory over the whole range.

For an active stall controller, the pitch angle may not change much with operating point; a gain schedule may not be required, but if it is, it may have to be a direct function of wind speed rather than pitch angle. This is one of the few occasions when the nacelle anemometer signal may have to be used as an input to the controller.

# 8.4.3 Adding more terms to the controller

It is often possible to improve the performance of a basic PI or PID controller by adding extra terms to modify the behaviour in a particular frequency range.

For example, a pitch control algorithm may be found to cause a large amount of pitch actuator activity at a relatively high frequency, which is of little benert in controlling the turbine and may be quite counter-productive. This may occur if some dynamic mode was not taken into account in the linearised model that was used to design the turbine. An example of this is the drive train torsional resonance in a variable-speed turbine, which can feed through to the measured generator speed and hence to the pitch control, causing high frequency pitch activity that is of no benert. Another likely cause is the pitch response to a major external forcing frequency, such as the blade passing frequency. While a low pass rlter in series with the controller will certainly reduce high frequency response, the resulting phase shift at lower frequencies may signircantly impair the overall performance of the controller. A better ‘cure’ for excessive activity at some well-derned frequency is to include a notch rlter in series with the controller. A simple second order notch rlter tuned to rlter out a particular frequency of 휔 rad/s has a transfer function

$$
\frac {1 + s ^ {2} / \omega^ {2}}{1 + 2 \zeta s / \omega + s ^ {2} / \omega^ {2}} \tag {8.32}
$$

where the ‘damping’ parameter 휁 represents the width or ‘strength’ of the notch rlter. This should be increased until the rltering effect is sufrcient at the target frequency, without too much detriment to the control performance at lower frequencies.

Another useful rlter is the phase advance or phase lag rlter,

$$
\frac {(1 + s / \omega_ {1})}{(1 + s / \omega_ {2})} \tag {8.33}
$$

which increases the open-loop phase lag between frequencies $\omega _ { 1 }$ and $\omega _ { 2 } \ ( \omega _ { 1 } < \omega _ { 2 } )$ , or decreases it if $\omega _ { 1 } > \omega _ { 2 }$ . Phase advance can sometimes be useful for improving the stability margins. Open-loop gain and phase plots can, therefore, be useful for helping to select $\omega _ { 1 }$ and $\omega _ { 2 }$ . A PID controller can be rewritten as a PI controller in series with a phase advance (or phase lag) rlter.

A general second order rlter of the form

$$
\frac {1 + 2 \zeta_ {1} s / \omega_ {1} + s ^ {2} / \omega_ {1} ^ {2}}{1 + 2 \zeta_ {2} s / \omega_ {2} + s ^ {2} / \omega_ {2} ^ {2}} \tag {8.34}
$$

can sometimes be useful for modifying the frequency response in a particular area. With $\omega _ { 1 } = \omega _ { 2 }$ and $\zeta _ { 1 } = 0$ this is just a notch rlter, as described above. With $\zeta _ { 1 } > \zeta _ { 2 }$ the rlter has a bandpass effect, which can be used to increase control action at a particular frequency. With different $\omega _ { 1 }$ and $\omega _ { 2 }$ there is also a high-pass or low-pass effect, because the high-frequency gain tends towards $( \omega _ { 2 } / \omega _ { 1 } ) ^ { 2 }$ .

A root locus plot is often useful for investigating the effect of such rlters. With experience, the effect on the loci of placing the rlter poles and zeros in particular ways can be anticipated. Such techniques can help to see how, for example, a pair of lightly damped poles due to a structural resonance can be dragged further away from the imaginary axis, so as to increase the damping.

# 8.4.4 Other extensions to classical controllers

Other extensions to classical controllers have sometimes been used to further improve the performance in particular ways; for example, the use of non-linear gains and variable or asymmetrical limits.

Non-linear gains are sometimes used to penalise large peaks or excursions in controlled variables. For example, the gain of a PI pitch controller can be increased as the power or speed error increases; or, rather than changing the gain, an additional term can be added to the demanded pitch rate that may be a function of the error, its rate of change, or both. Often the additional term would be normally zero, increasing only in case of large deviations from the desired operating condition. The extra term can conveniently be added before the PI integrator (see Section 8.6.2). Such techniques should be used with caution, however, as too much non-linearity will drive the system towards instability, in much the same way as if the linear gain is too high. This technique requires a trial-and-error approach because it is very difrcult to analyse the closed-loop behaviour of non-linear systems using standard methods. Any asymmetry in the additional term, e.g. if used only when the power or speed is above the set-point to help reduce peaks, will cause a reduction in the mean power or speed relative to the set-point.

Asymmetrical pitch rate limits can also be used to reduce peaks. By allowing the blades to pitch faster towards feather than towards rne, power, or speed peaks will be reduced. Once again the mean level will also be reduced by introducing this asymmetry.

However, this technique is somewhat more ‘comfortable’ than the use of non-linear gains because it is less likely to lead to instability.

There is often a desire to reduce the set-point in high winds, to reduce the infrequent but highly damaging loads experienced in those conditions at the expense of a small loss of output. It is straightforward to reduce the set-point as a function of wind speed (the pitch angle is usually used as a measure of the rotor averaged wind speed, as for gain scheduling). However, the most damaging loads occur during high turbulence, and so it would be better to reduce the set-point in high winds only when the turbulence is also high. Rather than actually reducing the set-point, asymmetrical rate limits provide a simple but effective means of achieving this effect, because the rate limits will only be reached when the turbulence is high.

A further extension of this technique is to modify the rate limits dynamically, even to the extent of changing the sign of a rate limit to force the pitch in one direction during certain conditions such as large power or speed excursions. A useful application of this is in the control of variable-slip systems, where it is important to keep the speed above the minimum slip point (point B in Figure 8.8). If the speed falls below this point, it then ceases to vary much as it is constrained by the minimum slip curve, and so the proportional term in the PI controller ceases to respond. Modifying the rate limits as a function of speed error as in Figure 8.18 is a useful technique to prevent this happening. Another useful application is to force some temporary pitch action such as a pitch ramp in response to a severe gust: by ramping the pitch rate limits, perhaps in response to an unusually large rate of generator acceleration, the PI controller can continue to act, albeit constrained by the rate limits, so that it resumes normal duty seamlessly when the rate limits are relaxed again.

Another case for set-point modircation in high winds is to prevent a sudden loss of power arising from high wind cut-out (Bossanyi and King 2012). If an increase in wind speed can cause all of the turbines in a large wind farm to shut down suddenly within a few minutes, the network will have to cope with this by maintaining spinning reserve. Instead of shutting down suddenly at 25 m/s, ramping the power output down smoothly from full power to zero between, say, 24 and 35 m/s will result in a much lower probability of a sudden shortfall, and the wind farm output can be considered more predictable (Bossanyi 1982), both effects leading to lower spinning reserve requirements and hence a higher value for the generated power. This will have little effect on fatigue loading and energy yield because of the small number of hours involved, but the effect on extreme loads will need to be considered. For offshore turbines, where wave-induced tower vibration is better damped if the turbine is operating, extending the operating range to higher wind speeds may help to reduce tower loading (Markou and Larsen 2009).

![](images/f4dba0d1d269faa2186cb17a6a36beb656c410fad490ad762590912a13309a7c.jpg)

<details>
<summary>line</summary>

| Slip speed | Pitch rate limits |
| :--- | :--- |
| 1% | +10 % |
| 10% | +10 % |
| 10% | -10 % |
Set-point, e.g. 4% slip
</details>

Figure 8.18 Pitch rate limit modircation for a variable-slip wind turbine

# 8.4.5 Optimal feedback methods

The controller design methods described above are based on classical design techniques, and often result in relatively simple PI or PID algorithms together with various rlters in series or in parallel, such as phase shift, notch, or bandpass rlters, and sometimes using additional sensor inputs. These methods can be used to design fairly complex high order controllers, but only with a considerable amount of experience on the part of the designer.

There is, however, a huge body of theory (and practice, although to a lesser degree) relating to more advanced controller design methods, some of which have been investigated to some extent in the context of wind turbine control, for example:

• Self-tuning controllers.   
• Fuzzy logic controllers.   
• Neural network methods.

• Model based controllers such as LQG/optimal feedback, $\mathrm { H } _ { \infty }$ , or model predictive control.

Self-tuning controllers (Clarke and Gawthrop 1975) are generally rxed order controllers derned by a set of coefrcients, which are based on an empirical linear model of the system. The model is used to make predictions of the sensor measurements, and the prediction errors are used to update the coefrcients of the model and the feedback law.

If the system dynamics are known, then some very similar mathematical theory can be used, but applied in a different way. Rather than rtting an empirical model, a linearised physical model is used to predict sensor outputs, and the prediction errors are used to update estimates of the system state variables. These variables may include rotational speeds, torques, desections, etc. as well as the actual wind speed, and so their values can be used to calculate appropriate control actions even though those particular variables are not actually measured.

Observers: A subset of the known dynamics may be used to make estimates of a particular variable – for example, some controllers use a wind speed observer to estimate the wind speed seen by the rotor from the measured power and/or rotational speed and the pitch angle. The estimated wind speed can then be used to derne the appropriate desired pitch angle.

State estimators: Alternatively, using a full model of the dynamics, a Kalman rlter can be used to estimate all of the system states from the prediction errors (Bossanyi 1987). This technique can explicitly use knowledge of the variance of any stochastic contributions to the dynamics, as well as noise on the measured signals, in a mathematically optimum way to generate the best estimates of the states. This relies on an assumption of Gaussian characteristics for the stochastic inputs. Thus it is possible explicitly to take account of the stochastic nature of the wind input by formulating a wind model driven by a Gaussian input. This can even be extended to include blade passing effects.

The Kalman rlter can readily take account of more than one sensor input in generating its ‘optimal’ state estimates. Thus it is ideal for making use of, for example, an accelerometer measuring tower fore–aft motion as well as the normal power or speed transducer. It would be straightforward to add other sensors, if available, to improve the state estimates further.

Optimal feedback: Knowing the state estimates, it is then possible to derne a cost function, which is a function of the system states and control actions. The controller objective can then be derned mathematically: the objective is to minimise the selected cost function. If the cost function is derned as a quadratic function of the states and control actions (which is actually a rather convenient formulation), then it is relatively straightforward to calculate the ‘optimal’ feedback law. This is derned as the feedback law that generates control signals as a linear combination of the states such that the cost function will be minimised. Because a linear model is required, with a quadratic cost function and Gaussian disturbances, this is known as an LQG controller.

This cost function approach means that the trade-off between a number of partially competing objectives is explicitly derned, by selecting suitable weights for the terms of the cost function. This makes such a method ideal for a controller that attempts to reduce loads as well as achieving its primary function of regulating power or speed. Although it is not practical to calculate the weightings in the cost function rigorously, they can be adjusted in a very intuitive way. This approach is also readily conrgured for multiple inputs and outputs, so, for example, as well as using generator speed and tower acceleration inputs, it can in principle simultaneously produce the pitch demand and torque demand outputs that will minimise the cost function.

Figure 8.19 illustrates the structure of the LQG controller, showing the state estimator and the optimal state feedback. For implementation, the entire controller can be reduced to a set of difference equations connecting the measured outputs (y) to the new control signals (u). This means that once the design is completed, the algorithm is easy to implement and does not require massive processing power.

![](images/0f49a03a7bfb956cd64601ba7db06d74278d322d4eb79116138a4d716b688f19.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["x(k-1)"] --> B["Turbine dynamics"]
    C["u(k-1)"] --> B
    D["y(k-1)"] --> E["Correction"]
    B --> E
    E --> F["Optimal state feedback"]
    F --> G["u(k)"]
    G --> H["Cost function J = x^T.P.x + u^T.Q.u"]
    I["x'(k)"] --> J["×"]
    K["y'(k-1)"] --> L["×"]
    M["x(k)"] --> N["×"]
    O["y(k-1) = measured signals"] --> P["y = predicted measurements"]
    Q["x = state estimates"] --> R["y' = predicted measurements"]
    S["x' = predicted states"] --> T["x' = predicted states"]
    U["u = control signals"] --> V["u(k)"]
```
</details>

Figure 8.19 Structure of the LQG controller

The linearised dynamics of the system are expressed in discrete state-space form:

$$
\mathrm{x} ^ {\prime} (\mathrm{k}) = \mathrm{Ax} (\mathrm{k} - 1) + \mathrm{Bu} (\mathrm{k} - 1) \tag {8.35}
$$

The Kalman gain L is calculated taking into account the stochastic disturbances affecting the system, and allows the state estimates to be improved by comparing the predicted sensor outputs $\mathrm { y ^ { \ast } }$ to the actual outputs y:

$$
\mathrm{x} (\mathrm{k}) = \mathrm{x} ^ {\prime} (\mathrm{k}) + \mathrm{L} (\mathrm{y} (\mathrm{k} - 1) - \mathrm{y} ^ {\prime} (\mathrm{k} - 1)) \tag {8.36}
$$

where

$$
\mathrm{y} ^ {\prime} (\mathrm{k} - 1) = \mathrm{Cx} (\mathrm{k} - 1) + \mathrm{Du} (\mathrm{k} - 1) \tag {8.37}
$$

The optimal state feedback gain K generates the control actions

$$
\mathrm{u} (\mathrm{k}) = - \mathrm{Kx} (\mathrm{k}) \tag {8.38}
$$

where K is calculated such that the quadratic cost function J is minimised. The cost function is

$$
\mathrm{J} = \mathrm{x} ^ {\mathrm{T}} \mathrm{Px} + \mathrm{u} ^ {\mathrm{T}} \mathrm{Qu} \tag {8.39}
$$

(actually the integral, or the mean value over time, or the expected value of this quantity). P and Q are the state and control weighting matrices. It is usually more useful to derne the cost function in terms of other quantities, v, which can be considered as extra (often unmeasured) outputs of the system:

$$
\mathrm{v} = \mathrm{C} _ {\mathrm{v}} \mathrm{x} + \mathrm{D} _ {\mathrm{v}} \mathrm{u} \tag {8.40}
$$

Hence the cost function is

$$
\mathrm{J} = \mathrm{v} ^ {\mathrm{T}} \mathrm{Rv} + \mathrm{u} ^ {\mathrm{T}} \mathrm{Su} = \mathrm{x} ^ {\mathrm{T}} \mathrm{C} _ {\mathrm{v}} ^ {\mathrm{T}} \mathrm{RC} _ {\mathrm{v}} \mathrm{x} + \mathrm{u} ^ {\mathrm{T}} \mathrm{D} _ {\mathrm{v}} ^ {\mathrm{T}} \mathrm{RD} _ {\mathrm{v}} \mathrm{u} + \mathrm{u} ^ {\mathrm{T}} \mathrm{Su} \tag {8.41}
$$

so that $\mathrm { P = C _ { v } ^ { \phantom { } T } R C _ { v } }$ and $\mathrm { Q } = \mathrm { D } _ { \mathrm { v } } ^ { \ \mathrm { T } } \mathrm { R } \mathrm { D } _ { \mathrm { v } } + \mathrm { S } .$ .

Another possibility is to generate optimal control signals directly as a function of the sensor outputs. This is known as optimal output feedback (Steinbuch 1989). However, the mathematical solution of this problem is based on necessary conditions for optimality that are not always sufScient for optimality. Therefore, the solutions generated can be, and in practice often are, non-optimal and potentially very far from optimal. This variation is therefore rather problematic.

As turbines become larger and the requirements placed on the controller become more demanding, advanced control methods such as LQG are likely to become increasingly used, although as yet there are few published examples of the practical application of these techniques in commercial wind turbines. However, this approach was used to design a controller for a 300 kW rxed-speed two bladed teetered turbine in the UK in 1992. After testing on a prototype turbine in the reld, this controller was shown to give signircant reductions in pitch activity and power excursions compared to the original PI controller, and it was subsequently adopted for the production machine and successfully used on over 70 turbines (Bossanyi 2000). Stol and Fingersh (2004) reported tests with a similar control scheme on a 600 kW research turbine.

LQG controllers are not necessarily robust, which means that they can be sensitive to errors in the turbine model. A similar approach is the $\mathrm { H } _ { \infty }$ controller, in which uncertainties in the turbine and wind models can explicitly be taken into account. Such a controller was evaluated in the reld on a 400 kW rxed-speed pitch-regulated turbine by (Knudsen et al. 1997), who reported a reduction in pitch activity and some potential for reduced fatigue loads compared to a PI controller.

# 8.4.6 Pros and cons of model based control methods

The methods of Section 8.4.5 are appealing as they use mathematical rigour to calculate an ‘optimal’ controller in the sense that it minimises a pre-derned and reasonably intuitive cost function, suggesting that the tuning could be an automatic process, whereas the classical approach relies on the skill and experience of the designer for each new tuning. They are also ideal for designing MIMO controllers, which could require a cumbersome iterative approach using classical design methods.

There are also some disadvantages, however, which may explain the continuing prevalence of classically designed controllers in commercial wind turbines.

In practice, ‘tuning’ the cost function may end up being just as difrcult as tuning a classical controller, and the tuning may need to be repeated for each new turbine even though in principle this ought to be unnecessary. The cost function needs to include terms for any states or outputs that should be minimised, but the choice of such variables is not as straightforward as it might appear. For example, for a variable-speed controller it would be logical to include a term to minimise the speed error; but in practice a term is also required to minimise the integral of the speed error, and adjusting the relative weights for these two terms is very similar to adjusting the proportional and integral gains in a classical design.

Also the cost function is derned as a quadratic function of the states and other variables, and this may not be appropriate for minimisation of fatigue loads for example, as fatigue is a highly non-linear process. Even for speed regulation, one could argue that minimising the speed error is not important (this may even contradict the need to minimise loads), but minimising extreme speed excursions to avoid any overspeed trips is all that matters. A quadratic cost function is not ideal for this, as the true ‘cost’ increases dramatically at the overspeed trip limit.

Classical controllers are simpler to implement; they can easily deal with nonlinearities through techniques such as gain scheduling, and simple adjustments such as the addition of notch rlters is straightforward, as is the imposition of rxed or variable rate limits. Model based controllers require further sophistication such as extended Kalman rlters or fuzzy transitions to deal with non-linearities, and any adjustment requires a complete recalculation of the controller. Integration with the supervisory control is also much less straightforward; for example, it might be desirable to modify the tower acceleration feedback and/or the individual pitch control during a shut-down to reduce extreme loads. With a classical controller it is easy to impose variable schedules or limits to achieve this, but it is much more difrcult to do this with model based controllers.

As explained in Section 8.3.10, most of the wind turbine control problem can be decomposed into separate, almost uncoupled SISO loops. This makes it perfectly feasible to use straightforward classical tuning techniques. The only signircant coupling between these loops is between speed regulation and tower damping, but this is easily dealt with by means of just one or two iterations, tuning each loop on its own with the other loop implemented as part of the plant.

Nevertheless, as turbines become larger, lighter, and more sexible, it is possible that model based multivariable methods, perhaps in conjunction with additional sensors, will increasingly rnd a role.

# 8.4.7 Other methods

Rule based or ‘fuzzy logic’ controllers are useful when the system dynamics are not well known or when they contain important non-linearities. Control actions are calculated by weighting the outcomes of a set of rules applied to the measured signals. Although there has been some work on fuzzy controllers for wind turbines, there is no clear evidence of benerts. In practice, quite a good knowledge of the system dynamics is usually available, and the dynamics can reasonably be linearised at each operating point, so there is no clear motivation for such an approach.

The same could be said of controllers based on neural networks. These are learning algorithms, which are ‘trained’ to generate suitable control actions using a particular set of conditions, and then allowed to use their learnt behaviour as a general control algorithm. While this is potentially a powerful technique, it is difrcult to be sure that such a controller will generate acceptable control actions in all circumstances.

Nevertheless, there may be some potential for such methods where signircant non-linearities or non-stationary dynamics are involved. These might be in the turbine itself (stall hysteresis might be one example), in the driving disturbances (the wind characteristics are not stationary), or in the controller objectives. For example, the controller objectives might change around rated wind speed, or non-linear effects such as fatigue damage might be included in the cost function.

# 8.5 Pitch actuators

An important part of the control system of a pitch-controlled turbine is the pitch actuation system (see also Section 6.7.2). Both hydraulic and electric actuators are commonly used, each type having its own particular advantages and disadvantages that should be considered at the design stage.

Smaller machines might have a single pitch actuator to control all of the blades simultaneously, but the current commercial turbines usually have individual pitch actuators for each blade. This has the advantage that it is then possible to dispense with the large and expensive shaft brake that would otherwise be needed. This is because of the requirement for a turbine to have at least two independent braking systems capable of bringing the turbine from full load to a safe state in the event of a failure. Provided the individual pitch actuators can be made independently fail-safe, and as long as the aerodynamic braking torque is always sufrcient to slow the rotor down to a safe speed even if one pitch actuator has failed at the working pitch angle, then multiple actuators may be considered to be independent braking systems for this purpose. There may still be a need for a parking brake, at least for the use of maintenance crews, but this may then be fairly small. It must at least be capable of bringing the rotor to a complete stop from a low speed, not necessarily in high or extreme wind speeds, for long enough to allow a rotor lock to be inserted.

Smaller, older turbines used a collective pitch actuation system that commonly consisted of an electric or hydraulic actuator in the nacelle, driving a push-rod that passes through the centre of the gearbox and hollow main shaft. The push-rod is attached to the pitchable blade roots through mechanical linkages in the hub. The actuator in the nacelle is often a simple hydraulic cylinder and piston. A charged hydraulic accumulator ensures that the blades can always be feathered even if the hydraulic pump loses power. An alternative arrangement is to use an electric servo motor to drive a ball-nut that engages with a ball-screw on the push-rod. Because the push-rod turns with the rotor, loss of power to the motor causes the ball-screw to wind the pitch to feather, giving failsafe pitch action. This requires a failsafe brake on the servo motor to ensure that the ball-nut stops turning if power is lost.

Individual pitch control requires separate actuators in the hub for each blade. Therefore, there must be some means of transmitting power to the rotating hub to drive the actuators. This can be achieved by means of slip rings in the case of electric actuators, or a rotary hydraulic joint for hydraulic actuators if the hydraulic power pack is located in the nacelle. A rotary transformer could be used to transmit electrical power to the hub without the inconvenience of slip rings, which require maintenance.

The need to ensure a backup power supply on the hub to enable the blades to pitch even in the event of power loss can be a source of problems. A hydraulic system needs an accumulator for each blade, while electric actuators usually have battery packs in the hub for this purpose. Such battery packs are large, heavy, and expensive, and alternative methods such as the use of hub-mounted generators, which can always generate power as long as the hub is turning, have been proposed. If a battery is used, the actuator motors must either be dc motors or (more commonly) ac motors with a frequency converter, with the batteries on the dc link. Because this will form part of the safety system, the reliability of the inverter between the dc link and the pitch motor is important. A hub-mounted generator would produce either dc or variable frequency ac, and once again the reliability of the connection to the pitch motor is important. Because the pitch actuators have to be independently failsafe, separate battery packs or generators and frequency converters, etc. must be provided for each blade.

The friction in the pitch bearing is often a signircant factor in the design of the pitch actuation system. The bearing friction depends on the loading applied to the bearing, and the large overturning moment acting on the bearing can lead to very high levels of friction: often most of the actuator torque is required to overcome the bearing friction.

A hydraulic actuator would usually be controlled by means of a proportional valve controlling the sow of oil to the actuator cylinder. The valve opening, and hence the oil sow rate, would be set in proportion to the required pitch rate. The demanded pitch rate may come directly from the turbine controller, or it might come from a pitch position feedback loop. In this case the turbine controller generates a pitch position demand. This is compared to the measured pitch position, and the pitch position error is turned into a pitch rate demand through a fast PI or PID control loop, implemented either digitally or by means of a simple analogue circuit.

In the case of an electric actuator, the motor controller usually requires a torque demand signal. This may be derived from a speed controller, which uses a fast PI or

PID controller acting on speed error to generate a torque demand. Once again the speed demand may come directly from the turbine controller or from a position feedback loop.

Simpler actuators could be used if a fast pitch response is not important – for example, in a turbine that is controlled by pitching to stall rather than to feather. In this case an actuator that merely pitches at a rxed rate in either direction may be adequate.

# 8.6 Control system implementation

Previous sections have explained some of the techniques whereby control algorithms can be designed. The system and controller dynamics have been described in continuous time in terms of the Laplace operator, s. While it is possible to implement a continuous-time controller – for example, using analogue circuitry – the use of digital controllers is now almost universal. The greater sexibility of digital systems is a factor here: simply by making software changes, the control logic can be changed completely.

A consequence of using digital control is that the control actions are calculated and updated on a discrete time step, rather than in continuous time. Control algorithms designed in continuous time must therefore be converted to discrete time for implementation in a digital controller. It is also possible to design controllers in discrete time, if the linearised model of the turbine is rrst discretised.

The following sections briesy describe some of the practical issues involved in implementing a control algorithm in a real digital controller. Once again, the reader is referred to standard control theory texts for more detailed treatments.

# 8.6.1 Discretisation

Supposing a control algorithm has been designed in continuous time as a transfer function (such as Eq. (8.1) for a PID controller, for example), it must be discretised before it can be implemented in a digital controller. Discretised transfer functions are usually represented in terms of the delay operator, z, where ${ \boldsymbol { \mathrm { z } } } ^ { - \mathrm { k } } { \boldsymbol { \mathrm { x } } }$ represents the value of x sampled k timesteps ago. As a simple example, a moving average or rrst order lag rlter from x to y is often implemented as

$$
\mathrm{y} _ {\mathrm{k}} = \mathrm{Fy} _ {\mathrm{k} - 1} + (1 - \mathrm{F}) \mathrm{x} _ {\mathrm{k}} \tag {8.42}
$$

This is a difference equation that can readily be implemented in code in a discrete controller. In terms of the delay operator, it can be written as

$$
(1 - \mathrm{Fz} ^ {- 1}) \mathrm{y} = (1 - \mathrm{F}) \mathrm{x} \tag {8.43}
$$

or alternatively as a transfer function consisting of a ratio of polynomials in $z ^ { - 1 }$ :

$$
\mathrm{y} = \frac {(1 - \mathrm{F})}{(1 - \mathrm{Fz} ^ {- 1})} \mathrm{x} \tag {8.44}
$$

Now the Laplace operator can be considered as a differentiation operator, and so as a simple approximation, it might be possible to convert a continuous transfer function into discrete form by replacing s by $( 1 - z ^ { - 1 } ) / \mathrm { T }$ , where T is the timestep.

In fact by simple algebraic manipulation, it is straightforward to show that with this substitution, the above discrete transfer function is in fact equivalent to the continuous transfer function representation of a rrst order lag with time constant 휏, namely

$$
\mathrm{y} = \frac {1}{1 + \mathrm{s} \tau} \mathrm{x} \tag {8.45}
$$

with the factor F being given by $\tau / ( \mathrm { T } + \tau )$ .

Clearly any discretised equation can only be an approximation to the continuous-time behaviour. There are other discretisation methods, and the so-called ‘bilinear’ or ‘Tutsin’ approximation often works better in practice. In this case the Laplace operator is replaced by

$$
\frac {2}{T} \frac {(1 - z ^ {- 1})}{(1 + z ^ {- 1})} \tag {8.46}
$$

Discretisation results in a phase shift compared to the continuous time process. This phase shift increases with frequency. If the algorithm performance is particularly sensitive to the phase shift at a certain frequency, then the discretisation can be ‘pre-warped’ to this frequency. Pre-warping modires the phase shift so that the phase of the discrete transfer function is correct at the chosen frequency, but deviates at lower and higher frequencies. An example of a situation where pre-warping may be important is in the case of a drive train resonance damper in a variable-speed turbine (Section 8.3.5). The resonant frequency that is being targeted is usually fairly high, typically around 3 or 4 Hz, and unless the controller timestep is very short the phase lag caused by discretisation may signircantly affect the performance of the damping algorithm.

The approximation for s used for discretisation with pre-warping about a frequency ω is

$$
\frac {\omega}{\tan (\omega \mathrm{T} / 2)} \frac {(1 - z ^ {- 1})}{(1 + z ^ {- 1})} \tag {8.47}
$$

# 8.6.2 Integrator desaturation

Controllers containing integral terms, such as PI or PID controllers, experience a particular problem known as integrator wind-up when the control action saturates at a limiting value. A common example is in pitch control, where the pitch angle is limited to the rne pitch position when the wind is below rated. For example, a PI pitch controller for a variable-speed turbine can be represented as in Figure 8.20.

Above rated wind speed, the speed error will be zero on average because of the integral term. Below rated, the pitch saturates at the rne pitch position, and the speed error will remain negative. The integral of the error will therefore grow more and more negative, and only the application of the limits prevents the actual pitch demand from doing the same.

![](images/d83b5a673048735c8275049af50d9ee5d3d092dc4d7bd532418db7ff9e915b62.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Power Speed"] --> B["P"]
    A --> C["I"]
    B --> D["+"]
    C --> D
    D --> E["Limits"]
    E --> F["Pitch demand"]
```
</details>

Figure 8.20 Limits applied to a PI controller

However, when the wind speed reaches rated again and the speed error becomes positive, it will take a long time before the integrated power error climbs back up to zero and starts to demand a positive pitch angle. To prevent this problem of integrator wind-up, the integral term must be prevented from integrating when the pitch is at the limit. This is easily implemented by separating out the integrator, I(z), from the rest of the controller, R(z). R(z) generates a change in demanded pitch angle, and I(z) then integrates this by adding it to the previous pitch demand after the limits have been applied.

As an example, a PI controller [Eq. (8.31)] discretised using the bilinear approximation would be

$$
\mathrm{y} = \mathrm{K} _ {\mathrm{p}} [ (\mathrm{T} / 2 \mathrm{T} _ {\mathrm{i}} + 1) + (\mathrm{T} / 2 \mathrm{T} _ {\mathrm{i}} - 1) \mathrm{z} ^ {- 1} ] \cdot \frac {1}{[ 1 - \mathrm{z} ^ {- 1} ]} \cdot \mathrm{x} = \mathrm{R} (\mathrm{z}) \cdot \mathrm{I} (\mathrm{z}) \cdot \mathrm{x} \tag {8.48}
$$

To avoid integrator wind-up, this can be implemented as follows:

$$
\Delta \mathrm{y} _ {\mathrm{k}} = \mathrm{K} _ {\mathrm{p}} [ (\mathrm{T} / 2 \mathrm{T} _ {\mathrm{i}} + 1) \mathrm{x} _ {\mathrm{k}} + (\mathrm{T} / 2 \mathrm{T} _ {\mathrm{i}} - 1) \mathrm{x} _ {\mathrm{k} - 1} ] (\text { implementation   of   R(z) })
$$

$$
\mathrm{y} _ {\mathrm{k}} ^ {*} = \mathrm{y} _ {\mathrm{k-1}} + \Delta \mathrm{y} _ {\mathrm{k}} (\text {integrator I(z) using previous limited output y} _ {\mathrm{k-1}})
$$

$$
\mathrm{y} _ {\mathrm{k}} = \lim (\mathrm{y} _ {\mathrm{k}} ^ {*}) (\text { application   of   limits })
$$

# References

Anderson, B.D.O. and Moore, J.B. (1979). Optimal Filtering. Prentice-Hall.   
Astrom, K.J. and Wittenmark, B. (1990). Computer-Controlled Systems. Prentice-Hall.   
Bossanyi, E.A. (1982). Probabilities of sudden drop in power from a wind turbine cluster. Proceedings of the 4th International Symposium on Wind Energy Systems, Cranreld, England (21–24 September 1982).   
Bossanyi, E.A. (1987). Adaptive pitch control for a 250 kW wind turbine. In: Proc. 9th BWEA Conference, Edinburgh, 85–92. Mechanical Engineering Publications.   
Bossanyi, E.A. (1994). Electrical aspects of variable speed operation of horizontal axis wind turbine generators. ETSU W/33/00221/REP, Energy Technology Support Unit, Harwell, UK.   
Bossanyi, E.A. (2000). Developments in closed loop controller design for wind turbines. Proceedings of the 2000 ASME Wind Energy Symposium, Reno, Nevada.   
Bossanyi, E.A. (2003). Individual blade pitch control for load reduction. Wind Energy 6 (2): 119–128.   
Bossanyi, E.A. (2004). Developments in individual blade pitch control. Proceedings of the EWEA conference ‘The Science of Making Torque from Wind’, Delft University of Technology (19–21 April 2004).   
Bossanyi, E. (2019). Optimising yaw control at wind farm level. J. Phys.: Conf. Ser. 1222: 1, 12023.   
Bossanyi, E., Delouvrié, T., and Lindahl, S. (2013). Long-term simulations for optimising yaw control and start-stop strategies. Proceedings of the European Wind Energy Conference, Vienna.   
Bossanyi, E., Fleming, P., and Wright, A. (2012a). Validation of individual pitch control by reld tests on two- and three-bladed wind turbines. Special issue on control in wind energy. IEEE Trans. Control Syst. Technol. 21 (4): 1067–1078.   
Bossanyi, E.A. and Gamble, C.R. (1991). Investigation of torque control using a variable slip induction generator, ETSU WN-6018, Energy Technology Support Unit, Harwell, UK.   
Bossanyi, E.A. and King, J. (2012). Improving wind farm output predictability by means of a soft cut-out strategy. Proceedings European Wind Energy Conference, Copenhagen, EWEA 2012.   
Bossanyi, E.A., Kumar, A., and Hugues-Salas, O. (2012b). Wind turbine control applications of turbine-mounted LIDAR. J. Phys.: Conf. Ser. 555 (1): 12011.

Bossanyi, E. and Wright, A. (2009). Field testing of individual pitch control. Proceedings of the European Wind Energy Conference, Marseille.   
Bossanyi, E., Wright, A., and Fleming, P. (2010). Progress with reld testing of individual pitch control. Proceedings of the EWEA conference ‘The Science of Making Torque from Wind’, Heraklion (28–30 June 2010).   
Caselitz, P., Kleinkauf, W., Krüger, T. et al. (1997). Reduction of fatigue loads on wind energy converters by advanced control methods. In: Proc. European Wind Energy Conference, Dublin, October 1997, 555–558. European Wind Energy Association.   
Clarke, D. and Gawthrop, P. (1975). Self-tuning controller. In: Proc. IEE 122, No. 9, 929–934.   
Coleman, R.P. and Feingold, A.M., (1957). Theory of self-excited mechanical oscillations of helicopter rotors with hinged blades. National Advisory Committee for Aeronautics Report 1351.   
D’Azzo, J.J. and Houpis, C.H. (1981). Linear Control System Analysis and Design. McGraw-Hill.   
Donham, R.E. and Heimbold R.L. (1979). Wind turbine. US Patent 4,297,076, rled 8 June 1979 and issued 1981.   
Fischer, T., Rainey, P., Bossanyi, E. and Kühn, M. (2010). Control strategies for an offshore wind turbine on a monopile under misaligned wind and wave loading. Proceedings of the EWEA conference ‘The Science of making Torque from Wind’, Heraklion (28–30 June 2010).   
Holley, W., Rock, S., and Chaney, K., (1999). Control of variable speed wind turbines below-rated wind speed. Proceedings of the 3rd ASME/JSME Conference, California.   
Knudsen, T., Andersen, P., and Töffner-Clausen, S. (1997). Comparing PI and robust pitch controllers on a 400 kW wind turbine by full-scale tests. In: Proc. European Wind Energy Conference, Dublin, October 1997, 546–550. European Wind Energy Association.   
Kragh, K.A., Fleming, P.A., and Scholbrock, A.K. (2013). Increased power capture by rotor speed–dependent yaw control of wind turbines. J. Sol. Energy Eng. 135 (3): 031018. https://doi .org/10.1115/1.4023971.   
Helen Markou and Torben J. Larsen (2009). Control strategies for operation of pitch regulated turbines above cut-out wind speeds. Proceedings of the European Wind Energy Conference, Marseille.   
Namik, H. and Stol, K. (2010). Individual blade pitch control of soating offshore wind turbines. Wind Energy 13: 74–85.   
Park, R.H. (1929). Two-reaction theory of synchronous machines. Trans. AIEE 48.   
Pedersen, T.K. (1995). Semi-variable speed – a compromise? In: Proc. Wind Energy Conversion 1995, 17th British Wind Energy Association Conference, Warwick, 249–260. Mechanical Engineering Publications.   
Pedersen, T.F. and Gómez Arranz, P. (2018). Spinner anemometer – best practice. DTU Wind Energy E, No. 165, https://backend.orbit.dtu.dk/ws/portalrles/portal/149827433/DTU\_ E\_0165\_Spinner\_Anemometry\_Best\_Practice.pdf.   
Ramtharan, G., Jenkins, N., Anaya-Lara, O., and Bossanyi, E. (2007). Insuence of rotor structural dynamics representations on the electrical transient performance of FSIG and DFIG wind turbines. Wind Energy 10 (4): 293–301.   
Rossetti, M. and Bossanyi, E. (2004). Damping of tower motions via pitch control – theory and practice. Proceedings of the European Wind Energy Conference.   
Savini, B. and Bossanyi, E.A. (2010). Supervisory control logic design for individual pitch control. Proceedings of the European Wind Energy Conference.   
Eric Simley, Lucy Pao, Rod Frehlich, Bonnie Jonkman, and Neil Kelley (2011). Analysis of wind speed measurements using continuous wave LIDAR for wind turbine control. Proceedings of the 49th AIAA Aerospace Sciences Meeting, https://arc.aiaa.org/doi/abs/10.2514/6.2011-263.   
Steinbuch, M., (1989). Dynamic modelling and robust control of a wind energy conversion system. PhD Thesis, University of Delft.

Stol, K. and Fingersh, L. (2004). Wind turbine reld testing of state-space controller designs. NREL/SR-500-35061, National Renewable Energy Laboratory.   
van Engelen, T. and van der Hooft, E. (2005). Individual pitch control inventory. ECN-C-03-138.   
Vanni, F., Rainey, P.J., and Bossanyi, E. (2015). A comparison of control-based platform stabilisation strategies for soating wind turbines. Proceedings of the European Wind Energy Association Conference, Paris.   
Vasiljevic, N., Lea, G., Courtney, M. et al. (2017). Long-range WindScanner system. ´ Remote Sens. 8 (11): 896. https://doi.org/10.3390/rs8110896.