from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class MapBounds(forms.Form):
    south = forms.CharField()
    north = forms.CharField()
    east = forms.CharField()
    west = forms.CharField()
