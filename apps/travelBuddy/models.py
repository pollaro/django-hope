from __future__ import unicode_literals
import re, bcrypt
from django.db import models

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
            user = Users.objects.filter(userName=postData['userName'])
        if not bcrypt.checkpw(encodePW,user.password.encode()):
            errors['login'] = 'Username and password not recognized'
        return errors


class Users(models.Model):
    name = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    plans = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer = models.ForeignKey(Users,related_name='tripsOrganized')
    joiners = models.ManyToManyField(Users,related_name='tripsJoined')
