from django.db import models

import os
from PIL import Image
from location_field.models.plain import PlainLocationField
from taggit.managers import TaggableManager


def get_header_images_default(): list([])


def get_location_city_default():
    return "46.55472,15.64667"


class Klub(models.Model):
    slug = models.SlugField(unique=True)

    ime = models.CharField(max_length=512)
    opis = models.CharField(max_length=4096)

    logo = models.ImageField(upload_to="klub_logo/", blank=True)

    location = PlainLocationField(
        based_fields=["city"], default=get_location_city_default()
    )

    urnik = models.CharField(max_length=512, null=True, blank=True)

    mail = models.EmailField(null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)

    twitter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)

    tags = TaggableManager()

    class Meta:
        verbose_name = "Klub"
        verbose_name_plural = "Klubi"

    def __str__(self):
        return self.ime


class SlikaKluba(models.Model):
    naslov = models.CharField(max_length=512)
    opis = models.CharField(max_length=4096)
    slika = models.ImageField(upload_to="header_slike/")

    klub = models.ForeignKey(Klub, on_delete=models.CASCADE, related_name="slike")

    class Meta:
        verbose_name = "Slika"
        verbose_name_plural = "Slike"

    def save(self, *args, **kwargs):
        instance = super(SlikaKluba, self).save(*args, **kwargs)

        image = Image.open(instance.slika.path).convert("RGB")

        path, ext = os.path.splitext(instance.slika.path)
        newPath = path + ".webp"

        image.save(newPath, "webp", lossless=False, quality=25)

        self.slika = newPath
        super(SlikaKluba, self).save(*args, **kwargs)
        return instance

    def __str__(self):
        return "%s - %s" % (self.klub, self.naslov)
