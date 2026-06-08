"""
Middleware: если у пользователя установлен флаг must_change_password,
все запросы перенаправляются на страницу смены пароля до тех пор,
пока он не сменит пароль.
"""
from django.shortcuts import redirect
from django.urls import reverse


class PasswordChangeMiddleware:
    """Принудительная смена временного пароля при первом входе."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.must_change_password:
            # Разрешённые пути: сама смена пароля, выход, админка, статика, медиа
            allowed = [
                reverse('password_change_required'),
                reverse('logout'),
            ]
            path = request.path
            is_allowed = (
                path in allowed
                or path.startswith('/admin/')
                or path.startswith('/static/')
                or path.startswith('/media/')
            )
            if not is_allowed:
                return redirect('password_change_required')

        return self.get_response(request)
