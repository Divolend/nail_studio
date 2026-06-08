"""
Модели каталога: услуги студии и фотографии портфолио мастеров.
Соответствует сущностям SERVICE и PORTFOLIO_PHOTO из ER-диаграммы.
"""
from django.db import models
from accounts.models import MasterProfile


class Service(models.Model):
    """Услуга студии маникюра."""

    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True)
    duration_minutes = models.PositiveIntegerField('Длительность (мин)')
    price = models.DecimalField('Цена, руб.', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} — {self.price} руб.'


class PortfolioPhoto(models.Model):
    """Фотография работы мастера в портфолио."""

    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name='portfolio_photos',
        verbose_name='Мастер',
    )
    image = models.ImageField('Изображение', upload_to='portfolio/')
    description = models.TextField('Описание', blank=True)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото портфолио'
        verbose_name_plural = 'Фото портфолио'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'Работа мастера {self.master} ({self.uploaded_at:%d.%m.%Y})'
