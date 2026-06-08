"""
Представления административного управления студией.
Доступны только пользователям с ролью «администратор».
"""
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required
from accounts.models import User, MasterProfile
from catalog.models import Service
from subscriptions.models import SubscriptionType

from .forms import ServiceForm, SubscriptionTypeForm, MasterCreateForm


@admin_required
def dashboard(request):
    """Главная страница панели управления со сводкой."""
    context = {
        'services_count': Service.objects.count(),
        'masters_count': MasterProfile.objects.count(),
        'subscription_types_count': SubscriptionType.objects.count(),
    }
    return render(request, 'management/dashboard.html', context)


# ---------- Услуги (CRUD) ----------

@admin_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'management/service_list.html', {'services': services})


@admin_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Услуга добавлена.')
            return redirect('mng_service_list')
    else:
        form = ServiceForm()
    return render(request, 'management/service_form.html',
                  {'form': form, 'title': 'Новая услуга'})


@admin_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Услуга обновлена.')
            return redirect('mng_service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'management/service_form.html',
                  {'form': form, 'title': 'Редактирование услуги'})


@admin_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Услуга удалена.')
        return redirect('mng_service_list')
    return render(request, 'management/confirm_delete.html',
                  {'object': service, 'title': 'Удаление услуги',
                   'back_url': 'mng_service_list'})


# ---------- Мастера ----------

@admin_required
def master_list(request):
    masters = MasterProfile.objects.select_related('user').all()
    return render(request, 'management/master_list.html', {'masters': masters})


@admin_required
def master_create(request):
    if request.method == 'POST':
        form = MasterCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Мастер {user.full_name} создан. Логин: {user.username}, '
                f'временный пароль передайте мастеру лично.'
            )
            return redirect('mng_master_list')
    else:
        form = MasterCreateForm()
    return render(request, 'management/master_form.html',
                  {'form': form, 'title': 'Новый мастер'})


@admin_required
def master_delete(request, pk):
    master = get_object_or_404(MasterProfile, pk=pk)
    if request.method == 'POST':
        user = master.user
        user.delete()  # удаление пользователя удалит и профиль (CASCADE)
        messages.success(request, 'Мастер удалён.')
        return redirect('mng_master_list')
    return render(request, 'management/confirm_delete.html',
                  {'object': master, 'title': 'Удаление мастера',
                   'back_url': 'mng_master_list'})


# ---------- Типы абонементов (CRUD) ----------

@admin_required
def subscription_type_list(request):
    types = SubscriptionType.objects.prefetch_related('services').all()
    return render(request, 'management/subscription_type_list.html', {'types': types})


@admin_required
def subscription_type_create(request):
    if request.method == 'POST':
        form = SubscriptionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип абонемента добавлен.')
            return redirect('mng_subscription_type_list')
    else:
        form = SubscriptionTypeForm()
    return render(request, 'management/subscription_type_form.html',
                  {'form': form, 'title': 'Новый тип абонемента'})


@admin_required
def subscription_type_edit(request, pk):
    stype = get_object_or_404(SubscriptionType, pk=pk)
    if request.method == 'POST':
        form = SubscriptionTypeForm(request.POST, instance=stype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип абонемента обновлён.')
            return redirect('mng_subscription_type_list')
    else:
        form = SubscriptionTypeForm(instance=stype)
    return render(request, 'management/subscription_type_form.html',
                  {'form': form, 'title': 'Редактирование типа абонемента'})


@admin_required
def subscription_type_delete(request, pk):
    stype = get_object_or_404(SubscriptionType, pk=pk)
    if request.method == 'POST':
        stype.delete()
        messages.success(request, 'Тип абонемента удалён.')
        return redirect('mng_subscription_type_list')
    return render(request, 'management/confirm_delete.html',
                  {'object': stype, 'title': 'Удаление типа абонемента',
                   'back_url': 'mng_subscription_type_list'})
