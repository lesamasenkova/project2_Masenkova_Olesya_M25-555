"""Constants for database operations."""

# File paths
METADATA_FILE = "db_meta.json"
DATA_DIR = "data"

# Valid data types
VALID_TYPES = {"int", "str", "bool"}

# Decorator messages
CONFIRM_DELETE_TABLE = "удаление таблицы"
CONFIRM_DELETE_RECORD = "удаление записи"

# Default values
DEFAULT_ID_COLUMN = "ID"
DEFAULT_ID_TYPE = "int"

# Error messages
ERROR_TABLE_EXISTS = 'Таблица "{table_name}" уже существует.'
ERROR_TABLE_NOT_FOUND = 'Таблица "{table_name}" не существует.'
ERROR_COLUMN_NOT_FOUND = "Таблица или столбец {column} не найден."
ERROR_FILE_NOT_FOUND = (
    "Ошибка: Файл данных не найден. "
    "Возможно, база данных не инициализирована."
)
ERROR_VALIDATION = "Ошибка валидации: {error}"
ERROR_UNEXPECTED = "Произошла непредвиденная ошибка: {error}"
ERROR_INVALID_VALUE = (
    "Некорректное значение '{value}' для столбца "
    "'{column}' типа '{col_type}'."
)

# Success messages
SUCCESS_TABLE_CREATED = (
    'Таблица "{table_name}" успешно создана со столбцами: {columns_str}'
)
SUCCESS_TABLE_DELETED = 'Таблица "{table_name}" успешно удалена.'
SUCCESS_RECORD_INSERTED = (
    'Запись с ID={record_id} успешно добавлена в таблицу "{table_name}".'
)
SUCCESS_RECORD_UPDATED = (
    'Запись с ID={record_id} в таблице "{table_name}" успешно обновлена.'
)
SUCCESS_RECORD_DELETED = (
    'Запись с ID={record_id} успешно удалена из таблицы "{table_name}".'
)

# Information messages
INFO_NO_TABLES = "Таблицы отсутствуют."
INFO_NO_DATA = "Нет данных для отображения."
INFO_NO_RECORDS_FOUND = "Записи не найдены."
INFO_OPERATION_CANCELLED = "Операция отменена."
INFO_NO_UPDATES = "Записи для обновления не найдены."
INFO_NO_DELETIONS = "Записи для удаления не найдены."
INFO_INVALID_COMMAND = "Функции {command} нет. Попробуйте снова."
INFO_INVALID_VALUE = "Некорректное значение. Попробуйте снова."

# Timing
TIMING_FORMAT = "Функция {func_name} выполнилась за {elapsed_time:.3f} секунд."

# Prompt messages
PROMPT_COMMAND = ">>>Введите команду: "
PROMPT_CONFIRM = 'Вы уверены, что хотите выполнить "{action}"? [y/n]: '

