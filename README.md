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

### Доступные команды

- `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` - создать таблицу
- `list_tables` - показать список всех таблиц
- `drop_table <имя_таблицы>` - удалить таблицу
- `help` - справочная информация
- `exit` - выход из программы

### Поддерживаемые типы данных

- `int` - целое число
- `str` - строка
- `bool` - логическое значение

### Примеры использования

create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

list_tables

users

drop_table users
Таблица "users" успешно удалена.


**Примечание:** Столбец `ID:int` добавляется автоматически к каждой таблице.

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
├── src/
│ └── primitive_db/
│ ├── core.py # Логика работы с таблицами
│ ├── engine.py # Игровой цикл и парсинг команд
│ ├── main.py # Точка входа
│ └── utils.py # Вспомогательные функции
├── db_meta.json # Метаданные таблиц
├── Makefile
└── pyproject.toml

undefined
