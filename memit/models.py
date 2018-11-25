from django.db import models
from django.utils import timezone
from datetime import datetime
from .settings import REVIEW_STAGE


# Create your models here.
class Card(models.Model):
    # row_id = models.AutoField(primary_key=True)
    front = models.TextField()
    back = models.TextField(blank=True, null=True)
    hint = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_stage_started = models.DateTimeField(default=timezone.now)
    stage = models.IntegerField()
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    deck = models.ForeignKey('Deck', on_delete=models.CASCADE)

    def __str__(self):
        length = 32
        ellipses = ""
        if len(self.front) > length:
            ellipses = "..."
        return f"{self.front[0:length]}{ellipses}"

    def get_absolute_url(self):
        """https://docs.djangoproject.com/en/2.0/ref/models/instances/#django.db.models.Model.get_absolute_url"""
        return "/card/%s" % self.id

    def process_review_result(self, result):
        if result == 'pass':
            # update date of last review and advance to next stage
            if self.is_due_for_review():
                self.date_stage_started = datetime.now()
                self.stage += 1
            else:
                pass
        elif result == 'fail':
            # go back a review stage so the user will review it sooner.
            if self.stage > 0:
                self.date_stage_started = datetime.now()
                self.stage -= 1
        else:
            raise ValueError(f"Invalid review result \"{result}\".")

        self.save()
        return None

    def is_due_for_review(self):
        import pytz
        delta = (timezone.now() - self.date_stage_started).days
        if delta >= REVIEW_STAGE[self.stage]:
            return True
        else:
            return False

    @staticmethod
    def all_cards_due_for_review(user):
        """Returns all of a user's cards that are due for review."""
        cards = Card.objects.filter(owner=user).order_by('deck', 'front')
        # Get a list of the cards due for review
        cards_due = []
        for card in cards:
            if card.is_due_for_review():
                cards_due.append(card)
        return cards_due


class Deck(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # cards = Card.objects.filter(deck_id=self.id)

    def __str__(self):
        return f"{self.id}: {self.name}"

    def get_absolute_url(self):
        """https://docs.djangoproject.com/en/2.0/ref/models/instances/#django.db.models.Model.get_absolute_url"""
        return "/deck/%s" % self.id

    def cards_due_for_review(self, user):
        """Returns all of a user's cards that are due for review."""
        cards = Card.objects.filter(owner=user, deck=self).order_by('front')
        # Get a list of the cards due for review
        cards_due = []
        for card in cards:
            if card.is_due_for_review():
                cards_due.append(card)
        return cards_due


class ReviewStack(models.Model):
    """This is a stack of cards that the user is currently reviewing"""
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE,
                                 unique=True)
    cards = models.TextField(null=True, blank=True)
    # cards will hold a comma separated list of card ids.
    card_last_viewed = models.IntegerField(null=True, blank=True)

    def set(user, cards):
        """populate the review stack with the user.id and cards"""
        card_ids = ""
        for card in cards:
            card_ids += str(card.id) + ", "

        # if ReviewStack already exists, update it, otherwise create one.
        try:
            review_stack = ReviewStack.objects.get(owner=user)
            review_stack.cards = card_ids
        except:
            review_stack = ReviewStack(owner=user, cards=card_ids)

        review_stack.card_last_viewed = None
        review_stack.save()

        return review_stack

    def next_card_url(self):
        """ Return the URL of the next card review i.e. /card/<card_id>/review/
		
		If there is no next card return URL /home/.
		If card_last_viewed == Null or is not in the ReviewStack,
		return the review url of the first card in the stack.
		"""
        # Convert the cards string to a list for ease of use.
        import ast
        cards = ast.literal_eval(self.cards)

        current_card = self.card_last_viewed
        current_card_found = False
        next_card = None

        if cards:
            if not current_card:
                # The user hasn't viewed any cards yet.
                return f'/card/{cards[0]}/review/'
            else:
                for card in cards:
                    if current_card_found:
                        next_card = card
                        break
                    if card == current_card:
                        current_card_found = True

                if current_card_found and next_card:
                    # Things worked as expected. Return URL of next_card
                    return f'/card/{next_card}/review/'
                elif current_card_found and not next_card:
                    # There are no more cards in the ReviewStack.
                    return f'/home/'
                else:
                    # The current_card was not in the ReviewStack.
                    return f'/card/{cards[0]}/review/'
        else:
            return '/home/'

    def previous_card_url(self):
        """ Return the URL of the prev card review i.e. /card/<card_id>/review/
		
		If there is no prev card return URL /deck/<deck_id of current card>.
		If card_last_viewed == Null or is not in the ReviewStack,
		return the review url of the first card in the stack.
		"""
        # Convert the cards string to a list for ease of use.
        import ast
        cards = ast.literal_eval(self.cards)

        current_card = self.card_last_viewed
        current_card_found = False
        prev_card = None

        if cards:
            if not current_card:
                # The user hasn't viewed any cards yet.
                return f'/home/'
            else:
                for card in cards:
                    if card == current_card:
                        current_card_found = True
                        break
                    prev_card = card

                if current_card_found and prev_card:
                    # Things worked as expected. Return URL of prev_card
                    return f'/card/{prev_card}/review/'
                elif current_card_found and not prev_card:
                    # There are no more cards in the ReviewStack.
                    return f'/home/'
                else:
                    # The current_card was not in the ReviewStack.
                    return f'/card/{cards[0]}/review/'
        else:
            return '/home/'
