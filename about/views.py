from rest_framework.generics import ListAPIView
from .models import Sections, Team, PopularLists
from .serializers import SectionsSerializer, TeamSerializer, PopularListsSerializer


class SectionsListView(ListAPIView):
    queryset = Sections.objects.all().order_by("order")
    serializer_class = SectionsSerializer


class TeamListView(ListAPIView):
    queryset = Team.objects.all().order_by("order")
    serializer_class = TeamSerializer


class PopularListView(ListAPIView):
    queryset = PopularLists.objects.all().order_by("order")[:20]
    serializer_class = PopularListsSerializer


def add_sample_entries():
    # Add sample entries to "Sections" model
    sections_data = [
        {
            "heading": "Sample Section 1",
            "content": "This is the first sample section content.",
            "call": "Learn More",
            "url": "https://example.com/section1",
            "order": 1,
            "alignRight": False,
        },
        {
            "heading": "Sample Section 2",
            "content": "This is the second sample section content.",
            "call": "View Details",
            "url": "https://example.com/section2",
            "order": 2,
            "alignRight": True,
        },
        {
            "heading": "Sample Section 3",
            "content": "This is the third sample section content.",
            "call": "Explore",
            "url": "https://example.com/section3",
            "order": 3,
            "alignRight": False,
        },
    ]

    for data in sections_data:
        Sections.objects.create(**data)

    # Add sample entries to "Teams" model
    team_data = [
        {
            "name": "John Doe",
            "content": "Experienced software engineer.",
            "order": 1,
        },
        {
            "name": "Jane Smith",
            "content": "Creative graphic designer.",
            "order": 2,
        },
        {
            "name": "Michael Johnson",
            "content": "Marketing specialist.",
            "order": 3,
        },
    ]

    for data in team_data:
        Team.objects.create(**data)


# add_sample_entries()
