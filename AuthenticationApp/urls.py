"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register$', views.select_type, name='Register'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),
    url(r'^StudentRegister', views.registe_student, name='StudentRegister'),
    url(r'^TeacherRegister', views.registe_teacher, name='TeacherRegister'),
    url(r'^EngineerRegister', views.registe_engineer, name='EngineerRegister'),
]