from .models import Users, Support
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput

class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ["name", "email", "password"]
        widgets = {
            "name": TextInput(attrs={"class": "form_el", "placeholder": "Login"}),
            "email": EmailInput(attrs={"class": "form_el", "placeholder": "Email"}),
            "password": PasswordInput(attrs={"class": "form_el", "placeholder": "Password"})
        }
    
class UsersLogin(ModelForm):
     class Meta:
        model = Users
        fields = ["name", "password"]
        widgets = {
            "name": TextInput(attrs={"class": "form_el", "placeholder": "Login"}),
            "password": PasswordInput(attrs={"class": "form_el", "placeholder": "Password"})
        }

class SupportForm(ModelForm):
     class Meta:
        model = Support
        fields = ["name", "email", "problem"]
        widgets = {
            "name": TextInput(attrs={"class": "form_el", "placeholder": "Name"}),
            "email": EmailInput(attrs={"class": "form_el", "placeholder": "Email"}),
            "problem": TextInput(attrs={"class": "form_problem", "placeholder": ""})
        }