import matplotlib.pyplot as plt
# БЕЗ БИБЛИОТЕК

# Функция, задающая систему дифференциальных уравнений
def system(t, P):
    P0, P1, P2, P3, P4 = P
    dP0dt = 0.5 * P1 + 4 * P2 - 1.4 * P0
    dP1dt = 0.9 * P0 + 1 * P3 - 2.5 * P1
    dP2dt = 0.5 * P0 + 1 * P4 - 6 * P2
    dP3dt = 2 * P1 - 1 * P3
    dP4dt = 2 * P2 - 1 * P4
    return [dP0dt, dP1dt, dP2dt, dP3dt, dP4dt]


# Метод Рунге-Кутты
def runge_kutta_4(func, t0, P0, t_end, dt):
    t_values = []
    P_values = []
    P = P0.copy()
    t = t0

    while t <= t_end:
        t_values.append(t)
        P_values.append(P.copy())

        # Вычисление коэффициентов k1, k2, k3, k4
        k1 = [dt * f for f in func(t, P)]
        temp = [P[i] + k1[i] / 2 for i in range(len(P))]
        k2 = [dt * f for f in func(t + dt / 2, temp)]
        temp = [P[i] + k2[i] / 2 for i in range(len(P))]
        k3 = [dt * f for f in func(t + dt / 2, temp)]
        temp = [P[i] + k3[i] for i in range(len(P))]
        k4 = [dt * f for f in func(t + dt, temp)]

        # Обновление значений
        for i in range(len(P)):
            P[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6

        t += dt

    return t_values, P_values


# Начальные условия
P0_initial = [1.0, 0.0, 0.0, 0.0, 0.0]  # P0(0)=1, остальные 0
t0 = 0.0  # Начальное время
t_end = 10.0  # Конечное время
dt = 0.01  # Шаг по времени

# Решение системы
t_values, P_values = runge_kutta_4(system, t0, P0_initial, t_end, dt)

# Визуализация результатов
P0 = [p[0] for p in P_values]
P1 = [p[1] for p in P_values]
P2 = [p[2] for p in P_values]
P3 = [p[3] for p in P_values]
P4 = [p[4] for p in P_values]

plt.figure(figsize=(10, 6))
plt.plot(t_values, P0, label='P0(t)')
plt.plot(t_values, P1, label='P1(t)')
plt.plot(t_values, P2, label='P2(t)')
plt.plot(t_values, P3, label='P3(t)')
plt.plot(t_values, P4, label='P4(t)')
plt.xlabel('Время (t)')
plt.ylabel('Вероятность P(t)')
plt.title('Решение системы методом Рунге-Кутты 4-го порядка')
plt.legend()
plt.grid(True)
plt.show()