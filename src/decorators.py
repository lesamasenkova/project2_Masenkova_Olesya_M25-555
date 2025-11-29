"""Decorators for database operations."""

import time

import prompt


def handle_db_errors(func):
    """
    Decorator to handle database errors.

    Catches and handles common database-related exceptions.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name):
    """
    Decorator factory for confirming dangerous operations.

    Args:
        action_name: Name of the action to confirm

    Returns:
        Decorator function
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            confirmation = prompt.string(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()

            if confirmation == "y":
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                return None

        return wrapper

    return decorator


def log_time(func):
    """
    Decorator to measure and log function execution time.

    Uses time.monotonic() for accurate measurement.
    """

    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()

        elapsed_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed_time:.3f} секунд.")

        return result

    return wrapper


def create_cacher():
    """
    Create a caching function using closures.

    Returns:
        cache_result function that caches function results
    """
    cache = {}

    def cache_result(key, value_func):
        """
        Cache result or retrieve from cache.

        Args:
            key: Cache key
            value_func: Function to call if key not in cache

        Returns:
            Cached or newly computed value
        """
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result
        return result

    return cache_result

