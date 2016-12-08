"""ProjectsApp Admin

Created by Harris Christiansen on 10/02/16.
"""
from django.contrib import admin

from . import models

admin.site.register(models.Project)
admin.site.register(models.PLRequired)
admin.site.register(models.YoERequired)
admin.site.register(models.Speciality)