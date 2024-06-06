"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from user.views import UserViewSet
from friend_request.views import FriendRequestViewSet


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"friend-request", FriendRequestViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include("dj_rest_auth.urls")),
    path("api/registration/", include("dj_rest_auth.registration.urls")),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # auth via drf api
    path("api-auth/", include("rest_framework.urls")),
    # docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # admin
    path("admin/", admin.site.urls),
]
