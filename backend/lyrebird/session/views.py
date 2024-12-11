from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyasn1_modules.rfc5755 import ClassList

from clinic.models import Clinic
from doctor.models import Doctor
from patient.models import Patient
from publisher.audio_process_publisher import AudioStorageProcessPublisher
from session.models import Session
from utils.storage import upload_to_gcs,download_audio_from_url,generate_signed_url
import speech_recognition as sr
import tempfile

@csrf_exempt
def create_session(request):

    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        audio_data = audio_file.read()
        # bucket_name = 'erentestproject'
        # destination_path = f'test_audio/{audio_file.name}'
        # public_url = upload_to_gcs(bucket_name, audio_file, destination_path)
        patient = Patient.objects.get(pk=1)
        doctor = Doctor.objects.get(pk=1)
        clinic = Clinic.objects.get(pk=1)

        session = Session(patient=patient, doctor=doctor, clinic=clinic, record_file=audio_file)
        _session = session.save()
        publisher = AudioStorageProcessPublisher(routing_key="audio_storage_processor", exchange="storage")
        event = {
            "session_id": _session.session_id,
            "event_name": "audio_storage_processor",
        }
        publisher.publish(body=event)
        return JsonResponse({'message': 'File uploaded successfully', 'url': "public_url"}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)