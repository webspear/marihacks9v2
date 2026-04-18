# ODE (from wookieepedia)
# d^2theta/dt^2 + (g/l) * sin(theta) = 0
# however, euler's method only works with first order ODEs
# so we have to convert to 2 first order ODEs
# dtheta/dt = w (1) dw/dt = -(g/l) * sin(theta) (2)
# using mr oiler's
# theta_{i+1} = theta_i + w_i * deltat
# w_{i+1}-(g/l)sin(theta_i)deltat

# finding phase transitions
# by energy conservaiton:
# Ei = Ef
# Eki + Ui = Ekf + Uf
# initial conditions: h = 0, theta = 0 since bottom of swing is h = 0
# Given that ki = 1/2 * m(Lw)^2 for rotional kinetics (v=Lw)
# Ei = 1/2 * mL^2*w^2
# critial condition
# theta = pi (top of swing), h = 2L  (diameter)
# kf should be zero as we want the pendulum to just reach the top
# so Ef = 2mgL
# thus, isolating for w, we get w = sqrt(4g/L) = 2*sqrt(g/L)
import matplotlib.pyplot as plt
import numpy as np

g = 9.81
l = 1  # length of pendulum
t_0 = 0
t_end = 20.0
steps = 1000

dt = (t_end - t_0) / steps
t = np.linspace(t_0, t_end, steps)
# print(len(t))
crit_omega = 2 * np.sqrt(g / l)
print(crit_omega)  # around 6
initial_omega = [3, 5, 6, crit_omega, 7, 8, 10]
for i in initial_omega:
    theta = np.zeros(steps)
    omega = np.zeros(steps)

    theta[0] = 0
    omega[0] = i
    for j in range(steps - 1):
        # print("step", j)
        # using explicit euler
        # theta[j + 1] = theta[j] + omega[j] * dt
        # omega[j + 1] = omega[j] - (g / l) * np.sin(theta[j]) * dt

        # using semi implicit euler
        omega[j + 1] = omega[j] - (g / l) * np.sin(theta[j]) * dt
        theta[j + 1] = theta[j] + omega[j + 1] * dt
        # print("t", theta[j + 1], "o", omega[j + 1])
    if i == crit_omega:
        plt.plot(theta, omega, "k--", linewidth=2, label=f"w_i = {i:.2f} (crit)")
        # animate(t, theta)
        # exit()
    else:
        plt.plot(theta, omega, label=f"w_i = {i:.2f}")

plt.xlabel("angle (rad)")
plt.ylabel("angular velocity (rad/s)")
plt.axvline(np.pi, color="red", linestyle=":", label="pi")
plt.legend(loc="upper right")
plt.grid(True)
plt.xlim(-np.pi * 1.5, np.pi * 3)
plt.show()
