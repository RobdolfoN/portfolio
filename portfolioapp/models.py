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
    
class Flight(models.Model):
    icao24 = models.CharField(max_length=24)
    callsign = models.CharField(max_length=8)
    airline = models.CharField(max_length=50)
    expected_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)  # "on_time" or "delayed"
    created_at = models.DateTimeField(auto_now_add=True)

    