"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/add', views.projectForm, name='projectForm'),
    url(r'^project/update', views.updateProject, name='updateProject'),
    url(r'^project/delete', views.deleteProject, name='deleteProject'),
    url(r'^project/mark', views.markProject, name='markProject'),
    url(r'^project/unmark', views.unmarkProject, name='unmarkProject'),
    url(r'^bookmarks', views.bookmarks, name='bookmarks'),
]