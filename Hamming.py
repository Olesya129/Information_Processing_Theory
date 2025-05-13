import random

def format_output(data, block_size=8):
    """Форматирует вывод данных, разбивая их на блоки по block_size символов"""
    return ' '.join([data[i:i+block_size] for i in range(0, len(data), block_size)])

""" Функция добавления контрольных битов в данные """
def insert_parity_bits(data):
    n = len(data)           # длина данных
    result = list(data)     # Преобразуем строку данных в список для вставки битов
    i = 0                   # Инициализируем счётчик для позиций контрольных битов
    while 2 ** i <= n + i:  # Проверяем, достаточно ли места для нового контрольного бита
        result.insert(2 ** i - 1, '0')  # Вставляем '0' в позицию 2^i - 1
        i += 1
    return ''.join(result)


""" Функция вычисления значений контрольных битов """
def calculate_parity_bits(data):
    data = list(data)   # Преобразуем входную строку в список для изменения
    n = len(data)       # Получаем длину данных
    i = 0               # Инициализируем счётчик для контрольных битов
    while 2 ** i < n:   # Проверяем все позиции контрольных битов (2^i)
        parity = 0      # Инициализируем значение контрольного бита
        for j in range(1, n + 1):       # Перебираем позиции битов (нумерация с 1)
            if j & (2 ** i):            # Проверяем, входит ли бит j в область контроля 2^i
                parity ^= int(data[j - 1])  # Вычисляем XOR для выбранных битов
        data[2 ** i - 1] = str(parity)      # Записываем контрольный бит в позицию 2^i - 1
        i += 1
    return ''.join(data)

""" Функция кодирования данных кодом Хэмминга """
def encode_hamming(data):
    data = insert_parity_bits(data)     # Вставляем позиции для контрольных битов
    data = calculate_parity_bits(data)  # Вычисляем значения контрольных битов
    return data

""" Функция внесения случайной ошибки """
def introduce_random_error(data):
    data = list(data)  # Преобразуем строку в список для изменения
    pos = random.randint(0, len(data) - 1)      # Выбираем случайную позицию для ошибки
    data[pos] = '1' if data[pos] == '0' else '0'   # Меняем бит (0 → 1 или 1 → 0)
    print(f"\nОшибка внесена в бит {pos + 1}")      # Выводим информацию об ошибке
    return ''.join(data)

""" Функция проверки и исправления ошибки """
def check_and_fix_error(encoded_data):
    encoded_data = list(encoded_data)  # Преобразуем строку в список для изменения
    n = len(encoded_data)              # Получаем длину данных
    error_position = 0                 # Инициализируем позицию ошибки
    i = 0
    while 2 ** i < n:       # Проверяем все контрольные биты
        parity = 0          # Инициализируем значение для пересчёта контрольного бита
        for j in range(1, n + 1):   # Перебираем позиции битов
            if j & (2 ** i):        # Проверяем, входит ли бит в область контроля
                parity ^= int(encoded_data[j - 1])  # Вычисляем XOR
        if parity:  # Если XOR не равен 0, есть ошибка
            error_position += 2 ** i  # Добавляем 2^i к позиции ошибки
        i += 1
    if error_position:  # Если найдена ошибка
        encoded_data[error_position - 1] = '1' if encoded_data[error_position - 1] == '0' else '0'  # Исправляем бит
        print(f"\nОшибка исправлена в позиции {error_position}")
    return ''.join(encoded_data)

""" Функция удаления контрольных битов """
def remove_parity_bits(data):
    n = len(data)   # Получаем длину данных
    result = []     # Создаём список для информационных битов
    i = 0
    for j in range(n):  # Перебираем все биты
        if j + 1 != 2 ** i:         # Если позиция не контрольная (не 1, 2, 4, ...)
            result.append(data[j])  # Добавляем информационный бит
        else:
            i += 1
    return ''.join(result)

""" Основная функция программы """
def main():
    binary_data = input("Введите двоичный код (только 0 и 1): ").strip()
    if not all(c in "01" for c in binary_data):
        print("Ошибка: введены некорректные символы. Введите только 0 и 1")
        return

    print(f"\nДвоичные данные:\n {format_output(binary_data)}")

    encoded_data = encode_hamming(binary_data)
    print(f"\nЗакодированные данные:\n {format_output(encoded_data)}")

    error_data = introduce_random_error(encoded_data)
    print(f"Данные с ошибкой:\n {format_output(error_data)}")

    fixed_data = check_and_fix_error(error_data)
    print(f"Исправленные данные:\n {format_output(fixed_data)}")

    decoded_binary = remove_parity_bits(fixed_data)
    print(f"\nДекодированные двоичные данные:\n {format_output(decoded_binary)}")


if __name__ == "__main__":
    main()