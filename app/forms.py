from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
my_choices = [('1', "admin"), ('2', "student"),
           ('3', "teacher"), ('4', "parent")]
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email" )
    username = forms.CharField(label="Username" )
    name = forms.CharField(label="First name" )
    user_type = forms.ChoiceField(choices=my_choices)
    class Meta:
        model = User
        fields = ("user_name", "name", "email","user_type")


