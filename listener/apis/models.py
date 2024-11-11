from django.db import models

class PotholeData(models.Model):
    timestamp = models.DateTimeField()
    load_value = models.FloatField()
    tilt_status = models.FloatField()
    distance = models.FloatField()
    label = models.IntegerField()

    def __str__(self):
        return f"Data at {self.timestamp} - Label: {self.label}"
