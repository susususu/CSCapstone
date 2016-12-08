"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from . import models
from . import forms
from CompaniesApp.models import Company
from datetime import datetime
from django.contrib import messages

def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
    in_project_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_project_name)
    bookmarked = False
    if models.BookMark.objects.filter(user=request.user).filter(project=in_project).exists():
        bookmarked = True
    context = {
        'project' : in_project,
        'flag' : bookmarked
    }
    return render(request, 'project.html', context)

def updateProject(request):
    in_project_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_project_name)
    
    form = forms.UpdateForm(request.POST or None, instance=in_project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, your project was saved!')
    context = {
        'project' : in_project,
        'form': form
    }
    return render(request, 'update.html', context)

def markProject(request):
    in_project_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_project_name)
    bm = models.BookMark(user=request.user, project=in_project, name=request.user.email)
    bm.save()
    bookmarked = False
    if models.BookMark.objects.filter(user=request.user).filter(project=in_project).exists():
        bookmarked = True
    context = {
        'project' : in_project,
        'flag' : bookmarked
    }
    return render(request, 'project.html', context)
    
def unmarkProject(request):
    in_project_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_project_name)
    models.BookMark.objects.filter(user=request.user).filter(project=in_project).delete()
    bookmarked = False
    if models.BookMark.objects.filter(user=request.user).filter(project=in_project).exists():
        bookmarked = True
    context = {
        'project' : in_project,
        'flag' : bookmarked
    }
    return render(request, 'project.html', context)
    
def bookmarks(request):
    bm = models.BookMark.objects.filter(name=request.user.email)
    context = {
        'bm' : bm
    }
    return render(request, 'mybookmarks.html', context)
    
def deleteProject(request):
    projects_list = models.Project.objects.all()
    in_project_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_project_name)
    if request.user.engineer.company != in_project.company.name:
        messages.error(request, "You are not allowed to do this.")
        return render(request, 'projects.html', {
        'projects': projects_list,
    })
    in_project.delete()
    return render(request, 'projects.html', {
        'projects': projects_list,
    })
    
def projectForm(request):
    if not request.user.is_engineer:
        return render(request, 'typeerror.html')
    projects_list = models.Project.objects.all()
    form = forms.ProjectForm(request.POST or None)
    if form.is_valid():
        in_company_name = request.user.engineer.company
        in_company = Company.objects.get(name=in_company_name)
        re1 = models.PLRequired.objects.get(name=form.cleaned_data['required1'])
        re2 = models.YoERequired.objects.get(name=form.cleaned_data['required2'])
        re3 = models.Speciality.objects.get(name=form.cleaned_data['required3'])
        pro = models.Project(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            company = in_company,
            created_at = datetime.now(),
            updated_at = datetime.now(),
            r1 = models.PLRequired.objects.get(name=form.cleaned_data['required1']),
            r2 = models.YoERequired.objects.get(name=form.cleaned_data['required2']),
            r3 = models.Speciality.objects.get(name=form.cleaned_data['required3']),
        )
        pro.save()
        pro.PLRequirement = re1
        pro.YoERequirement = re2
        pro.SpecialityRequirement = re3
        return render(request, 'projects.html', {
            'projects': projects_list,
        })
    else:
        context = {
            'form': form
        }
        return render(request, 'projectform.html', context)
