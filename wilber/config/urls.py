"""wilber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views


from django.views.generic import TemplateView
from rest_framework import routers


from users.views import SignupView
from assets.views import *
from assets.api import *


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'asset', AssetViewSet)
router.register(r'user', UserViewSet)
router.register(r'profile', UserProfileViewSet)

react_view = TemplateView.as_view(template_name='index.html')


urlpatterns = []




urlpatterns = [
    url(r'api/', include(router.urls)),

    #path('api-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/signup', SignupView.as_view()),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include("massadmin.urls")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    #path('asset/', include('assets.urls', namespace='asset'),  ),
    path('user/', include('users.urls', namespace='user'),  ),
    #path('django/', AssetListView.as_view()),
    #path('', AssetListView.as_view()),
    path('', react_view),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


urlpatterns += [
    url(r'^(?:.*)/?$', react_view),
]
