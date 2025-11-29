"""Utility functions for file operations."""

import json
import os

from src.primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """
    Load metadata from JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        Dictionary with metadata or empty dict if file not found
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """
    Save metadata to JSON file.

    Args:
        filepath: Path to JSON file
        data: Dictionary to save
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_table_data(table_name):
    """
    Load table data from JSON file.

    Args:
        table_name: Name of the table

    Returns:
        List of records or empty list if file not found
    """
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """
    Save table data to JSON file.

    Args:
        table_name: Name of the table
        data: List of records to save
    """
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

