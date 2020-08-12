from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$',views.showauthor),
	url(r'^(?P<nidn>[0-9]{10})/$', views.show_detailauthor),
]