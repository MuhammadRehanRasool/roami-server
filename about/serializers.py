from rest_framework import serializers
from .models import Sections, Team, PopularLists
from places.models import Location


class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["place_name", "place_name_slug"]


class PopularListsSerializer(serializers.ModelSerializer):
    pin = PinSerializer()

    class Meta:
        model = PopularLists
        fields = "__all__"
