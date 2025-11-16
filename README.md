# Проект "Примитивная база данных"
### Домашнее задание №2. Примитивная база данных.
#### Выполнил студент Хилалов Муслим, группа М25-555

## Управление таблицами

#### Интерфейс для работы с таблицами в базе данных:

|Команда|Описание|
|:-|-:|
|`create_table` `tab_name` `column1_name:column1_type` .. |Создать таблицу `tab_name`(`column1_name:column1_type`, ..)|
|`list_tables`|Отобразить список таблиц|
|`drop_table` `tab_name`|Удалить таблицу `tab_name`|
|`help`|Отобразить команды и их описания|
|`exit`|Выйти из программы|

#### Пример работы с таблицами:

<pre>Введите команду: create_table users name:str age:int has_job:bool
Таблица &quot;users&quot; успешно создана со столбцами: id:int, name:str, age:int, has_job:bool
</pre>

<pre>Введите команду: list_tables
- users
</pre>

<pre>Введите команду: drop_table users
Таблица &quot;users&quot; успешно удалена.
</pre>

<pre>Введите команду: exit
Выход из программы.
</pre>

#### Пример работы с таблицами (asciinema):

[![asciicast](https://asciinema.org/a/kOpWCJUFBPD3y7mvGiaiMBvZV.svg)](https://asciinema.org/a/kOpWCJUFBPD3y7mvGiaiMBvZV)

## CRUD-операции

#### Интерфейс для CRUD-операций:

|Команда|Описание|
|:-|-:|
|`insert` `into` `tab_name` `values` (`value1`, ..)|Добавить новую запись (`value1`, ..) в таблицу `tab_name`|
|`select` `from` `tab_name` `where` `column = value`|Выбрать записи из таблицы `tab_name` по условию `where`|
|`select` `from` `tab_name`|Выбрать все записи из таблицы `tab_name`|
|`update` `tab_name` `set` `column = value` `where` `column = value`|Обновить записи таблицы `tab_name` по правилу `set` по условию `where`|
|`delete` `from` `tab_name` `where` `column = value`|Удалить записи из таблицы `tab_name` по условию `where`|
|`info` `tab_name`|Вывести краткую информацию по таблице `tab_name`|

#### Пример работы с CRUD-операциями:

<pre>Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, has_job:bool
Количество записей: 2</pre>

<pre>Введите команду: insert into users values (&quot;Jack&quot;, 42, true)
Запись с ID=3 успешно добавлена в таблицу &quot;users&quot;.</pre>

<pre>Введите команду: select from users
+----+--------+-----+---------+
| ID |  name  | age | has_job |
+----+--------+-----+---------+
| 1  | Sergey |  29 |   True  |
| 2  |  Max   |  31 |  False  |
| 3  |  Jack  |  42 |   True  |
+----+--------+-----+---------+
</pre>

<pre>Введите команду: select from users where has_job = true
+----+--------+-----+---------+
| ID |  name  | age | has_job |
+----+--------+-----+---------+
| 1  | Sergey |  29 |   True  |
| 3  |  Jack  |  42 |   True  |
+----+--------+-----+---------+
</pre>

<pre>Введите команду: update users set has_job = true where name = &quot;Max&quot;
Запись с ID=2 в таблице &quot;users&quot; успешно обновлена.
</pre>

<pre>Введите команду: select from users
+----+--------+-----+---------+
| ID |  name  | age | has_job |
+----+--------+-----+---------+
| 1  | Sergey |  29 |   True  |
| 2  |  Max   |  31 |   True  |
| 3  |  Jack  |  42 |   True  |
+----+--------+-----+---------+
</pre>

<pre>Введите команду: delete from users where name = &quot;Max&quot;
Запись с ID=2 успешно удалена из таблицы &quot;users&quot;.</pre>

<pre>Введите команду: select from users
+----+--------+-----+---------+
| ID |  name  | age | has_job |
+----+--------+-----+---------+
| 1  | Sergey |  29 |   True  |
| 3  |  Jack  |  42 |   True  |
+----+--------+-----+---------+
</pre>

#### Пример работы с CRUD-операциями (asciinema):

[![asciicast](https://asciinema.org/a/gbZWqY44Rxua1fFnkaJsDRhEN.svg)](https://asciinema.org/a/gbZWqY44Rxua1fFnkaJsDRhEN)