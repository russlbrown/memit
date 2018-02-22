from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import Card, Deck



# Create your views here.
def index(request):
	# if user is logged in return home.html
	if request.user.is_authenticated:
		return redirect('home')
	# if user is not logged in return login.html
	else:
		return redirect('login')

def home(request):
	user = request.user
	if not user.is_authenticated:
		return render(request, 'message.html',
			{'message': "you are not logged in"})
		
	decks = Deck.objects.filter(owner_id=user.id)
	return render(request, 'home.html', {'decks': decks})


def login_user(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			return redirect('home')
		else:
			message = "Invalid username or password"
			return render(request, 'message.html', {'message': message})
	form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})


def signup(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})


def new_deck(request):
	user = request.user


def logout(request):
	from django.contrib.auth import logout
	
	if request.user.is_authenticated:
		logout(request)
		return render(request, 'message.html',
				{'message': "You logged out successfully."})
	else:
		return render(request, 'message.html',
			{'message': 'You were already logged out'})
