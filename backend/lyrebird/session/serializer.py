
from rest_framework import serializers
from .models import Patient, Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id', 'patient', 'doctor', 'clinic', 'started_at', 'end_at', 'recording_notes', 'note']