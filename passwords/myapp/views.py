from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,User_profile_form
from .models import User_profile_info
from  django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'html/index.html')

@login_required
def special(request):
    return HttpResponse("you are logged in, great!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def registration(request):
    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=User_profile_form(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=User_profile_form()

    return render(request,'html/registration.html',context={'user_form':user_form,
                                                    'profile_form':profile_form,'registered':registered })
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                print("USER IS NOT ACTIVE")
        else:
            print("someone tired to login and failed")
            print("usernam:{} and password:{}",format(username,password))
            return HttpResponse("invalid login details supplied ")

    else:
        return render(request,"html/login.html")



