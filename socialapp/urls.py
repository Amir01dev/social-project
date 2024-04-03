from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "social"

urlpatterns = [
    path("", views.profile, name="profile"),
    # path('login', views.user_login, name="login"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('logout', views.log_out, name="logout"),
    path('register', views.register, name="register"),
    path('user/edit', views.edit_user, name="edit_account"),
    path('ticket', views.ticket, name="ticket"),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password-change_done"),
    # url to reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/password_reset/complete/'), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('posts/', views.post_list, name="post_list")
]
