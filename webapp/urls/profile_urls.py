from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.profile_views import *

urlpatterns = [
    path(_('first-login-info/'), FirstLoginInfoView.as_view(), name='first-login-info_view'),
    path(_('first-login-p1/'), FirstLoginP1View.as_view(), name='first-login-p1_view'),
    path(_('first-login-p21/'), FirstLoginP21View.as_view(), name='first-login-p21_view'),
    path(_('first-login-p22/<option>'), FirstLoginP22View.as_view(), name='first-login-p22_view'),
    path(_('first-login-p31/'), FirstLoginP31View.as_view(), name='first-login-p31_view'),
    path(_('first-login-p32/<option>'), FirstLoginP32View.as_view(), name='first-login-p32_view'),
]