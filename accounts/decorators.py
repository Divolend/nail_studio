"""
Вспомогательные декораторы для проверки ролей.
"""
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """Допускает к представлению только администраторов студии.

    Администратором считается пользователь с ролью 'admin'
    либо суперпользователь Django.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        is_admin = request.user.is_superuser or request.user.role == 'admin'
        if not is_admin:
            messages.error(request, 'Доступ только для администратора.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
