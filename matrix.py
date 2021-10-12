import csv
import random
from concurrent.futures import ProcessPoolExecutor, as_completed


class Matrix:

    @classmethod
    def read(cls, filename):
        """
        filename: csv файл для записи.

        Считывает значения матрицы из csv файла filename.
        """
        with open(filename, newline='') as file:
            reader = csv.reader(file, delimiter=';')
            return cls([list(map(int, row)) for row in reader])

    def __init__(self, matrix=None, rows=None, columns=None):
        """
        Если корректно указаны rows и columns, создается матрица размера
        row * columns, заполненная элементами None.

        matrix: двумерный список - матрица.
        row: число строк.
        columns: число столбцов.
        """
        if rows and columns:
            self._matrix = [[None] * columns for _ in range(rows)]
        else:
            self._matrix = matrix

    @property
    def rows(self):
        """
        Возвращает количество строк матрицы.
        """
        return len(self._matrix)

    @property
    def columns(self):
        """
        Возвращает количество столбцов матрицы.
        """
        return len(self._matrix[0])

    def write(self, filename):
        """
        filename: csv файл для записи.

        Создает (перезаписывает) csv файл filename текущими значениями матрицы.
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(self._matrix)

    def multiply(self, other, filename=None, max_processes=None):
        """
        Умножает матрицу other на текущую в нескольких процессах.

        other: объект типа Matrix, вторая матрица для умножения на текущую.
        filename: имя промежуточного csv файла для записи значений при их
        подсчете в процессе.
        max_processes: максимальное кол-во одновременно работающих потоков. По
        умолчанию это число равно кол-ву элементов результирующей матрицы.
        """

        # Вычисляем кол-во потоков максимально, если значение не указано.
        if max_processes is None:
            max_processes = self.rows * other.columns

        # Добавляем в пул процессов новые процессы. В двух циклах формируем все
        # пары индексов, по котором нужно вычислить элементы результирующей
        # матрицы. Помимо создания процесса, сохраняем ссылку на объект,
        # который мы будем использовать для получения результата, когда
        # процесс завершится.
        results = []
        with ProcessPoolExecutor(max_processes) as executor:
            for row in range(self.rows):
                for column in range(other.columns):
                    results.append(
                        executor.submit(self._dot_product, other, row, column)
                    )

        # Создаем пустую матрицу нужной размерности. В нее будеем записывать
        # результаты.
        result_matrix = type(self)(rows=self.rows, columns=other.columns)

        # Интерируемся по последовальности завершенных процессов и запоминаем
        # результат вычисления, индекс строки и колонки этого результата.
        # Затем заполняем по этим индексам значение в новой матрице. Если
        # промежточный файл указан, записываем то, что есть в результирующей
        # матрице.
        for future in as_completed(results):
            value, row, column = future.result()
            result_matrix._matrix[row][column] = value
            if filename is not None:
                result_matrix.write(filename)
        return result_matrix

    def _dot_product(self, other, row, column):
        """
        Возвращает результат вычисления элемента результирующей матрицы.

        other: объект типа Matrix, вторая матрица для умножения на текущую.
        row: индекс строки элемента результирующей матрицы.
        column: индекс столбца элемента результирующей матрицы.
        """
        return sum([
            self._matrix[row][i] * other._matrix[i][column]
            for i in range(other.rows)
        ]), row, column


def sqr_random(n, min, max):
    return Matrix(
        [[random.randint(min, max) for _ in range(n)] for _ in range(n)]
    )