import random

# Функция генерации пары ключей
def create_key_pair():
    p = make_prime()  # Генерируем первое простое число p
    q = make_prime()  # Генерируем второе простое число q
    while p == q:           # Проверяем, что p и q разные
        q = make_prime()    # Если одинаковые, генерируем новое q
    modulus = p * q         # Вычисляем модуль n = p * q
    phi = (p - 1) * (q - 1)  # Вычисляем функцию Эйлера phi = (p-1) * (q-1)
    public_exp = select_public_exponent(phi)        # Выбираем экспоненту e
    private_exp = compute_inverse(public_exp, phi)  # Вычисляем экспоненту d
    return public_exp, private_exp, modulus, p, q

# Функция генерации большого простого числа
def make_prime(bits=32):
    while True:
        num = random.getrandbits(bits)  # Генерируем случайное число с заданным количеством бит
        num |= (1 << bits - 1) | 1      # Устанавливаем старший и младший биты (для нечётности и размера)
        if check_prime(num):  # Проверяем, является ли число простым
            return num

# Функция проверки числа на простоту
def check_prime(n, tests=20):
    if n < 2:  # Если число меньше 2, оно не простое
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:  # Проверяем делимость на малые простые числа
        if n % p == 0:      # Если делится на p
            return n == p   # Число простое, только если оно равно p
    d = n - 1   # Инициализируем d
    s = 0       # Инициализируем счётчик делений на 2
    while d % 2 == 0:   # Разлагаем n-1 на 2^s * d
        d //= 2         # Делим d на 2
        s += 1
    for _ in range(tests):  # Проводим tests итераций теста
        a = random.randint(2, n - 2)  # Выбираем случайное число a
        x = fast_pow(a, d, n)            # Вычисляем a^d mod n
        if x == 1 or x == n - 1:         # Если x = 1 или x = n-1, тест пройден
            continue
        for __ in range(s - 1):     # Проверяем последовательные квадраты
            x = fast_pow(x, 2, n)  # Вычисляем x^2 mod n
            if x == n - 1:  # Если x = n-1, тест пройден
                break
        else:
            return False
    return True

# Функция выбора публичной экспоненты
def select_public_exponent(phi):
    common_e_values = [65537, 257, 17, 5, 3]  # Список стандартных значений e
    for e in common_e_values:                 # Перебираем стандартные e
        if e < phi and compute_gcd(e, phi) == 1:  # Если e < phi и взаимно просто с phi
            return e
    for e in range(phi - 1, 1, -1):     # Если стандартные не подошли, ищем e сверху вниз
        if compute_gcd(e, phi) == 1:    # Если e взаимно просто с phi
            return e
    raise ValueError("Не удалось найти подходящую экспоненту")

# Функция вычисления НОД
def compute_gcd(a, b):
    while b:  # Пока b не равно 0
        a, b = b, a % b  # Обновляем a и b по алгоритму Евклида
    return a  # Возвращаем НОД

# Вычисление модульного обратного с использованием алгоритма Евклида
def compute_inverse(a, m):
    def extended_euclid(a, b):  # Внутренняя функция для расширенного алгоритма Евклида
        if b == 0:          # Если b равно 0
            return a, 1, 0  # Возвращаем НОД и коэффициенты
        else:
            g, x, y = extended_euclid(b, a % b)  # Получаем НОД и коэффициенты
            return g, y, x - (a // b) * y        # Вычисляем новые коэффициенты
    g, x, y = extended_euclid(a, m)  # Вызываем расширенный алгоритм Евклида
    if g != 1:  # Если НОД не равен 1
        raise ValueError("Обратного элемента не существует")
    return x % m  # Возвращаем модульный обратный элемент

# Функция шифрования текста
def encode_text(text, public_exp, modulus):
    return [fast_pow(ord(c), public_exp, modulus) for c in text]  # Шифруем каждый символ (ord(c)^e mod n)

# Функция быстрого возведения в степень
def fast_pow(base, exponent, modulus):
    result = 1
    while exponent > 0:  # Пока экспонента больше 0
        if exponent % 2 == 1:  # Если текущий бит экспоненты равен 1
            result = (result * base) % modulus  # Умножаем результат на base по модулю
        base = (base * base) % modulus  # Возводим base в квадрат по модулю
        exponent = exponent // 2  # Делим экспоненту на 2
    return result

# Функция дешифрования текста
def decode_text(encoded, private_exp, modulus):
    """Дешифрование текста"""
    decrypted = []  # Создаём список для дешифрованных чисел
    for num in encoded:  # Перебираем зашифрованные числа
        decrypted_num = fast_pow(num, private_exp, modulus)  # Дешифруем: num^d mod n
        if decrypted_num > 0x10FFFF:  # Проверяем, не превышает ли число максимальный код Unicode
            raise ValueError("Некорректное значение при дешифровании")  # Ошибка при большом значении
        decrypted.append(decrypted_num)  # Добавляем дешифрованное число в список
    try:  # Пробуем преобразовать числа в символы
        return ''.join(chr(c) for c in decrypted)
    except ValueError:
        return "Ошибка при декодировании сообщения"

# Основная функция программы
def main():
    public_key, private_key, modulus, p, q = create_key_pair()  # Генерируем ключи
    print("Генерация ключей...")
    print(f"Простое число p: {p}")
    print(f"Простое число q: {q}")
    print(f"Открытый ключ (e, n): ({public_key}, {modulus})")
    print(f"Закрытый ключ (d, n): ({private_key}, {modulus})")

    message = "Hello 123"
    print(f"\nИсходное сообщение: {message}")

    print("\nШифрование...")
    encrypted = encode_text(message, public_key, modulus)
    print("Зашифрованное сообщение:", encrypted)

    print("\nДешифрование...")
    decrypted = decode_text(encrypted, private_key, modulus)
    print("Расшифрованное сообщение:", decrypted)

# Точка входа в программу
if __name__ == "__main__":
    main()