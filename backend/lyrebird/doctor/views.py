from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
# Create your views here.


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'doctor_profile'):
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'user': user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials or not a doctor'}, status=401)

    return JsonResponse({'error': 'Invalid request'}, status=400)