from django.db import models
from django.utils import timezone

# Create your models here.
class Card(models.Model):
	#row_id = models.AutoField(primary_key=True)
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
		return f"{self.id}: {self.front[0:32]}"

	def get_absolute_url(self):
		"""https://docs.djangoproject.com/en/2.0/ref/models/instances/#django.db.models.Model.get_absolute_url"""
		return "/card/%s" % self.id

	def in_deck(deck):
		return Cards.objects.filter(deck_id=deck.id)

class Deck(models.Model):
	name = models.CharField(max_length=200)
	date_created = models.DateTimeField()
	owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	#cards = Card.objects.filter(deck_id=self.id)

	def __str__(self):
		return f"{self.id}: {self.name}"

	def get_absolute_url(self):
		"""https://docs.djangoproject.com/en/2.0/ref/models/instances/#django.db.models.Model.get_absolute_url"""
		return "/deck/%s" % self.id