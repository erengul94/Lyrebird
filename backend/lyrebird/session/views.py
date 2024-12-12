from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from clinic.models import Clinic
from doctor.models import Doctor
from patient.models import Patient
from publisher.audio_process_publisher import Publisher
from session.models import Session
import logging

# Initialize logger
logger = logging.getLogger(__name__)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    audio_file = request.FILES.get('audio')
    patient_id = request.data.get('patientID')

    if not audio_file:
        return JsonResponse({'error': 'No audio file provided'}, status=400)

    if not patient_id:
        return JsonResponse({'error': 'No patient ID provided'}, status=400)

    try:
        # Retrieve Patient, Doctor, and Clinic objects
        patient = get_patient(patient_id)
        doctor = get_doctor(request.user.pk)
        clinic = get_clinic(doctor)

        # Create and save session
        session = create_session_record(patient, doctor, clinic, audio_file)
        directory_name = build_directory_name(clinic, doctor, patient_id, session)

        # Publish event
        publish_audio_event(session, directory_name)

        return JsonResponse({'message': 'File uploaded successfully', "data": {"session_id": session.session_id}},
                            status=200)

    except Patient.DoesNotExist:
        logger.error(f"Patient with ID {patient_id} does not exist.")
        return JsonResponse({'error': 'Patient not found'}, status=404)

    except Doctor.DoesNotExist:
        logger.error(f"Doctor with ID {request.user.pk} does not exist.")
        return JsonResponse({'error': 'Doctor not found'}, status=404)

    except Clinic.DoesNotExist:
        logger.error(f"Clinic for doctor ID {request.user.pk} does not exist.")
        return JsonResponse({'error': 'Clinic not found'}, status=404)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


def get_patient(patient_id):
    """Retrieve patient by ID"""
    return Patient.objects.get(pk=patient_id)


def get_doctor(doctor_id):
    """Retrieve doctor by ID"""
    return Doctor.objects.get(pk=doctor_id)


def get_clinic(doctor):
    """Retrieve clinic based on the doctor's client"""
    return Clinic.objects.get(pk=doctor.client.pk)


def create_session_record(patient, doctor, clinic, audio_file):
    """Create and save session record"""
    session = Session(patient=patient, doctor=doctor, clinic=clinic, record_file=audio_file)
    session.save()
    return session


def build_directory_name(clinic, doctor, patient_id, session):
    """Build the directory name for the storage"""
    return f"{clinic.pk}/{doctor.pk}/{patient_id}/{session.session_id}"


def publish_audio_event(session, directory_name):
    """Publish the event for audio storage processing"""
    publisher = Publisher(routing_key="audio_storage_processor", exchange="storage")
    event = {
        "session_id": str(session.session_id),
        "event_name": "audio_storage_processor",
        "directory_name": directory_name,
        "file_path": session.record_file.path
    }
    publisher.publish(body=event)
