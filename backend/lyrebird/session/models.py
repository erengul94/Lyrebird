import uuid

from django.db import models

from clinic.models import Clinic
from doctor.models import Doctor
from patient.models import Patient



class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(auto_now_add=True)
    record_file = models.FileField(upload_to="records", null=True) # URL to the audio recording


    def __str__(self):
        return (f"Doctor:{self.doctor} // Patient: {self.patient} // Clinic: {self.clinic} "
                f"// Started At: {self.started_at}")
