from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from accounts.models import User
from accounts.serializers import GetFullUserSerializer
from .models import Location, Rating
from django.db.models import Avg

# class PlaceSerializer(TaggitSerializer, serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)
#     place_name_slug = serializers.SerializerMethodField()
#     tags = TagListSerializerField()
#     user = GetFullUserSerializer(
#         read_only=True, default=serializers.CurrentUserDefault()
#     )

#     class Meta:
#         model = Location
#         fields = [
#             "id",
#             "user",
#             "location_link",
#             "place_name",
#             "place_name_slug",
#             "description",
#             "country",
#             "city",
#             "tags",
#             "photo_1",
#             "photo_2",
#             "photo_3",
#             "photo_4",
#             "photo_5",
#         ]

#     def get_place_name_slug(self, obj):
#         return obj.place_name_slug

# def update(self, instance, validated_data):
#     photo_fields = ["photo_1", "photo_2", "photo_3", "photo_4", "photo_5"]

#     # Handle photo fields
#     for field in photo_fields:
#         if field in validated_data:
#             value = validated_data.pop(field)
#             print(value)
#             setattr(instance, field, value)

#     # Continue with the default update behavior
#     return super().update(instance, validated_data)


class PlaceSerializer(TaggitSerializer, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    place_name_slug = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    user = GetFullUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    isFollowed = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    averageRatings = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "id",
            "user",
            "location_link",
            "place_name",
            "place_name_slug",
            "description",
            "country",
            "city",
            "tags",
            "photo_1",
            "photo_2",
            "photo_3",
            "photo_4",
            "photo_5",
            "isFollowed",
            "reviews",
            "averageRatings",
        ]

    def get_place_name_slug(self, obj):
        return obj.place_name_slug

    def update(self, instance, validated_data):
        photo_fields = ["photo_1", "photo_2", "photo_3", "photo_4", "photo_5"]

        # Handle photo fields
        for field in photo_fields:
            if field in validated_data:
                value = validated_data.pop(field)
                print(value)
                setattr(instance, field, value)

        # Continue with the default update behavior
        return super().update(instance, validated_data)

    def get_isFollowed(self, obj):
        user_id = self.context.get("user_id")
        if user_id:
            return obj.followed_list.filter(id=user_id).exists()
        return False

    def get_reviews(self, obj):
        return RatingSerializer(obj.user_place_rating.all(), many=True).data

    def get_averageRatings(self, obj):
        return obj.user_place_rating.aggregate(Avg("rating"))["rating__avg"] or 0.0


class SearchPlaceSerializer(serializers.Serializer):
    city = serializers.CharField()
    country = serializers.CharField()
    population = serializers.IntegerField()


class UserPlaceSerializer(TaggitSerializer, serializers.ModelSerializer):
    place_followed = PlaceSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "place_followed"]


class UserRatingInfoSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "reviews_count"]

    def get_reviews_count(self, obj):
        return Rating.objects.filter(user=obj).count()


class RatingSerializer(serializers.ModelSerializer):
    user = UserRatingInfoSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ["user", "rating", "comment_body"]
