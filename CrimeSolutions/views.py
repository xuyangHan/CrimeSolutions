from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth import authenticate
from .models import Activities, People
from .forms import SignUpForm
from django.contrib import messages
from rest_framework import generics
from .serializers import ActivitiesSerializer
import requests
from datetime import date



# API
class ListActivitiesView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer


# Create your views here.
def index(request):
    context = {
        "activities": Activities.objects.all()
    }
    return render(request, "CrimeSolutions/index.html", context)


def crime_map(request):
    activities_json = serializers.serialize("json", Activities.objects.all())
    context = {
        "activities": Activities.objects.all(),
        "activities_json": activities_json,
    }
    return render(request, "CrimeSolutions/idx_map.html", context)


def activity(request, activity_id):
    try:
        activity = Activities.objects.get(pk=activity_id)
    except Activities.DoesNotExist:
        raise Http404("Activity does not exist.")
    context = {
        "activity": activity,
    }
    return render(request, "CrimeSolutions/activity.html", context)


def endorse(request, activity_id):
    if request.method == 'POST':
        activity = Activities.objects.get(pk=activity_id)
        activity.endorsed_number += 1
        activity.save()
        return HttpResponseRedirect(reverse('index'))


def report(request):
    errors = []
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if len(first_name) == 0 or len(first_name) == 0:
            errors.append('Please enter your name.')
            return render(request, "CrimeSolutions/report.html", {'errors': errors})

        person = People(first_name=first_name, last_name=last_name)
        person.save()

        act_name = request.POST.get('activity_name', '')
        if len(act_name) == 0:
            errors.append('Please enter name of the crime.')
            return render(request, "CrimeSolutions/report.html", {'errors': errors})

        location = request.POST.get('activity_location', '')
        if len(location) == 0:
            errors.append('Please enter name of the location.')
            return render(request, "CrimeSolutions/report.html", {'errors': errors})

        # loc_lat = request.POST.get('loc_lat', '')
        # loc_long = request.POST.get('loc_long', '')
        address = request.POST.get('address', '')
        if len(address) == 0:
            errors.append('Please enter detailed address.')
            return render(request, "CrimeSolutions/report.html", {'errors': errors})

        api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' \
                  + address + \
                  '&key=AIzaSyDCd0jbz9KTcTtx3QV-DafS44lsXDBAmHY'
        response = requests.get(url=api_url)
        data = response.json()
        loc_lat = data['results'][0]["geometry"]['location']['lat']
        loc_long = data['results'][0]["geometry"]['location']['lng']

        time = request.POST.get('time', '')
        if len(time) == 0:
            errors.append('Please enter time.')
            return render(request, "CrimeSolutions/report.html", {'errors': errors})

        description = request.POST.get('activity_description', '')
        act = Activities(act_name=act_name, location=location, time=time, description=description, loc_lat=loc_lat,
                         loc_long=loc_long, report_person=person)
        act.save()

        return HttpResponseRedirect(reverse('index'))
    return render(request, "CrimeSolutions/report.html")


def launch(request):
    return render(request, "CrimeSolutions/landing.html")


def user(request):
    i = 0
    for activity in Activities.objects.all():
        if activity.endorsed_number >= 5:
            i += 1

    start_time = date(2018, 10, 29)
    time_elp = date.today() - start_time

    youtube_api_url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCAx84KwRItMl_a2G-m0VpoA&key=AIzaSyDCd0jbz9KTcTtx3QV-DafS44lsXDBAmHY'
    youtube_response = requests.get(url=youtube_api_url)
    youtube_data = youtube_response.json()
    views = youtube_data["items"][0]["statistics"]["viewCount"]
    context = {
        "activities": Activities.objects.all(),
        "endorsed_number": i,
        "time": time_elp,
        "views": views
    }
    return render(request, "CrimeSolutions/user.html", context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            return redirect('home')
        else:
            messages.warning(request, 'Please correct the error below.')

    else:
        form = SignUpForm()
    return render(request, 'CrimeSolutions/signup.html', {'form': form})
