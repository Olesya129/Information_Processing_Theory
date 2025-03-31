import numpy as np
import matplotlib.pyplot as plt

# Функция, задающая систему дифференциальных уравнений
def system(t, P):
    P0, P1, P2, P3, P4 = P
    dP0dt = 0.5 * P1 + 4 * P2 - 1.4 * P0
    dP1dt = 0.9 * P0 + 1 * P3 - 2.5 * P1
    dP2dt = 0.5 * P0 + 1 * P4 - 6 * P2
    dP3dt = 2 * P1 - 1 * P3
    dP4dt = 2 * P2 - 1 * P4
    return np.array([dP0dt, dP1dt, dP2dt, dP3dt, dP4dt], dtype=np.float64)

# Метод Эйлера
def euler_method(func, t0, P0, t_end, dt):
    t_values = np.arange(t0, t_end, dt)
    P_values = []
    P = np.array(P0, dtype=np.float64)  # Явно указываем тип float64
    for t in t_values:
        P_values.append(P.copy())
        P += dt * func(t, P)  # Обновляем P по методу Эйлера
        # Выводим значения переменных для текущего шага
        print(f"t = {t:.2f} : P0 = {P[0]:.6f}, P1 = {P[1]:.6f}, P2 = {P[2]:.6f}, P3 = {P[3]:.6f}, P4 = {P[4]:.6f}")
    return np.array(P_values), t_values

# Начальные условия (теперь явно float)
P0_initial = [1.0, 0.0, 0.0, 0.0, 0.0]  # P0(0) = 1.0 (float), остальные 0.0
t0 = 0.0    # Начальное время (float)
t_end = 10.0  # Конечное время (float)
dt = 0.01   # Шаг по времени

# Решаем систему методом Эйлера
P_values, t_values = euler_method(system, t0, P0_initial, t_end, dt)

# Визуализация результатов
plt.figure(figsize=(10, 6))
plt.plot(t_values, P_values[:, 0], label='P0(t)')
plt.plot(t_values, P_values[:, 1], label='P1(t)')
plt.plot(t_values, P_values[:, 2], label='P2(t)')
plt.plot(t_values, P_values[:, 3], label='P3(t)')
plt.plot(t_values, P_values[:, 4], label='P4(t)')
plt.xlabel('Время (t)')
plt.ylabel('Вероятность P(t)')
plt.title('Решение системы дифференциальных уравнений методом Эйлера')
plt.legend()
plt.grid(True)
plt.show()