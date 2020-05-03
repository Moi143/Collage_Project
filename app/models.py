from django.db import models
from datetime import datetime, date
from django.core.validators import validate_slug, validate_email

# Create your models here.
class database(models.Model):

    student_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=30)
    roll_no = models.CharField(max_length=30)
    department_name = models.CharField(max_length=30)
    event = models.ForeignKey('app.event', on_delete=models.SET_NULL, null=True, blank=True)
    phone_no = models.CharField(max_length=30)
    email_id = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        db_table = 'database'

    def __str__(self):
        return self.student_name

class visitor(models.Model):
    v_name = models.CharField(max_length=200)
    v_email = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    Comment = models.TextField()
    class Meta:
        db_table='visitor'

    def __str__(self):
        return self.v_name

class signup(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    class Meta:
        db_table='signup'

    def __str__(self):
        return self.name

class event(models.Model):
    event_type= models.CharField(max_length=20)
    event_name = models.CharField(max_length=20)
    event_create_date = models.DateTimeField(auto_now_add=False)

    class Meta:
        db_table='event'

    def __str__(self):
        return self.event_name
