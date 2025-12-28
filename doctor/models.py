from django.db import models
from accounts.models import Account # Import your custom user model

class Doctor(models.Model):
    # This links the Doctor record to the Account record
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='doctor_profile')
    
    # Your doctor-specific attributes
    specialization = models.CharField(max_length=100)
    available_days = models.CharField(max_length=100)
    available_time = models.TimeField()
    

    def __str__(self):
        return f"Dr. {self.user.last_name}"
    


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE) # The Patient
    doctor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    prescription = models.FileField(upload_to='appointments/prescriptions/', blank=True, null=True)
    message = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.doctor.first_name}"