from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Room,PageView
from django.contrib.auth.models import User
from django.views.generic import View

@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")
    if(PageView.objects.count()<=0):
        x=PageView.objects.create()
        x.save()
    else:
        x=PageView.objects.all()[0]
        x.hits=x.hits+2
        x.save()

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,'page':x.hits,
    })

from chat.forms import *
def register_page(request):
    if(PageView.objects.count()<=0):
        x=PageView.objects.create()
        x.save()
    else:
        x=PageView.objects.all()[0]
        x.hits=x.hits+2
        x.save()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            return HttpResponseRedirect('/')
    form = RegistrationForm()
    
    return render(request,'registration.html',{'form':form ,'page':x.hits,})