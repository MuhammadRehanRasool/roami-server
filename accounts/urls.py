from django.urls import path
from . import views
from .views import ProfileUpdateAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("api/auth/google/", views.GoogleAuthView.as_view(), name="google_auth"),
    path("account/create/", views.RegisterView.as_view()),
    path("account/login/", views.LoginView.as_view(), name="login"),
    path(
        "account/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("account/logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "account/profile/update/<int:user_id>/",
        ProfileUpdateAPIView.as_view(),
        name="profile",
    ),
    path(
        "account/check-email-exists/",
        views.CheckEmailExistsView.as_view(),
        name="check-email-exists",
    ),
    path(
        "account/profile/<str:username_slug>/",
        views.PublicUserProfile.as_view(),
        name="get-profile",
    ),
    path(
        "account/import/list/",
        views.ImportList.as_view(),
        name="add-import-list-count",
    ),
    path(
        "account/auth/google/login/",
        views.GoogleAuthLogin.as_view(),
        name="google-login",
    ),
    path("interests/", views.InterestListView.as_view(), name="interests"),
]
