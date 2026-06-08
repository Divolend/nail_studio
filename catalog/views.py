"""
Представления каталога: главная, мастера, услуги,
управление портфолио мастера.
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import MasterProfile
from .models import Service, PortfolioPhoto
from .forms import PortfolioPhotoForm


def home(request):
    """Главная страница со списком мастеров."""
    masters = MasterProfile.objects.select_related('user').all()
    return render(request, 'catalog/home.html', {'masters': masters})


def master_detail(request, pk):
    """Страница мастера с портфолио."""
    master = get_object_or_404(MasterProfile.objects.select_related('user'), pk=pk)
    photos = master.portfolio_photos.all()
    return render(request, 'catalog/master_detail.html', {
        'master': master,
        'photos': photos,
    })


def service_list(request):
    """Список услуг студии."""
    services = Service.objects.all()
    return render(request, 'catalog/service_list.html', {'services': services})


@login_required
def portfolio_manage(request):
    """Управление портфолио: просмотр и загрузка фото (для мастера)."""
    if not request.user.is_master:
        messages.error(request, 'Доступно только мастерам.')
        return redirect('account')

    profile = request.user.master_profile

    if request.method == 'POST':
        form = PortfolioPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.master = profile
            photo.save()
            messages.success(request, 'Фотография добавлена в портфолио.')
            return redirect('portfolio_manage')
    else:
        form = PortfolioPhotoForm()

    photos = profile.portfolio_photos.all()
    return render(request, 'catalog/portfolio_manage.html', {
        'form': form,
        'photos': photos,
    })


@login_required
def portfolio_delete(request, pk):
    """Удаление фотографии из портфолио."""
    photo = get_object_or_404(PortfolioPhoto, pk=pk)
    if request.user.is_master and photo.master == request.user.master_profile:
        photo.delete()
        messages.success(request, 'Фотография удалена.')
    return redirect('portfolio_manage')
