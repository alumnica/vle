from django.urls import path

from webapp.views.moment_views import MomentView, H5PackageView

urlpatterns = [
    path('<int:pk>/', MomentView.as_view(), name='moment_view'),
    path('package_view/<str:job_id>/', H5PackageView.as_view(), name='package_view'),
]
