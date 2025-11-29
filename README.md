text
# project2_Masenkova_Olesya_M25-555

Primitive database management system - консольное приложение для управления примитивной базой данных.

## Установка

Клонирование репозитория
git clone https://github.com/lesamasenkova/project2_Masenkova_Olesya_M25-555.git
cd project2_Masenkova_Olesya_M25-555

Установка зависимостей
make install

## Запуск

Запуск через make
make project

Или напрямую через poetry
poetry run project

## Управление таблицами

### Команды создания и удаления таблиц

- `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` - создать таблицу
- `list_tables` - показать список всех таблиц
- `drop_table <имя_таблицы>` - удалить таблицу

### Поддерживаемые типы данных

- `int` - целое число
- `str` - строка
- `bool` - логическое значение

### Пример

create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

list_tables

users

## CRUD-операции

### Доступные команды

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` - добавить запись
- `select from <имя_таблицы>` - показать все записи
- `select from <имя_таблицы> where <столбец> = <значение>` - показать записи по условию
- `update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>` - обновить записи
- `delete from <имя_таблицы> where <столбец> = <значение>` - удалить записи
- `info <имя_таблицы>` - показать информацию о таблице
- `help` - справочная информация
- `exit` - выход из программы

### Примеры использования

insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

select from users
+----+--------+-----+-----------+
| ID | name | age | is_active |
+----+--------+-----+-----------+
| 1 | Sergei | 28 | True |
+----+--------+-----+-----------+

select from users where age = 28
+----+--------+-----+-----------+
| ID | name | age | is_active |
+----+--------+-----+-----------+
| 1 | Sergei | 28 | True |
+----+--------+-----+-----------+

update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице "users" успешно обновлена.

delete from users where ID = 1
Запись с ID=1 успешно удалена из таблицы "users".

info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0


**Важно:** 
- Столбец `ID` генерируется автоматически и не указывается при вставке
- Строковые значения должны быть в кавычках: `"text"`
- Логические значения: `true` или `false`

## Сборка и публикация

Сборка пакета
make build

Отладка публикации
make publish

Установка пакета в систему
make package-install

## Проверка качества кода

make lint


## Структура проекта

project2_Masenkova_Olesya_M25-555/
├── data/ # Данные таблиц (.json файлы)
├── src/
│ └── primitive_db/
│ ├── core.py # Логика CRUD операций
│ ├── engine.py # Главный цикл и парсинг команд
│ ├── main.py # Точка входа
│ ├── parser.py # Парсеры SQL-like команд
│ └── utils.py # Работа с файлами
├── db_meta.json # Метаданные таблиц
├── Makefile
└── pyproject.toml

undefined
