from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.user_views import LoginView, SignUpView

urlpatterns = [
    path(_('login/'), LoginView.as_view(), name='login_view'),
    path(_('signup/'), SignUpView.as_view(), name='signup_view'),
]