"""Core logic for table and data management."""

from prettytable import PrettyTable

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
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = []
    parsed_columns.append(("ID", "int"))

    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

        col_name, col_type = col.split(":", 1)

        if col_type not in VALID_TYPES:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

        parsed_columns.append((col_name, col_type))

    metadata[table_name] = {
        "columns": [{"name": name, "type": typ} for name, typ in parsed_columns]
    }

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


def validate_value(value, expected_type):
    """
    Validate value type.

    Args:
        value: Value to validate
        expected_type: Expected type string ("int", "str", "bool")

    Returns:
        Validated value or None if invalid
    """
    if expected_type == "int":
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    elif expected_type == "str":
        return str(value)
    elif expected_type == "bool":
        if isinstance(value, bool):
            return value
        if str(value).lower() in ("true", "1"):
            return True
        if str(value).lower() in ("false", "0"):
            return False
        return None
    return None


def insert(metadata, table_name, values, table_data):
    """
    Insert a new record into table.

    Args:
        metadata: Metadata dictionary
        table_name: Name of the table
        values: List of values (without ID)
        table_data: Current table data

    Returns:
        Updated table data or None if error
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name]["columns"]

    # Check number of values (excluding ID)
    if len(values) != len(columns) - 1:
        print(
            f"Ошибка: Ожидается {len(columns) - 1} значений, "
            f"получено {len(values)}."
        )
        return None

    # Generate new ID
    if table_data:
        new_id = max(record["ID"] for record in table_data) + 1
    else:
        new_id = 1

    # Validate and create record
    record = {"ID": new_id}

    for i, value in enumerate(values):
        col = columns[i + 1]  # Skip ID column
        col_name = col["name"]
        col_type = col["type"]

        validated_value = validate_value(value, col_type)
        if validated_value is None and col_type != "str":
            print(
                f"Ошибка: Некорректное значение '{value}' "
                f"для столбца '{col_name}' типа '{col_type}'."
            )
            return None

        record[col_name] = validated_value

    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data


def select(table_data, where_clause=None):
    """
    Select records from table.

    Args:
        table_data: Table data
        where_clause: Dictionary like {'age': 28} or None for all records

    Returns:
        List of matching records
    """
    if where_clause is None:
        return table_data

    result = []
    for record in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in record or record[key] != value:
                match = False
                break
        if match:
            result.append(record)

    return result


def update(table_name, table_data, set_clause, where_clause):
    """
    Update records in table.

    Args:
        table_name: Name of the table
        table_data: Table data
        set_clause: Dictionary like {'age': 29}
        where_clause: Dictionary like {'name': 'Sergei'}

    Returns:
        Updated table data
    """
    updated_count = 0

    for record in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in record or record[key] != value:
                match = False
                break

        if match:
            for key, value in set_clause.items():
                if key in record and key != "ID":
                    record[key] = value
                    updated_count += 1

    if updated_count > 0:
        # Get ID of first updated record for message
        for record in table_data:
            match = True
            for key, value in where_clause.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                print(
                    f'Запись с ID={record["ID"]} в таблице "{table_name}" '
                    f"успешно обновлена."
                )
                break
    else:
        print("Записи для обновления не найдены.")

    return table_data


def delete(table_name, table_data, where_clause):
    """
    Delete records from table.

    Args:
        table_name: Name of the table
        table_data: Table data
        where_clause: Dictionary like {'ID': 1}

    Returns:
        Updated table data
    """
    deleted_ids = []

    new_data = []
    for record in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in record or record[key] != value:
                match = False
                break

        if match:
            deleted_ids.append(record["ID"])
        else:
            new_data.append(record)

    if deleted_ids:
        for deleted_id in deleted_ids:
            print(
                f'Запись с ID={deleted_id} успешно удалена из таблицы "{table_name}".'
            )
    else:
        print("Записи для удаления не найдены.")

    return new_data


def display_table(table_data, columns):
    """
    Display table data using PrettyTable.

    Args:
        table_data: List of records
        columns: List of column definitions
    """
    if not table_data:
        print("Нет данных для отображения.")
        return

    table = PrettyTable()
    column_names = [col["name"] for col in columns]
    table.field_names = column_names

    for record in table_data:
        row = [record.get(col, "") for col in column_names]
        table.add_row(row)

    print(table)


def show_table_info(metadata, table_name, table_data):
    """
    Show table information.

    Args:
        metadata: Metadata dictionary
        table_name: Name of the table
        table_data: Table data
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]["columns"]
    columns_str = ", ".join([f"{col['name']}:{col['type']}" for col in columns])

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_str}")
    print(f"Количество записей: {len(table_data)}")

