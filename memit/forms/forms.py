from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from ..models import Card, Deck


class SignUpForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False,
    #							 help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False,
    #							help_text='Optional.')
    email = forms.EmailField(max_length=254,
        help_text='Required. Provide a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder': 'Your email address'}))

    username = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Pick a username'}))


    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
            model = User
            fields = ('username', #'first_name', 'last_name',
                'email', 'password1', 'password2', )


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['front', 'back']