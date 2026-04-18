# ODE (from wikipedia)
# d^2theta/dt^2 + (g/l) * sin(theta) = 0
# however, Euler's method only works with first order ODEs
# so we have to convert to 2 first order ODEs
# dtheta/dt = w (1) dw/dt = -(g/l) * sin(theta) (2)
# using Euler's
# theta_{i+1} = theta_i + w_i * deltat
# w_{i+1}-(g/l)sin(theta_i)deltat

import matplotlib.pyplot as plt
import numpy as np

g = 9.81
l = 1
t_0 = 0
t_end = 10
steps = 1000
dt = (t_end - t_0) / steps
# dt = 0.1

t = np.linspace(t_0, t_end, steps)  # more like liminal space
# print(len(t))
theta = np.zeros(steps)
omega = np.zeros(steps)

theta[0] = np.pi / 4
omega[0] = 0

for i in range(steps - 1):
    print("step", i)
    # using explicit euler - fah the energy not conserved
    # theta[i + 1] = theta[i] + omega[i] * dt
    # omega[i + 1] = omega[i] - (g / l) * np.sin(theta[i]) * dt

    # using semi implicit euler
    omega[i + 1] = omega[i] - (g / l) * np.sin(theta[i]) * dt
    theta[i + 1] = theta[i] + omega[i + 1] * dt
fig, (axe1, axe2) = plt.subplots(1, 2, figsize=(12, 6))


axe1.plot(t, theta)
axe1.set_title("Trajectory of the pendulum")
axe1.set_xlabel("Time (s)")
axe1.set_ylabel("Angle (rad)")
axe1.grid(True)


axe2.plot(theta, omega)
axe2.set_title("Phase space")
axe2.set_xlabel("Angle (rad)")
axe2.set_ylabel("Angular velocity (rad/s)")
axe2.grid(True)

plt.suptitle('Pendulum Motion', fontsize=16)

plt.tight_layout()
plt.show()
