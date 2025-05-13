def shell_sort(arr, h_sequence):
    N = len(arr)
    t = len(h_sequence)

    for s in range(t - 1, -1, -1):
        h = h_sequence[s]
        print(f"\n=== Шаг h={h} ===")
        print(f"Массив до сортировки: {arr}")

        # Формируем подгруппы
        subgroups = []
        for start in range(h):
            subgroup = [arr[i] for i in range(start, N, h)]
            subgroups.append(subgroup)
        print(f"Подгруппы до сортировки: {subgroups}")

        # Сортировка вставками с шагом h
        for j in range(h, N):
            K = arr[j]
            i = j - h
            print(f"\nШаг вставки: j = {j} (значение {K})")

            while i >= 0 and K < arr[i]:
                print(f"  i = {i}, arr[{i}] = {arr[i]}, K = {K}")
                print(f"  {K} < {arr[i]} → сдвигаем {arr[i]} вправо: arr[{i + h}] = {arr[i]}")
                arr[i + h] = arr[i]
                i -= h

            print(f"  Вставляем {K} на позицию arr[{i + h}]")
            arr[i + h] = K

            # Показать текущее состояние подгруппы после вставки
            start = j % h
            updated_subgroup = [arr[k] for k in range(start, N, h)]
            print(f"  Подгруппа после вставки: {updated_subgroup}")

    return arr


# Тестовый массив и шаги
# array = [32, 47, 2, 65, 89, 30, 52, 14, 76, 22, 35, 10]
array = [503, 87, 512, 61, 908, 170, 897, 275, 653, 426, 154, 509, 612, 677, 765, 703]
h_sequence = [1, 2, 4, 8]

sorted_array = shell_sort(array.copy(), h_sequence)

print("\nОтсортированный массив:", sorted_array)
if sorted_array == sorted(array):
    print("Массив отсортирован корректно")
else:
    print("Ошибка сортировки")
