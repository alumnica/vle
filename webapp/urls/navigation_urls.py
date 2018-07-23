from django.urls import path
from webapp.views.navigation_views import SearchView

urlpatterns = [
    path('search_odas/<slug:text>/', SearchView.as_view(), name='search_view'),
]