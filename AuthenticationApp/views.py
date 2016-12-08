#!/usr/bin/python
# -*- coding: utf-8 -*-

"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import LoginForm, RegisterForm, UpdateForm, UpdateFormStudent, UpdateFormTeacher, UpdateFormEngineer, StudentRegisterForm, TeacherRegisterForm, EngineerRegisterForm
from .models import MyUser, Student, Teacher, Engineer
from UniversitiesApp.models import University
from CompaniesApp.models import Company


def select_type(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render(request, 'user_selection.html')

def registe_student(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    form = StudentRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password2'],
            first_name=form.cleaned_data['firstname'],
            last_name=form.cleaned_data['lastname'],
            is_student=True
            )
        new_user.save()

        uni = University.objects.filter(name=form.cleaned_data['university'])
        uni[0].members.add(new_user)
        new_u = Student(user=new_user)
        new_u.contact = form.cleaned_data['contact']
        new_u.about = form.cleaned_data['about']
        new_u.university = uni[0].name
        new_u.save()
        
        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        'form': form,
        'page_name': 'Register',
        'button_value': 'Register',
        'links': ['login'],
        }
    return render(request, 'auth_form.html', context)
        
def registe_teacher(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    form = TeacherRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password2'],
            first_name=form.cleaned_data['firstname'],
            last_name=form.cleaned_data['lastname'],
            is_professor=True
            )
        new_user.save()

        uni = University.objects.filter(name=form.cleaned_data['university'])
        uni[0].members.add(new_user)
        new_u = Teacher(user=new_user)
        new_u.contact = form.cleaned_data['contact']
        new_u.about = form.cleaned_data['about']
        new_u.university = uni[0].name
        new_u.save()
        
        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        'form': form,
        'page_name': 'Register',
        'button_value': 'Register',
        'links': ['login'],
        }
    return render(request, 'auth_form.html', context)
    
def registe_engineer(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    form = EngineerRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password2'],
            first_name=form.cleaned_data['firstname'],
            last_name=form.cleaned_data['lastname'],
            is_engineer=True
            )
        new_user.save()

        com = Company.objects.filter(name=form.cleaned_data['company'])
        com[0].members.add(new_user)
        new_u = Engineer(user=new_user)
        new_u.alma_mater = form.cleaned_data['alma_mater']
        new_u.contact = form.cleaned_data['contact']
        new_u.about = form.cleaned_data['about']
        new_u.company = form.cleaned_data['company']
        new_u.save()
        
        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        'form': form,
        'page_name': 'Register',
        'button_value': 'Register',
        'links': ['login'],
        }
    return render(request, 'auth_form.html', context)
# Auth Views

def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if next_url is None:
        next_url = '/'
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            messages.success(request, 'Success! Welcome, '
                             + (user.first_name or ''))
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            messages.warning(request, 'Invalid username or password.')

    context = {
        'form': form,
        'page_name': 'Login',
        'button_value': 'Login',
        'links': ['register'],
        }
    return render(request, 'auth_form.html', context)


def auth_logout(request):
    logout(request)
    messages.success(request, 'Success, you are now logged out')
    return render(request, 'index.html')


def auth_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        stu = False
        pro = False
        eng = False
        role = form.cleaned_data['role']
        if role == 'STUDENT':
            stu = True
        elif role == 'TEACHER':
            pro = True
        else:
            eng = True
        print(form.cleaned_data['firstname'])
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password2'],
            first_name=form.cleaned_data['firstname'],
            last_name=form.cleaned_data['lastname'],
            is_student=stu,
            is_professor=pro,
            is_engineer=eng,
            )
        new_user.save()

        uni = University.objects.filter(name=form.cleaned_data['university'])
        uni[0].members.add(new_user)
        
        if new_user.is_student:
            new_u = Student(user=new_user)
            new_u.save()
        elif new_user.is_professor:
            new_u = Teacher(user=new_user)
            new_u.save()
        else:
            new_u = Engineer(user=new_user)
            new_u.save()
        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        'form': form,
        'page_name': 'Register',
        'button_value': 'Register',
        'links': ['login'],
        }
    return render(request, 'auth_form.html', context)


@login_required
def update_profile(request):
    form = UpdateForm(request.POST or None, instance=request.user)
    if request.user.is_student:
        type_form = UpdateFormStudent(request.POST or None, instance=request.user.student)
    elif request.user.is_professor:
        type_form = UpdateFormTeacher(request.POST or None, instance=request.user.teacher)
    else:
        type_form = UpdateFormEngineer(request.POST or None, instance=request.user.engineer)
    if form.is_valid() and type_form.is_valid():
        form.save()
        if request.user.is_student:
            student = request.user.student
            student.contact = type_form.cleaned_data['contact']
            student.about = type_form.cleaned_data['about']
            student.save()
        elif request.user.is_professor:
            teacher = request.user.teacher
            teacher.contact = type_form.cleaned_data['contact']
            teacher.about = type_form.cleaned_data['about']
            teacher.save()
        else:
            engineer = request.user.engineer
            engineer.alma_mater = type_form.cleaned_data['alma_mater']
            engineer.contact = type_form.cleaned_data['contact']
            engineer.about = type_form.cleaned_data['about']
            engineer.save()
        messages.success(request, 'Success, your profile was saved!')

    context = {
        'form': form,
        'type_form': type_form,
        'page_name': 'Update',
        'button_value': 'Update',
        'links': ['logout'],
        }
    return render(request, 'auth_form.html', context)