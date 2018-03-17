from django.urls import path

from webapp.views.user_views import *

urlpatterns = [
    path('login_view', LoginView.as_view(), name="login_view"),
    path('signup_view', SignUpView.as_view(), name="signup_view"),
]