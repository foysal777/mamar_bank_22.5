from django.contrib import admin
from .models import UserAccount,UserAddress
# Register your models here.
admin.site.register(UserAddress)
admin.site.register(UserAccount)
