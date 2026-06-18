#!/usr/bin/env bash
# Скрипт сборки для Render: ставит зависимости, собирает статику, применяет миграции.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
