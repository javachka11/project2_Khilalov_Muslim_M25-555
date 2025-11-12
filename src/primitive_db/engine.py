import prompt
import shlex
from src.primitive_db.utils import load_metadata, save_metadata
from src.primitive_db.core import create_table, drop_table, list_tables

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
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """
        Основная функция-обработчик команд.
    """
    
    filepath = 'src/primitive_db/db_meta.json'
    while True:
        metadata = load_metadata(filepath)
        command = welcome().lower()
        args = shlex.split(s=command, comments=True)
        match args:
            case ['create_table', table_name, *columns]:

                create_table(metadata, table_name, columns)
            case ['drop_table', table_name]:
                drop_table(metadata, table_name)
            case ['list_tables']:
                list_tables(metadata)
            case ['help']:
                print_help()
            case ['exit']:
                print('Выход из программы.\n')
                return
            case _:
                print(f'Функции <{args[0]}> нет. Попробуйте снова.')
        save_metadata(filepath, metadata)
