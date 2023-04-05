from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def patient_required(function=None):
    def test(user):
        return user.is_authenticated and hasattr(user, 'patient')
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator

def doctor_required(function=None):
    def test(user):
        return user.is_authenticated and hasattr(user, 'doctor')
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator

def nurse_required(function=None):
    def test(user):
        return user.is_authenticated and hasattr(user, 'nurse')
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator

def pharmacist_required(function=None):
    def test(user):
        return user.is_authenticated and hasattr(user, 'pharmacist')
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator

def receptionist_required(function=None):
    def test(user):
        return user.is_authenticated and hasattr(user, 'receptionist')
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator

def superuser_required(function=None):
    def test(user):
        return user.is_authenticated and user.is_superuser
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator

def administrator_required(function=None):
    def test(user):
        return user.is_authenticated and hasattr(user, 'administrator')
    
    actual_decorator = user_passes_test(test)
    if function:
        return actual_decorator(function)
    return actual_decorator
