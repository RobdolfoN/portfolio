from django.db import models

# Create your models here.

class ElevationData(models.Model):
    south = models.FloatField()
    north = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()
    data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Elevation Data ({self.south}, {self.north}, {self.east}, {self.west})"