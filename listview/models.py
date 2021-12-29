from django.db import models
from django.forms import ModelForm, Textarea


# Create your models here.
class Customer(models.Model):
  id = models.AutoField(primary_key=True)
  linkedin = models.CharField(max_length=150, null=True)
  name = models.CharField(max_length=150, null=True)
  company = models.TextField(null=True)
  linkedin_title = models.TextField(null=True)
  current_role = models.TextField(null=True)
  nature_of_work = models.TextField(null=True)
  linkedin_summary = models.TextField(null=True)
  email = models.EmailField(max_length=150, null=True)
  phone = models.CharField(max_length=10, null=True)
  date = models.DateField(auto_now_add=True)
  category = models.CharField(max_length=200, null=True)
  rating = models.CharField(max_length=40, null=True)
  connection = models.CharField(max_length=150, null=True)
  status = models.CharField(max_length=150, null=True)
  connect_type = models.CharField(max_length=150, null=True)

  def __str__(self):
    return f'{ self.name }'

class Login_Details(models.Model):
  u_name = models.CharField(max_length=40)
  u_email = models.EmailField(max_length=40, primary_key=True)
  u_pass = models.CharField(max_length=40)
  u_access = models.CharField(max_length=40)

  def __str__(self):
    return f'{ self.u_name }'

class Base_Email(models.Model):
  b_name = models.CharField(max_length=40)
  b_email = models.EmailField(max_length=40)
  b_pass = models.CharField(max_length=40, null=True)

  def __str__(self):
    return f'{ self.b_name }'