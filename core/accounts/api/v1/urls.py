# from .views import RegisterViewSet, LoginViewSet, LogoutViewSet
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path

router = DefaultRouter()
router.register("auth", views.AuthViewSet, basename="auth")

urlpatterns = [
    path(
        "token/login/",
        views.CustomObtaionAuthToken.as_view(),
        name="token_login",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token_logout",
    ),
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
]
# router.register("register", RegisterViewSet, basename="register")
# router.register("login",LoginViewSet,basename="login")
# router.register("logout",LogoutViewSet,basename="logout")

urlpatterns += router.urls
