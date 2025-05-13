# Функция для нахождения обратного элемента a^{-1} mod m (a * x ≡ 1 mod m)
def modinv(a, m):
    # Внутренняя функция: расширенный алгоритм Евклида
    # Возвращает (НОД(a, b), x, y), где a*x + b*y = НОД(a, b)
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)  # База рекурсии: если a = 0, НОД = b, x = 0, y = 1
        else:
            # Рекурсивный вызов для b % a и a
            g, y, x = egcd(b % a, a)
            # Обновление коэффициентов: x' = x - (b//a)*y, y' = y
            return (g, x - (b // a) * y, y)

    # Вычисление НОД и коэффициентов
    g, x, y = egcd(a, m)
    # Если НОД ≠ 1, обратного элемента не существует
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        # Возвращаем x % m как обратный элемент
        return x % m


# Алгоритм 1.2 для вычисления xR mod N (Замечание 2)
def algorithm_1_2(x, y, N, beta, n):
    # Шаг 1: Разложение x на цифры в системе счисления с основанием beta
    x_digits = []
    temp = x
    for _ in range(n):
        x_digits.append(temp % beta)  # Получаем младшую цифру
        temp //= beta  # Удаляем младшую цифру

    # Шаг 2: Проверка, что -N % beta и beta взаимно просты
    from math import gcd
    if gcd(-N % beta, beta) != 1:
        raise Exception(f'Параметры не подходят: -N % beta = {-N % beta} и beta = {beta} не взаимно просты')

    # Шаг 3: Вычисление обратного элемента (-N % beta)^{-1} mod beta
    N_inv = modinv(-N % beta, beta)

    # Шаг 4: Итеративное вычисление z
    z = 0  # Начальное значение z
    for i in range(n):
        # u = (z + x_i * y) % beta
        u = (z + x_digits[i] * y) % beta
        # v = u * (-N % beta)^{-1} mod beta
        v = (u * N_inv) % beta
        # z = (z + x_i * y + v * N) // beta
        z = (z + x_digits[i] * y + v * N) // beta

    # Шаг 5: Приведение результата по модулю N
    z = z % N
    return z


# Функция для вычисления φ_R^{-1}(x) = xR mod N
def phi_R_inv(x, N, beta, n):
    # R = beta^n
    R = beta ** n
    # R^2 mod N (используется как y в algorithm_1_2)
    R2 = (R * R) % N
    # Вызов algorithm_1_2 для вычисления xR mod N
    return algorithm_1_2(x, R2, N, beta, n)


# Пример использования с развернутым выводом
x = 7  # Входное число
N = 13  # Модуль
beta = 2  # Основание системы счисления
n = 4  # Количество разрядов, R = 2^4 = 16

# Вычисление R и R^2 mod N
R = beta ** n
R2 = (R * R) % N

# Разложение x на цифры
x_digits = []
temp = x
for _ in range(n):
    x_digits.append(temp % beta)
    temp //= beta

# Вычисление результата
result = phi_R_inv(x, N, beta, n)

# Развернутый вывод
print("=== Вычисление φ_R^{-1}(x) = xR mod N ===")
print(f"Входные параметры:")
print(f"  x = {x}")
print(f"  N = {N}")
print(f"  β = {beta}")
print(f"  n = {n}")
print(f"Вычисленные значения:")
print(f"  R = β^n = {beta}^{n} = {R}")
print(f"  R^2 mod N = {R}^2 mod {N} = {R2}")
print(f"Разложение x = {x} в системе счисления с основанием β = {beta}:")
print(f"{x_digits}")
print(f"Результат: φ_R^{-1}({x}) = {x} * {R} mod {N} = {result}")
print(f"Проверка: ({x} * {R}) mod {N} = {(x * R) % N}")
