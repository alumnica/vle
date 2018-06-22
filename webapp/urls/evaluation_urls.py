from django.urls import path

from webapp.views.evaluation_views import EvaluationView

urlpatterns = [
    path('<int:pk>/', EvaluationView.as_view(), name='evaluation_view'),
]