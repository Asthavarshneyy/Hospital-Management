from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from .models import *
from .forms import *


#utilities
def register(request):
    if request.method == 'POST':
        # Get user data from POST request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create new user object
        user = User.objects.create_user(username=username, email=email, password=password)

        # Set user inactive until email is confirmed
        user.is_active = False
        user.save()

        # Send email confirmation to user
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string('activate_account_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        from_email = 'astha119btcse21@igdtuw.ac.in'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        # Redirect to confirmation page
        return redirect('registration_confirmation')

    # Render registration form
    return render(request, 'register.html')

def activate_account(request, uidb64, token):
    try:
        # Get user object from URL params
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check that token is valid for user
    if user is not None and account_activation_token.check_token(user, token):
        # Activate user and login
        user.is_active = True
        user.save()
        login(request, user)

        # Redirect to success page
        return redirect('registration_success')
    else:
        # Redirect to error page
        return redirect('registration_error')  
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required
def home(request):
    if request.user.is_staff:
        return redirect('dashboard')
    if request.user.is_superuser:
        return render(request, 'admin_home.html')
    else:
        return render(request, 'home.html')
    
@login_required
def dashboard(request):
  if request.user.is_staff:
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    context = {
        'patients': patients,
        'doctors': doctors
    }
    return render(request, 'admin_dashboard.html', context)
  else:
    patient = Patient.objects.get(user=request.user)
    context = {
        'patient': patient
    }
    return render(request, 'patient_dashboard.html', context)
  

#Patient views
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})

@login_required
def my_prescriptions(request):
    prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})





# Appointment views
@login_required
def appointment_list(request):
  user = request.user
  if user.is_superuser or user.groups.filter(name='Doctors').exists():
    # Get all appointments
    appointments = Appointment.objects.all()
    context = {
            'appointments': appointments,
        }
    return render(request, 'appointment_list.html', context)
  else:
      raise PermissionDenied()

@login_required
def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})

@login_required
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointment_form.html', {'form': form})

@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('appointment_list')



# Patient views
@user_passes_test(lambda u: u.is_superuser)
class PatientListView(ListView):
  model = Patient
  template_name = 'patient_list.html'
  context_object_name = 'patients'

@user_passes_test(lambda u: u.is_superuser)
class PatientDetailView(DetailView):
  model = Patient
  template_name = 'patient_detail.html'

@user_passes_test(lambda u: u.is_superuser)
def create_patient(request):
  if request.method == 'POST':
   form = PatientForm(request.POST)
  if form.is_valid():
    patient = form.save(commit=False)
    patient.user = request.user
    patient.save()
    messages.success(request, 'Patient created successfully.')
    return redirect('patient_detail', pk=patient.pk)
  else:
    form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def update_patient(request, pk):
  patient = get_object_or_404(Patient, pk=pk)
  if request.method == 'POST':
   form = PatientForm(request.POST, instance=patient)
  if form.is_valid():
    patient = form.save()
    messages.success(request, 'Patient updated successfully.')
    return redirect('patient_detail', pk=patient.pk)
  else:
    form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_patient(request, pk):
  patient = get_object_or_404(Patient, pk=pk)
  patient.delete()
  messages.success(request, 'Patient deleted successfully.')
  return redirect('patient_list')




# Doctor Views
@user_passes_test(lambda u: u.is_superuser)
class DoctorListView(ListView):
  model = Doctor
  template_name = 'doctor_list.html'
  context_object_name = 'doctors'

@user_passes_test(lambda u: u.is_superuser)
class DoctorDetailView(DetailView):
  model = Doctor
  template_name = 'doctor_detail.html'

@user_passes_test(lambda u: u.is_superuser)
def create_doctor(request):
  if request.method == 'POST':
   form = DoctorForm(request.POST)
  if form.is_valid():
    doctor = form.save(commit=False)
    doctor.user = request.user
    doctor.save()
    messages.success(request, 'Doctor created successfully.')
    return redirect('doctor_detail', pk=doctor.pk)
  else:
    form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def update_doctor(request, pk):
  doctor = get_object_or_404(Doctor, pk=pk)
  if request.method == 'POST':
    form = DoctorForm(request.POST, instance=doctor)
  if form.is_valid():
    doctor = form.save()
    messages.success(request, 'Doctor updated successfully.')
    return redirect('doctor_detail', pk=doctor.pk)
  else:
    form = DoctorForm(instance=doctor)
    return render(request, 'doctor_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_doctor(request, pk):
  doctor = get_object_or_404(Doctor, pk=pk)
  doctor.delete()
  messages.success(request, 'Doctor deleted successfully.')
  return redirect('doctor_list')




# Billing views
@user_passes_test(lambda u: u.is_superuser)
def create_billing(request):
    if request.method == 'POST':
        form=BillingForm(request.POST)
        if form.is_valid():
           billing=form.save(commit=False)
           billing.user=request.user
           billing.save()
           messages.success(request, 'Billing created successfully.')
           return redirect('billing_detail', pk=billing.pk)
        else:
           form=BillingForm()
           return render(request, 'create_billing.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def billing_list(request):
    billings = Billing.objects.all()
    return render(request, 'billing_list.html', {'billings': billings})

@user_passes_test(lambda u: u.is_superuser)
def billing_detail(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    return render(request, 'billing_detail.html', {'billing': billing})

@user_passes_test(lambda u: u.is_superuser)
def update_billing(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=billing)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.save()
            return redirect('billing_detail', pk=billing.pk)
    else:
        form = BillingForm(instance=billing)
    return render(request, 'billing_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def deleted_billing(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    billing.delete()
    return redirect('billing_list')


# Prescription views
@user_passes_test(lambda u: u.is_superuser)
def prescription_list(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

@user_passes_test(lambda u: u.is_superuser)
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'prescription_detail.html', {'prescription': prescription})

@user_passes_test(lambda u: u.is_superuser)
def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm()
    return render(request, 'prescription_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def update_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'prescription_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    prescription.delete()
    return redirect('prescription_list')




# Inventory views
@user_passes_test(lambda u: u.is_superuser)
def inventory_list(request):
    inventory = Inventory.objects.all()
    return render(request, 'inventory_list.html', {'inventory': inventory})

@user_passes_test(lambda u: u.is_superuser)
def inventory_detail(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'inventory_detail.html', {'item': item})

@user_passes_test(lambda u: u.is_superuser)
def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('inventory_detail', pk=item.pk)
    else:
        form = InventoryForm()
    return render(request, 'inventory_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def update_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('inventory_detail', pk=item.pk)
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    item.delete()
    return redirect('inventory_list')
