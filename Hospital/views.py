from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import *
from .forms import *
from .decorators import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


def trial(request):
    context={}
    return render(request, "base.html", context)



# @receiver(post_save, sender=Patient)
# def create_medical_history(sender, instance, created, **kwargs):
#     if created:
#         Medical_History.objects.create(patient=instance)


# #utilities
# # def register(request):
# #     if request.method == 'POST':
# #         # Get user data from POST request
# #         username = request.POST['username']
# #         email = request.POST['email']
# #         password = request.POST['password']

# #         # Create new user object
# #         user = User.objects.create_user(username=username, email=email, password=password)

# #         # Set user inactive until email is confirmed
# #         user.is_active = False
# #         user.save()

# #         # Send email confirmation to user
# #         current_site = get_current_site(request)
# #         subject = 'Activate Your Account'
# #         message = render_to_string('activate_account_email.html', {
# #             'user': user,
# #             'domain': current_site.domain,
# #             'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
# #             'token': account_activation_token.make_token(user),
# #         })
# #         from_email = 'astha119btcse21@igdtuw.ac.in'
# #         recipient_list = [user.email]
# #         send_mail(subject, message, from_email, recipient_list)

# #         # Redirect to confirmation page
# #         return redirect('registration_confirmation')

# #     # Render registration form
# #     return render(request, 'register.html')

# # def activate_account(request, uidb64, token):
# #     try:
# #         # Get user object from URL params
# #         uid = urlsafe_base64_decode(uidb64).decode()
# #         user = User.objects.get(pk=uid)
# #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
# #         user = None

# #     # Check that token is valid for user
# #     if user is not None and account_activation_token.check_token(user, token):
# #         # Activate user and login
# #         user.is_active = True
# #         user.save()
# #         login(request, user)

# #         # Redirect to success page
# #         return redirect('registration_success')
# #     else:
# #         # Redirect to error page
# #         return redirect('registration_error')  

# # Register Views
# # REGISTER A NEW PATIENT AND CREATE A MEDICAL HISTORY
# def patient_register(request):
#     if request.method == 'POST':
#         patient_form = PatientForm(request.POST)
#         medical_history_form = MedicalHistoryForm(request.POST, request.FILES)
#         if patient_form.is_valid() and medical_history_form.is_valid():
#             # Create a new patient instance
#             patient = patient_form.save(commit=False)
#             patient.user = request.user
#             patient.save()

#             # Create a new medical history instance for the new patient
#             medical_history = medical_history_form.save(commit=False)
#             medical_history.patient = patient
#             medical_history.save()

#             messages.success(request, 'Patient and medical history added successfully!')
#             return redirect('home')
#     else:
#         patient_form = PatientForm()
#         medical_history_form = MedicalHistoryForm()
#     context = {
#         'patient_form': patient_form,
#         'medical_history_form': medical_history_form,
#     }
#     return render(request, 'create_patient.html', context)

# # REGISTER A NEW STAFF
# def staff_register(request):
#     if request.method == 'POST':
#         staff_type = request.POST.get('staff_type')
#         if staff_type == 'doctor':
#             form = DoctorForm(request.POST)
#         elif staff_type == 'nurse':
#             form = NurseForm(request.POST)
#         elif staff_type == 'receptionist':
#             form = ReceptionistForm(request.POST)
#         elif staff_type == 'pharmacist':
#             form = PharmacistForm(request.POST)
#         elif staff_type == 'administrator':
#             form = AdministratorForm(request.POST)
#         else:
#             messages.error(request, 'Invalid staff type selected.')
#             return redirect('staff_register')
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, f'You have successfully registered as a {staff_type}.')
#             return redirect('home')
#     else:
#         form = DoctorForm()
#     return render(request, 'staff_register.html', {'form': form})


# # UPDATE A PROFILE
# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('update_profile')
#     else:
#         form = UserUpdateForm(instance=request.user)

#     context = {'form': form}
#     return render(request, 'update_profile.html', context)

# # SEE YOUR PROFILE
# @login_required
# def view_profile(request):
#     user = request.user
#     model = get_user_model()
    
#     # check if the user is of any model
#     if isinstance(user, model):
#         profile = get_object_or_404(model, pk=user.pk)
#         return render(request, 'profile.html', {'profile': profile})
#     else:
#         return HttpResponseForbidden()
    
# # READ A PATIENT
# @superuser_required
# @receptionist_required
# @doctor_required
# @nurse_required
# def all_patients(request):
#     patients = Patient.objects.all()
#     return render(request, 'patients.html', {'patients': patients})

