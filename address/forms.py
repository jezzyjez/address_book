from django import forms
from .models import PersonalInfo

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ('first_name', 'last_name', 'address', 'contact_number')
