from django.shortcuts import render, redirect
from .forms import userForm
from .models import User
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
    return render(request, 'website/result.html')