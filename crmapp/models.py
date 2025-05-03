from django.db import models
from datetime import date

# -------------------signup--------------------

class User(models.Model):
    name = models.CharField(max_length=50)
    email  = models.EmailField()
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


# -------------------Customer--------------------

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email  = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    date = models.DateField(default=date.today)
    
    # Add this field to track lead conversion
    from_lead = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name
    

# -------------------Lead--------------------

class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email  = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    lead_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leads")
    lead_date = models.DateField()
    status_changed_at = models.DateTimeField(auto_now=True)  # Track when status changes to 'Customer'
    
    def __str__(self):
        return self.first_name
    

class EmailGroup(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    purpose = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

class EmailGroupMember(models.Model):
    email_group = models.ForeignKey(EmailGroup, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('Lead', 'Lead'), ('Customer', 'Customer')])
    status = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.type} ({self.email})"
   
   
class EmailHistory(models.Model):
    group = models.ForeignKey(EmailGroup, on_delete=models.CASCADE, related_name="email_histories")
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.group_name} - {self.subject} ({self.sent_at.strftime('%Y-%m-%d')})"