from multiprocessing import Process,  Event
import shutil
from pathlib import Path

import keyboard

import matrix

MATRICES_DIR = 'matrices'
FILENAME_BASE = 'matrix'
STOP_KEY = 'x'


def task(n, min_value, max_value, stop):
    count = 1
    while not stop.is_set():
        first_matrix = matrix.sqr_random(n, min_value, max_value)
        first_matrix.write(f'{MATRICES_DIR}/{count}_{FILENAME_BASE}_first.csv')
        second_matrix = matrix.sqr_random(n, min_value, max_value)
        second_matrix.write(f'{MATRICES_DIR}/{count}_{FILENAME_BASE}_second.csv')
        result_matrix = first_matrix.multiply(
            second_matrix, f'{MATRICES_DIR}/{count}_{FILENAME_BASE}_temp.csv'
        )
        result_matrix.write(f'{MATRICES_DIR}/{count}_{FILENAME_BASE}_result.csv')
        count += 1


def recreate_matrices_dir():
    shutil.rmtree(MATRICES_DIR)
    Path(MATRICES_DIR).mkdir()


def _main():
    recreate_matrices_dir()
    stop = Event()
    n = int(input('Введите размерность матриц: '))
    min_value = int(input('Введите минимальный элемент матриц: '))
    max_value = int(input('Введите максимальный элемент матриц: '))
    p = Process(target=task, args=(n, min_value, max_value, stop))
    p.start()
    while True:
        if keyboard.is_pressed(STOP_KEY):
            stop.set()
            break
    p.join()


if __name__ == '__main__':
    _main()
