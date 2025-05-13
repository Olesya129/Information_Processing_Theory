import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Загрузка датасета MNIST с OpenML (70,000 изображений рукописных цифр 28x28)
mnist = fetch_openml('mnist_784', version=1)
# Нормализация данных: преобразование значений пикселей из 0-255 в 0-1
X = mnist['data'].values / 255.0
# Преобразование меток в целые числа (0-9)
y = mnist['target'].values.astype(int)

# Разделение данных на обучающую (70%) и тестовую (30%) выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Масштабирование данных: стандартизация (среднее = 0, стандартное отклонение = 1)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Создание модели нейронной сети: 1 скрытый слой с 128 нейронами, ReLU, Adam, 10 итераций
model = MLPClassifier(hidden_layer_sizes=(128,), max_iter=10, activation='relu', solver='adam', random_state=42)
# Обучение модели на обучающей выборке
model.fit(X_train, y_train)

# Предсказание меток для тестовой выборки
y_pred = model.predict(X_test)
# Вычисление точности модели
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность модели: {accuracy * 100:.2f}%")

# Подсчет числа корректно обработанных изображений и ошибок
correct = np.sum(y_test == y_pred)  # Количество совпадений (истинная метка = предсказанная)
errors_count = len(y_test) - correct  # Количество ошибок (общее - корректные)
print(f"Корректно обработано изображений: {correct} из {len(y_test)}")
print(f"Изображений с ошибкой: {errors_count}")


n_images = 20
n_rows = 2
n_cols = n_images // n_rows if n_images % n_rows == 0 else n_images // n_rows + 1
plt.figure(figsize=(n_cols * 2, n_rows * 3))
for i in range(n_images):
    plt.subplot(n_rows, n_cols, i + 1)
    plt.imshow(X_test[i].reshape(28, 28), cmap='gray')
    plt.title(f'Истинная: {y_test[i]}\nПредсказание: {y_pred[i]}', fontsize=8)
    plt.axis('off')
plt.tight_layout()
plt.show()

# Окно 2: Визуализация несовпадений (до 3 ошибок)
errors = np.where(y_test != y_pred)[0]  # Индексы, где предсказания ошибочны

if len(errors) > 0:
    n_errors = min(3, len(errors))  # Ограничение до 3 ошибок
    plt.figure(figsize=(9, 3))
    for i, idx in enumerate(errors[:n_errors]):
        plt.subplot(1, 3, i + 1)
        plt.imshow(X_test[idx].reshape(28, 28), cmap='gray')
        plt.title(f'Истинная: {y_test[idx]}\nПредсказание: {y_pred[idx]}', fontsize=10)
        plt.axis('off')
    plt.tight_layout()
    plt.show()
else:
    print("Ошибок не найдено!")