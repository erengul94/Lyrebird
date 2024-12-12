import logging
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Set up a logger for the module
logger = logging.getLogger(__name__)

@api_view(['POST'])
def doctor_login(request):
    """
    Handle doctor login requests. The user credentials (username and password) are 
    authenticated, and if valid, a JWT refresh and access token are generated. The user's 
    profile data is returned if the login is successful.

    Args:
        request (HttpRequest): The incoming HTTP request containing the login credentials.

    Returns:
        JsonResponse: A response containing a success message, user profile data, and token data 
                      if login is successful, or an error message if the credentials are invalid.
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Log the login attempt
        logger.info(f"Login attempt for username: {username}")

        if not username or not password:
            logger.warning("Username or password missing in request data.")
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'doctor_profile'):
            # Successful login
            login(request, user)
            refresh = RefreshToken.for_user(user)

            # Prepare token data
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            logger.info(f"Login successful for doctor: {username}")
            return JsonResponse({
                'message': 'Login successful',
                'user': user.doctor_profile.toDict(),
                "token_data": token_data
            })
        else:
            # Invalid credentials or user is not a doctor
            logger.warning(f"Invalid credentials or user {username} is not a doctor.")
            return JsonResponse({'error': 'Invalid credentials or not a doctor'}, status=401)

    # Handle invalid request method
    logger.error("Invalid request method. Expected POST.")
    return JsonResponse({'error': 'Invalid request'}, status=400)