# # IN DETAIL
# @doctor_required
# @nurse_required
# @receptionist_required
# @superuser_required
# @pharmacist_required
# def patient_detail(request, pk):
#     patient = Patient.objects.get(pk=pk)
#     # Check that the requesting user has access to the patients
#     if request.user.is_receptionist or request.user.is_superuser or request.is_nurse or request.is_doctor or request.is_pharmacist:
#         # Receptionist, Doctor, Pharmacist and Nurse can see all patients
#         pass
#     else:
#         # Return 403 forbidden if user does not have access
#         return HttpResponseForbidden("You do not have permission to view this Patient.")

#     # Render template with appointment details
#     context = {'patient': patient}
#     return render(request, 'patient_detail.html', context)
    
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid login credentials.')
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     messages.success(request, 'You have been logged out.')
#     return redirect('login')

# def landing_page(request):
#     return render(request, 'landing_page.html')

# # @login_required
# # def home(request):
# #     if request.user.is_staff:
# #         return redirect('dashboard')
# #     if request.user.is_superuser:
# #         return render(request, 'admin_home.html')
# #     else:
# #         return render(request, 'home.html')
    

    
# # @login_required
# # def dashboard(request):
# #   if request.user.is_staff:
# #     patients = Patient.objects.all()
# #     doctors = Doctor.objects.all()
# #     context = {
# #         'patients': patients,
# #         'doctors': doctors
# #     }
# #     return render(request, 'admin_dashboard.html', context)
# #   else:
# #     patient = Patient.objects.get(user=request.user)
# #     context = {
# #         'patient': patient
# #     }
# #     return render(request, 'patient_dashboard.html', context)




# # Appointment views
# # READ AN APPOINTMENT
# @superuser_required
# @receptionist_required
# @nurse_required
# def all_appointments(request):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments.html', {'appointments': appointments})

# @patient_required
# def patient_appointments(request):
#     appointments = Appointment.objects.filter(patient=request.user.patient)
#     return render(request, 'appointments.html', {'appointments': appointments})

# @doctor_required
# def doctor_appointments(request):
#     appointments = Appointment.objects.filter(doctor=request.user.doctor)
#     return render(request, 'appointments.html', {'appointments': appointments})


# # IN DETAIL
# @doctor_required
# @patient_required
# @receptionist_required
# @superuser_required
# def appointment_detail(request, pk):
#     appointment = Appointment.objects.get(pk=pk)
#     # Check that the requesting user has access to the appointment
#     if request.user.is_doctor and request.user.doctor == appointment.doctor:
#         # Doctor can see all appointments associated with them
#         pass
#     elif request.user.is_patient and request.user.patient == appointment.patient:
#         # Patient can see all appointments associated with them
#         pass
#     elif request.user.is_receptionist or request.user.is_superuser:
#         # Receptionist can see all appointments
#         pass
#     else:
#         # Return 403 forbidden if user does not have access
#         return HttpResponseForbidden("You do not have permission to view this appointment.")

#     # Render template with appointment details
#     context = {'appointment': appointment}
#     return render(request, 'appointment_detail.html', context)


# # CREATE AN APPOINTMENT
# @login_required
# def create_appointment(request):
#     if not request.user.receptionist:
#         # Only receptionists can create appointments
#         messages.error(request, 'You do not have permission to create appointments. Please contact a receptionist to schedule an appointment')
#         return redirect('home')
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.created_by = request.user
#             appointment.save()
#             messages.success(request, 'Appointment created successfully.')
#             return redirect('appointment_detail', pk=appointment.pk)
#     else:
#         form = AppointmentForm()
#         # TEMPLATE: create_appointment.html
#     return render(request, 'create_appointment.html', {'form': form})

# # UPDATE AN APPOINTMENT
# @login_required
# def update_appointment(request, pk):
#     appointment = get_object_or_404(Appointment, pk=pk)
#     if request.user != appointment.created_by:
#         # Only the user who created the appointment can update it
#         messages.error(request, 'You do not have permission to update this appointment.')
#         return redirect('appointment_detail', pk=appointment.pk)
#     if request.method == "POST":
#         form = AppointmentForm(request.POST, instance=appointment)
#         if form.is_valid():
#             form.save()
#             return redirect('appointment_detail', pk=appointment.pk)
#     else:
#         form = AppointmentForm(instance=appointment)
#     # TEMPLATE: update_appointment
#     return render(request, 'update_appointment.html', {'form': form})



# # Billing views
# # CREATE BILLING
# @login_required
# def create_billing(request):
#     if not request.user.receptionist:
#         # Only receptionists can create billings
#         messages.error(request, 'You do not have permission to create billings.')
#         return redirect('home')

#     if request.method == 'POST':
#         form = BillingForm(request.POST)
#         if form.is_valid():
#             billing = form.save(commit=False)
#             billing.created_by = request.user
#             billing.save()
#             messages.success(request, 'Billing created successfully.')
#             return redirect('billing_detail', billing.pk)
#     else:
#         form = BillingForm()
#     # TEMPLATE: create_billing
#     return render(request, 'create_billing.html', {'form': form})

