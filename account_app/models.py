from django.db import models
from django.contrib.auth.models import User

# Define choices as tuples
ACCOUNT_TYPE = (
    ('Savings', 'Savings'),
    ('Current', 'Current'),
)

GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=7, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique = True )
    birth_date = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    def __str__(self):
            return f"{self.account_no}"
            # return f"{self.account_no}, {self.user}"
   
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
       
    def __str__(self):
        return self.user.email
