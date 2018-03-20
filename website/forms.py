from django import forms

from .models import *

class HelpRequestForm(forms.ModelForm):
	class Meta:
		model = HelpRequest
		fields = ['name', 'email', 'organization', 'problem']
