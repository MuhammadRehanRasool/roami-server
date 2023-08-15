from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User, Profile, Interest
from django.db.models import Count
from places import models

MUST_FIELDS = [
    "id",
    "profile_picture",
    "bio",
    "users_interest",
    "address",
    "paypal",
    "instagram",
    "youtube",
    "tiktok",
    "timestamp",
]


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    # users_interest = InterestSerializer(many=True)
    communityScore = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [*MUST_FIELDS, "communityScore"]

    def get_communityScore(self, obj):
        # 1. (count of entries in "Location" model search using Location__user) * 10
        location_count = models.Location.objects.filter(user=obj.user).count() * 10
        # 2. (count of followers in all objects of "Location" model search using Location__user and Location__followed_list)
        follower_count = models.Location.objects.filter(user=obj.user).aggregate(
            total_followers=Count("followed_list")
        )["total_followers"]
        # 3. (count of entries in "Rating" model search using Rating__user) * 5
        rating_count = models.Rating.objects.filter(user=obj.user).count() * 5
        # 4. ("list_import_count" in current User model) * 10
        list_import_count = obj.list_import_count * 10
        # Add them all and return the final value
        total_score = location_count + follower_count + rating_count + list_import_count
        return total_score


class UserSerializerWithToken(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", "isGoogle")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class GetFullUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username_slug",
            "email",
            "profile",
            "isGoogle"
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username_slug", "email", "isGoogle")


class GetFullProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", *MUST_FIELDS]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_user_data(self, user):
        serializer = GetFullUserSerializer(user)
        return serializer.data

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        # Add custom data to the response
        # , **self.get_user_data(self.user)
        return {**data}


class UpdateProfileSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField(required=True)
    name = serializers.CharField(max_length=100, source="user.name")

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "bio",
            "users_interest",
            "address",
            "paypal",
            "instagram",
            "youtube",
            "tiktok",
            "name",
        ]

    def update(self, instance, validated_data):
        interests_data = validated_data.pop("users_interest", None)

        # Update nested user data
        user_data = validated_data.pop("user", {})
        instance.user.name = user_data.get("name", instance.user.name)
        instance.user.save()

        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.address = validated_data.get("address", instance.address)
        instance.paypal = validated_data.get("paypal", instance.paypal)
        instance.instagram = validated_data.get("instagram", instance.instagram)
        instance.youtube = validated_data.get("youtube", instance.youtube)
        instance.tiktok = validated_data.get("tiktok", instance.tiktok)
        instance.save()

        if interests_data is not None:
            instance.users_interest.clear()
            for interest_data in interests_data:
                interest = Interest.objects.get(pk=interest_data.id)
                instance.users_interest.add(interest)

        return instance
