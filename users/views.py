import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import RegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            'Подтверждение почты',
            f'Перейдите по ссылке, чтобы подтвердить вашу почту: {url}',
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_users'


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse('users:login'))


def pass_recovery(request):
    context = {
        'success_message': 'Пароль сброшен. Новый пароль отправлен на вашу электронную почту'
    }
    if request.method == 'GET':
        return render(request, 'users/pass_recovery.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        password = User.objects.make_random_password(length=10)
        user.set_password(password)
        user.save()
        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {password}',
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        return render(request, 'users/pass_recovery.html', context)


@permission_required('users.block_users')
def block_user(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:users_list'))
