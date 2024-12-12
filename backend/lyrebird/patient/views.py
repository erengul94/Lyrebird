import logging
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from patient.models import Patient
from session.models import Session
from session.serializer import SessionSerializer
from .serializer import PatientSerializer

# Set up a logger for the module
logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_list(request):
    """
    Endpoint to retrieve a list of all patients for the authenticated doctor.

    This endpoint fetches all patient records associated with the logged-in doctor's client
    and returns them in a JSON format. Each patient entry includes details such as the first name,
    last name, email, and phone number. The response is serialized using the `PatientSerializer`.

    Error Handling:
    - If no patients are found, a 404 status code with a "Patient not found" error
      message is returned.
    - If there is a validation error while serializing the data, a 400 status code
      with the error message is returned.
    - If there is an integrity error (e.g., duplicate entries), a 400 status code
      with a general integrity error message is returned.
    - If an unexpected error occurs, a 500 status code with a general error message
      and details about the exception is returned.

    Returns:
        JsonResponse: Returns a list of patients in JSON format if successful, or error messages.
    """
    try:
        client_of_doctor = request.user.doctor_profile.client
        patients = Patient.objects.filter(client=client_of_doctor)

        # Log the number of patients found
        logger.info(f"Found {patients.count()} patients for doctor {request.user.username}")

        if not patients.exists():
            logger.warning("No patients found for the doctor.")
            return JsonResponse({'error': 'Patient not found'}, status=404)

        serializer = PatientSerializer(patients, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

    except ObjectDoesNotExist:
        logger.error("Error: Patient object does not exist.")
        return JsonResponse({'error': 'Patient not found'}, status=404)
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except IntegrityError:
        logger.error("Integrity error, possibly a duplicate entry.")
        return JsonResponse({'error': 'Integrity error, possibly a duplicate entry'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request, _id):
    """
    Endpoint to retrieve details for a specific patient, including their sessions.

    This endpoint fetches details of a single patient based on the provided patient ID (`_id`)
    and also retrieves the associated sessions. The patient details and session data are returned
    in JSON format, with `PatientSerializer` and `SessionSerializer` being used to serialize the data.

    Error Handling:
    - If the patient with the specified ID does not exist, a 404 status code with an error message is returned.
    - If an unexpected error occurs, a 500 status code with a general error message and details about the exception is returned.

    Returns:
        JsonResponse: Returns patient and session details in JSON format if successful, or an error message.
    """
    try:
        patient = Patient.objects.get(id=_id)
        sessions = Session.objects.filter(patient=patient)

        # Log the successful retrieval of patient data
        logger.info(f"Patient data retrieved for patient ID: {_id}")

        patient_serializer = PatientSerializer(patient)
        session_serializer = SessionSerializer(sessions, many=True)

        return JsonResponse({
            'patient': patient_serializer.data,
            'sessions': session_serializer.data
        }, status=200)

    except ObjectDoesNotExist:
        logger.error(f"Error: Patient with ID {_id} does not exist.")
        return JsonResponse({'error': 'Patient not found'}, status=404)
    except Exception as e:
        logger.error(f"Unexpected error while fetching patient or sessions: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)
