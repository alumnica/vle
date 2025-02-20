from django.urls import path

from webapp.views.user_views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('signup/', SignUpView.as_view(), name='signup_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('confirm_signup/<str:uidb64>, <str:token>', SignUpConfirmation.as_view(), name='signup_confirmation_view'),
    path('confirmation_error/<int:pk>/', SignupConfirmationError.as_view(), name='confirmation_error_view')
]
