"""Engine module for handling user interaction and commands."""

import prompt


def welcome():
    """Display welcome message and handle user commands."""
    print("\nПервая попытка запустить проект!")
    print("\n***")
    print("mmand> exit - выйти из программы")
    print("mmand> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ").strip().lower()

        if command == "exit":
            print("Выход из программы.")
            break
        elif command == "help":
            print("\nmmand> exit - выйти из программы")
            print("mmand> help - справочная информация")
        else:
            print(f"Неизвестная команда: {command}")

