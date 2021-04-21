"""sportaj_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static
from rest_framework import routers

import sportaj_app.views

router = routers.DefaultRouter()

urlpatterns = [
                  path("", sportaj_app.views.HomeView.as_view(), name = "home"),
                  path("", include('pwa.urls')),
                  path("zemljevid/", sportaj_app.views.ZemljevidView.as_view(), name = "zemljevid"),
                  path("klub/<slug>", cache_page(60 * 15)(sportaj_app.views.KlubView.as_view()), name = "klub"),
                  path("admin/", admin.site.urls),
                  path('faicon/', include('faicon.urls')),
                  path('/v1', include(router.urls))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
