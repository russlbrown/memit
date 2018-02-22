

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^deck/new$', views.new_deck, name='new_deck')
]