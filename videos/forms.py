from django import forms
from django.forms import fields
# from .models import Video, Comment, Reply, Playlist
from .models import Playlist, Video

from django.contrib.auth.models import User


class NewVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','description','path']
    # title = forms.CharField(label='Title', max_length=20)
    # description = forms.CharField(label='Description', max_length=200)
    # file = forms.FileField()





class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['Name','description']