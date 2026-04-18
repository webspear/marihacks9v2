# the phase space is a sylinder because the angle of the pendulum is periodic

import matplotlib.pyplot as plt
import numpy as np

g = 9.81
l = 1  # length of pendulum
t_0 = 0
t_end = 10
steps = 1000

dt = (t_end - t_0) / steps
t = np.linspace(t_0, t_end, steps)
# print(len(t))
crit_omega = 2 * np.sqrt(g / l)
# print(crit_omega)  # around 6
initial_omega = [3, 5, 6, crit_omega, 7, 8, 10]

fig = plt.figure(figsize=(8, 6))
# fig, axe = plt.subplots(figsize=(8, 6)) # ts no work for 3d
axe = fig.add_subplot(111, projection="3d")

cyl_t = np.linspace(-np.pi, np.pi, 100)
z_grid = np.linspace(-10, 10, 100)
cyl_t, z_grid = np.meshgrid(cyl_t, z_grid)

x_cyl = np.cos(cyl_t)
y_cyl = np.sin(cyl_t)
axe.plot_surface(x_cyl, y_cyl, z_grid, alpha=0.2)


for i in initial_omega:
    # print(i)
    theta = np.zeros(steps)
    omega = np.zeros(steps)

    theta[0] = 0
    omega[0] = i
    for j in range(steps - 1):
        # print("step", j)
        # using explicit euler - fah the energy not conserved
        # theta[j + 1] = theta[j] + omega[j] * dt
        # omega[j + 1] = omega[j] - (g / l) * np.sin(theta[j]) * dt

        # using semi implicit euler
        omega[j + 1] = omega[j] - (g / l) * np.sin(theta[j]) * dt
        theta[j + 1] = theta[j] + omega[j + 1] * dt
        # print("t", theta[j + 1], "o", omega[j + 1])
        x3 = np.cos(theta)
        y3 = np.sin(theta)
        z3 = omega
        # print(x_3, y_3, x_3)
    if i == crit_omega:
        axe.plot(x3, y3, z3, "k--", label=f"w_i = {i:.2f} (crit)")
    else:
        axe.plot(x3, y3, z3, label=f"w_i = {i:.2f}")

axe.set_xlabel("x, cos(theta)")
axe.set_ylabel("y, sin(theta)")
axe.set_zlabel("z, angular velocity (rad/s)")
axe.legend(loc="upper right")

plt.suptitle('Phase Space as cylinder', fontsize=16)

plt.show()
