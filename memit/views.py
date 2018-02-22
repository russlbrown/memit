from django.shortcuts import render
from .models import Card, Deck


# Create your views here.
def home(request):
	user = request.user
	decks = Deck.objects.filter(owner_id=user.id)
	return render(request, 'home.html', {'decks': decks})


def new_deck(request):
	user = request.user
	