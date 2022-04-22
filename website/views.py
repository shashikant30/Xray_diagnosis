from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import userForm
from .models import Patient
from Xray_diagnosis.settings import cnn
import cv2
import numpy as np
import os
#name_12=""
#address_12=""
#age_12=0
# Create your views here.
def userFormView(request):
    if request.method == 'POST':
        clear_mediadir() 
        form = userForm(request.POST, request.FILES)
        if form.is_valid():
            form.user =request.user
            name_12=request.POST['Name']
            address_12=request.POST['Address']
            age_12=request.POST['age']
            form.save()
            return redirect("/result")  
    else:
        form = userForm()
    return render(request, 'website/userInfo.html', {'form' : form})

def clear_mediadir():
    media_dir = "D:\B.E\\final project\Xray_diagnosis\media\images"
    for f in os.listdir(media_dir):
        os.remove(os.path.join(media_dir, f))

def previous_uploads(request):
    list = Patient.objects.filter(user=request.user)
    return render(request, "website/history.html",{'list':list})

def resultView(request):
    categories = ["COVID", "Viral Pneumonia", "Normal"]
    img_array=cv2.imread(os.path.join('D:\B.E\\final project\Xray_diagnosis\media\images',os.listdir('D:\B.E\\final project\Xray_diagnosis\media\images')[-1]))
    os.rename(os.path.join('D:\B.E\\final project\Xray_diagnosis\media\images',os.listdir('D:\B.E\\final project\\Xray_diagnosis\\media\\images')[-1]), 'D:\\B.E\\final project\\Xray_diagnosis\\media\\images\\ip_img.png')
    new_array = cv2.resize(img_array,(224, 224))
    image = np.expand_dims(new_array, 0)
    a=cnn.predict(image)
    #print(a.argmax())
    #print(categories[a.argmax()])
    result=categories[a.argmax()]
    return render(request, 'website/result.html',{'result':result})


def home(request):
    return render(request, "website/index.html")


def home1(request):
    return render(request, "website/home.html")

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
        myuser.is_active = True
        myuser.save()
        
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
            return redirect('home')
            #return render(request, "website/userInfo.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            #return redirect('userFormView')
            return redirect('home')
    
    return render(request, "website/signIn.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')