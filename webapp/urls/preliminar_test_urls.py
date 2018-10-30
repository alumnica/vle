from django.urls import path

from webapp.views.preliminar_test_views import LoginTestView, SignUpTestView, SignUpTestConfirmation, \
    SignupTestConfirmationError, FirstLoginTestInfoView, FirstLoginTestP1View

urlpatterns = [
    path('login_test/', LoginTestView.as_view(), name='login_test_view'),
    path('signup_test/', SignUpTestView.as_view(), name='signup_test_view'),
    path('confirm_signup_test/<str:uidb64>, <str:token>', SignUpTestConfirmation.as_view(), name='signup_test_confirmation_view'),
    path('confirmation_error_test/<int:pk>/', SignupTestConfirmationError.as_view(), name='confirmation_test_error_view'),
    path('first_login_test_info/', FirstLoginTestInfoView.as_view(), name='first_login_test_info_view'),
    path('first_login_test_p1/', FirstLoginTestP1View.as_view(), name='first_login_test_p1_view')
]