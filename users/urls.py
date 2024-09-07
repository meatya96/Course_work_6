from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_confirm, pass_recovery, UserListView, block_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email_confirm/<str:token>/', email_confirm, name='email_confirm'),
    path('pass_recovery/', pass_recovery, name='pass_recovery'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('block_user/<int:pk>/', block_user, name='block_user'),
]
