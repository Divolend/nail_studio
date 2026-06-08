"""
Представления приложения accounts:
регистрация, личный кабинет, профиль мастера.
"""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ClientRegistrationForm, MasterProfileForm, EmailLoginForm


def login_view(request):
    """Вход пользователя по электронной почте."""
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import authenticate
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('account')
            messages.error(request, 'Неверная почта или пароль.')
    else:
        form = EmailLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    """Регистрация нового клиента."""
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите, используя свою электронную почту.')
            return redirect('login')
    else:
        form = ClientRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def account(request):
    """Личный кабинет. Содержимое зависит от роли пользователя."""
    user = request.user

    if user.is_master:
        profile = getattr(user, 'master_profile', None)
        return render(request, 'accounts/account_master.html', {
            'profile': profile,
        })
    else:
        appointments = user.appointments.select_related(
            'service', 'time_slot', 'time_slot__master__user'
        ).all()
        subscriptions = user.subscriptions.select_related('subscription_type').all()
        return render(request, 'accounts/account_client.html', {
            'appointments': appointments,
            'subscriptions': subscriptions,
        })


@login_required
def edit_master_profile(request):
    """Редактирование профиля мастера самим мастером."""
    if not request.user.is_master:
        messages.error(request, 'Доступно только мастерам.')
        return redirect('account')

    profile = request.user.master_profile

    if request.method == 'POST':
        form = MasterProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('account')
    else:
        form = MasterProfileForm(instance=profile)

    return render(request, 'accounts/edit_master_profile.html', {'form': form})


@login_required
def password_change_required(request):
    """Принудительная смена временного пароля при первом входе.

    Используется встроенная форма Django PasswordChangeForm.
    После успешной смены снимается флаг must_change_password.
    """
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.must_change_password = False
            user.save(update_fields=['must_change_password'])
            # Чтобы пользователя не разлогинило после смены пароля
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён. Добро пожаловать!')
            return redirect('account')
    else:
        form = PasswordChangeForm(request.user)

    # Bootstrap-классы
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'accounts/password_change_required.html', {'form': form})
