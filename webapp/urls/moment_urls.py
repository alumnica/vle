from django.urls import path

from webapp.views.moment_views import MomentView

urlpatterns = [
    path('<int:pk>/', MomentView.as_view(), name='moment_view'),
]