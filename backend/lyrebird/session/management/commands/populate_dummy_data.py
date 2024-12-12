from django.core.management.base import BaseCommand
from client.models import Client
from clinic.models import Clinic
from doctor.models import Doctor
from patient.models import Patient
from session.models import Session
from django.contrib.auth.models import User
import random
from faker import Faker
import uuid

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Create dummy Clients
        client = Client.objects.create(
            name=fake.company(),
            email=fake.company_email(),
            password='password123',  # You can use a hashed password in real-world cases
        )
        self.stdout.write(self.style.SUCCESS(f'Created Client: {client.name}'))

        # Step 2: Create dummy Clinics
        clinic = Clinic.objects.create(
            name=fake.company(),
            address=fake.address(),
            city=fake.city(),
            state=fake.state(),
            country=fake.country(),
            client=client
        )
        self.stdout.write(self.style.SUCCESS(f'Created Clinic: {clinic.name}'))

        # Step 3: Create dummy Doctors
        user = User.objects.create_user(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password='password123'
        )
        doctor = Doctor.objects.create(
            user=user,
            address=fake.address(),
            client=client
        )
        self.stdout.write(self.style.SUCCESS(f'Created Doctor: {doctor}'))

        # Step 4: Create dummy Patients
        patient = Patient.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            client=client
        )
        self.stdout.write(self.style.SUCCESS(f'Created Patient: {patient}'))

        # Step 5: Create dummy Sessions
        session = Session.objects.create(
            doctor=doctor,
            patient=patient,
            clinic=clinic,
            started_at=fake.date_time_this_year(),
            end_at=fake.date_time_this_year(),
            recording_notes=fake.text(),
            note=fake.text(),
            record_file=None  # Or you can add a mock file path here
        )
        self.stdout.write(self.style.SUCCESS(f'Created Session: {session.session_id}'))

        # Generate multiple dummy sessions for the same patient and doctor
        for _ in range(5):  # Adjust the number of dummy sessions as needed
            session = Session.objects.create(
                doctor=doctor,
                patient=patient,
                clinic=clinic,
                started_at=fake.date_time_this_year(),
                end_at=fake.date_time_this_year(),
                recording_notes=fake.text(),
                note=fake.text(),
                record_file=None  # Or you can add a mock file path here
            )
            self.stdout.write(self.style.SUCCESS(f'Created Session: {session.session_id}'))
