# Generated by Django 2.0.6 on 2018-12-04 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_name', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('loc_lat', models.FloatField()),
                ('loc_long', models.FloatField()),
                ('time', models.DateField(max_length=64)),
                ('description', models.CharField(max_length=5000)),
                ('endorsed_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='activities',
            name='report_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CrimeSolutions.People'),
        ),
    ]
