from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms.forms import SignUpForm, DeckForm, CardForm
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
	if request.POST:
		logout(request)
		username = password = ''
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


def logout(request):
	from django.contrib.auth import logout
	
	if request.user.is_authenticated:
		logout(request)
		return render(request, 'message.html',
				{'message': "You logged out successfully."})
	else:
		return render(request, 'message.html',
			{'message': 'You were already logged out'})


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


def deck(request, deck_id):
	user = request.user
	deck = Deck.objects.get(id=deck_id)
	if user.is_authenticated and deck.owner_id == user.id:
		# The user is logged in an the deck belongs to them
		cards = Card.objects.filter(deck_id=deck_id)
		return render(request, "deck.html", {'deck': deck, 'cards': cards})
	else:
		message = ("You are not logged in or are not the owner of deck " +
				   str(deck_id) + '.')
		return render(request, "message.html", {'message': message})

@login_required
def deck_edit(request):
	""" Add or edit a deck. """
	user = request.user
	if request.method == "POST":
		form = DeckForm(request.POST)
		if form.is_valid():
			from datetime import datetime
			deck = form.save(commit=False)
			deck.date_created = datetime.now()
			deck.owner = user
			deck.save()
			return redirect('home')
	else:
		form = DeckForm()
		return render(request, "deck_edit.html", {'form': form})


@login_required
def card_edit(request):
	""" Add or edit a card. """
	user = request.user
	if request.method == "POST":
		form = CardForm(request.POST)
		if form.is_valid():
			from datetime import datetime
			card = form.save(commit=False)
			card.date_created = datetime.now()
			card.owner = user
			card.is_archived = False
			card.date_stage_started = card.date_created
			card.stage = 0
			card.save()
			return redirect(f'/deck/{card.deck.id}')
	else:
		form = CardForm()
		return render(request, "card_edit.html", {'form': form})


def card(request, card_id):
	user = request.user
	card = Card.objects.get(id=card_id)
	if user.is_authenticated and card.owner_id == user.id:
		# The user is logged in an the card belongs to them
		return render(request, "card.html", {'card': card})
	else:
		message = ("You are not logged in or are not the owner of card " +
				   str(card_id) + '.')
		return render(request, "message.html", {'message': message})

