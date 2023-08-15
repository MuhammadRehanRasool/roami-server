from django.urls import path
from . import views

urlpatterns = [
    path("add/place/", views.PlaceCreateView.as_view(), name="add_place"),
    path("search_places/", views.SearchPlaceListView.as_view(), name="search_places"),
    path("places/", views.PlaceListView.as_view(), name="places"),
    path(
        "user/pla          ces/", views.UserPlaceListView.as_view(), name="user_places"
    ),
    path(
        "user/followed/list/",
        views.UserFollowedList.as_view(),
        name="user_followed_list",
    ),
    path(
        "place/<int:pk>/update/", views.PlaceUpdateView.as_view(), name="place_update"
    ),
    path(
        "place/followed/<int:place_id>/",
        views.PlaceFollowedView.as_view(),
        name="place-followed",
    ),
    path(
        "public/<str:username_slug>/followed/places/",
        views.PublicUserProfileFollowedList.as_view(),
        name="public-user-followed-list",
    ),
    path(
        "public/<str:username_slug>/places/",
        views.PublicUserProfilePlacesView.as_view(),
        name="public-user-followed-list",
    ),
    path(
        "place/search/", views.PlaceSearchEngine.as_view(), name="place-search-engine"
    ),
    path("place/rating/<int:place_id>/", views.RatingView.as_view(), name="rating"),
]