# # READ BILLINGS
# @superuser_required
# @receptionist_required
# def all_billings(request):
#     billings = Billing.objects.all()
#     return render(request, 'billings.html', {'billings': billings})

# @patient_required
# def patient_billings(request):
#     billings = Billing.objects.filter(patient=request.user.patient)
#     return render(request, 'billings.html', {'billings': billings})

# # IN DETAIL
# @patient_required
# @receptionist_required
# def billing_detail(request, pk):
#     billing = Billing.objects.get(pk=pk)
#     # Check that the requesting user has access to the appointment
#     if request.user.is_patient and request.user.patient == billing.patient:
#         # Patient can see all appointments associated with them
#         pass
#     elif request.user.is_receptionist or request.user.is_superuser:
#         # Receptionist can see all appointments
#         pass
#     else:
#         # Return 403 forbidden if user does not have access
#         return HttpResponseForbidden("You do not have permission to view this billing.")

#     # Render template with appointment details
#     context = {'billing': billing}
#     return render(request, 'billing_detail.html', context)


# # UPDATE BILLING
# @login_required
# def update_billing(request, pk):
#     billing = get_object_or_404(Billing, pk=pk)
#     if not request.user.receptionist:
#         # Only receptionists can update billings
#         messages.error(request, 'You do not have permission to update this billing.')
#         return redirect('home')

#     if request.method == 'POST':
#         form = BillingForm(request.POST, instance=billing)
#         if form.is_valid():
#             billing = form.save(commit=False)
#             billing.updated_by = request.user
#             billing.save()
#             messages.success(request, 'Billing updated successfully.')
#             return redirect('billing_detail', pk=billing.pk)
#     else:
#         form = BillingForm(instance=billing)
#     # TEMPLATE: update_billing
#     return render(request, 'update_billing.html', {'form': form, 'billing': billing})




# # Prescription views
# # READ A PRESCRIPTION
# @superuser_required
# @receptionist_required
# @pharmacist_required
# def all_prescriptions(request):
#     prescriptions = Prescription.objects.all()
#     return render(request, 'prescriptions.html', {'prescriptions': prescriptions})

# @patient_required
# def patient_prescriptions(request):
#     prescriptions = Prescription.objects.filter(patient=request.user.patient)
#     return render(request, 'prescriptions.html', {'prescriptions': prescriptions})

# @doctor_required
# def doctor_prescriptions(request):
#     prescriptions = Prescription.objects.filter(doctor=request.user.patient)
#     return render(request, 'prescriptions.html', {'prescriptions': prescriptions})

# # IN DETAIL
# @doctor_required
# @patient_required
# @receptionist_required
# @pharmacist_required
# @superuser_required
# def prescription_detail(request, pk):
#     prescription = Prescription.objects.get(pk=pk)
#     # Check that the requesting user has access to the appointment
#     if request.user.is_doctor and request.user.doctor == prescription.doctor:
#         # Doctor can see all appointments associated with them
#         pass
#     elif request.user.is_patient and request.user.patient == prescription.patient:
#         # Patient can see all appointments associated with them
#         pass
#     elif request.user.is_receptionist or request.user.is_pharmacist or request.user.is_superuser:
#         # Receptionist and Pharmacist can see all appointments
#         pass
#     else:
#         # Return 403 forbidden if user does not have access
#         return HttpResponseForbidden("You do not have permission to view this prescription.")

#     # Render template with appointment details
#     context = {'prescription': prescription}
#     return render(request, 'prescription_detail.html', context)

# # CREATE PRESCRIPTION
# @login_required
# def create_prescription(request):
#     if not request.user.doctor:
#         # Only doctors can create prescriptions
#         messages.error(request, 'You do not have permission to create prescriptions.')
#         return redirect('home')

#     if request.method == 'POST':
#         form = PrescriptionForm(request.POST)
#         if form.is_valid():
#             prescription = form.save(commit=False)
#             prescription.created_by = request.user
#             prescription.save()
#             messages.success(request, 'Prescription created successfully.')
#             return redirect('prescription_detail', prescription.pk)
#     else:
#         form = PrescriptionForm()

#     return render(request, 'create_prescription.html', {'form': form})

# # UPDATE PRESCRIPTION
# @login_required
# def update_prescription(request, pk):
#     prescription = get_object_or_404(Prescription, pk=pk)

#     if not request.user.doctor:
#         # Only doctors can update prescriptions
#         messages.error(request, 'You do not have permission to update prescriptions.')
#         return redirect('home')

