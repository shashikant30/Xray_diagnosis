from django.forms import ModelForm
from .models import Patient
class userForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['Name','Address','age','Xray_image']