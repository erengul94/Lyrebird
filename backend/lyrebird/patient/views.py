from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from patient.models import Patient
from session.models import Session
from session.serializer import SessionSerializer
from .serializer import PatientSerializer
import pdb


@api_view(['GET'])
def patient_list(request):
    """
    Endpoint to retrieve a list of all patients.

    This endpoint fetches all patient records from the database and returns them
    in a JSON format. Each patient entry includes details such as the first name,
    last name, email, and phone number. The response is serialized using the
    `PatientSerializer`.

    Error Handling:
    - If no patients are found, a 404 status code with a "Patient not found" error
      message is returned.
    - If there is a validation error while serializing the data, a 400 status code
      with the error message is returned.
    - If there is an integrity error (e.g., duplicate entries), a 400 status code
      with a general integrity error message is returned.
    - If an unexpected error occurs, a 500 status code with a general error message
      and details about the exception is returned.

    Responses:
        200 OK: Returns a list of patients in JSON format.
        400 Bad Request: Returns an error message for validation or integrity issues.
        404 Not Found: Returns an error message if no patients are found.
        500 Internal Server Error: Returns a general error message in case of an unexpected error.

    """
    try:
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except IntegrityError:
        return JsonResponse({'error': 'Integrity error, possibly a duplicate entry'}, status=400)



@api_view(['GET'])
def get_patient(request, _id):
    try:
        patient = Patient.objects.get(id=_id)
        sessions = Session.objects.filter(patient=patient)
        patient_serializer = PatientSerializer(patient)
        session_serializer = SessionSerializer(sessions, many=True)
        return JsonResponse({
                'patient': patient_serializer.data,
                'sessions': session_serializer.data
            }, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)




