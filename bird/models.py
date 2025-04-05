from django.db import models

from django.db import models

class BirdSpecies(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Imgbirds/')
    audio = models.FileField(upload_to='Audiobirds/')
    description = models.TextField()

    def __str__(self):
        return self.name
