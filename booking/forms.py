"""
Формы записи: выставление слота мастером, запись клиента на процедуру.
"""
from django import forms

from .models import TimeSlot, Appointment
from catalog.models import Service


class TimeSlotForm(forms.ModelForm):
    """Форма добавления рабочего слота мастером."""

    class Meta:
        model = TimeSlot
        fields = ('date', 'start_time', 'duration_minutes')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AppointmentForm(forms.Form):
    """Форма записи клиента на процедуру.

    Клиент выбирает услугу, свободный слот, способ оплаты
    и при желании прикрепляет фото-референс.
    """
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label='Услуга',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        label='Свободное время',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    reference_photo = forms.ImageField(
        label='Фото-референс желаемого дизайна (необязательно)',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )
    payment_choice = forms.ChoiceField(
        label='Способ оплаты',
        widget=forms.RadioSelect,
        choices=[],
    )

    def __init__(self, *args, master=None, client=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Только свободные слоты выбранного мастера
        if master is not None:
            self.fields['time_slot'].queryset = TimeSlot.objects.filter(
                master=master, status=TimeSlot.Status.FREE
            )
        # Формируем варианты оплаты: разово + активные абонементы клиента
        choices = [('single', 'Разовая оплата на месте')]
        if client is not None:
            for sub in client.subscriptions.all():
                if sub.is_active:
                    choices.append((
                        f'sub_{sub.pk}',
                        f'Списать с абонемента «{sub.subscription_type.name}» '
                        f'(осталось {sub.procedures_left})'
                    ))
        self.fields['payment_choice'].choices = choices
