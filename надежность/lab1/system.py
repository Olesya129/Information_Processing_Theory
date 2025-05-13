# Импорт необходимых библиотек
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, truncnorm
from scipy.integrate import quad
from scipy.optimize import brentq

# - numpy: для работы с массивами, генерации временных точек и вычислений.
# - matplotlib.pyplot: для построения графиков (плотность, вероятность, интенсивность).
# - scipy.stats.expon: экспоненциальное распределение с методами pdf (плотность), sf (функция выживания).
# - scipy.stats.truncnorm: усечённое нормальное распределение, нормализованное на заданном интервале.
# - scipy.integrate.quad: численное интегрирование для среднего времени и второго момента.
# - scipy.optimize.brentq: поиск корня уравнения для гамма-процентной наработки.

# Параметры распределений для трёх элементов системы
# 1. Экспоненциальное распределение: Exp(λ = 1e-4)
lambda1 = 1e-4  # Интенсивность отказов
dist1 = expon(scale=1/lambda1)  # Экспоненциальное распределение, scale = 1/λ = 10000

# - λ = 1e-4 задаёт медленное убывание вероятности (среднее время до отказа = 10000).
# - dist1 предоставляет pdf(t) = λe^(-λt) и sf(t) = e^(-λt).

# 2. Усечённое нормальное распределение: TN(μ=400, σ²=9095, усечение при t=0)
mu, sigma = 400, np.sqrt(9095)  # Среднее и стандартное отклонение (σ ≈ 95.34)
a, b = 0, np.inf  # Усечение слева при t=0, справа — бесконечность
dist2 = truncnorm((a - mu)/sigma, (b - mu)/sigma, loc=mu, scale=sigma)

# - μ и σ задают центр и разброс нормального распределения до усечения.
# - Усечение [0, ∞) исключает отрицательное время.
# - dist2.pdf(t) и dist2.sf(t) дают плотность и вероятность безотказной работы, нормализованные на [0, ∞).

# 3. Распределение Парето: P(α=2.1, t0=5)
alpha, t0 = 2.1, 5  # Параметр формы и минимальное время

def pareto_pdf(t):
    """Плотность распределения Парето.
    Формула: f(t) = (α/t0) * (t0/t)^(α+1) для t > t0, иначе 0.
    Показывает вероятность отказа в единицу времени."""
    return (alpha/t0) * (t0/t)**(alpha + 1) if t > t0 else 0

def pareto_sf(t):
    """Функция выживания Парето.
    Формула: P(t) = (t0/t)^α для t > t0, иначе 1.
    Показывает вероятность работы до времени t."""
    return (t0/t)**alpha if t > t0 else 1.0

# - α = 2.1 определяет тяжёлый хвост (вероятность убывает медленно для больших t).
# - t0 = 5 — минимальное время, до которого отказ невозможен.
# - pareto_sf возвращает 1 для t ≤ t0, так как распределение начинается с t0.

# Функции для системы (последовательное соединение трёх элементов)
def f(t):
    """Плотность времени до отказа системы.
    Формула: f(t) = f1(t)P2(t)P3(t) + f2(t)P1(t)P3(t) + f3(t)P1(t)P2(t).
    Учитывает отказ одного элемента при условии работы остальных."""
    f1 = dist1.pdf(t)  # Плотность экспоненциального
    f2 = dist2.pdf(t)  # Плотность усечённого нормального
    f3 = pareto_pdf(t)  # Плотность Парето
    P1 = dist1.sf(t)   # P(t) экспоненциального
    P2 = dist2.sf(t)   # P(t) усечённого нормального
    P3 = pareto_sf(t)  # P(t) Парето
    return f1 * P2 * P3 + f2 * P1 * P3 + f3 * P1 * P2

# - Система отказывает, если отказывает любой элемент.
# - Каждое слагаемое — это вклад отказа одного элемента, умноженный на вероятности работы остальных.

def P(t):
    """Вероятность безотказной работы системы.
    Формула: P(t) = P1(t) * P2(t) * P3(t).
    Система работает, если все элементы работают."""
    return dist1.sf(t) * dist2.sf(t) * pareto_sf(t)

# - P(t) — произведение вероятностей безотказной работы трёх элементов.
# - Убывает с ростом t, так как каждая P_i(t) уменьшается.

def lambda_t(t):
    """Интенсивность отказов системы.
    Формула: λ(t) = f(t) / P(t).
    Показывает вероятность отказа в момент t при условии работы до t."""
    P_val = P(t)
    return f(t) / P_val if P_val > 0 else np.nan

# - Интенсивность показывает риск отказа в данный момент.
# - np.nan для P(t) = 0 предотвращает деление на ноль.

def T_gamma(gamma, t_min=0, t_max=100):
    """Гамма-процентная наработка.
    Решает: 1 - P(t) = γ/100, чтобы найти t, где вероятность отказа равна γ%.
    Использует brentq для поиска корня."""
    target = gamma / 100
    func = lambda t: (1 - P(t)) - target
    try:
        t_gamma = brentq(func, t_min, t_max, xtol=1e-8, rtol=1e-8)
        return t_gamma
    except ValueError:
        return np.nan

