"""Utility functions for file operations."""

import json


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

