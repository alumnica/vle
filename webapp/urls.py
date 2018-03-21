from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.user_views import LoginView, SignUpView

urlpatterns = [
<<<<<<< HEAD
    path('login_view/', LoginView.as_view(), name="login_view"),
    path('signup_view/', SignUpView.as_view(), name="signup_view"),
    path('logout_view', LogoutView.as_view(), name="logout_view"),
=======
    path(_('login/'), LoginView.as_view(), name='login_view'),
    path(_('signup/'), SignUpView.as_view(), name='signup_view'),
>>>>>>> da9c0a46540845372681e37725917f818122afbf
]