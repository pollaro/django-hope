from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register',views.register,name='register'),
    url(r'^login',views.login,name='login'),
    url(r'^travels$',views.travel,name='travel'),
    url(r'^logout',views.logout,name='logout'),
    url(r'^travels/add',views.addTravel,name='addTravel'),
    url(r'^submitTrip',views.submitTrip,name='submitTrip'),
    url(r'^joinTrip/(?P<id>[0-9]+)',views.joinTrip,name='joinTrip'),
    url(r'^trip/(?P<id>[0-9]+)',views.trip,name='trip')
]
