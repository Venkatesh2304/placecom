from typing import Any
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User,Student,Signed,IAF
from django.contrib import messages
from django import forms

# Views
@login_required
def home(request):
    return render(request, "registration/success.html", {})

@login_required
def get_resume(request) :
    return FileResponse( request.user.student.resume )

from django import forms
from django.views.generic.edit import FormView

class StudentForm(forms.ModelForm) : 
    class Meta : 
        model = Student
        fields = "__all__"
        exclude = ["user"]


class StudentFormView(FormView):
    template_name = "student_form.html"
    form_class = StudentForm
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
     
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user 
            instance.save()
            return ""
        else:
            return self.form_invalid(form)



class UserForm(forms.Form) : 
      email = forms.EmailField(max_length=20) 
      password = forms.CharField(max_length=20)

def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            if User.objects.filter( email = email ).count() > 0 : 
               messages.error(request,'Email Already Exists')
               return redirect("register")
            user = User.objects.create( email = email )
            user.set_password(raw_password=password)
            user.save() 
            user = authenticate( username = email , password = password )
            login(request, user)
            return redirect("home")
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form } )

def login_view(request) : 
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate( username = email , password = password )
            if user is None : 
               messages.error(request,"Email or password is incorrect")
               return redirect("login")
            login(request, user)
            return redirect("home")
    else:
        form = UserForm()
    return render(request, 'registration/login.html', {'form': form } )