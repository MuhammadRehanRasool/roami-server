from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User
from accounts.permission import IsOwnerOrReadOnly
from places.models import Location, Rating
from places.serializers import (
    PlaceSerializer,
    UserPlaceSerializer,
    RatingSerializer,
    SearchPlaceSerializer,
)
from django.db.models import Exists, OuterRef
from accounts.constants import LIST_OF_CITIES
from accounts.models import User

# Create your views here.


@permission_classes([AllowAny])
class SearchPlaceListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = SearchPlaceSerializer

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        filtered_cities = [
            city for city in LIST_OF_CITIES if query.lower() in city["city"].lower()
        ]
        sorted_cities = sorted(
            filtered_cities, key=lambda x: x["population"], reverse=True
        )
        top_5_cities = sorted_cities[:5]

        return top_5_cities


# @permission_classes([AllowAny])
# class PlaceListView(ListAPIView):
#     pagination_class = LimitOffsetPagination
#     serializer_class = PlaceSerializer

#     def get_queryset(self):
#         id = self.request.GET.get("id", None)
#         user_id = self.request.GET.get("user_id", None)
#         if id is None:
#             return Location.objects.all()
#         return Location.objects.filter(pk=id)


class PlaceListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = PlaceSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_id"] = self.request.GET.get("user_id")
        return context

    def get_queryset(self):
        id = self.request.GET.get("id", None)
        queryset = Location.objects.all()

        if id is not None:
            queryset = queryset.filter(pk=id)

        return queryset


class UserPlaceListView(ListAPIView):
    serializer_class = PlaceSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.GET.get("user_id", None)
        return Location.objects.filter(user__id=user_id)


# current user followed list
class UserFollowedList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    queryset = Location.objects.all()
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Location.objects.filter(followed_list=self.request.user)


class PublicUserProfilePlacesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        username_slug = self.kwargs.get("username_slug")
        user = get_object_or_404(User, username_slug=username_slug)
        places = Location.objects.filter(user=user)
        return places


class PublicUserProfileFollowedList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        username_slug = self.kwargs.get("username_slug")
        user = get_object_or_404(User, username_slug=username_slug)
        places = user.place_followed.all()
        return places


# @permission_classes([IsAuthenticated])
class PlaceCreateView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = PlaceSerializer

    def post(self, request, format=None):
        error_result = {}
        # request.data["tags"] = json.loads(request.data["tags"])
        # print(request.data["tags"])
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_place = serializer.save(
                user=User.objects.get(pk=int(self.request.data["user"]))
            )
            new_place.save()
            output = "Published your pin successfully."
            content = {
                "status": True,
                "message": output,
                "result": serializer.data,
            }
            return Response(content, status=status.HTTP_200_OK)
        content = {
            "status": False,
            "message": serializer.errors,
            "result": error_result,
        }
        return Response(content, status=status.HTTP_200_OK)


class PlaceUpdateView(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsOwnerOrReadOnly]
    permission_classes = [AllowAny]
    lookup_field = "pk"
    parser_class = (FileUploadParser,)
    serializer_class = PlaceSerializer
    queryset = Location.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )  # set partial=True to
        # update a data partially
        if serializer.is_valid():
            serializer.save()
            content = {
                "status": True,
                "message": {"Successfully place updated"},
                "result": serializer.data,
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"status": False, "message": serializer.errors, "result": {}}
            return Response(content, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # delete_action(instance, instance.id)
            instance.delete()
            content = {"status": True, "message": {"Successfully place deleted"}}
            return Response(content, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            content = {"status": False, "message": {"something went wrong"}}
            return Response(content, status=status.HTTP_200_OK)


class PlaceFollowedView(views.APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, place_id, format=None):
        place = get_object_or_404(Location, id=place_id)
        user = get_object_or_404(User, id=int(request.data["user_id"]))

        if place.user.id == user.id:
            resp = {"error": "can not follow own place."}
            return Response(resp, status=status.HTTP_200_OK)

        else:
            if Location.objects.filter(id=place_id, followed_list=user):
                place.followed_list.remove(user)
                resp = {"status": "unfollowed place", "follow": False}
            else:
                place.followed_list.add(user)

                resp = {"status": "followed place", "follow": True}

            return Response(resp, status=status.HTTP_200_OK)


class PlaceSearchEngine(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["city", "tags__name", "country", "place_name"]
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_id"] = self.request.GET.get("user_id")
        return context

    def get_queryset(self):
        queryset = Location.objects.all()
        search_query = self.request.query_params.get("search")
        if search_query:
            queryset = (
                queryset.filter(city__icontains=search_query)
                | queryset.filter(tags__name__icontains=search_query)
                | queryset.filter(country__icontains=search_query)
                | queryset.filter(place_name__icontains=search_query)
            )
        return queryset


class RatingView(views.APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = RatingSerializer

    def post(self, request, place_id, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request": self.request})
        if serializer.is_valid():
            rating = serializer.data["rating"]
            comment_body = serializer.data["comment_body"]

            place = get_object_or_404(Location, id=place_id)
            user = get_object_or_404(User, id=data["user_id"])

            if place.user.id == user.id:
                resp = {"error": "can not rate own place."}
                return Response(resp, status=status.HTTP_200_OK)

            else:
                if Rating.objects.filter(id=place_id, user=user).count() > 0:
                    resp = {"status": "already reviewed", "reviewed": False}
                else:
                    Rating.objects.create(
                        user=user,
                        rating=rating,
                        place=place,
                        comment_body=comment_body,
                    )

                    resp = {"status": "review added", "reviewed": True}

            return Response(resp, status=status.HTTP_200_OK)

    def get(self, request, place_id, *args, **kwargs):
        ratings = Rating.objects.filter(place_id=place_id)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
