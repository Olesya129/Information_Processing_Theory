import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Функция, задающая систему дифференциальных уравнений
def system(t, P):
    P0, P1, P2, P3, P4 = P
    dP0dt = 0.5 * P1 + 4 * P2 - 1.4 * P0
    dP1dt = 0.9 * P0 + 1 * P3 - 2.5 * P1
    dP2dt = 0.5 * P0 + 1 * P4 - 6 * P2
    dP3dt = 2 * P1 - 1 * P3
    dP4dt = 2 * P2 - 1 * P4
    return [dP0dt, dP1dt, dP2dt, dP3dt, dP4dt]

# Начальные условия
P0_initial = [1.0, 0.0, 0.0, 0.0, 0.0]  # P0(0) = 1.0, остальные 0.0
t0, t_end = 0.0, 10.0  # Временной интервал
dt = 0.01  # Шаг по времени

# Решаем систему уравнений
solution = solve_ivp(system, (t0, t_end), P0_initial, method='RK45', t_eval=np.arange(t0, t_end, dt))

# График результатов
plt.figure(figsize=(10, 6))
plt.plot(solution.t, solution.y[0], label='P0(t)')
plt.plot(solution.t, solution.y[1], label='P1(t)')
plt.plot(solution.t, solution.y[2], label='P2(t)')
plt.plot(solution.t, solution.y[3], label='P3(t)')
plt.plot(solution.t, solution.y[4], label='P4(t)')
plt.xlabel('Время (t)')
plt.ylabel('Вероятность P(t)')
plt.title('Решение системы дифференциальных уравнений')
plt.legend()
plt.grid(True)
plt.show()