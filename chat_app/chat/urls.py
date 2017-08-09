from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.views import login,logout
from chat.views import index
urlpatterns = [
	url(r'^$', index, name ='homepage'),
	url(r'^accounts/login/$',login,name ='login'),
	url(r'^accounts/logout/$',logout,name ='logout'),
	]
	
