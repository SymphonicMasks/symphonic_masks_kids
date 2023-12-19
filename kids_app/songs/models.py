from django.db import models


# Create your models here.
class Song(models.Model):
    title = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.title

    @property
    def midi_path(self):
        return f"data/midi/{self.title}.midi"
