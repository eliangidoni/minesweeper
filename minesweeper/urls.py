"""minesweeper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
import api.views
from rest_framework import viewsets
from rest_framework.response import Response
admin.site.site_header = 'Minesweeper Admin'


class SettingsViewSet(viewsets.GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response(settings.EXPORTED_SETTINGS)


router = routers.DefaultRouter()
router.register(r'settings', SettingsViewSet, base_name='settings')
router.register(r'games', api.views.GameViewSet, base_name='api_games')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/v1/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
