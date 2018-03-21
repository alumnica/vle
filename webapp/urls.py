from django.urls import path
from django.utils.translation import gettext_lazy as _
from webapp.views.user_views import LoginView, SignUpView, LoggedInView, LogoutView

urlpatterns = [
    path(_('login/'), LoginView.as_view(), name='login_view'),
    path(_('signup/'), SignUpView.as_view(), name='signup_view'),
    path(_('loggedin/'), LoggedInView.as_view(), name= 'loggedin_view'),
    path(_('logout/'), LogoutView.as_view(), name='logout_view'),
]