"""
Бэкенд аутентификации по адресу электронной почты.
Позволяет пользователям входить, указывая email вместо логина.
Логин (username) сохраняется для совместимости с админкой Django.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """Аутентификация по email (без учёта регистра)."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username здесь содержит то, что ввели в поле входа (email)
        email = kwargs.get('email', username)
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # На случай нескольких аккаунтов с одним email — берём первый активный
            user = User.objects.filter(email__iexact=email).order_by('id').first()
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
