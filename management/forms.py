"""
Формы административного управления (для роли «администратор»):
услуги, типы абонементов, создание мастеров.
"""
from django import forms

from catalog.models import Service
from subscriptions.models import SubscriptionType
from accounts.models import User


class ServiceForm(forms.ModelForm):
    """Форма создания/редактирования услуги."""

    class Meta:
        model = Service
        fields = ('name', 'description', 'duration_minutes', 'price')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SubscriptionTypeForm(forms.ModelForm):
    """Форма создания/редактирования типа абонемента.

    Поле services позволяет выбрать, на какие услуги распространяется
    абонемент (связь многие-ко-многим).
    """

    class Meta:
        model = SubscriptionType
        fields = ('name', 'procedures_count', 'validity_days',
                  'discount_percent', 'total_price', 'services')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'procedures_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'validity_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'services': forms.CheckboxSelectMultiple(),
        }


class MasterCreateForm(forms.ModelForm):
    """Форма создания мастера администратором.

    Администратор задаёт логин, ФИО и временный пароль.
    Роль автоматически — «Мастер», флаг смены пароля включён.
    """
    temp_password = forms.CharField(
        label='Временный пароль',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Передайте этот пароль мастеру. При первом входе он его сменит.',
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.MASTER
        user.must_change_password = True
        user.set_password(self.cleaned_data['temp_password'])
        if commit:
            user.save()  # сигнал создаст MasterProfile автоматически
        return user
