from django.urls import path
from .views import SectionsListView, TeamListView, PopularListView

urlpatterns = [
    path("sections/", SectionsListView.as_view(), name="sections-list"),
    path("team/", TeamListView.as_view(), name="team-list"),
    path("popular/", PopularListView.as_view(), name="popular-list"),
]
