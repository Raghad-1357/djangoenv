from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'address']


class Student2Form(forms.ModelForm):

    address = forms.ModelMultipleChoiceField(
        queryset = Address2.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
        label = "Address"
    )
    class Meta:
        model = Student2
        fields = ['name', 'age', 'address']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'profile_pic']