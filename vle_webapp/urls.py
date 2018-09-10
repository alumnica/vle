"""vle_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers

from webapp import api_viewsets
from webapp.views import navigation_views
from webapp.views.user_views import IndexView, LandingPageView

router = routers.DefaultRouter()

urlpatterns = [
                  path('', include('pwa.urls')),
                  path('', LandingPageView.as_view(), name='index_view'),
                  path('learn/', IndexView.as_view(), name='index_view'),
                  path('users/', include('webapp.urls.users_urls')),
                  path('profile/', include('webapp.urls.profile_urls')),
                  path('ambit/', include('webapp.urls.ambit_urls')),
                  path('subjects/', include('webapp.urls.subject_urls')),
                  path('odas/', include('webapp.urls.oda_urls')),
                  path('moments/', include('webapp.urls.moment_urls')),
                  path('evaluations/', include('webapp.urls.evaluation_urls')),
                  path('admin/', admin.site.urls),
                  path('oauth/', include('social_django.urls', namespace='social')),
                  path('api/', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
                  path('search/', include('webapp.urls.navigation_urls')),
                  path('registration', include('django.contrib.auth.urls')),
                  path('api/microodas/<int:learner>,<int:uODA>,<str:duration>/', api_viewsets.MicroodaViewSet.as_view(),
                       name='microoda_view'),
                  path('api/evaluation/', api_viewsets.EvaluationViewSet.as_view(), name='evaluation_review_view'),
                  path('api/avatar/', api_viewsets.ChangeUserAvatar.as_view(), name='avatar_change_view'),
                  path('api/profile_info/', api_viewsets.SaveExtraProfileInfo.as_view(), name='profile_extr_info_view'),
                  url(r'^api/h5p_finished/(?P<user>\d+)/(?P<momento>\d+)/$', api_viewsets.H5PFinished.as_view(),
                      name='h5p_finished_view'),
                  url(r'^api/h5p_data/(?P<subContentId>\d+)/$', api_viewsets.H5PToXapi.as_view(), name='h5p_data_view'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = navigation_views.Error404
handler400 = navigation_views.Error404
handler500 = navigation_views.Error404
