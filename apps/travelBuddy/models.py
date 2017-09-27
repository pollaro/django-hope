from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime

nameRegex = r'^[A-Za-z]{3,}'
userRegex = r'^\w{3,}'
passRegex = r'^\w{8,}'
nameRegex = re.compile(nameRegex)
userRegex = re.compile(userRegex)
passRegex = re.compile(passRegex)

class UserManager(models.Manager):
    def validator(self,postData):
        errors={}
        if not nameRegex.match(postData['name']):
            errors['name'] = 'Please enter a name of at least 3 letters'
        if not userRegex.match(postData['userName']):
            errors['user'] = 'Please enter a username of at least 3 characters'
        if not passRegex.match(postData['password']):
            errors['password'] = 'Please enter a password of at least 8 characters'
        if postData['password'] != postData['confirmPW']:
            errors['confirm'] = 'Password and confirm password must match'
        if len(Users.objects.filter(userName=postData['userName'])) > 0:
            errors['userNameInUse'] = 'Username is already in use'
        return errors
    def loginValid(self,postData):
        errors={}
        encodePW = postData['password'].encode()
        if not len(Users.objects.filter(userName=postData['userName'])) > 0:
            errors['login'] = 'Username and password not recognized'
        else:
            user = Users.objects.get(userName=postData['userName'])
        if not bcrypt.checkpw(encodePW,user.password.encode()):
            errors['login'] = 'Username and password not recognized'
        return errors

class TripManager(models.Manager):
    def tripValid(self,postData):
        errors={}
        if len(postData['destination']) == 0 or len(postData['description']) == 0 or len(postData['travelFrom']) == 0 or len(postData['travelTo']) == 0:
            errors['blanks'] = 'All fields must be filled out'
        elif datetime.now() > datetime.strptime(postData['travelFrom'],'%Y-%m-%d'):
            errors['future'] = 'Travel must start after today'
        elif datetime.strptime(postData['travelTo'],'%Y-%m-%d') < datetime.strptime(postData['travelFrom'],'%Y-%m-%d'):
            errors['wrongDates'] = 'Travel From date must be before Travel To date'
        return errors

class Users(models.Model):
    name = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    plans = models.TextField()
    organized = models.ForeignKey(Users,related_name='tripsOrganized')
    joined = models.ManyToManyField(Users,through='Plans',through_fields=('trip','join'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class Plans(models.Model):
    trip = models.ForeignKey(Trips,related_name='tripPlan')
    join = models.ForeignKey(Users,related_name='userJoin')
