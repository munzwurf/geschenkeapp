from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^result/$', views.results, name = 'results'),
	url(r'^ajax/next/$', views.next_question, name = 'next_question'),
	]