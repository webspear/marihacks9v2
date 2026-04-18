# F = -kx
# F = ma
# -> a = -(k/m)x
# app were doing implicit, so:
# v_{n+1} = v_n + a_{n}*dt
# x_{n+1} = x_{n} + v_{n}*dt

import numpy as np
import matplotlib.pyplot as plt

def solver(m, k, x0, v0, dt, t_max):
    t = np.arange(0, t_max, dt)
    x, v = np.zeros(len(t)), np.zeros(len(t))
    x[0], v[0] = x0, v0

    # euler method (semi-implicit)
    for i in range(len(t) - 1):
        accel = -(k / m) * x[i]
        v[i+1] = v[i] + accel * dt
        x[i+1] = x[i] + v[i+1] * dt
    return t, x, v

def exact_solution(m, k, x0, v0, t):
    # formula: x(t) = A*cos(wt) + B*sin(wt), wt is just sqrt(k/m)*t
    return x0 * np.cos(np.sqrt(k / m) * t) + (v0 / np.sqrt(k / m)) * np.sin(np.sqrt(k / m) * t)

# params
m = 1.0
k = 10.0
x0, v0 = 1.0, 0.0
t_max = 12.0

dt1 = 0.1

fig, axs = plt.subplots(1, 3, figsize=(20, 6))

# numerical
t_num, x_num, v_num = solver(m, k, x0, v0, dt1, t_max)
# exact
x_exact = exact_solution(m, k, x0, v0, t_num)

# random bs go
axs[0].plot(t_num, x_exact, color='black', linestyle='--', label='Exact Solution', alpha=0.7)
axs[0].plot(t_num, x_num, color='tab:blue', label=f'Numerical (dt={dt1})', linewidth=2)
axs[0].set_title('Position vs Time', fontsize=13)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Position (m)')
axs[0].legend()
axs[0].grid(True)

# diff iterations on pahse sapce graph
dts_phase = [0.2, 0.1, 0.05]
colors = ['tab:red', 'tab:blue', 'tab:green']

for i, dt_p in enumerate(dts_phase):
    l, x_p, v_p = solver(m, k, x0, v0, dt_p, t_max) # l is fuck all
    axs[1].plot(x_p, v_p, color=colors[i], label=f'dt={dt_p}', alpha=0.6)

# what the bs
t_fine = np.linspace(0, t_max, 1000)
x_e_fine = exact_solution(m, k, x0, v0, t_fine)
v_e_fine = -x0 * np.sqrt(k/m) * np.sin(np.sqrt(k/m) * t_fine) + v0 * np.cos(np.sqrt(k/m) * t_fine)
axs[1].plot(x_e_fine, v_e_fine, color='black', linestyle='--', label='Exact Orbit', linewidth=2.5)

# plott
axs[1].set_title('Phase Space (w/ divergences)', fontsize=13)
axs[1].set_xlabel('Position (m)')
axs[1].set_ylabel('Velocity (m/s)')
axs[1].legend()
axs[1].grid(True)
axs[1].axis('equal')

# global err convergence
dts_convergence = np.logspace(-4, -1, 10)
max_errors = []

# measure gte
for dt_c in dts_convergence:
    t_c, x_c, l = solver(m, k, x0, v0, dt_c, t_max)
    x_e_c = exact_solution(m, k, x0, v0, t_c)
    max_errors.append(np.max(np.abs(x_c - x_e_c)))

axs[2].loglog(dts_convergence, max_errors, 'o-', color='tab:red', label='Measured Error', markersize=8)

slope_ref = max_errors[-1] / dts_convergence[-1]
axs[2].loglog(dts_convergence, dts_convergence * slope_ref, '--', color='black', label='O(dt) Slope Reference', alpha=0.5)

axs[2].set_title('Global Error vs. dt', fontsize=13)
axs[2].set_xlabel('Time-step size (dt) (log-scale)')
axs[2].set_ylabel('Max Global Error (log-scale)')
axs[2].legend()
axs[2].grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()