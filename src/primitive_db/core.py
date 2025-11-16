import os
from src.primitive_db.parser import parser


DATA_DIR = 'data/'

def create_table(metadata, table_name, columns):
    """
        Создать таблицу в базе данных.
        Если таблица с таким названием уже есть в БД, то вывести ошибку.
        Если дан некорректный тип данных для колонки, то вывести ошибку.

        metadata - словарь существующих таблиц и их схем в базе данных;
        table_name - название создаваемой таблицы;
        columns - список элементов вида <имя_колонки>:<тип_данных_колонки>
        (возможные типы данных колонок - int, str, bool).
    """

    if table_name in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    table = dict()
    table['ID'] = 'int'
    table.update(col.lower().split(':') for col in columns)

    disp_cols = ''

    for key, val in table.items():
        if val not in ['int', 'str', 'bool']:
            print(f'Некорректное значение: <{val}>. Попробуйте снова.')
            return None

        disp_cols += f'{key}:{val}, '
    
    print(f'Таблица "{table_name}" успешно создана ' \
          f'со столбцами: {disp_cols[:-2]}')    
    metadata[table_name] = table


def drop_table(metadata, table_name):
    """
        Удалить таблицу из базы данных.
        Если таблицы там нет, то выводится ошибка.

        metadata - словарь существующих таблиц и их схем в базе данных;
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

        metadata - словарь существующих таблиц и их схем в базе данных.
    """

    for table_name in metadata.keys():
        print(f'- {table_name}')


def insert(metadata, table_data, table_name, values):
    """
        Вставить новую запись (строку) в таблицу.

        metadata - словарь существующих таблиц и их схем в базе данных;
        table_data - список записей (строк) таблицы (вставка производится in place);
        table_name - название таблицы, куда производится вставка.
    """

    if table_name not in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    
    num_values = len(values)
    num_columns = len(metadata[table_name])

    if num_values != num_columns - 1:
        print(f'Ошибка: В таблице {num_columns} колонок, '\
              f'а было передано {num_values+1} значений.')
        return None
    
    columns = list(metadata[table_name].keys())

    validate_values = []

    for i in range(1,num_columns):
        val_dict = parser('='.join([columns[i], values[i-1]]),
                          metadata, table_name)
        if val_dict is None:
            return None
        validate_values.append(val_dict[columns[i]])

    entry_id = len(table_data) + 1
    values = [entry_id] + validate_values

    entry = dict(zip(columns, values))

    table_data.append(entry)
    print(f'Запись с ID={entry_id} успешно добавлена в таблицу "{table_name}".')



def select(metadata, table_data, table_name, where_clause=None):
    """
        Выбрать подмножество записей из таблицы в соответствии с условием
        в where_clause.

        metadata - словарь существующих таблиц и их схем в базе данных;
        table_data - список записей (строк) таблицы;
        table_name - название таблицы, откуда берётся подмножество строк;
        where_clause - словарь вида {'column': value}, по которому выбирается
        подмножество записей (строки, для которых column == value).
        Если None, то возвращается вся таблица целиком.
    """
    
    if table_name not in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    if where_clause is None:
        return [list(entry.values()) for entry in table_data]
    if not isinstance(where_clause, dict):
        print('Ошибка: Некорректное значение параметра <where_clause>.')
        return None
    
    where_column, where_value = next(iter(where_clause.items()))
        
    if where_column not in metadata[table_name].keys():
        print(f'Ошибка: Колонка {where_column} не существует '\
              f'в таблице {table_name}')
        return None
        
    select_result = []
    for entry in table_data:
        value = entry[where_column]
        if value == where_value:
            select_result.append(list(entry.values()))
    
    return select_result
    

def update(metadata, table_data, table_name, set_clause, where_clause):
    """
        Обновить в таблице атрибут (колонку) по правилу set_clause,
        для записей (строк), удовлетворяющих правилу where_clause.

        metadata - словарь существующих таблиц и их схем в базе данных;
        table_data - список записей (строк) таблицы (обновление происходит in place);
        table_name - название таблицы, в которой происходит обновление;
        set_clause - словарь вида {'column': value}, задающий изменение
        текущего значения колонки column на значение value;
        where_clause - словарь вида {'column': value}, по которому выбирается
        подмножество записей для обновления (строки, для которых column == value).
    """

    if table_name not in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    if not isinstance(set_clause, dict):
        print('Ошибка: Некорректное значение параметра <set_clause>.')
        return None
    if not isinstance(where_clause, dict):
        print('Ошибка: Некорректное значение параметра <where_clause>')
        return None

    set_column, set_value = next(iter(set_clause.items()))
    where_column, where_value = next(iter(where_clause.items()))

    if set_column not in metadata[table_name].keys():
        print(f'Ошибка: Колонка {set_column} не существует '\
              f'в таблице {table_name}')
        return None
    
    if where_column not in metadata[table_name].keys():
        print(f'Ошибка: Колонка {where_column} не существует '\
              f'в таблице {table_name}')
        return None

    for entry in table_data:
        value = entry[where_column]
        if value == where_value:
            entry[set_column] = set_value
            print(f'Запись с ID={entry["ID"]} в таблице '\
                  f'"{table_name}" успешно обновлена.')



def delete(metadata, table_data, table_name, where_clause):
    """
        Удалить из таблицы записи (строки), для которых выполняется
        условие where_clause.

        metadata - словарь существующих таблиц и их схем в базе данных;
        table_data - список записей (строк) таблицы (удаление происходит in place);
        table_name - название таблицы, в которой происходит удаление;
        where_clause - словарь вида {'column': value}, по которому выбирается
        подмножество записей для удаления (строки, для которых column == value).
    """

    if table_name not in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    
    if not isinstance(where_clause, dict):
        print('Ошибка: Некорректное значение параметра <where_clause>.')
        return None
    
    where_column, where_value = next(iter(where_clause.items()))
    if where_column not in metadata[table_name].keys():
        print(f'Ошибка: Колонка {where_column} не существует '\
              f'в таблице {table_name}')
        return None
    
    for ind, entry in enumerate(table_data):
        value = entry[where_column]
        if value == where_value:
            del table_data[ind]
            print(f'Запись с ID={entry["ID"]} успешно удалена '\
                  f'из таблицы "{table_name}".')


def info(metadata, table_data, table_name):
    """
        Вывести краткую информацию по таблице.

        metadata - словарь существующих таблиц и их схем в базе данных;
        table_data - список записей (строк) таблицы;
        table_name - название таблицы.
    """
    
    if table_name not in metadata.keys():
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    
    info_result = f'Таблица: {table_name}\nСтолбцы: '

    info_result += ', '.join(f'{col_name}:{col_type}'
                             for col_name, col_type in
                             metadata[table_name].items())
    info_result += f'\nКоличество записей: {len(table_data)}'

    print(info_result)
