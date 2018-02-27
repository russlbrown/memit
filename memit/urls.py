

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
	url(r'^card/new/$', views.card_edit, name='card_new'),
	url(r'^card/(?P<card_id>\d+)/$', views.card, name='card'),
]