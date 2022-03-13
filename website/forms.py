from django.forms import ModelForm
from .models import User
class userForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'