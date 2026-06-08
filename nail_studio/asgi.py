"""
ASGI-конфигурация для проекта «Студия маникюра».
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nail_studio.settings')
application = get_asgi_application()
