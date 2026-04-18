# entirely copy pasted from 2-1a lmao
import numpy as np
import matplotlib.pyplot as plt

def solver(m, g, x0, v0, dt, t_max):
    t = np.arange(0, t_max, dt)
    x, v = np.zeros(len(t)), np.zeros(len(t))
    x[0], v[0] = x0, v0

    # euler method (semi-implicit)
    for i in range(len(t) - 1):
        accel = g 
        v[i+1] = v[i] + accel * dt
        x[i+1] = x[i] + v[i+1] * dt
    return t, x, v

def exact_solution(m, g, x0, v0, t):
    # formula: x(t) = x0 + v0*t + 0.5*g*t^2
    return x0 + v0 * t + 0.5 * g * t**2

# params
m = 1.0
g = -9.81
x0, v0 = 500.0, 0.0
t_max = 10.0

dt_example = 0.5

fig, axs = plt.subplots(1, 3, figsize=(20, 6))

# numerical
t_num, x_num, v_num = solver(m, g, x0, v0, dt_example, t_max)
# exact
x_exact = exact_solution(m, g, x0, v0, t_num)

axs[0].plot(t_num, x_exact, color='black', linestyle='--', label='Exact Solution', alpha=0.7)
axs[0].plot(t_num, x_num, color='tab:blue', label=f'Numerical (dt={dt_example})', linewidth=2, marker='o')
axs[0].set_title('Position vs Time', fontsize=13)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Position (m)')
axs[0].legend()
axs[0].grid(True)

# diff iterations on pahse sapce graph
dts_phase = [0.5, 0.2, 0.1]
colors = ['tab:red', 'tab:blue', 'tab:green']

for i, dt_p in enumerate(dts_phase):
    l, x_p, v_p = solver(m, g, x0, v0, dt_p, t_max) # l is fuck all
    axs[1].plot(x_p, v_p, color=colors[i], label=f'dt={dt_p}', alpha=0.6)

# what the bs
t_fine = np.linspace(0, t_max, 1000)
x_e_fine = exact_solution(m, g, x0, v0, t_fine)
v_e_fine = v0 + g * t_fine
axs[1].plot(x_e_fine, v_e_fine, color='black', linestyle='--', label='Exact Orbit', linewidth=2.5)

# plott
axs[1].set_title('Phase Space (w/ divergences)', fontsize=13)
axs[1].set_xlabel('Position (m)')
axs[1].set_ylabel('Velocity (m/s)')
axs[1].legend()
axs[1].grid(True)

# global err convergence
dts_convergence = np.logspace(-4, -1, 10)
max_errors = []

# measure gte
for dt_c in dts_convergence:
    t_c, x_c, l = solver(m, g, x0, v0, dt_c, t_max)
    x_e_c = exact_solution(m, g, x0, v0, t_c)
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