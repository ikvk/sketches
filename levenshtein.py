"""
Примерный алгоритм, который можно применить для сравнения ФИО с учетом возможного изменения порядка слов и опечаток:

Применение Расстояния Левенштейна:
    Рассчитайте расстояние Левенштейна между двумя ФИО.
    Определите порог расстояния Левенштейна, который будет указывать на то,
    насколько два ФИО считаются достаточно похожими.
Учет изменения порядка слов:
    Для учета изменения порядка слов в ФИО можно рассчитать расстояние Левенштейна
    для всех возможных перестановок слов и выбрать минимальное значение.
"""

import itertools
import Levenshtein

def compare_names(name1, name2):
    permutations_name1 = [' '.join(p) for p in itertools.permutations(name1.split())]
    permutations_name2 = [' '.join(p) for p in itertools.permutations(name2.split())]
    min_distance = float('inf')
    for perm1 in permutations_name1:
        for perm2 in permutations_name2:
            distance = Levenshtein.distance(perm1, perm2)
            if distance < min_distance:
                min_distance = distance
    return min_distance

name1 = "Иванов Петр Сергеевич"
# name2 = "Петров Иван Сергеевич"
name2 = "Петр Иванов123 Сергеевич"
distance = compare_names(name1, name2)

print(distance)
if distance <= 3:
    print("ФИО считаются достаточно похожими.")
else:
    print("ФИО не считаются достаточно похожими.")
