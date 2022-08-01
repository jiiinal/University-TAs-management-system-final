from django.forms import ModelForm
from django import forms
from django.forms.widgets import DateInput, TextInput
from .models import *


class addstudent(forms.ModelForm):
    class Meta:
        model=student
        fields = '__all__'

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
        #print(self.fields['cid'].widget.attrs['size'])
        #self.fields['cid'].widget.attrs['width']=50

class addcourse(forms.ModelForm):

    class Meta:
        model=course
        fields = '__all__'

class addfaculty(forms.ModelForm):

    class Meta:
        model=faculty
        exclude = ('an',)

class addta(forms.ModelForm):

    class Meta:
        model=ta
        exclude= ('cid','star','status','an',)

class allocateta(forms.ModelForm):

    class Meta:
        model=ta
        fields = ['cid']
