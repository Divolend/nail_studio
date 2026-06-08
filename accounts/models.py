"""
Модели пользователей: кастомный User с ролями и профиль мастера.
Соответствует сущностям USER и MASTER_PROFILE из ER-диаграммы.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь системы с ролевой моделью.

    Расширяет стандартную модель Django, добавляя роль и телефон.
    Поле email используется как основной контакт.
    """

    class Role(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        MASTER = 'master', 'Мастер'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    email = models.EmailField('Эл. почта', unique=True)
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=False,  # разрешаем повторяющиеся имена
    )
    full_name = models.CharField('ФИО', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    must_change_password = models.BooleanField(
        'Требуется смена пароля',
        default=False,
        help_text='Если включено, пользователь будет обязан сменить пароль при следующем входе.',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.full_name or self.username} ({self.get_role_display()})'

    @property
    def display_name(self):
        """Отображаемое имя: ФИО, либо Имя+Фамилия, либо логин."""
        if self.full_name:
            return self.full_name
        combined = f'{self.first_name} {self.last_name}'.strip()
        if combined:
            return combined
        return self.username

    @property
    def is_master(self):
        return self.role == self.Role.MASTER

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT


class MasterProfile(models.Model):
    """Профиль мастера. Связь 1:1 с пользователем (роль = master)."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='master_profile',
        verbose_name='Пользователь',
    )
    specialization = models.CharField('Специализация', max_length=100, blank=True)
    experience_years = models.PositiveIntegerField('Опыт работы (лет)', default=0)
    biography = models.TextField('Биография', blank=True)
    avatar = models.ImageField('Фото профиля', upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль мастера'
        verbose_name_plural = 'Профили мастеров'

    def __str__(self):
        return f'Мастер: {self.user.full_name or self.user.username}'
