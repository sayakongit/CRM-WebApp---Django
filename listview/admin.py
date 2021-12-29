from django.contrib import admin

# Register your models here.
from . models import Customer, Base_Email

admin.site.register(Customer)
admin.site.register(Base_Email)


# class CustomerAdmin(admin.ModelAdmin):
#   list_display = ['id', name]