#!/usr/bin/env python
"""Утилита командной строки Django для проекта «Студия маникюра»."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nail_studio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Не удалось импортировать Django. Убедитесь, что он установлен '
            'и доступен в переменной PYTHONPATH, а также что активировано '
            'виртуальное окружение.'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
