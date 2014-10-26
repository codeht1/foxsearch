from django import forms
from .models import Searchreq

class SearchForm(forms.Form):
	email = forms.EmailField()
	query = forms.CharField(label='Query', max_length=200)

class SearchreqForm(forms.ModelForm):
	class Meta:
		model = Searchreq
		fields = ["email","query",]

#class ResultForm(forms.Form):
#	result = forms.CharField(label='Result')
