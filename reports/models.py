from django.db import models
import uuid
# Create your models here.
class Pole (models.Model):
    pole_id = models.CharField(max_length = 20)
    street_name = models.CharField(max_length = 100)
   
    STATUS_CHOICES = [
        ('working', 'Working'),
        ('fused', 'Fused'),
        ('burning during day', 'Burning During Day'),
    ]

    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'working'
    )

    def __str__(self):
        return self.pole_id

class Report(models.Model):
    pole = models.ForeignKey(Pole, on_delete = models.CASCADE)
    
    REPORT_CHOICES = [
        ('working', 'Working'),
        ('fused', 'Fused'),
        ('burning during day', 'Burning During Day'),
    ]

    reported_status = models.CharField(max_length = 20, choices = REPORT_CHOICES)

    REPORT_STATE = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('fixed', 'Fixed'),
    ]
    
    repair_status = models.CharField(
        max_length = 20,
        choices = REPORT_STATE,
        default = 'pending'
    )
    full_address = models.TextField(blank = True)
    latitude = models.FloatField(null = True, blank = True)
    longitude = models.FloatField(null = True, blank = True)
    pole_image = models.ImageField(
        upload_to = 'pole_images/',
        blank = True,
        null = True
    )
    pole_number_image = models.ImageField(
        upload_to = 'pole_number_images/',
        blank = True,
        null = True
    )

    reported_at = models.DateTimeField(auto_now_add= True)
    complaint_id = models.CharField(max_length=12, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.complaint_id:
            self.complaint_id = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

        if self.repair_status == 'fixed':
            self.pole.status = 'working'
        else:
            self.pole.status = self.reported_status
        self.pole.save()

    def __str__(self):
        return self.pole.pole_id