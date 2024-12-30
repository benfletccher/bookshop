from django import forms
from isbn_field import ISBNField
from django.contrib.auth.forms import UserCreationForm
from .models import Cadet, Course
import re
from django.core.exceptions import ValidationError

class CreateAccount(UserCreationForm):
    #cadetId = forms.CharField(label="C-Number", max_length=20)
    #firstName = forms.CharField(label="First Name", max_length=50)
    #lastName = forms.CharField(label="Last Name", max_length=50)
    email = forms.EmailField(label="Email")
    company = forms.CharField(label="Company", max_length=50)
    grad_year = forms.IntegerField(label="Graduation Year")

    class Meta:
        model = Cadet
        fields = ['cadet_id', 'first_name', 'last_name', 'email', 'company', 'grad_year', 'password1', 'password2']
        labels = {
            'cadet_id': 'C-Number',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }

class Login(forms.Form):
    cnumber = forms.CharField(label="C-Number", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class NewListing(forms.Form):
    isbn = forms.CharField(label="Enter ISBN-13 with Hyphens", max_length=17)
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2)

class NewBook(forms.Form):
    isbn = forms.CharField(label="Enter ISBN-13 with Hyphens", max_length=17, required=True)
    title = forms.CharField(label="Title", max_length=255)
    author = forms.CharField(label="Author (First M Last)")
    edition = forms.CharField(label="Edition", required=False)
    course = forms.ChoiceField(label="Course")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = [
            (course.course_id, str(course.course_id)) for course in Course.objects.all().order_by('course_id')
        ]
