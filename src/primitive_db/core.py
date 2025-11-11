def create_table(metadata, table_name, columns):
    if table_name in metadata.keys():
        print(f'Ошибка: таблица с именем {table_name} уже существует.')
        return None

    d = dict()
    d['id'] = 'int'
    d.update(col.strip().lower().split(':') for col in columns)

    for k, v in d.items():
        if v not in ['int', 'str', 'bool']:
            print(f'Ошибка: некорректный тип данных для столбца {k} - {v}.')
            return None
    
    metadata[table_name] = d
    return metadata


def drop_table(metadata, table_name):
    table = metadata.pop(table_name)
    if table is None:
        print(f'Ошибка: таблицы с именем {table_name} не существует.')
        return None
    
    return metadata
