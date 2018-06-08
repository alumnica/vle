from django.urls import path

from webapp.views.odas_views import ODAView

urlpatterns = [
    path('<int:pk>/', ODAView.as_view(), name='oda_view'),
]