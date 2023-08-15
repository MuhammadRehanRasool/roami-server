from django.db import models
from places.models import Location

# Create your models here.


class Sections(models.Model):
    heading = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    call = models.CharField(max_length=256, help_text="Text for button.")
    url = models.URLField(help_text="URL for button.", null=True, blank=True)
    image = models.ImageField(upload_to="about_images", null=True, blank=True)
    order = models.IntegerField(null=False, blank=False, unique=True)
    alignRight = models.BooleanField(
        default=True, help_text="Display image on right side?"
    )

    def __str__(self):
        return f"{self.heading}"

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"


class Team(models.Model):
    name = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="about_team_images", null=True, blank=True)
    order = models.IntegerField(null=False, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class PopularLists(models.Model):
    pin = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        help_text="Click help icon to search for your pin.",
        unique=True,
        blank=False,
        null=False,
    )
    order = models.IntegerField(null=False, blank=False, unique=True)

    def __str__(self):
        return f"{self.pin}"

    class Meta:
        verbose_name = "Popular List"
        verbose_name_plural = "Popular Lists"