# - Tγ — время, при котором вероятность отказа системы равна γ%.
# - brentq ищет t, где 1 - P(t) = γ/100, на интервале [0, 100].
# - np.nan возвращается, если корень не найден.

def T_mid(limit=100000):
    """Средняя наработка до отказа.
    Формула: E[T] = ∫₀∞ P(t) dt.
    Интегрируем численно до limit."""
    val, _ = quad(P, 0, limit)
    return val

# - Среднее время до отказа — интеграл P(t).
# - limit = 100000 достаточно, так как P(t) быстро падает.

def moment2(limit=100000):
    """Второй момент.
    Формула: E[T^2] = ∫₀∞ 2t P(t) dt."""
    val, _ = quad(lambda t: 2 * t * P(t), 0, limit)
    return val

# - Нужен для дисперсии: Var[T] = E[T^2] - E[T]^2.
# - Интегрируем 2t P(t) вместо t^2 f(t) для упрощения.

def D(limit=100000):
    """Дисперсия.
    Формула: Var[T] = E[T^2] - E[T]^2."""
    Tmid = T_mid(limit)
    return moment2(limit) - Tmid**2

# - Показывает разброс времени до отказа.

def sigma(limit=100000):
    """Среднеквадратическое отклонение.
    Формула: σ = √Var[T]."""
    var = D(limit)
    return np.sqrt(var) if var > 0 else 0

# - СКО показывает типичное отклонение от среднего.

def plot_graphs():
    """Строит графики: f(t), P(t), γ(t), λ(t).
    Для γ(t): ось X — γ (%), ось Y — время t, с плавным убыванием к γ=0."""
    epsilon = 0.01  # Смещение от t=0 для избежания артефактов
    # Для f(t), P(t), λ(t): диапазон времени от -50 до 50
    t_values_neg = np.linspace(-50, 0, 500)  # Отрицательная часть оси t
    t_values_pos = np.linspace(0, 50, 5000)  # Положительная часть оси t
    t_values = np.concatenate((t_values_neg, t_values_pos[1:]))  # Объединяем
    f_values = [0 if t < 0 else f(t) for t in t_values]
    t_values_pos_only = np.linspace(epsilon, 50, 5000)
    P_values = [P(t) for t in t_values_pos_only]
    lambda_values = [lambda_t(t) for t in t_values_pos_only]

    # Для γ(t): расширенный диапазон времени для плавного убывания
    t_max_gamma = 1000  # Увеличиваем диапазон, чтобы P(t) приблизилось к 0
    t_values_gamma = np.linspace(epsilon, t_max_gamma, 10000)
    gamma_values = [100 * P(t) for t in t_values_gamma]  # γ в процентах
    # Добавляем начальную точку (t=0, γ=100%)
    t_values_gamma = np.concatenate(([0], t_values_gamma))
    gamma_values = [100] + gamma_values

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # График 1: Плотность распределения f(t)
    axs[0, 0].plot(t_values, f_values, label="f(t)", color="tab:blue")
    axs[0, 0].set_xlabel("Время t")
    axs[0, 0].set_ylabel("f(t)")
    axs[0, 0].set_title("Плотность распределения f(t)")
    axs[0, 0].legend()
    axs[0, 0].grid()
    axs[0, 0].set_xlim(-50, 50)

    # График 2: Вероятность безотказной работы P(t)
    axs[0, 1].plot(t_values_pos_only, P_values, label="P(t)", color="tab:green")
    axs[0, 1].set_xlabel("Время t")
    axs[0, 1].set_ylabel("P(t)")
    axs[0, 1].set_title("Вероятность безотказной работы P(t)")
    axs[0, 1].legend()
    axs[0, 1].grid()

    # График 3: Процентная вероятность безотказной работы γ(t)
    axs[1, 0].plot(gamma_values, t_values_gamma, 'k-', label="t(γ)")
    axs[1, 0].set_xlabel("γ, %")
    axs[1, 0].set_ylabel("Время t")
    axs[1, 0].set_title("Время до отказа для γ(t)")
    axs[1, 0].set_xlim(0, 100)  # Полный диапазон γ от 0% до 100%
    axs[1, 0].legend()
    axs[1, 0].grid()

    # График 4: Интенсивность отказов λ(t)
    axs[1, 1].plot(t_values_pos_only, lambda_values, label="λ(t)", color="tab:red")
    axs[1, 1].set_xlabel("Время t")
    axs[1, 1].set_ylabel("λ(t)")
    axs[1, 1].set_title("Интенсивность отказов λ(t)")
    axs[1, 1].legend()
    axs[1, 1].grid()

    plt.tight_layout()
    plt.show()

# Вывод численных характеристик
print("System Reliability Numerical Characteristics:")
print("Средняя наработка до отказа T_mid: {:.2f}".format(T_mid()))
print("Дисперсия D: {:.2f}".format(D()))
print("Среднее квадратическое отклонение sigma: {:.2f}".format(sigma()))

# Примеры характеристик в точке
t_example = 500
print("\nДополнительные характеристики при t = {}:".format(t_example))
print("P(t): {:.6f}".format(P(t_example)))
print("f(t): {:.6f}".format(f(t_example)))
print("λ(t): {:.6f}".format(lambda_t(t_example)))

# Построение графиков
plot_graphs()