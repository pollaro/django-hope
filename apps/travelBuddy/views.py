from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Users,Trips,Plans
from datetime import datetime
import bcrypt

def index(request):
    return render(request,'travelBuddy/index.html')

def register(request):
    errors = Users.objects.validator(request.POST)
    if len(errors):
        for tag,error in errors.iteritems():
            messages.error(request,error,extra_tags=tag)
        return redirect('index')
    else:
        hashedPW = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        Users.objects.create(name=request.POST['name'],userName=request.POST['userName'],password=hashedPW)
        user = Users.objects.get(userName=request.POST['userName'])
        request.session['name'] = user.name
        request.session['userName'] = user.userName
        request.session['userID'] = user.id
        return redirect('travel')

def login(request):
    errors = Users.objects.loginValid(request.POST)
    if len(errors):
        for tag,error in errors.iteritems():
            messages.error(request,error,extra_tags=tag)
        return redirect('index')
    else:
        user = Users.objects.get(userName=request.POST['userName'])
        request.session['name'] = user.name
        request.session['userName'] = user.userName
        request.session['userID'] = user.id
        return redirect('travel')

def travel(request):
    userTrips = Trips.objects.filter(joined=request.session['userID'])|Trips.objects.filter(organized=request.session['userID'])
    otherTrips = Trips.objects.exclude(organized=Users.objects.get(id=request.session['userID'])).exclude(joined=Users.objects.get(id=request.session['userID']))
    context = {
        'userTrips':userTrips,
        'otherTrips':otherTrips
    }
    return render(request,'travelBuddy/travel.html',context)

def addTravel(request):
    return render(request,'travelBuddy/addTravel.html')

def submitTrip(request):
    errors = Trips.objects.tripValid(request.POST)
    if len(errors):
        for tag,error in errors.iteritems():
            messages.error(request,error,extra_tags=tag)
        return redirect('addTravel')
    else:
        Trips.objects.create(destination=request.POST['destination'],plans=request.POST['description'],startDate=datetime.strptime(request.POST['travelFrom'],'%Y-%m-%d'),endDate=datetime.strptime(request.POST['travelTo'],'%Y-%m-%d'),organized=Users.objects.get(id=request.session['userID']))
        trip = Trips.objects.get(destination=request.POST['destination'],startDate=datetime.strptime(request.POST['travelFrom'],'%Y-%m-%d'),endDate=datetime.strptime(request.POST['travelTo'],'%Y-%m-%d'),organized=Users.objects.get(id=request.session['userID']))
        return redirect('travel')

def joinTrip(request,id):
    Plans.objects.create(trip=Trips.objects.get(id=id),join=Users.objects.get(id=request.session['userID']))
    return redirect('travel')

def trip(request,id):
    trip = Trips.objects.get(id=id)
    plans = Plans.objects.filter(trip=trip)
    context = {
        'trip':trip,
        'plans':plans
    }
    return render(request,'travelBuddy/trip.html',context)

def logout(request):
    request.session.clear()
    return redirect('index')
