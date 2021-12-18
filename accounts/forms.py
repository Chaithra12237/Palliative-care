from .models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

class AddServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['category']

class PublicUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','password1','password2']

class UserSignUpForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'mob','sex','house','street1','street2','city','district','state','pin']

class ProviderSignUpForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'mob','sex','house','street1','street2','city','district','state','pin','organization','document']

class AddSubProductForm(ModelForm):
    count = forms.CharField(required=False)
    class Meta:
        model = SubProduct
        fields = ['name', 'count','cost','details']

class AddReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['message']

class AdminProfileEditForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name','email','mob','sex']

class ServiceProviderProfileEditForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name','email','mob','organization','house','street1','street2','city','district','state','pin','age','sex']

class PublicProfileEditForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name','email','mob','house','street1','street2','city','district','state','pin','age','sex']

class UpdatePic(ModelForm):
    class Meta:
        model = Users
        fields = ['profile_picture']

class AdminMessageForm(ModelForm):
    class Meta:
        model = AdminMessage
        fields = ['message']

