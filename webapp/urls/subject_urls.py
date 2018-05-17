from django.urls import path
from django.utils.translation import gettext_lazy as _

from webapp.views.subject_views import SubjectView

urlpatterns = [
    path('subject/<int:pk>/', SubjectView.as_view(), name='subject_view'),
]