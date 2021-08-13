from django import forms
from django.forms import fields
# from .models import Video, Comment, Reply, Playlist
from .models import Hord,Comment,Reply,Playlist, Video
from django.contrib.auth.models import User


class NewVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','description','path']
    # title = forms.CharField(label='Title', max_length=20)
    # description = forms.CharField(label='Description', max_length=200)
    # file = forms.FileField()

class CreateHordF(forms.ModelForm):

    class Meta:
        model = Hord
        fields = ["Name","description"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['c_text']
    # video = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['r_text']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['Name','description']