from django.urls import path
from webapp.views.navigation_views import SearchView, RecentActivitiesView

urlpatterns = [
    path(u'search_odas/<str:text>/', SearchView.as_view(), name='search_view'),
    path('recent_activity/', RecentActivitiesView.as_view(), name='recent_activity_view'),
]
