from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=512)
    image_id = models.CharField(max_length=16)
    server = models.CharField(max_length=16)
    secret = models.CharField(max_length=16)
    latitude = models.DecimalField(max_digits=18, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "locations"

