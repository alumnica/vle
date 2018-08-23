from django.urls import path

from webapp.views.ambit_views import *

urlpatterns = [
    path('ambit_grid/', AmbitGridView.as_view(), name='ambitos-grid_view'),
]
