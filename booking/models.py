"""
Модели записи на процедуры.
Соответствует сущностям TIME_SLOT и APPOINTMENT из ER-диаграммы.
"""
from django.db import models

from accounts.models import User, MasterProfile
from catalog.models import Service
from subscriptions.models import Subscription


class TimeSlot(models.Model):
    """Временной слот в расписании мастера.

    Мастер выставляет слоты заранее. Клиент видит свободные слоты
    и записывается на них.
    """

    class Status(models.TextChoices):
        FREE = 'free', 'Свободен'
        BUSY = 'busy', 'Занят'

    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name='time_slots',
        verbose_name='Мастер',
    )
    date = models.DateField('Дата')
    start_time = models.TimeField('Время начала')
    duration_minutes = models.PositiveIntegerField('Длительность (мин)', default=60)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.FREE,
    )

    class Meta:
        verbose_name = 'Временной слот'
        verbose_name_plural = 'Временные слоты'
        ordering = ['date', 'start_time']
        unique_together = ('master', 'date', 'start_time')

    def __str__(self):
        return f'{self.master} — {self.date:%d.%m.%Y} {self.start_time:%H:%M}'


class Appointment(models.Model):
    """Запись клиента на процедуру."""

    class PaymentMethod(models.TextChoices):
        SINGLE = 'single', 'Разовая оплата'
        SUBSCRIPTION = 'subscription', 'По абонементу'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активна'
        COMPLETED = 'completed', 'Выполнена'
        CANCELLED = 'cancelled', 'Отменена'

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Клиент',
    )
    time_slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='appointment',
        verbose_name='Слот',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='Услуга',
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name='Абонемент',
    )
    reference_photo = models.ImageField(
        'Фото-референс',
        upload_to='references/',
        null=True,
        blank=True,
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.SINGLE,
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.client.full_name} — {self.service.name} ({self.time_slot.date:%d.%m.%Y})'
