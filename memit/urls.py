

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_user, name='login'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
	url(r'^deck/(?P<deck_id>\d+)/$', views.deck, name='deck'),
	url(r'^deck/new/$', views.deck_edit, name='deck_new'),
	url(r'^deck/(?P<deck_id>\d)/new_card/$', views.card_new,
		name='deck_card_new'),
	url(r'^card/(?P<card_id>\d+)/review/$', views.card_review,
		name='card_review'),
	
	 url(r'^card/(?P<card_id>\d+)/edit/$', views.card_edit,
		name='card_edit'),
	
	url(r'^card/review_cards_due/$', views.card_review_cards_due,
		name='card_review_cards_due'),
	url(r'^review_stack/next_card/$', views.review_stack_next_card,
		name='review_stack_next_card'),
	url(r'^review_stack/previous_card/$', views.review_stack_previous_card,
		name='review_stack_previous_card'),
	url(r'^deck/(?P<deck_id>\d+)/review_all/$', views.deck_review_all, 
		name='deck_review_all'),
	url(r'^deck/(?P<deck_id>\d+)/review_cards_due/$',
		views.deck_review_cards_due, name='deck_review_cards_due'),
]