from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$',views.showtopic),
    url(r'^(?P<id_topic>[0-9]+)/$', views.show_detailtopic),
]