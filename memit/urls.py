

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_user, name='login'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
	url(r'^deck/new/$', views.new_deck, name='new_deck'),
]