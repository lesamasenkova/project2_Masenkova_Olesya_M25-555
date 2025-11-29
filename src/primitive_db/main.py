#!/usr/bin/env python3
"""Main entry point for the primitive database application."""

from src.primitive_db.engine import welcome


def main():
    """Run the main application."""
    print("DB project is running!")
    welcome()


if __name__ == "__main__":
    main()

