import json
import os


DATA_DIR = 'data/'

def load_metadata(filepath):
    """
        Загрузить словарь с таблицами базы данных из JSON-файла.
        Если файла по данному пути не существует, то вернуть пустой словарь.

        filepath - путь к JSON-файлу (относительно корневого каталога проекта).
    """

    metadata = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        metadata = dict()
    else:
        metadata = json.load(fp)
        fp.close()
    return metadata


def save_metadata(filepath, data):
    """
        Сохранить словарь с таблицами в JSON-файл базы данных.

        filepath - путь к JSON-файлу (относительно корневого каталога проекта)
        (если файла не существует, он будет создан);
        data - сохраняемый словарь с таблицами.
    """

    with open(filepath, 'w') as fp:
        json.dump(data, fp)


def load_table_data(table_name):
    filepath = os.path.join(DATA_DIR, table_name+'.json')

    metadata = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        metadata = dict()
    else:
        metadata = json.load(fp)
        fp.close()
    return metadata


def save_table_data(table_name, data):
    filepath = os.path.join(DATA_DIR, table_name+'.json')

    with open(filepath, 'w') as fp:
        json.dump(data, fp)