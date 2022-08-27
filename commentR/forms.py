
from django import forms
from django.forms import fields
# from .models import Video, Comment, Reply, Playlist
from .models import Comment,Reply

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['c_text']
    # video = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['r_text']