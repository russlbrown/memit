from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..models import Card, Deck

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False,
								 help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False,
								help_text='Optional.')
	email = forms.EmailField(max_length=254,
		help_text='Required. Provide a valid email address.')

	class Meta:
			model = User
			fields = ('username', 'first_name', 'last_name',
				'email', 'password1', 'password2', )


class DeckForm(forms.ModelForm):
	class Meta:
		model = Deck
		fields = ['name']


class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		fields = ['front', 'back', 'stage']