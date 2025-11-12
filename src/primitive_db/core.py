def create_table(metadata, table_name, columns):
    """
        Создать таблицу в базе данных.
        Если таблица с таким названием уже есть в БД, то вывести ошибку.
        Если дан некорректный тип данных для колонки, то вывести ошибку. 

        metadata - словарь существующих таблиц в базе данных;
        table_name - название создаваемой таблицы;
        columns - список элементов вида <имя_колонки>:<тип_данных_колонки>
        (возможные типы данных колонок - int, str, bool).
    """

    if table_name in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return

    table = dict()
    table['id'] = 'int'
    table.update(col.lower().split(':') for col in columns)

    disp_cols = ''

    for key, val in table.items():
        if val not in ['int', 'str', 'bool']:
            print(f'Некорректное значение: <{val}>. Попробуйте снова.')
            return

        disp_cols += f'{key}:{val}, '
    
    print(f'Таблица "{table_name}" успешно создана ' \
          f'со столбцами: {disp_cols[:-2]}')
    
    metadata[table_name] = table


def drop_table(metadata, table_name):
    """
        Удалить таблицу из базы данных.
        Если таблицы там нет, то выводится ошибка.

        metadata - словарь существующих таблиц в базе данных;
        table_name - название удаляемой таблицы.
    """

    table = metadata.pop(table_name, None)
    if table is None:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    else:
        print(f'Таблица "{table_name}" успешно удалена.')


def list_tables(metadata):
    """
        Отобразить существующие в базе данных таблицы.

        metadata - словарь существующих таблиц в базе данных.
    """

    for table_name in metadata.keys():
        print(f'- {table_name}')
