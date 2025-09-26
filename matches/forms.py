from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_initial', 'id_number', 'year_section', 'photo', 'e_signature']
