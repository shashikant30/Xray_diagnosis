from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import userForm
from .models import User
from Xray_diagnosis.settings import cnn
import cv2
import numpy as np
import os
# Create your views here.
def userFormView(request):
    if request.method == 'POST':
        form = userForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/result/")  
    else:
        form = userForm()
    return render(request, 'website/userInfo.html', {'form' : form})

def resultView(request):
    categories = ["COVID", "Viral Pneumonia", "Normal"]
    img_array=cv2.imread(os.path.join('D:\B.E\\final project\Xray_diagnosis\media\images',os.listdir('D:\B.E\\final project\Xray_diagnosis\media\images')[-1]))
    new_array = cv2.resize(img_array,(224, 224))
    image = np.expand_dims(new_array, 0)
    a=cnn.predict(image)
    #print(a.argmax())
    #print(categories[a.argmax()])
    result=categories[a.argmax()]
    return render(request, 'website/result.html',{'result':result})


def home(request):
    return render(request, "website/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        return redirect('signin')
        
        
    return render(request, "website/Register.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('userFormView')
            #return render(request, "website/userInfo.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "website/signIn.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')