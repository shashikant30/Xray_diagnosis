from django.shortcuts import render, redirect
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
