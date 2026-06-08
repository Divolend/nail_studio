"""Формы каталога: загрузка фото в портфолио."""
from django import forms

from .models import PortfolioPhoto


class PortfolioPhotoForm(forms.ModelForm):
    """Форма загрузки фотографии работы мастера."""

    class Meta:
        model = PortfolioPhoto
        fields = ('image', 'description')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Описание работы (необязательно)'}),
        }
