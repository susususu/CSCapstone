"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from CompaniesApp.models import Company
from AuthenticationApp.models import MyUser

class PLRequired(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(MyUser, blank=True)
    
    def __str__(self):
        return self.name
        
class YoERequired(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(MyUser, blank=True)
    
    def __str__(self):
        return self.name
        
class Speciality(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(MyUser, blank=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    PLRequirement = models.ForeignKey(PLRequired, on_delete=models.SET_NULL, null=True)
    YoERequirement = models.ForeignKey(YoERequired, on_delete=models.SET_NULL, null=True)
    SpecialityRequirement = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    r1 = models.CharField(max_length=50, null=True, blank=True)
    r2 = models.CharField(max_length=50, null=True, blank=True)
    r3 = models.CharField(max_length=50, null=True, blank=True)

    # TODO Task 3.5: Add field for company relationship
    # TODO Task 3.5: Add fields for project qualifications (minimum required: programming language, years of experience, speciality)

    def __str__(self):
        return self.name
        
class BookMark(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name