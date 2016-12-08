from django.shortcuts import render

from . import models
from . import forms

# Create your views here.
def getComments(request):
    comments_list = models.Comment.objects.all()
    context = {
        'comments' : comments_list,
    }
    return render(request, 'newComments.html', context)
	
def getCommentForm(request):
    return render(request, 'commentForm.html')
	
def addComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            in_name = request.GET.get('group', 'None')
            in_group = models.Group.objects.get(name__exact=in_name)
            new_comment = models.Comment(comment=form.cleaned_data['comment'], group=in_group, user=request.user)
            new_comment.save()
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : comments_list,
            }
            return render(request, 'newComments.html', context)
        else:
            form = forms.CommentForm()
    return render(request, 'newComments.html')
