import prompt
import shlex
from src.primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data
from src.primitive_db.core import create_table, drop_table, list_tables, insert, select, update, delete, info
from src.primitive_db.parser import parser
from prettytable import PrettyTable


def welcome():
    """
        Отобразить приглашение для ввода команды.
    """
    
    command = prompt.string('\nВведите команду: ')
    return command



def print_help():
    """
        Отобразить список команд и их описания.
    """
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> "\
          ".. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values "\
          "(<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> "
          "where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "\
          "where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where "\
          "<столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")


    print("\nОбщие команды:")
    print("<command> exit | quit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """
        Основная функция-обработчик команд.
    """
    
    filepath = 'db_meta.json'
    while True:
        command = welcome()
        metadata = load_metadata(filepath)
        sh = shlex.shlex(command, punctuation_chars='()')
        sh.whitespace = ',= '
        sh.whitespace_split = True
        args = list(sh)

        match args:
            case ['create_table', table_name, *columns]:
                create_table(metadata, table_name, columns)

            case ['drop_table', table_name]:
                save_table_data(table_name, [], metadata)
                drop_table(metadata, table_name)

            case ['list_tables']:
                list_tables(metadata)

            case ['insert', 'into', table_name, 'values', '(', *values, ')']:
                table_data = load_table_data(table_name)
                insert(metadata, table_data, table_name, values)
                save_table_data(table_name, table_data, metadata)

            case ['select', 'from', table_name, 'where', where_column, where_value]:
                table_data = load_table_data(table_name)
                where_clause = parser('='.join([where_column, where_value]),
                                      metadata, table_name)
                if where_clause is not None:
                    select_data = select(metadata, table_data, table_name, where_clause)

                    if select_data is not None:
                        select_table = PrettyTable()
                        select_table.field_names = list(metadata[table_name].keys())
                        select_table.add_rows(select_data)
                        print(select_table)
            
            case ['select', 'from', table_name]:
                table_data = load_table_data(table_name)
                select_data = select(metadata, table_data, table_name, None)

                if select_data is not None:
                    select_table = PrettyTable()
                    select_table.field_names = list(metadata[table_name].keys())
                    select_table.add_rows(select_data)
                    print(select_table)

            case ['update', table_name, 'set', set_column, set_value,
                  'where', where_column, where_value]:
                table_data = load_table_data(table_name)
                set_clause = parser('='.join([set_column, set_value]),
                                      metadata, table_name)
                where_clause = parser('='.join([where_column, where_value]),
                                      metadata, table_name)
                update(metadata, table_data, table_name, set_clause, where_clause)
                save_table_data(table_name, table_data, metadata)

            case ['delete', 'from', table_name, 'where', where_column, where_value]:
                table_data = load_table_data(table_name)
                where_clause = parser('='.join([where_column, where_value]),
                                      metadata, table_name)
                delete(metadata, table_data, table_name, where_clause)
                save_table_data(table_name, table_data, metadata)

            case ['info', table_name]:
                table_data = load_table_data(table_name)
                info(metadata, table_data, table_name)

            case ['help']:
                print_help()

            case ['exit']:
                print('Выход из программы.\n')
                return
            
            case ['quit']:
                print('Выход из программы.\n')
                return
            
            case _:
                print(f'Команда не найдена. Попробуйте снова.')
        save_metadata(filepath, metadata)
