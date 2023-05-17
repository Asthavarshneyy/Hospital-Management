from django.urls import path
from .views import *

app_name="Hospital"

urlpatterns = [
      path('',trial, name='trial_page')]
#     path('', views.landing_page, name='landing_page'),
#     path('patient_register/', views.patient_register, name='patient_register'),
#     path('staff_register/', views.staff_register, name='staff_register'),
#     path('update_profile/', views.update_profile, name='update_profile'),
#     path('view_profile/', views.view_profile, name='view_profile'),
#     #path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     #path('home/', views.home, name='home'),
#     #path('dashboard/', views.dashboard, name='dashboard'),
#     path('all_appointments/', views.all_appointments, name='all_appointments'),
#     path('patient_appointments/', views.patient_appointments, name='patient_appointments'),
#     path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
#     path('create_appointment/', views.create_appointment, name='create_appointment'),
#     path('appointment_detail/<int:pk>/', views.appointment_detail, name='appointment_detail'),
#     path('update_appointment/<int:pk>/', views.update_appointment, name='update_appointment'),
#     path('all_patients/', views.all_patients, name='all_patients'),
#     path('patient_detail/<int:pk>/', views.patient_detail, name='patient_detail'),
#     path('all_billings/', views.all_billings, name='all_billings'),
#     path('patient_billings/', views.patient_billings, name='patient_billings'),
#     path('create_billing/', views.create_billing, name='create_billing'),
#     path('billing_detail/<int:pk>/', views.billing_detail, name='billing_detail'),
#     path('update_billing/<int:pk>/', views.update_billing, name='update_billing'),
#     path('all_prescriptions/', views.all_prescriptions, name='all_prescriptions'),
#     path('patient_prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
#     path('doctor_prescriptions/', views.doctor_prescriptions, name='doctor_prescriptions'),
#     path('create_prescription/', views.create_prescription, name='create_prescription'),
#     path('prescription_detail/<int:pk>/', views.prescription_detail, name='prescription_detail'),
#     path('update_prescription/<int:pk>/', views.update_prescription, name='update_prescription'),
#     path('all_inventorys/', views.all_inventorys, name='all_inventorys'),
#     path('create_inventory/', views.create_inventory, name='create_inventory'),
#     path('inventory_detail/<int:pk>/', views.inventory_detail, name='inventory_detail'),
#     path('update_inventory/<int:pk>/', views.update_inventory, name='update_inventory'),
#     path('update_medical_history/<int:pk>/', views.update_medical_history, name='update_medical_history'),
#     path('medical_history_detail/<int:pk>/', views.medical_history_detail, name='medical_history_detail'),
# ]
