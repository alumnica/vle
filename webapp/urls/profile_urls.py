from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.profile_views import *

urlpatterns = [
    path(_('first-login-info/'), FirstLoginInfoView.as_view(), name='first-login-info_view'),
    path(_('first-login-p1/'), FirstLoginP1View.as_view(), name='first-login-p1_view'),
    path(_('first-login-p2/'), FirstLoginP2View.as_view(), name='first-login-p2_view'),
    path(_('first-login-p3/'), FirstLoginP3View.as_view(), name='first-login-p3_view'),
]