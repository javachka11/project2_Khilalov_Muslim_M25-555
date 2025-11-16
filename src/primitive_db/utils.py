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
    """
        Загрузить строки таблицы из JSON-файла в список Python.
        Если файл отсутствует, то либо таблица ещё не создана,
        либо в неё ни разу ещё не добавлялись записи.

        table_name - название таблицы, из файла которой будут
        загружаться записи.
    """

    filepath = os.path.join(DATA_DIR, table_name+'.json')
    table_data = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        table_data = []
    else:
        table_data = json.load(fp)
        fp.close()
    return table_data


def save_table_data(table_name, data, metadata):
    """
        Сохранить список записей таблицы (если она
        существует в БД) в JSON-файл.

        table_name - название таблицы, в файл которой будут сохраняться данные
        (если она существует в базе данных);
        data - список записей для сохранения;
        metadata - словарь существующих таблиц и их схем в базе данных.
    """

    if table_name in metadata.keys():
        filepath = os.path.join(DATA_DIR, table_name+'.json')
        with open(filepath, 'w') as fp:
            json.dump(data, fp)
