class LZ77:
    def __init__(self, window_size=64):
        # Размер окна поиска (search window) — сколько символов назад мы можем искать совпадения.
        self.window_size = window_size

    def find_longest_match(self, search_window, lookahead_buffer):
        # Метод ищет самую длинную подстроку в окне поиска, совпадающую с началом буфера предпросмотра.
        # Окно поиска — уже обработанный текст, буфер предпросмотра — ещё не закодированный.
        best_offset = 0  # Лучшее смещение (расстояние до начала совпадения).
        max_length = 0  # Максимальная длина совпадения.

        # Перебираем позиции в окне поиска с конца к началу.
        for i in range(len(search_window) - 1, -1, -1):
            length = 0  # Текущая длина совпадения.
            # Проверяем, сколько символов совпадают, начиная с позиции i в окне поиска.
            while (length < len(lookahead_buffer) and  # Не выходим за буфер предпросмотра.
                   i + length < len(search_window) and  # Не выходим за окно поиска.
                   search_window[i + length] == lookahead_buffer[length]):  # Символы совпадают.
                length += 1
            # Если текущее совпадение длиннее предыдущего, обновляем параметры.
            if length > max_length:
                max_length = length
                best_offset = len(search_window) - i - 1  # Смещение — расстояние от конца окна.
                # Если совпадение равно длине буфера, дальше искать не нужно.
                if max_length == len(lookahead_buffer):
                    break
        # Возвращаем смещение и длину лучшего совпадения.
        return best_offset, max_length

    def encode(self, input_string):
        # Метод кодирует входную строку, заменяя повторяющиеся подстроки на ссылки (смещение, длина).
        encoded_data = []  # Список для хранения закодированных данных.
        search_window = ""  # Окно поиска — уже обработанный текст.
        lookahead_buffer = input_string  # Буфер предпросмотра — ещё не обработанный текст.
        pos = 0  # Текущая позиция в строке.

        # Обрабатываем строку, пока не закодируем все символы.
        while pos < len(input_string):
            # Если окно поиска превышает заданный размер, обрезаем до последних window_size символов.
            if len(search_window) > self.window_size:
                search_window = search_window[-self.window_size:]

            # Берём первый символ буфера предпросмотра.
            current_char = lookahead_buffer[0]
            # Ищем самое длинное совпадение в окне поиска.
            offset, length = self.find_longest_match(search_window, lookahead_buffer)

            # Если совпадений нет (length == 0), кодируем одиночный символ.
            if length == 0:
                # Добавляем кортеж: (символ, флаг=0, смещение=0, длина=0, строковый код).
                encoded_data.append((current_char, 0, 0, 0, f"0bin({current_char})"))
                # Добавляем символ в окно поиска.
                search_window += current_char
                # Удаляем первый символ из буфера предпросмотра.
                lookahead_buffer = lookahead_buffer[1:]
                pos += 1
            # Если совпадение найдено, кодируем подстроку.
            else:
                # Берём подстроку длиной length из буфера предпросмотра.
                matched_sequence = lookahead_buffer[:length]
                # Добавляем кортеж: (подстрока, флаг=1, смещение, длина, строковый код).
                encoded_data.append((
                    matched_sequence,
                    1,
                    offset,
                    length,
                    f"1 {offset} {length}"
                ))
                # Добавляем подстроку в окно поиска.
                search_window += matched_sequence
                # Удаляем length символов из буфера предпросмотра.
                lookahead_buffer = lookahead_buffer[length:]
                pos += length
        # Возвращаем список закодированных данных.
        return encoded_data

    def print_encoded_data(self, encoded_data):
        # Метод выводит таблицу с результатами кодирования и подсчитывает биты.
        from math import log2, ceil

        def unar(n):
            # Унарное кодирование: n-1 единиц и ноль (например, unar(3) = "110").
            return '1' * (n - 1) + '0'

        def bin_str(n):
            # Двоичное представление числа без префикса "0b" и ведущих нулей.
            return bin(n)[3:]

        def mon(i):
            # Кодирование длины: унарное представление длины двоичного числа + само число.
            # Например, mon(3): bin(3)="11", длина=2, unar(3)="110", итог="11011".
            return unar(len(bin_str(i)) + 1) + bin_str(i)

        # Выводим заголовок таблицы.
        print(
            "| ШАГ  | ФЛАГ | ПОСЛЕДОВАТЕЛЬНОСТЬ БУКВ | РАССТОЯНИЕ (d) | ДЛИНА (l) | КОДОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ | БИТЫ  |")
        print("-" * 107)

        # Подсчитываем общее количество символов во входной строке.
        total_len = sum(len(seq) if flag else 1 for seq, flag, *_ in encoded_data)
        lookahead_remaining = total_len  # Оставшиеся символы для обработки.
        total_bits = 0  # Общее количество бит.

        # Обрабатываем каждый кортеж закодированных данных.
        for i, (sequence, flag, distance, length, code) in enumerate(encoded_data):
            # Если флаг=0 (одиночный символ).
            if flag == 0:
                # Биты: 1 (флаг) + 8 (символ в ASCII).
                bits = 1 + 8
                code_str = f"0bin({sequence})"
                step_len = 1  # Длина шага — 1 символ.
            # Если флаг=1 (совпадение).
            else:
                # Реальный размер окна поиска: минимум из window_size и оставшихся символов.
                real_window = max(1, min(total_len - lookahead_remaining, self.window_size))
                print(real_window)
                # Биты для смещения: log2(размер окна + 1), округлённое вверх.
                offset_bits = max(1, ceil(log2(real_window + 1)))
                # Двоичное представление смещения с нужным количеством бит.
                offset_bin = format(distance, f'0{offset_bits}b')
                # Кодирование длины.
                if length == 1:
                    length_bin = '0'  # Длина 1 кодируется одним битом.
                else:
                    length_bin = mon(length)  # Унарное + двоичное для длины > 1.
                length_bits = len(length_bin)
                # Общее количество бит: 1 (флаг) + биты смещения + биты длины.
                bits = 1 + offset_bits + length_bits
                # Кодовая строка: флаг, смещение, длина.
                code_str = f"1 {offset_bin} {length_bin}"
                step_len = length  # Длина шага — длина совпадения.
            # Суммируем биты.
            total_bits += bits
            # Выводим строку таблицы.
            print(f"| {i:<4} | {flag:<4} | {sequence:<24}| {distance:<14} | {length:<8} | {code_str:<27}| {bits:<5} |")
            # Уменьшаем оставшиеся символы.
            lookahead_remaining -= step_len

        # Выводим разделитель и общее количество бит.
        print("-" * 107)
        print(f"{'Итого:':>95} {total_bits} бит")



if __name__ == "__main__":
    input_text = "IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN"
    lz77 = LZ77(window_size=64)
    encoded = lz77.encode(input_text)
    lz77.print_encoded_data(encoded)