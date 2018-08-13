from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.user_views import *

urlpatterns = [
    path(_('login/'), LoginView.as_view(), name='login_view'),
    path(_('signup/'), SignUpView.as_view(), name='signup_view'),
    path(_('dashboard/'), DashboardView.as_view(), name='dashboard_view'),
    path(_('logout/'), LogoutView.as_view(), name='logout_view'),
]
