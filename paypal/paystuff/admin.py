from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Transaction)
admin.site.register(BillingAddress)
admin.site.register(CardDetails)
admin.site.register(User)
