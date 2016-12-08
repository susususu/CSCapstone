"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render
from django.contrib import messages

from . import models
from . import forms

from AuthenticationApp.models import Student, MyUser

def getCourses(request):
	if request.user.is_authenticated():
		if request.user.is_professor:
			courses_list = models.Course.objects.filter(creator=request.user.email)
			context = {
				'courses' : courses_list,
			}
			return render(request, 'courses.html', context)
		else:
			return render(request, 'typeerror.html')
	return render(request, 'autherror.html')

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def removeStudent(request):
	if not request.user.is_authenticated():
		return render(request, 'autherror.html')
	if not request.user.is_professor:
		return render(request, 'typeerror.html')
	in_university_name = request.GET.get('name', 'None')
	in_university = models.University.objects.get(name__exact=in_university_name)
	in_course_tag = request.GET.get('course', 'None')
	in_course = in_university.course_set.get(tag__exact=in_course_tag)
	user_name = request.GET.get('student', 'None')
	user = MyUser.objects.get(email__exact=user_name)
	in_course.members.remove(user)
	messages.success(request, "Success! You have remove " + user_name + "from " + in_course_tag + '.')
	
	context = {
		'university' : in_university,
		'course' : in_course,
	}
	
	return render(request, 'course.html', context)
	
def studentForm(request):
	if request.user.is_authenticated():
		#in_university_name = request.GET.get('name', 'None')
		in_university_name = request.user.teacher.university
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		context = {
			'university' : in_university,
			'course' : in_course,
		}
		return render(request, 'studentform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')
	
def addStudent(request):
	if not request.user.is_authenticated():
		return render(request, 'autherror.html')
	if not request.user.is_professor:
		return render(request, 'typeerror.html')
	if request.method == 'POST':
		form = forms.StudentForm(request.POST)
		if form.is_valid():
			in_university_name = request.user.teacher.university
			in_university = models.University.objects.get(name__exact=in_university_name)
			email = form.cleaned_data['email']
			student = (MyUser.objects.get(email__exact=email))
			in_course_tag = request.GET.get('course', 'None')
			in_course = models.Course.objects.get(tag__exact=in_course_tag)
			
			context = {
				'university' : in_university,
				'course' : in_course,
			}
			
			if in_course.members.filter(email__exact=form.cleaned_data['email']).exists():
				messages.error(request, email + ' is already in ' + in_course_tag + '.')
				return render(request, 'course.html', context)
			in_course.members.add(student)
			messages.success(request, 'Success! You add ' + email + 'to ' + in_course_tag + '.')
			
			return render(request, 'course.html', context)
		else:
			return render(request, 'index.html')
	else:
		form = forms.CourseForm()
		return render(request, 'courseform.html')
	
def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def getCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		is_member = in_course.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : is_member,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		#in_university_name = request.GET.get('name', 'None')
		in_university_name = request.user.teacher.university
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.CourseForm(request.POST)
			if form.is_valid():
				#in_university_name = request.GET.get('name', 'None')
				in_university_name = request.user.teacher.university
				in_university = models.University.objects.get(name__exact=in_university_name)
				if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
					return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
				new_course = models.Course(tag=form.cleaned_data['tag'],
										   name=form.cleaned_data['name'],
										   description=form.cleaned_data['description'],
										   university=in_university,
										   creator = request.user.email)
				new_course.save()
				in_university.course_set.add(new_course)
				is_member = in_university.members.filter(email__exact=request.user.email)
				context = {
					'university' : in_university,
					'userIsMember': is_member,
				}
				messages.success(request, 'Success! Your class was created.')
				return render(request, 'index.html', context)
			else:
				return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
		else:
			form = forms.CourseForm()
			return render(request, 'courseform.html')
		# render error page if user is not logged in
	return render(request, 'autherror.html')
		
def removeCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		if request.user.email != in_course.creator:
			return render(request, 'typeerror.html')
		in_course.delete()
		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.add(request.user)
		in_course.save();
		request.user.course_set.add(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': True,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')
