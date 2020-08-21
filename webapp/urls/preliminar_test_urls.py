from django.urls import path

from webapp.views.preliminar_test_views import SignUpTestView, SignUpTestConfirmation, \
    SignupTestConfirmationError, FirstLoginTestInfoView, FirstLoginTestP1View, TestAnswered

urlpatterns = [
    path('signup/', SignUpTestView.as_view(), name='signup_test_view'),
    path('confirm_signup/<str:uidb64>,<str:token>/', SignUpTestConfirmation.as_view(),
         name='signup_test_confirmation_view'),
    path('confirmation_error/<int:pk>/', SignupTestConfirmationError.as_view(), name='confirmation_test_error_view'),
    path('first_login_info/<int:pk>/', FirstLoginTestInfoView.as_view(), name='first_login_test_info_view'),
    path('first_login_p1/<int:pk>/', FirstLoginTestP1View.as_view(), name='first_login_test_p1_view'),
    path('test_answered/<int:pk>/', TestAnswered.as_view(), name='test_answered_view')
]
