"""
Сигналы приложения accounts.
Автоматически создают профиль мастера, когда пользователю
назначается роль «Мастер».
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, MasterProfile


@receiver(post_save, sender=User)
def manage_master_profile(sender, instance, created, **kwargs):
    """Создаёт MasterProfile при назначении роли «Мастер».

    Если пользователь стал мастером, а профиля ещё нет — создаём.
    Профиль не удаляется при смене роли, чтобы не терять
    портфолио и историю.
    """
    if instance.role == User.Role.MASTER:
        MasterProfile.objects.get_or_create(user=instance)
