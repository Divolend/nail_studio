"""
Представления записи на процедуры.
Клиент: выбор мастера, услуги, слота, запись.
Мастер: управление слотами, просмотр записей, отметка выполнения.
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import MasterProfile
from subscriptions.models import Subscription
from .models import TimeSlot, Appointment
from .forms import TimeSlotForm, AppointmentForm


# ===================== СТОРОНА КЛИЕНТА =====================

@login_required
def book_appointment(request, master_pk):
    """Запись клиента на процедуру к выбранному мастеру."""
    master = get_object_or_404(MasterProfile.objects.select_related('user'), pk=master_pk)

    if not request.user.is_client:
        messages.error(request, 'Записываться могут только клиенты.')
        return redirect('master_detail', pk=master_pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES,
                               master=master, client=request.user)
        if form.is_valid():
            slot = form.cleaned_data['time_slot']
            service = form.cleaned_data['service']
            payment_choice = form.cleaned_data['payment_choice']
            reference_photo = form.cleaned_data['reference_photo']

            # Определяем способ оплаты
            subscription = None
            if payment_choice == 'single':
                payment_method = Appointment.PaymentMethod.SINGLE
            else:
                # payment_choice вида 'sub_<id>'
                sub_id = int(payment_choice.split('_')[1])
                subscription = get_object_or_404(
                    Subscription, pk=sub_id, client=request.user
                )
                payment_method = Appointment.PaymentMethod.SUBSCRIPTION

            # Создаём запись
            Appointment.objects.create(
                client=request.user,
                time_slot=slot,
                service=service,
                subscription=subscription,
                reference_photo=reference_photo,
                payment_method=payment_method,
            )
            # Слот занят
            slot.status = TimeSlot.Status.BUSY
            slot.save(update_fields=['status'])

            messages.success(request, 'Вы успешно записались на процедуру!')
            return redirect('account')
    else:
        form = AppointmentForm(master=master, client=request.user)

    # Группируем свободные слоты по датам для удобного выбора
    free_slots = master.time_slots.filter(status=TimeSlot.Status.FREE).order_by('date', 'start_time')
    slots_by_date = []
    current = None
    months = ['января','февраля','марта','апреля','мая','июня','июля',
              'августа','сентября','октября','ноября','декабря']
    weekdays = ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']
    for slot in free_slots:
        if current is None or current['date'] != slot.date:
            label = f'{slot.date.day} {months[slot.date.month-1]}, {weekdays[slot.date.weekday()]}'
            current = {'date': slot.date, 'label': label, 'slots': []}
            slots_by_date.append(current)
        current['slots'].append(slot)

    return render(request, 'booking/book_appointment.html', {
        'master': master,
        'form': form,
        'slots_by_date': slots_by_date,
    })


@login_required
def cancel_appointment(request, pk):
    """Отмена записи клиентом."""
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    if request.method == 'POST':
        # Освобождаем слот
        slot = appointment.time_slot
        slot.status = TimeSlot.Status.FREE
        slot.save(update_fields=['status'])
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=['status'])
        messages.success(request, 'Запись отменена.')
    return redirect('account')


# ===================== СТОРОНА МАСТЕРА =====================

@login_required
def master_schedule(request):
    """Расписание мастера: недельная сетка слотов и добавление новых."""
    if not request.user.is_master:
        messages.error(request, 'Доступно только мастерам.')
        return redirect('account')

    profile = request.user.master_profile

    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.master = profile
            slot.save()
            messages.success(request, 'Слот добавлен в расписание.')
            return redirect('master_schedule')
    else:
        form = TimeSlotForm()

    # Определяем текущую неделю (понедельник — воскресенье)
    from datetime import timedelta
    import datetime as _dt
    today = timezone.now().date()
    week_param = request.GET.get('week')
    if week_param:
        try:
            base = _dt.date.fromisoformat(week_param)
        except ValueError:
            base = today
    else:
        base = today
    monday = base - timedelta(days=base.weekday())

    weekday_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    week_days = []
    for i in range(7):
        d = monday + timedelta(days=i)
        day_slots = profile.time_slots.filter(date=d).order_by('start_time')
        week_days.append({
            'name': weekday_names[i],
            'date': d,
            'slots': day_slots,
        })

    prev_week = (monday - timedelta(days=7)).isoformat()
    next_week = (monday + timedelta(days=7)).isoformat()
    week_end = monday + timedelta(days=6)

    return render(request, 'booking/master_schedule.html', {
        'form': form,
        'week_days': week_days,
        'week_start': monday,
        'week_end': week_end,
        'prev_week': prev_week,
        'next_week': next_week,
    })


@login_required
def slot_delete(request, pk):
    """Удаление свободного слота мастером."""
    slot = get_object_or_404(TimeSlot, pk=pk)
    if request.user.is_master and slot.master == request.user.master_profile:
        if slot.status == TimeSlot.Status.FREE:
            slot.delete()
            messages.success(request, 'Слот удалён.')
        else:
            messages.error(request, 'Нельзя удалить занятый слот.')
    return redirect('master_schedule')


@login_required
def master_appointments(request):
    """Записи клиентов к мастеру."""
    if not request.user.is_master:
        messages.error(request, 'Доступно только мастерам.')
        return redirect('account')

    profile = request.user.master_profile
    appointments = Appointment.objects.select_related(
        'client', 'service', 'time_slot', 'subscription'
    ).filter(time_slot__master=profile).order_by('-time_slot__date')

    return render(request, 'booking/master_appointments.html', {
        'appointments': appointments,
    })


@login_required
def complete_appointment(request, pk):
    """Отметка о выполнении процедуры мастером.

    При выполнении, если оплата по абонементу, списывается
    одна процедура с абонемента клиента.
    """
    appointment = get_object_or_404(Appointment, pk=pk)

    if not request.user.is_master or appointment.time_slot.master != request.user.master_profile:
        messages.error(request, 'Недостаточно прав.')
        return redirect('account')

    if request.method == 'POST':
        if appointment.status == Appointment.Status.ACTIVE:
            appointment.status = Appointment.Status.COMPLETED
            appointment.save(update_fields=['status'])

            # Списываем процедуру с абонемента, если оплата по нему
            if (appointment.payment_method == Appointment.PaymentMethod.SUBSCRIPTION
                    and appointment.subscription):
                sub = appointment.subscription
                if sub.procedures_left > 0:
                    sub.procedures_left -= 1
                    sub.save(update_fields=['procedures_left'])

            messages.success(request, 'Процедура отмечена как выполненная.')
    return redirect('master_appointments')
