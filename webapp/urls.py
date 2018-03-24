from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.profile_views import *
from webapp.views.user_views import *

urlpatterns = [
    path(_('login/'), LoginView.as_view(), name='login_view'),
    path(_('signup/'), SignUpView.as_view(), name='signup_view'),
    path(_('dashboard/'), DashboardView.as_view(), name='dashboard_view'),
    path(_('logout/'), LogoutView.as_view(), name='logout_view'),
    path(_('first-login-info/'), FirstLoginInfoView.as_view(), name='first-login-info_view'),
    path(_('first-login-p1/'), FirstLoginP1View.as_view(), name='first-login-p1_view'),
    path(_('first-login-p21/'), FirstLoginP1View.as_view(), name='first-login-p21_view'),
    path(_('first-login-p22/'), FirstLoginP21View.as_view(), name='first-login-p22_view'),
    path(_('test/'), test_view, name='test_view'),
]