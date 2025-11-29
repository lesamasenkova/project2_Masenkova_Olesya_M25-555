"""Core logic for table and data management."""

from prettytable import PrettyTable

from src.decorators import confirm_action, handle_db_errors, log_time
from src.primitive_db.constants import (
    CONFIRM_DELETE_RECORD,
    CONFIRM_DELETE_TABLE,
    ERROR_INVALID_VALUE,
    ERROR_TABLE_EXISTS,
    ERROR_TABLE_NOT_FOUND,
    INFO_NO_DATA,
    INFO_NO_DELETIONS,
    INFO_NO_TABLES,
    INFO_NO_UPDATES,
    SUCCESS_RECORD_DELETED,
    SUCCESS_RECORD_INSERTED,
    SUCCESS_RECORD_UPDATED,
    SUCCESS_TABLE_CREATED,
    SUCCESS_TABLE_DELETED,
    VALID_TYPES,
)


@handle_db_errors
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
        raise KeyError(ERROR_TABLE_EXISTS.format(table_name=table_name))

    parsed_columns = []
    parsed_columns.append(("ID", "int"))

    for col in columns:
        if ":" not in col:
            raise ValueError(f"Некорректное значение: {col}")

        col_name, col_type = col.split(":", 1)

        if col_type not in VALID_TYPES:
            raise ValueError(f"Некорректное значение: {col}")

        parsed_columns.append((col_name, col_type))

    metadata[table_name] = {
        "columns": [{"name": name, "type": typ} for name, typ in parsed_columns]
    }

    columns_str = ", ".join([f"{name}:{typ}" for name, typ in parsed_columns])
    print(
        SUCCESS_TABLE_CREATED.format(
            table_name=table_name, columns_str=columns_str
        )
    )

    return metadata


@confirm_action(CONFIRM_DELETE_TABLE)
@handle_db_errors
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
        raise KeyError(ERROR_TABLE_NOT_FOUND.format(table_name=table_name))

    del metadata[table_name]
    print(SUCCESS_TABLE_DELETED.format(table_name=table_name))

    return metadata


@handle_db_errors
def list_tables(metadata):
    """
    List all tables.

    Args:
        metadata: Current metadata dictionary
    """
    if not metadata:
        print(INFO_NO_TABLES)
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


@handle_db_errors
@log_time
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
        raise KeyError(ERROR_TABLE_NOT_FOUND.format(table_name=table_name))

    columns = metadata[table_name]["columns"]

    if len(values) != len(columns) - 1:
        raise ValueError(
            f"Ожидается {len(columns) - 1} значений, получено {len(values)}."
        )

    if table_data:
        new_id = max(record["ID"] for record in table_data) + 1
    else:
        new_id = 1

    record = {"ID": new_id}

    for i, value in enumerate(values):
        col = columns[i + 1]
        col_name = col["name"]
        col_type = col["type"]

        validated_value = validate_value(value, col_type)
        if validated_value is None and col_type != "str":
            raise ValueError(
                ERROR_INVALID_VALUE.format(
                    value=value, column=col_name, col_type=col_type
                )
            )

        record[col_name] = validated_value

    table_data.append(record)
    print(
        SUCCESS_RECORD_INSERTED.format(
            record_id=new_id, table_name=table_name
        )
    )

    return table_data


@handle_db_errors
@log_time
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


@handle_db_errors
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
        for record in table_data:
            match = True
            for key, value in where_clause.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                print(
                    SUCCESS_RECORD_UPDATED.format(
                        record_id=record["ID"], table_name=table_name
                    )
                )
                break
    else:
        print(INFO_NO_UPDATES)

    return table_data


@confirm_action(CONFIRM_DELETE_RECORD)
@handle_db_errors
def delete(table_name, table_data, where_clause):
    """
    Delete records from table.

    Args:
        table_name: Name of the table
        table_data: Table data
        where_clause: Dictionary like {'ID': 1}

    Returns:
        Updated table data or None if cancelled
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
                SUCCESS_RECORD_DELETED.format(
                    record_id=deleted_id, table_name=table_name
                )
            )
    else:
        print(INFO_NO_DELETIONS)

    return new_data


def display_table(table_data, columns):
    """
    Display table data using PrettyTable.

    Args:
        table_data: List of records
        columns: List of column definitions
    """
    if not table_data:
        print(INFO_NO_DATA)
        return

    table = PrettyTable()
    column_names = [col["name"] for col in columns]
    table.field_names = column_names

    for record in table_data:
        row = [record.get(col, "") for col in column_names]
        table.add_row(row)

    print(table)


@handle_db_errors
def show_table_info(metadata, table_name, table_data):
    """
    Show table information.

    Args:
        metadata: Metadata dictionary
        table_name: Name of the table
        table_data: Table data
    """
    if table_name not in metadata:
        raise KeyError(ERROR_TABLE_NOT_FOUND.format(table_name=table_name))

    columns = metadata[table_name]["columns"]
    columns_str = ", ".join([f"{col['name']}:{col['type']}" for col in columns])

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_str}")
    print(f"Количество записей: {len(table_data)}")

