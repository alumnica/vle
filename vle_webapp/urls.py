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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers

from webapp import api_viewsets
from webapp.views.user_views import IndexView, LandingPageView

router = routers.DefaultRouter()
router.register(r'evaluation', api_viewsets.EvaluationViewSet)


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', LandingPageView.as_view(), name='index_view'),
    path(_('learn/'), IndexView.as_view(), name='index_view'),
    path(_('users/'), include('webapp.urls.users_urls')),
    path(_('profile/'), include('webapp.urls.profile_urls')),
    path(_('ambit/'), include('webapp.urls.ambit_urls')),
    path(_('subjects/'), include('webapp.urls.subject_urls')),
    path(_('odas/'), include('webapp.urls.oda_urls')),
    path(_('moments/'), include('webapp.urls.moment_urls')),
    path(_('evaluations/'), include('webapp.urls.evaluation_urls')),
    path(_('admin/'), admin.site.urls),
    path(_('api/'), include(router.urls)),
    path(_('api-auth/'), include('rest_framework.urls', namespace='rest_framework')),
    path(_('jsi18n/'), JavaScriptCatalog.as_view(), name='javascript-catalog'),
)
