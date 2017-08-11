from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from .forms import UserForm
from django.views.generic import View

@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })
class UserFormView(View):
    form_class = UserForm
    template_name = "registration.html"
    #to render empty form
    def get(self,request):
        form =self.form_class(None)
        return render(request,self.template_name,{'form':form})
    #To save data in the database
    def post(self,request):
        form =self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            #normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username = username , password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("chat:index")