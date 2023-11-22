"""
Salesman
---
Решает задачу коммивояжера, заданную матрицей в файле,
и выводит решение в терминал.
"""

def read_matrix(path):
    """Чтение матрицы из файла."""
    matrix = []
    with open(path, 'r', encoding='utf-8') as file:
        source = file.read().split('\n')
    for i in source:
        line = list(map(int, i.split()))
        matrix.append(line)
    return matrix

def minimal(lst, myindex):
    """Находит минимальный элемент, исключая текущий."""
    return min(x for idx, x in enumerate(lst) if idx != myindex)

def delete_item(mtrx, index1, index2):
    """Удаляет нужные строку и столбцец."""
    del mtrx[index1]
    for i in mtrx:
        del i[index2]
    return mtrx

def print_matrix(matrix, separator):
    """Печатает матрицу в терминал."""
    print(separator)
    for i in range(len(matrix)):
        print('\t'.join([str(j) if j != 0 else '-' for j in matrix[i]]))
    print(separator)

def main(path: str):
    """Главная функция, выполняющая алгоритм решения задачи."""
    h = 0
    path_length = 0
    row_indexes = []
    column_indexes = []
    res = []
    result = []
    start_matrix = []

    # Читаем матрицу из файла
    matrix = read_matrix(path)
    print('Исходная матрица:')
    n = len(matrix)
    separator = '=======\t' * n
    print_matrix(matrix, separator)

    # Инициализируем массивы для сохранения индексов
    for i in range(n):
        row_indexes.append(i)
        column_indexes.append(i)

    # Сохраняем изначальную матрицу
    for i in range(n):
        start_matrix.append(matrix[i].copy())

    # Присваеваем главной диагонали float(inf)
    for i in range(n):
        matrix[i][i] = float('inf')

    while True:
        # Редуцируем
        # Вычитаем минимальный элемент в строках
        for i in range(len(matrix)):
            temp = min(matrix[i])
            h += temp
            for j in range(len(matrix)):
                matrix[i][j] -= temp

        # Вычитаем минимальный элемент в столбцах
        for i in range(len(matrix)):
            temp = min(row[i] for row in matrix)
            h += temp
            for j in range(len(matrix)):
                matrix[j][i] -= temp

        # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
        null_max = 0
        index_1 = 0
        index_2 = 0
        tmp = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:
                    tmp = minimal(matrix[i], j) + minimal((row[j] for row in matrix), i)
                    if tmp >= null_max:
                        null_max = tmp
                        index_1 = i
                        index_2 = j

        # Находим нужный нам путь, записываем его в res и удаляем все ненужное
        res.append(row_indexes[index_1]+1)
        res.append(column_indexes[index_2]+1)

        old_index_1 = row_indexes[index_1]
        old_index_2 = column_indexes[index_2]
        if old_index_2 in row_indexes and old_index_1 in column_indexes:
            new_index_1 = row_indexes.index(old_index_2)
            new_index_2 = column_indexes.index(old_index_1)
            matrix[new_index_1][new_index_2] = float('inf')
        del row_indexes[index_1]
        del column_indexes[index_2]
        matrix = delete_item(matrix, index_1, index_2)
        if len(matrix) == 1:
            break

    # Формируем порядок пути
    for i in range(0, len(res)-1, 2):
        if res.count(res[i]) < 2:
            result.append(res[i])
            result.append(res[i+1])
    for i in range(0, len(res)-1, 2):
        for j in range(0, len(res)-1, 2):
            if result[len(result)-1] == res[j]:
                result.append(res[j])
                result.append(res[j+1])
    print('Путь:')
    print(separator)
    print(f'1->{result[0]}', end=' ')
    for i in range(0, len(result), 2):
        print(result[i], result[i+1], sep='->', end=' ')

    # Считаем длину пути
    for i in range(0, len(result)-1, 2):
        if i == len(result)-2:
            path_length += start_matrix[result[i]-1][result[i+1]-1]
            path_length += start_matrix[result[i+1]-1][result[0]-1]
        else:
            path_length += start_matrix[result[i]-1][result[i+1]-1]
    print('=', path_length)
    print(separator)

if __name__ == '__main__':
    main('matrix1.txt')
