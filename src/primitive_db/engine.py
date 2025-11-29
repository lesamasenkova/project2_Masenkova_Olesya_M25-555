"""Engine module for handling user interaction and commands."""

import shlex

import prompt

from src.decorators import create_cacher
from src.primitive_db.constants import (
    INFO_INVALID_VALUE,
    METADATA_FILE,
    PROMPT_COMMAND,
)
from src.primitive_db.core import (
    create_table,
    delete,
    display_table,
    drop_table,
    insert,
    list_tables,
    select,
    show_table_info,
    update,
)
from src.primitive_db.parser import (
    parse_set_clause,
    parse_values,
    parse_where_clause,
)
from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

# Initialize cacher for select operations
cacher = create_cacher()


def print_help():
    """Print the help message."""
    print("\n***Операции с данными***\n")
    print("Функции:")
    print(
        "mmand> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) "
        "- создать запись."
    )
    print(
        "mmand> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("mmand> select from <имя_таблицы> - прочитать все записи.")
    print(
        "mmand> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "mmand> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("mmand> info <имя_таблицы> - вывести информацию о таблице.")
    print(
        "mmand> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу"
    )
    print("mmand> list_tables - показать список всех таблиц")
    print("mmand> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("mmand> exit - выход из программы")
    print("mmand> help - справочная информация\n")


def run():
    """Run the main database engine loop."""
    print_help()

    while True:
        try:
            user_input = prompt.string(PROMPT_COMMAND).strip()

            if not user_input:
                continue

            user_lower = user_input.lower()

            if user_lower == "exit":
                print("Выход из программы.")
                break

            elif user_lower == "help":
                print_help()

            elif user_lower == "list_tables":
                metadata = load_metadata(METADATA_FILE)
                list_tables(metadata)

            elif user_lower.startswith("create_table "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)
                if len(args) < 2:
                    print(INFO_INVALID_VALUE)
                    continue
                table_name = args[1]
                columns = args[2:] if len(args) > 2 else []
                metadata = create_table(metadata, table_name, columns)
                save_metadata(METADATA_FILE, metadata)

            elif user_lower.startswith("drop_table "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)
                if len(args) < 2:
                    print(INFO_INVALID_VALUE)
                    continue
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                if metadata is not None:
                    save_metadata(METADATA_FILE, metadata)

            elif user_lower.startswith("insert into "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)

                if "values" not in user_lower:
                    print(INFO_INVALID_VALUE)
                    continue

                table_name = args[2]
                values_start = next(
                    (i for i, a in enumerate(args) if a.lower() == "values"),
                    None,
                )

                if values_start is None:
                    print(INFO_INVALID_VALUE)
                    continue

                values_str = " ".join(args[values_start + 1 :])
                values = parse_values(values_str)

                table_data = load_table_data(table_name)
                table_data = insert(metadata, table_name, values, table_data)

                if table_data is not None:
                    save_table_data(table_name, table_data)

            elif user_lower.startswith("select from "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)

                table_name = args[2]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)

                where_clause = None
                if "where" in user_lower:
                    where_idx = next(
                        (i for i, a in enumerate(args) if a.lower() == "where"),
                        None,
                    )
                    if where_idx is not None:
                        where_str = " ".join(args[where_idx + 1 :])
                        where_clause = parse_where_clause(where_str)

                # Use cacher for select results
                cache_key = f"{table_name}:{where_clause}"
                result = cacher(
                    cache_key, lambda: select(table_data, where_clause)
                )
                columns = metadata[table_name]["columns"]
                display_table(result, columns)

            elif user_lower.startswith("update "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)

                if "set" not in user_lower or "where" not in user_lower:
                    print(INFO_INVALID_VALUE)
                    continue

                table_name = args[1]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                set_idx = next(
                    (i for i, a in enumerate(args) if a.lower() == "set"), None
                )
                where_idx = next(
                    (i for i, a in enumerate(args) if a.lower() == "where"),
                    None,
                )

                if set_idx is None or where_idx is None:
                    print(INFO_INVALID_VALUE)
                    continue

                set_str = " ".join(args[set_idx + 1 : where_idx])
                where_str = " ".join(args[where_idx + 1 :])

                set_clause = parse_set_clause(set_str)
                where_clause = parse_where_clause(where_str)

                if not set_clause or not where_clause:
                    print(INFO_INVALID_VALUE)
                    continue

                table_data = load_table_data(table_name)
                table_data = update(
                    table_name, table_data, set_clause, where_clause
                )
                save_table_data(table_name, table_data)

            elif user_lower.startswith("delete from "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)

                if "where" not in user_lower:
                    print(INFO_INVALID_VALUE)
                    continue

                table_name = args[2]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                where_idx = next(
                    (i for i, a in enumerate(args) if a.lower() == "where"),
                    None,
                )

                if where_idx is None:
                    print(INFO_INVALID_VALUE)
                    continue

                where_str = " ".join(args[where_idx + 1 :])
                where_clause = parse_where_clause(where_str)

                if not where_clause:
                    print(INFO_INVALID_VALUE)
                    continue

                table_data = load_table_data(table_name)
                table_data = delete(table_name, table_data, where_clause)
                # Проверяем подтверждение (если None, пользователь отказал)
                if table_data is not None:
                    save_table_data(table_name, table_data)

            elif user_lower.startswith("info "):
                args = shlex.split(user_input)
                metadata = load_metadata(METADATA_FILE)

                if len(args) < 2:
                    print(INFO_INVALID_VALUE)
                    continue

                table_name = args[1]
                table_data = load_table_data(table_name)
                show_table_info(metadata, table_name, table_data)

            else:
                print(f"Функции {user_lower.split()[0]} нет. Попробуйте снова.")

        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

