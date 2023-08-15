from django.contrib import admin
from .models import Location, Rating

# Register your models here.


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "place_name",
        "city",
        "country",
    )
    list_filter = (
        "city",
        "country",
    )
    search_fields = (
        "place_name",
        "city",
        "description",
    )


admin.site.register(Location, LocationAdmin)
admin.site.register(Rating)
