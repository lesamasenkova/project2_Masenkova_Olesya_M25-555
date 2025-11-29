"""Core logic for table management."""

VALID_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    """
    Create a new table.

    Args:
        metadata: Current metadata dictionary
        table_name: Name of the table to create
        columns: List of column definitions in format "name:type"

    Returns:
        Updated metadata dictionary
    """
    # Check if table already exists
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    # Parse columns
    parsed_columns = []

    # Add ID column automatically
    parsed_columns.append(("ID", "int"))

    # Parse user-defined columns
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

        col_name, col_type = col.split(":", 1)

        if col_type not in VALID_TYPES:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

        parsed_columns.append((col_name, col_type))

    # Save table metadata
    metadata[table_name] = {
        "columns": [{"name": name, "type": typ} for name, typ in parsed_columns]
    }

    # Print success message
    columns_str = ", ".join([f"{name}:{typ}" for name, typ in parsed_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')

    return metadata


def drop_table(metadata, table_name):
    """
    Delete a table.

    Args:
        metadata: Current metadata dictionary
        table_name: Name of the table to delete

    Returns:
        Updated metadata dictionary
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata):
    """
    List all tables.

    Args:
        metadata: Current metadata dictionary
    """
    if not metadata:
        print("Таблицы отсутствуют.")
        return

    for table_name in metadata:
        print(f"- {table_name}")

