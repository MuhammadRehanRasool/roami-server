from django.contrib import admin
from about import models

# Register your models here.


class PopularListsAdmin(admin.ModelAdmin):
    raw_id_fields = ('pin',)
    list_display = ("pin", "order")
    list_filter = ("pin",)
    search_fields = (
        "pin__name",
        "pin__other_field",
    )

admin.site.register(models.Sections)
admin.site.register(models.Team)
admin.site.register(models.PopularLists, PopularListsAdmin)
