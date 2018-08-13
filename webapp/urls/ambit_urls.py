from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.ambit_views import *

urlpatterns = [
    path(_('ambit_grid/'), AmbitGridView.as_view(), name='ambitos-grid_view'),
]
