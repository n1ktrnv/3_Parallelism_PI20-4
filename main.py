from matrix import Matrix


FILENAME_BASE = 'matrix'


def _main():
    matrix1 = Matrix.read(f'{FILENAME_BASE}_1.csv')
    matrix2 = Matrix.read(f'{FILENAME_BASE}_2.csv')
    result_matrix = matrix1.multiply(matrix2, f'{FILENAME_BASE}_tmp.csv')
    result_matrix.write(f'result_{FILENAME_BASE}_result.csv')


if __name__ == '__main__':
    _main()
