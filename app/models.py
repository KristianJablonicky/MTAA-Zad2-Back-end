# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    worker_id = models.IntegerField()
    job_offer_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    response = models.BooleanField(blank=True, null=True)
    created_on = models.DateTimeField()
    expires_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'application'


class Call(models.Model):
    id = models.IntegerField(primary_key=True)
    worker_id = models.IntegerField()
    employer_id = models.IntegerField()
    name = models.CharField(max_length=30)
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'call'


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    detail = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class Employer(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employer'


class JobOffer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    employer_id = models.IntegerField()
    field = models.CharField(max_length=30)
    salary = models.TextField(blank=True, null=True)  # This field type is a guess.
    working_hours = models.DurationField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_offer'


class Worker(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_date = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker'
