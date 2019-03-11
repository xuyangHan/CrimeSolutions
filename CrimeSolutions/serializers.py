from .models import Activities
from rest_framework import serializers


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ("act_name", "location", "loc_lat", "loc_long", "time", "description", "endorsed_number")


