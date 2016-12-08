from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from . import models

class ProjectForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput, required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    
    all_PLRequired = models.PLRequired.objects.all()
    required1 = forms.ChoiceField(choices=[(x, x) for x in all_PLRequired])
    all_YoERequired = models.YoERequired.objects.all()
    required2 = forms.ChoiceField(choices=[(x, x) for x in all_YoERequired])
    all_Speciality = models.Speciality.objects.all()
    required3 = forms.ChoiceField(choices=[(x, x) for x in all_Speciality])
    
class UpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput, required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    
    all_PLRequired = models.PLRequired.objects.all()
    required1 = forms.ChoiceField(choices=[(x, x) for x in all_PLRequired])
    all_YoERequired = models.YoERequired.objects.all()
    required2 = forms.ChoiceField(choices=[(x, x) for x in all_YoERequired])
    all_Speciality = models.Speciality.objects.all()
    required3 = forms.ChoiceField(choices=[(x, x) for x in all_Speciality])
    class Meta:
        model = models.Project
        fields = ('name', 'description')