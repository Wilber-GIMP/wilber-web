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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from rest_framework_jwt.views import obtain_jwt_token

from apps.assets.api import AssetViewSet
from apps.assets.api import UserProfileViewSet
from apps.assets.api import UserViewSet
from apps.assets.views import AssetListView
from apps.core.views import ReportIssue
from apps.users.views import SignupView


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"asset", AssetViewSet)
router.register(r"user", UserViewSet)
router.register(r"profile", UserProfileViewSet)

react_view = TemplateView.as_view(template_name="index.html")


urlpatterns = []


def trigger_error(request):
    division_by_zero = 1 / 0
    print(division_by_zero)


urlpatterns = [
    url(r"api/", include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
    path("sentry-debug/", trigger_error),
    path("token-auth/", obtain_jwt_token),
    url(r"^api-token-auth/", authtoken_views.obtain_auth_token),
    url(r"^rest-auth/", include("rest_auth.urls")),
    url(r"^rest-auth/registration/", include("rest_auth.registration.urls")),
    url(r"^accounts/signup", SignupView.as_view()),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^admin/", include("massadmin.urls")),
    path(
        "social-login/",
        TemplateView.as_view(template_name="pages/social-login.html"),
        name="social-login",
    ),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("asset/", include("assets.urls", namespace="asset")),
    path("user/", include("users.urls", namespace="user")),
    path("django/", AssetListView.as_view()),
    path("react/", react_view),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "privacy/",
        TemplateView.as_view(template_name="pages/privacy.html"),
        name="privacy",
    ),
    path(
        "terms/",
        TemplateView.as_view(template_name="pages/terms.html"),
        name="terms",
    ),
    path(
        "download/",
        TemplateView.as_view(template_name="pages/download.html"),
        name="download",
    ),
    path("report/", ReportIssue.as_view(), name="report"),
    path(
        "", TemplateView.as_view(template_name="pages/home.html"), name="home"
    ),
    # path('', AssetListView.as_view(), name='assets'),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns


# urlpatterns += [
#    url(r'^(?:.*)/?$', react_view),
# ]
