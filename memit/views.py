from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms.forms import SignUpForm, DeckForm, CardForm
from .models import Card, Deck, ReviewStack


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
    cards_due = len(Card.all_cards_due_for_review(user))
    return render(request, 'home.html', {'decks': decks,
                                         'cards_due': cards_due})


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
        cards_due = len(Deck.cards_due_for_review(user=user, deck=deck))
        return render(request, "deck.html", {'deck': deck, 'cards': cards,
                                             'cards_due': cards_due})
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
def card_new(request, deck_id):
    """ Add a card. """
    user = request.user
    if request.method == "POST" and Deck.objects.get(id=deck_id).owner == user:
        form = CardForm(request.POST)
        if form.is_valid():
            from datetime import datetime
            card = form.save(commit=False)
            card.date_created = datetime.now()
            card.owner = user
            card.is_archived = False
            card.date_stage_started = card.date_created
            if not card.stage:
                card.stage = 0
            card.deck_id = deck_id
            card.save()
            return redirect(f'/deck/{card.deck.id}')
    else:
        form = CardForm()
        return render(request, "card_edit.html", {'form': form})


@login_required
def card_edit(request, card_id):
    """Edit a card"""
    user = request.user
    card = Card.objects.get(id=card_id)
    if user.is_authenticated and card.owner == user:
        if request.method == "POST":
            form = CardForm(request.POST, instance=card)
            if form.is_valid():
                from datetime import datetime
                card = form.save(commit=False)
                # card.is_archived = False
                # card.date_stage_started = card.date_created
                # card.stage = 0
                # card.deck_id = deck_id
                card.save()
                return redirect(f'/deck/{card.deck.id}')
        else:
            form = CardForm(instance=card)
            return render(request, "card_edit.html", {'form': form})
    else:
        message = ("You are not logged in or are not the owner of card " +
                   str(card_id) + '.')
        return render(request, "message.html", {'message': message})


@login_required
def card_review(request, card_id):
    user = request.user
    card = Card.objects.get(id=card_id)
    if user.is_authenticated and card.owner_id == user.id:
        # The user is logged in an the card belongs to them
        review_result = request.GET.get('review_result', '')

        if review_result:
            # Process the result of the card review
            card.process_review_result(review_result)
            # set ReviewStack.last_card_viewed
            try:
                review_stack = ReviewStack.objects.get(owner=user)
                review_stack.card_last_viewed = card_id
                review_stack.save()
            except:
                pass
            return redirect('review_stack_next_card')
        else:
            try:
                review_stack = ReviewStack.objects.get(owner=user)
                review_stack.card_last_viewed = card_id
                review_stack.save()
            except:
                pass
            deck = Deck.objects.get(id=card.deck_id)
            return render(request, "card_review.html", {'card': card, 'deck': deck})
    else:
        message = ("You are not logged in or are not the owner of card " +
                   str(card_id) + '.')
        return render(request, "message.html", {'message': message})


@login_required
def card_review_cards_due(request):
    user = request.user

    # Stop user if they are not logged in.
    if not user.is_authenticated:
        message = ("You are not logged in.")
        return render(request, "message.html", {'message': message})

    cards_due = Card.all_cards_due_for_review(user)
    review_stack = ReviewStack.set(user=user, cards=cards_due)

    message = (f"review stack set: {review_stack.cards}")
    return redirect(review_stack_next_card)


def review_stack_next_card(request):
    """Redirect to the review screen of the next card in ReviewStack.cards."""
    user = request.user
    review_stack = ReviewStack.objects.get(owner=user)
    # figure out which card is the next card
    return redirect(review_stack.next_card_url())


def review_stack_previous_card(request):
    """Redirect to the review screen of the next card in ReviewStack.cards."""
    user = request.user
    review_stack = ReviewStack.objects.get(owner=user)
    # figure out which card is the next card
    return redirect(review_stack.previous_card_url())


@login_required
def deck_review_all(request, deck_id):
    user = request.user
    deck = None
    try:
        deck = Deck.objects.get(id=deck_id, owner=user)
    except:
        pass

    # Stop user if they are not logged in or don't own the deck.
    if not user.is_authenticated or not deck:
        message = ("You aren't logged in, or don't own this deck.")
        return render(request, "message.html", {'message': message})

    cards = Card.objects.filter(deck=deck_id, owner=user)

    # set up the ReviewStack
    review_stack = ReviewStack.set(user=user, cards=cards)
    return redirect('review_stack_next_card')


@login_required
def deck_review_cards_due(request, deck_id):
    user = request.user

    # Stop user if they are not logged in.
    if not user.is_authenticated:
        message = ("You are not logged in.")
        return render(request, "message.html", {'message': message})

    cards = Card.objects.filter(deck=deck_id, owner=user)
    cards_due = []

    for card in cards:
        if card.is_due_for_review():
            cards_due.append(card)

    review_stack = ReviewStack.set(user=user, cards=cards_due)
    return redirect('review_stack_next_card')
