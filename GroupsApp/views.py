"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.contrib import messages

from . import models
from . import forms

from AuthenticationApp.models import MyUser
from CommentsApp.models import Comment
from CommentsApp.forms import CommentForm

def addComment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            in_name = request.GET.get('group', 'None')
            in_group = models.Group.objects.get(name__exact=in_name)
            new_comment = Comment(comment=form.cleaned_data['comment'], group=in_group)
            new_comment.save()
            comments_list = Comment.objects.filter(group=in_group)
            context = {
                'comments' : comments_list,
                'group' : in_group,
            }
            return render(request, 'group.html', context)
        else:
            form = CommentForm()
    return render(request, 'newComments.html')

from datetime import datetime
    
def removeComment(request):
    at_time = request.GET.get('time', 'None')
    in_name = request.GET.get('name', 'None')
    in_group = models.Group.objects.get(name__exact=in_name)
    datetime_object = datetime.strptime(at_time, '%b %d, %Y, %I:%M %p')
    Comment.objects.filter(time=datetime_object).filter(user=request.user).delete()
    comments_list = Comment.objects.filter(group=in_group)
    context = {
        'comments' : comments_list,
        'group' : in_group,
    }
    return render(request, 'group.html', context)

def getMyGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        print(groups_list)
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def memberForm(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'memberform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addMember(request):
    if not request.user.is_authenticated():
        return render(request, 'autherror.html')
    if request.method == 'POST':
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            in_name = request.GET.get('name', 'None')
            in_group = models.Group.objects.get(name__exact=in_name)
            email = form.cleaned_data['email']
            student = (MyUser.objects.get(email__exact=email))
                
            context = {
                'group' : in_group,
            }
            if not student.is_student:
                messages.error(request, email + ' is not a Student.')
                return render(request, 'group.html', context)
            if in_group.members.filter(email__exact=form.cleaned_data['email']).exists():
                messages.error(request, email + ' is already in ' + in_name + '.')
                return render(request, 'group.html', context)
            in_group.members.add(student)
            messages.success(request, 'Success! You add ' + email + 'to ' + in_name + '.')

            return render(request, 'group.html', context)
        else:
            return render(request, 'index.html')
    else:
        form = forms.CourseForm()
        return render(request, 'studentform.html')

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        comments = Comment.objects.filter(group=in_group)
        context = {
            'comments' : comments,
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                new_group.members.add(request.user)
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        if not in_group.members.all().exists():
            models.Group.objects.get(name__exact=in_name).delete()
            return render(request, 'index.html')
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    