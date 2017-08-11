from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import index,register_page
	

app_name= "multichat"

urlpatterns = [url(r'^home/$', index),
    url(r'^$', index),
    url(r'^register/$', register_page),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout,{'next_page': '/home/'}),
    url(r'^admin/', admin.site.urls),
]
