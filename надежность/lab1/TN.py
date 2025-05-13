import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Параметры усеченного нормального распределения TN(400, 9095)
mu = 400
sigma = np.sqrt(9095)  # ≈ 95.37
a = 0  # Нижняя граница усечения (t ≥ 0)
b = np.inf  # Верхняя граница усечения

# Создаем объект усеченного нормального распределения
trunc_norm = stats.truncnorm((a - mu)/sigma, (b - mu)/sigma, loc=mu, scale=sigma)

# Временная сетка для построения графиков
t = np.linspace(0, 1000, 1000)

# 1. Вероятность безотказной работы P(t) = 1 - F(t)
P_t = trunc_norm.sf(t)

# 2. Средняя наработка до отказа T_mid (математическое ожидание)
T_mid = trunc_norm.mean()

# 3. Дисперсия и среднеквадратическое отклонение
D_t = trunc_norm.var()  # Дисперсия
sigma_T = trunc_norm.std()  # Среднеквадратическое отклонение

# 4. Интенсивность отказов λ(t) = f(t) / P(t)
f_t = trunc_norm.pdf(t)  # Плотность распределения времени до отказа f(t) (пункт 5)
lambda_t = np.divide(f_t, P_t, out=np.zeros_like(f_t), where=P_t > 0)

# 6. Гамма-процентная наработка T_gamma для γ = 0,10,20,...,100
gamma_percentages = np.arange(0, 101, 10)  # 0%, 10%, ..., 100%
T_gamma = np.array([trunc_norm.ppf(1 - (g / 100)) if g < 100 else np.inf for g in gamma_percentages])

# Создаем таблицу для гамма-процентной наработки
gamma_table = np.column_stack((gamma_percentages, T_gamma))

# Построение графиков
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# График 1: Плотность распределения f(t) (пункт 5)
axs[0, 0].plot(t, f_t, label="f(t)", color="tab:blue")
axs[0, 0].set_xlabel("Время t")
axs[0, 0].set_ylabel("f(t)")
axs[0, 0].set_title(" Плотность распределения времени до отказа")
axs[0, 0].legend()
axs[0, 0].grid()

# График 2: Вероятность безотказной работы P(t) (пункт 1)
axs[0, 1].plot(t, P_t, label="P(t)", color="tab:green")
axs[0, 1].set_xlabel("Время t")
axs[0, 1].set_ylabel("P(t)")
axs[0, 1].set_title(" Вероятность безотказной работы")
axs[0, 1].legend()
axs[0, 1].grid()

# График 3: Гамма-процентная наработка T_gamma (пункт 6)
axs[1, 0].plot(gamma_percentages[:-1], T_gamma[:-1], marker='o', linestyle='-', color='blue', label="T_gamma")
axs[1, 0].set_xlabel("γ, %")
axs[1, 0].set_ylabel("Время T_gamma")
axs[1, 0].set_title(" Гамма-процентная наработка до отказа")
axs[1, 0].legend()
axs[1, 0].grid()

# График 4: Интенсивность отказов λ(t) (пункт 4)
axs[1, 1].plot(t, lambda_t, label="λ(t)", color="tab:red")
axs[1, 1].set_xlabel("Время t")
axs[1, 1].set_ylabel("λ(t)")
axs[1, 1].set_title(" Интенсивность отказов")
axs[1, 1].legend()
axs[1, 1].grid()

plt.tight_layout()
plt.show()

# Вывод числовых характеристик
print("\nЧисловые характеристики усеченного нормального распределения TN(400, 9095):")
print(f" Средняя наработка до отказа T_mid: {T_mid:.2f}")
print(f" Дисперсия времени безотказной работы D: {D_t:.2f}")
print(f" Среднее квадратическое отклонение σ: {sigma_T:.2f}")

# Пример расчета интенсивности отказов для конкретного времени
sample_t = 100
lambda_val = trunc_norm.pdf(sample_t) / trunc_norm.sf(sample_t)
print(f"\n Интенсивность отказов при t={sample_t}: {lambda_val:.6f}")

# Вывод таблицы гамма-процентной наработки
print("\n Таблица гамма-процентной наработки:")
print("+--------+--------------+")
print("| γ, %   | T_gamma      |")
print("+--------+--------------+")
for g, tg in gamma_table:
    if g == 100:
        print(f"| {g:6} | {'∞':12} |")
    else:
        print(f"| {g:6} | {tg:12.2f} |")
print("+--------+--------------+")

