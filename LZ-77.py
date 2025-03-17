class LZ77Encoder:
    def __init__(self, window_size=64):
        self.window_size = window_size

    def find_longest_match(self, search_window, lookahead_buffer):
        """Ищет самое длинное совпадение между буфером поиска и буфером просмотра."""
        max_length = 0
        best_offset = 0

        # Проверка на все возможные совпадения
        for i in range(len(search_window)):
            length = 0
            while (length < len(lookahead_buffer) and
                   i + length < len(search_window) and
                   search_window[i + length] == lookahead_buffer[length]):
                length += 1

            # Если найдено большее совпадение, обновляем
            if length > max_length:
                max_length = length
                best_offset = i

        return best_offset, max_length

    def encode(self, input_string):
        encoded_data = []
        search_window = ""
        lookahead_buffer = input_string
        pos = 0

        while pos < len(input_string):
            # Если размер окна поиска превышает, то сдвигаем
            if len(search_window) > self.window_size:
                search_window = search_window[-self.window_size:]

            # Смотрим на первый символ окна просмотра
            current_char = lookahead_buffer[0]

            # Находим совпадение в поисковом окне
            offset, length = self.find_longest_match(search_window, lookahead_buffer)

            # Если нет совпадений, добавляем символ в окно поиска
            if length == 0:
                encoded_data.append((current_char, 0))
                search_window += current_char
                lookahead_buffer = lookahead_buffer[1:]
                pos += 1
            else:
                # Если нашли совпадение, добавляем его в результат
                matched_sequence = lookahead_buffer[:length]
                encoded_data.append((matched_sequence, 1))

                # Обновляем окна
                search_window += matched_sequence
                lookahead_buffer = lookahead_buffer[length:]
                pos += length

        return encoded_data

    def print_encoded_data(self, encoded_data):
        print("| ШАГ    | ФЛАГ    | ПОСЛЕДОВАТЕЛЬНОСТЬ БУКВ    ")
        print("-" * 40)
        for i, (sequence, flag) in enumerate(encoded_data):
            print(f"| {i:<4}   | {flag:<4}    | {sequence:<20}      ")

# Пример использования
input_text = "EARLY_TO_BED_AND_EARLY_TO_RISE_MAKES_A_MAN_WISE"
lz77 = LZ77Encoder(window_size=64)
encoded = lz77.encode(input_text)
lz77.print_encoded_data(encoded)
