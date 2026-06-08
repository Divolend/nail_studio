"""
Формы приложения accounts: регистрация клиента,
редактирование профиля мастера.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, MasterProfile


class EmailLoginForm(forms.Form):
    """Форма входа по электронной почте."""
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class ClientRegistrationForm(UserCreationForm):
    """Форма регистрации клиента.

    Роль автоматически устанавливается «Клиент».
    """
    full_name = forms.CharField(label='ФИО', max_length=100)
    email = forms.EmailField(label='Эл. почта')
    phone = forms.CharField(label='Телефон', max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем проверку уникальности имени пользователя
        self.fields['username'].validators = []
        self.fields['username'].help_text = 'Не более 150 символов.'
        # Добавляем Bootstrap-класс ко всем полям
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        user.full_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class MasterProfileForm(forms.ModelForm):
    """Форма редактирования профиля мастера (заполняет сам мастер)."""

    class Meta:
        model = MasterProfile
        fields = ('avatar', 'specialization', 'experience_years', 'biography')
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
