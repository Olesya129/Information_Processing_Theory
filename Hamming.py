import random


# преобразуем текст в двоичный код
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


# преобразуем двоичный код в текст
def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))


# добавляем контрольные биты в данные
def insert_parity_bits(data):
    n = len(data)
    result = list(data)
    i = 0
    while 2 ** i <= n + i:
        result.insert(2 ** i - 1, '0')  # вставляем нулевой контрольный бит
        i += 1
    return ''.join(result)


# вычисляем значения контрольных битов
def calculate_parity_bits(data):
    data = list(data)
    n = len(data)
    i = 0
    while 2 ** i < n:
        parity = 0
        for j in range(1, n + 1):
            if j & (2 ** i):
                parity ^= int(data[j - 1])
        data[2 ** i - 1] = str(parity)  # записываем вычисленное значение в позицию контрольного бита
        i += 1
    return ''.join(data)


# кодируем данные кодом Хэмминга
def encode_hamming(data):
    data = insert_parity_bits(data)     # вставляем контрольные биты
    data = calculate_parity_bits(data)  # вычисляем их значения
    return data


# вносим ошибку в данные на случайную позицию
def introduce_random_error(data):
    data = list(data)
    pos = random.randint(0, len(data) - 1)  # выбираем случайный бит для замены
    data[pos] = '1' if data[pos] == '0' else '0'
    print(f"\nОшибка внесена в бит {pos + 1}")
    return ''.join(data)


# проверяем и исправляем ошибку
def check_and_fix_error(encoded_data):
    encoded_data = list(encoded_data)
    n = len(encoded_data)
    error_position = 0
    i = 0
    while 2 ** i < n:
        parity = 0
        for j in range(1, n + 1):
            if j & (2 ** i):
                parity ^= int(encoded_data[j - 1])
        if parity:
            error_position += 2 ** i  # Определяем позицию ошибочного бита
        i += 1
    if error_position:
        encoded_data[error_position - 1] = '1' if encoded_data[error_position - 1] == '0' else '0'
        print(f"\nОшибка исправлена в позиции {error_position}")
    return ''.join(encoded_data)


# удаляем контрольные биты из закодированных данных
def remove_parity_bits(data):
    n = len(data)
    result = []
    i = 0
    for j in range(n):
        if j + 1 != 2 ** i:
            result.append(data[j])  # добавляем только обычные биты
        else:
            i += 1
    return ''.join(result)


def main():
    choice = input("Выберите тип данных для кодирования:\n1 - текст, 2 - двоичный код: ").strip()

    if choice == "1":
        text = input("Введите текст для кодирования: ")
        binary_data = text_to_binary(text)  # Преобразуем текст в двоичный код
    elif choice == "2":
        binary_data = input("Введите двоичный код (только 0 и 1): ").strip()
        if not all(c in "01" for c in binary_data):
            print("Ошибка: введены некорректные символы. Введите только 0 и 1")
            return
    else:
        print("Некорректный выбор")
        return

    print(f"\nДвоичные данные:\n {binary_data}")

    encoded_data = encode_hamming(binary_data)      # кодируем данные по Хэммингу
    print(f"\nЗакодированные данные:\n {encoded_data}")

    error_data = introduce_random_error(encoded_data)  # вносим случайную ошибку
    print(f"Данные с ошибкой:\n {error_data}")

    fixed_data = check_and_fix_error(error_data)    # проверяем и исправляем ошибку
    print(f"Исправленные данные:\n {fixed_data}")

    decoded_binary = remove_parity_bits(fixed_data)    # удаляем контрольные биты

    if choice == "1":
        decoded_text = binary_to_text(decoded_binary)  # декодируем обратно в текст
        print(f"\nДекодированный текст:\n {decoded_text}")
    else:
        print(f"\nДекодированные двоичные данные:\n {decoded_binary}")


if __name__ == "__main__":
    main()
