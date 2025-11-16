def parser(clause, metadata, table_name):
    """
        Перевести выражение "column = value" в словарь {'column': value}.

        clause - строковое выражение вида "column = value";
        metadata - словарь существующих таблиц в базе данных;
        table_name - название таблицы, для которой парсится выражение.
    """

    clause = clause.strip().split('=')
    column, value = clause[0].rstrip(), clause[1].lstrip()

    column_type = metadata[table_name].get(column)
    if column_type is None:
        print(f'Ошибка: Колонка {column} не существует '\
              f'в таблице {table_name}')
        return None
    if column_type == 'int' and value.isnumeric():
        value = int(value)
    elif column_type == 'bool' and value in ['true', 'false']:
        value = value == 'true'
    elif (column_type == 'str' and len(value) >= 2 and
          value[0] == value[-1] in ['"', "'"]):
        value = value.strip('"\'')
    else:
        print(f'Ошибка: Нельзя привести значение {value} '\
              f'к типу {column_type}.')
        return None
    
    return {column: value}