#     if request.method == 'POST':
#         form = PrescriptionForm(request.POST, instance=prescription)
#         if form.is_valid():
#             prescription = form.save(commit=False)
#             prescription.created_by = request.user
#             prescription.save()
#             messages.success(request, 'Prescription updated successfully.')
#             return redirect('prescription_detail', pk=prescription.pk)
#     else:
#         form = PrescriptionForm(instance=prescription)

#     return render(request, 'update_prescription.html', {'form': form, 'prescription': prescription})



# # Inventory views
# # READ AN INVENTORY
# @superuser_required
# @doctor_required
# @nurse_required
# @pharmacist_required
# def all_inventorys(request):
#     inventorys = Inventory.objects.all()
#     return render(request, 'inventorys.html', {'inventorys': inventorys})


# # IN DETAIL
# @doctor_required
# @nurse_required
# @pharmacist_required
# @superuser_required
# def inventory_detail(request, pk):
#     inventory = Inventory.objects.get(pk=pk)
#     if request.user.is_doctor or request.user.is_pharmacist or request.user.is_superuser or request.user.is_nurse:
#         # Doctor, Nurse and Pharmacist can see all appointments
#         pass
#     else:
#         # Return 403 forbidden if user does not have access
#         return HttpResponseForbidden("You do not have permission to view this inventory.")

#     # Render template with appointment details
#     context = {'inventory': inventory}
#     return render(request, 'inventory_detail.html', context)


# # CREATE INVENTORY
# @login_required
# def create_inventory(request):
#     if not request.user.pharmacist:
#         # Only pharmacists can create inventories
#         messages.error(request, 'You do not have permission to create inventories.')
#         return redirect('home')
#     if request.method == 'POST':
#         form = InventoryForm(request.POST)
#         if form.is_valid():
#             inventory = form.save(commit=False)
#             inventory.save()
#             messages.success(request, 'Inventory created successfully.')
#             return redirect('inventory_detail', inventory.pk)
#     else:
#         form = InventoryForm()
# # TEMPLATE: create_inventory.html
#     return render(request, 'create_inventory.html', {'form': form})

# # UPDATE INVENTORY
# @login_required
# def update_inventory(request, pk):
#     inventory = get_object_or_404(Inventory, pk=pk)
#     if not request.user.pharmacist:
#         # Only pharmacists can update inventories
#         messages.error(request, 'You do not have permission to update inventories.')
#         return redirect('home')

#     if request.method == 'POST':
#         form = InventoryForm(request.POST, instance=inventory)
#         if form.is_valid():
#             inventory = form.save()
#             messages.success(request, 'Inventory updated successfully.')
#             return redirect('inventory_detail', inventory.pk)
#     else:
#         form = InventoryForm(instance=inventory)
#     # TEMPLATE: update_inventory.html
#     return render(request, 'update_inventory.html', {'form': form, 'inventory': inventory})


# # Medical History views
# # UPDATE MEDICAL HISTORY
# @login_required
# def update_medical_history(request, pk):
#     medical_history = get_object_or_404(Medical_History, pk=pk)
#     patient = medical_history.patient
#     if not request.user.receptionist:
#         # Only receptionists can update medical history
#         messages.error(request, 'You do not have permission to update this medical history record.')
#         return redirect('home')
#     if request.method == 'POST':
#         form = MedicalHistoryForm(request.POST, request.FILES, instance=medical_history)
#         if form.is_valid():
#             medical_history = form.save(commit=False)
#             medical_history.prescription = patient.current_prescription
#             medical_history.save()
#             messages.success(request, 'Medical history updated successfully.')
#             return redirect('medical_history_detail', medical_history.pk)
#     else:
#         form = MedicalHistoryForm(instance=medical_history)
#     # TEMPLATE: update_medical_history
#     return render(request, 'update_medical_history.html', {'form': form, 'medical_history': medical_history})

# # READ A MEDICAL HISTORY
# # IN DETAIL
# @doctor_required
# @patient_required
# @receptionist_required
# @superuser_required
# def medical_history_detail(request, pk):
#     medical_history = Medical_History.objects.get(pk=pk)
#     # Check that the requesting user has access to the appointment
#     # see if this works!
#     if request.user.is_doctor and request.user.doctor == medical_history.appointment.doctor: 
#         # Doctor can see all appointments associated with them
#         pass
#     elif request.user.is_patient and request.user.patient == medical_history.patient:
#         # Patient can see all medical history associated with them
#         pass
#     elif request.user.is_receptionist or request.user.is_superuser:
#         # Receptionist can see all medical history
#         pass
#     else:
#         # Return 403 forbidden if user does not have access
#         return HttpResponseForbidden("You do not have permission to view this medical_history.")

#     # Render template with appointment details
#     context = {'medical_history': medical_history}
#     return render(request, 'medical_history_detail.html', context)