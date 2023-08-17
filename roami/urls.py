from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from drf_yasg.views import get_schema_view
from rest_framework import permissions

# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Places Project",
#         default_version="v1",
#         description="description",
#         terms_of_service="https://your-terms-of-service.com/",
#     ),
#     public=True,
#     permission_classes=[
#         permissions.AllowAny,
#     ],
# )
urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # path(
    #     "api/v1/redoc/",
    #     schema_view.with_ui("redoc", cache_timeout=0),
    #     name="schema-redoc",
    # ),
    # path("accounts/", include("allauth.urls")),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/about/", include("about.urls")),
    path("api/v1/", include("places.urls")),
    # path(
    #     "api/v1/password_reset/",
    #     include("django_rest_passwordreset.urls", namespace="password_reset"),
    # ),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
