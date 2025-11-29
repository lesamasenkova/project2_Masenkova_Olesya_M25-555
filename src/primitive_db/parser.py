"""Parser for SQL-like commands."""


def parse_where_clause(where_str):
    """
    Parse WHERE clause into dictionary.

    Args:
        where_str: String like "age = 28" or "name = \"Sergei\""

    Returns:
        Dictionary like {'age': 28} or {'name': 'Sergei'}
    """
    if not where_str:
        return None

    parts = where_str.split("=", 1)
    if len(parts) != 2:
        return None

    column = parts[0].strip()
    value_str = parts[1].strip()

    # Remove quotes if present
    if (value_str.startswith('"') and value_str.endswith('"')) or (
        value_str.startswith("'") and value_str.endswith("'")
    ):
        value = value_str[1:-1]
    elif value_str.lower() == "true":
        value = True
    elif value_str.lower() == "false":
        value = False
    else:
        # Try to convert to int
        try:
            value = int(value_str)
        except ValueError:
            value = value_str

    return {column: value}


def parse_set_clause(set_str):
    """
    Parse SET clause into dictionary.

    Args:
        set_str: String like "age = 29" or "name = \"Ivan\""

    Returns:
        Dictionary like {'age': 29} or {'name': 'Ivan'}
    """
    return parse_where_clause(set_str)


def parse_values(values_str):
    """
    Parse VALUES clause into list.

    Args:
        values_str: String like "(\"Sergei\", 28, true)"

    Returns:
        List like ['Sergei', 28, True]
    """
    # Remove parentheses
    values_str = values_str.strip()
    if values_str.startswith("(") and values_str.endswith(")"):
        values_str = values_str[1:-1]

    # Split by comma
    parts = []
    current = ""
    in_quotes = False
    quote_char = None

    for char in values_str:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
        elif char == "," and not in_quotes:
            parts.append(current.strip())
            current = ""
            continue

        current += char

    if current:
        parts.append(current.strip())

    # Convert values
    result = []
    for part in parts:
        part = part.strip()

        # Remove quotes
        if (part.startswith('"') and part.endswith('"')) or (
            part.startswith("'") and part.endswith("'")
        ):
            result.append(part[1:-1])
        elif part.lower() == "true":
            result.append(True)
        elif part.lower() == "false":
            result.append(False)
        else:
            # Try to convert to int
            try:
                result.append(int(part))
            except ValueError:
                result.append(part)

    return result

