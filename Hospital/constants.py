STATUS_CHOICES=(
    ("Active", "Active"),
    ("Cancelled", "Cancelled"),
    ("Rescheduled", "Rescheduled"),
    ("Completed", "Completed"),
)

BLOOD_CHOICES=(
    ("O+","O+"),
    ("O-","O-"),
    ("A+","A+"),
    ("A-","A-"),
    ("B+","B+"),
    ("B-","B-"),
    ("AB+","AB+"),
    ("AB-","AB-"),
)

SEX_CHOICES=(
    ("M","Male"),
    ("F", "Female"),
    ("I", "Intersex"),
)

SHIFT_CHOICES=(
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('N', 'Night')
)

MEDICINE_TYPES = (
        ('tab', 'Tablet'),
        ('cap', 'Capsule'),
        ('syp', 'Syrup'),
        ('inj', 'Injection'),
        ('oth', 'Other'),
    )

PRESCRIPTION_STATUS_CHOICES=(
    ("Active", "Active"),
    ("Expired", "Expired"),
    ("Completed", "Completed"),
)

PAYMENT_MODE_CHOICES = (  
    ('cash', 'Cash'),    
    ('card', 'Card'),    
    ('netbanking', 'Net Banking'),    
    ('upi', 'UPI'),
)

BILLING_STATUS_CHOICES = (    
    ('unpaid', 'Unpaid'),    
    ('paid', 'Paid'),
)

PAYMENT_STATUS_CHOICES = (    
    ('pending', 'Pending'),    
    ('paid', 'Paid'),    (
    'failed', 'Failed'),
)
