from collections import defaultdict

# Словари для хранения статистики по регионам
region_stats = defaultdict(lambda: [0, 0])  # [всего_стран, грамотных_стран]

# Чтение и обработка данных за один проход
with open('input.txt', 'r', encoding='utf-8') as file:
    # Пропускаем заголовок
    file.readline()

    # Обрабатываем каждую строку.
    for line in file:
        parts = line.strip().split(';')
        if len(parts) < 6:
            continue

        region = parts[1]
        literacy = parts[5]

        # Увеличиваем счетчик стран в регионе
        region_stats[region][0] += 1

        # Проверяем грамотность
        try:
            if float(literacy) > 90.0:
                region_stats[region][1] += 1
        except ValueError:
            pass

# Вычисляем доли и находим максимальную
max_ratio = 0.0
best_regions = []

for region, (total, literate) in region_stats.items():
    if total > 0:
        ratio = literate / total
        if ratio > max_ratio:
            max_ratio = ratio
            best_regions = [region]
        elif ratio == max_ratio:
            best_regions.append(region)

# Сортируем и записываем результат
best_regions.sort()
with open('output.txt', 'w', encoding='utf-8') as output_file:
    for region in best_regions:
        output_file.write(region + '\n')