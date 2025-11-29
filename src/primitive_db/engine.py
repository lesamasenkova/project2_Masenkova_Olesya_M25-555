"""Engine module for handling user interaction and commands."""

import shlex

import prompt

from src.primitive_db.core import create_table, drop_table, list_tables
from src.primitive_db.utils import load_metadata, save_metadata

METADATA_FILE = "db_meta.json"


def print_help():
    """Print the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
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
    print("\n***База данных***\n")
    print("Функции:")
    print(
        "mmand> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. "
        "- создать таблицу"
    )
    print("mmand> list_tables - показать список всех таблиц")
    print("mmand> drop_table <имя_таблицы> - удалить таблицу")
    print("mmand> exit - выход из программы")
    print("mmand> help - справочная информация\n")

    while True:
        try:
            user_input = prompt.string(">>>Введите команду: ").strip()

            if not user_input:
                continue

            # Parse command using shlex for proper handling of quotes and spaces
            args = shlex.split(user_input)
            command = args[0].lower()

            # Load current metadata
            metadata = load_metadata(METADATA_FILE)

            # Process commands
            if command == "exit":
                print("Выход из программы.")
                break

            elif command == "help":
                print_help()

            elif command == "create_table":
                if len(args) < 2:
                    print("Некорректное значение. Попробуйте снова.")
                    continue

                table_name = args[1]
                columns = args[2:] if len(args) > 2 else []

                metadata = create_table(metadata, table_name, columns)
                save_metadata(METADATA_FILE, metadata)

            elif command == "drop_table":
                if len(args) < 2:
                    print("Некорректное значение. Попробуйте снова.")
                    continue

                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(METADATA_FILE, metadata)

            elif command == "list_tables":
                list_tables(metadata)

            else:
                print(f"Функции {command} нет. Попробуйте снова.")

        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

