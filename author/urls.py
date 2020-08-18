from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$',views.showauthor),
	url(r'^(?P<nidn>[0-9]{10})/$', views.show_detailauthor),
	url(r'^SVG/$',views.SVG),
	url('ajax/',views.AjaxHandlerView.as_view()),
	# url(r'^coba/$',views.coba),
]