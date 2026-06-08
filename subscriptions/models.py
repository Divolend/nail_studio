"""
Модели абонементов.
Соответствует сущностям SUBSCRIPTION_TYPE, SUBSCRIPTION_TYPE_SERVICE
и SUBSCRIPTION из ER-диаграммы.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from catalog.models import Service


class SubscriptionType(models.Model):
    """Тип (шаблон) абонемента, который настраивает администратор.

    Например: «3 нюдовых маникюра», «5 любых маникюров».
    Связь «многие ко многим» с услугами реализована через
    промежуточную модель SubscriptionTypeService.
    """

    name = models.CharField('Название', max_length=150)
    procedures_count = models.PositiveIntegerField('Количество процедур')
    validity_days = models.PositiveIntegerField('Срок действия (дней)')
    discount_percent = models.PositiveIntegerField('Скидка, %', default=0)
    total_price = models.DecimalField('Итоговая цена, руб.', max_digits=10, decimal_places=2)
    services = models.ManyToManyField(
        Service,
        through='SubscriptionTypeService',
        related_name='subscription_types',
        verbose_name='Доступные услуги',
    )

    class Meta:
        verbose_name = 'Тип абонемента'
        verbose_name_plural = 'Типы абонементов'
        ordering = ['total_price']

    def __str__(self):
        return f'{self.name} ({self.procedures_count} проц.)'


class SubscriptionTypeService(models.Model):
    """Связующая таблица: какие услуги входят в тип абонемента.

    Реализует связь «многие ко многим» между SubscriptionType и Service.
    """

    subscription_type = models.ForeignKey(
        SubscriptionType,
        on_delete=models.CASCADE,
        verbose_name='Тип абонемента',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга',
    )

    class Meta:
        verbose_name = 'Услуга в абонементе'
        verbose_name_plural = 'Услуги в абонементах'
        unique_together = ('subscription_type', 'service')

    def __str__(self):
        return f'{self.subscription_type.name} — {self.service.name}'


class Subscription(models.Model):
    """Конкретный абонемент, купленный клиентом."""

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Ожидает оплаты'
        PAID = 'paid', 'Оплачен'
        EXPIRED = 'expired', 'Истёк'

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Клиент',
    )
    subscription_type = models.ForeignKey(
        SubscriptionType,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='Тип абонемента',
    )
    purchase_date = models.DateField('Дата покупки', auto_now_add=True)
    procedures_left = models.PositiveIntegerField('Осталось процедур')
    payment_status = models.CharField(
        'Статус оплаты',
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        ordering = ['-purchase_date']

    def __str__(self):
        return f'{self.subscription_type.name} — {self.client.full_name}'

    def save(self, *args, **kwargs):
        # При создании автоматически заполняем остаток процедур
        if not self.pk and not self.procedures_left:
            self.procedures_left = self.subscription_type.procedures_count
        super().save(*args, **kwargs)

    @property
    def expiry_date(self):
        """Дата окончания действия абонемента."""
        return self.purchase_date + timedelta(days=self.subscription_type.validity_days)

    @property
    def is_active(self):
        """Абонемент активен: оплачен, есть процедуры, не истёк."""
        return (
            self.payment_status == self.PaymentStatus.PAID
            and self.procedures_left > 0
            and self.expiry_date >= timezone.now().date()
        )
