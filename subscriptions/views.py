"""
Представления абонементов: каталог, оформление покупки,
имитация онлайн-оплаты.
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import SubscriptionType, Subscription


def subscription_list(request):
    """Каталог доступных типов абонементов."""
    types = SubscriptionType.objects.prefetch_related('services').all()
    return render(request, 'subscriptions/subscription_list.html', {'types': types})


@login_required
def subscription_checkout(request, pk):
    """Оформление покупки абонемента.

    Доступно только клиентам. Показывает детали абонемента
    и форму имитации онлайн-оплаты.
    """
    stype = get_object_or_404(SubscriptionType, pk=pk)

    if not request.user.is_client:
        messages.error(request, 'Покупка абонементов доступна только клиентам.')
        return redirect('subscription_list')

    if request.method == 'POST':
        # Имитация онлайн-оплаты через банк.
        # В учебном проекте реальная платёжная система не подключается;
        # считаем, что оплата прошла успешно.
        subscription = Subscription.objects.create(
            client=request.user,
            subscription_type=stype,
            procedures_left=stype.procedures_count,
            payment_status=Subscription.PaymentStatus.PAID,
        )
        messages.success(
            request,
            f'Абонемент «{stype.name}» успешно оплачен! '
            f'Доступно процедур: {subscription.procedures_left}.'
        )
        return redirect('account')

    return render(request, 'subscriptions/checkout.html', {'stype': stype})
