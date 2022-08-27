
from django import forms
from django.forms import fields

from .models import Hord
class CreateHordF(forms.ModelForm):

    class Meta:
        model = Hord
        fields = ["Name","description"]
