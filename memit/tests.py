from django.test import TestCase
import unittest
from .models import Card
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from .settings import REVIEW_STAGE


# Create your tests here.
class CardTestCase(TestCase):
    def setUp(self):
        Card.objects.create(id=123, front='Test front', back='test_back',
                            hint='test hint',
                            date_created=datetime(2018, 3, 1, 8, 15, 12, 0, pytz.UTC),
                            is_archived=False, owner_id=1, stage=3, deck_id=2)

        Card.objects.create(id=0, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=timezone.now(),
                            is_archived=False, owner_id=1, stage=0, deck_id=2)

        Card.objects.create(id=10, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=(timezone.now()
                                                - timedelta(days=(REVIEW_STAGE[1] - 1))),
                            is_archived=False, owner_id=1, stage=1, deck_id=2)
        Card.objects.create(id=11, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=(timezone.now()
                                                - timedelta(days=(REVIEW_STAGE[1]))),
                            is_archived=False, owner_id=1, stage=1, deck_id=2)

        Card.objects.create(id=20, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=(timezone.now()
                                                - timedelta(days=(REVIEW_STAGE[2] - 1))),
                            is_archived=False, owner_id=1, stage=2, deck_id=2)
        Card.objects.create(id=21, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=(timezone.now()
                                                - timedelta(days=(REVIEW_STAGE[2]))),
                            is_archived=False, owner_id=1, stage=2, deck_id=2)

        Card.objects.create(id=30, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=(timezone.now()
                                                - timedelta(days=(REVIEW_STAGE[3] - 1))),
                            is_archived=False, owner_id=2, stage=3, deck_id=2)
        Card.objects.create(id=31, front='Test front', back='test_back',
                            hint='test hint',
                            date_stage_started=(timezone.now()
                                                - timedelta(days=(REVIEW_STAGE[3]))),
                            is_archived=False, owner_id=2, stage=3, deck_id=2)

    def test_recall(self):
        card = Card.objects.get(id=123)
        assert card.id == 123
        assert card.front == "Test front"
        assert card.back == "test_back"
        assert card.hint == "test hint"
        assert card.date_created == datetime(2018, 3, 1, 8, 15, 12, 0, pytz.UTC)
        assert card.is_archived == False
        assert card.owner_id == 1
        assert card.deck_id == 2
        assert card.stage == 3

    def test_is_due_for_review(self):
        card0 = Card.objects.get(id=0)
        card10 = Card.objects.get(id=10)
        card11 = Card.objects.get(id=11)
        card20 = Card.objects.get(id=20)
        card21 = Card.objects.get(id=21)
        card30 = Card.objects.get(id=30)
        card31 = Card.objects.get(id=31)

        assert card0.is_due_for_review()
        assert not card10.is_due_for_review()
        assert card11.is_due_for_review()
        assert not card20.is_due_for_review()
        assert card21.is_due_for_review()
        assert not card30.is_due_for_review()
        assert card31.is_due_for_review()

    def test_all_cards_due_for_review(self):
        cards_due = Card.all_cards_due_for_review(user=1)
        cards = [Card.objects.get(id=0), Card.objects.get(id=11),
                 Card.objects.get(id=21)]
        assert cards_due == cards

    def test_process_review_result(self):
        card10 = Card.objects.get(id=10)
        card11 = Card.objects.get(id=11)
        card20 = Card.objects.get(id=20)
        card21 = Card.objects.get(id=21)

        card10.process_review_result('pass')
        card11.process_review_result('pass')
        card20.process_review_result('fail')
        card21.process_review_result('fail')

        assert card10.stage == 1
        assert card11.stage == 2
        assert card20.stage == 1
        assert card21.stage == 1

        self.assertRaises(ValueError, card10.process_review_result, 'banana')

    def test_delete(self):
        card10 = Card.objects.get(id=10)
        card10.delete()

        assert (card10 is None)
