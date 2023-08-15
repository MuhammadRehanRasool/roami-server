from tkinter import Place

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from accounts.models import User


# Create your models here.
class Location(models.Model):
    location_link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=255)
    place_name_slug = models.SlugField()
    description = models.CharField(max_length=2000)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    tags = TaggableManager()
    photo_1 = models.ImageField(upload_to="places_images", null=True, blank=True)
    photo_2 = models.ImageField(upload_to="place_images", null=True, blank=True)
    photo_3 = models.ImageField(upload_to="places_images", null=True, blank=True)
    photo_4 = models.ImageField(upload_to="places_images", null=True, blank=True)
    photo_5 = models.ImageField(upload_to="places_images", null=True, blank=True)
    followed_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="place_followed", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.place_name} has places from {self.city}, {self.country}"

    def save(self, *args, **kwargs):  # new
        if not self.place_name_slug:
            self.place_name_slug = slugify(self.place_name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "List"
        verbose_name_plural = "Lists"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(
        Location, related_name="user_place_rating", on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField()
    comment_body = models.CharField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Rating: {self.rating} by {self.user.username} for {self.place.place_name}"
        )
