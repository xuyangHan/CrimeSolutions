from django.db import models


class People(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Activities(models.Model):
    act_name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    loc_lat = models.FloatField()
    loc_long = models.FloatField()
    time = models.DateField(max_length=64)
    report_person = models.ForeignKey(People, on_delete=models.CASCADE)
    description = models.CharField(max_length=5000)
    endorsed_number = models.IntegerField(default=0)

    def __str__(self):
        return f" ACT: {self.act_name}  LOC: {self.location} TIME: {self.time}"


