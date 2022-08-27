from django.shortcuts import render
import random
import string
import os
from wsgiref.util import FileWrapper
# from videos.owner import OwnerListView,OwnerCreateView,OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy,reverse
# from .forms import NewVideoForm, CreateHordF,CommentForm,ReplyForm
from django.contrib.auth import update_session_auth_hash,login,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .models import VidLikes,VidDislikes
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.conf import settings

from moviepy.editor import *
from django.apps import apps


Video = apps.get_model('videos','Video')


from PIL import Image
# Create your views here.



from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("About to Add like for video PK",pk)
        t = get_object_or_404(Video, id=pk)

        already_disliked = VidDislikes.objects.filter(user=request.user, video=t).exists()
        if already_disliked:
            print("The video was disliked already, Deleting dislike ....")

            VidDislikes.objects.get(user=request.user, video=t).delete()

            print("DisLike Deleted")

        lik = VidLikes(user=request.user, video=t)
        try:
            lik.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteLikeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("About to delete like for video PK",pk)
        t = get_object_or_404(Video, id=pk)
        try:
            lik = VidLikes.objects.get(user=request.user, video=t).delete()
        except VidLikes.DoesNotExist as e:
            pass

        return HttpResponse()

# Dislike Functionality
@method_decorator(csrf_exempt, name='dispatch')
class AddDisLikeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        t = get_object_or_404(Video, id=pk)
        already_liked = VidLikes.objects.filter(user=request.user, video=t).exists()
        if already_liked:
            print("The video was liked already, Deleting like ....")

            VidLikes.objects.get(user=request.user, video=t).delete()

            print("Like Deleted")
        
        Dlike =  VidDislikes(user=request.user, video=t)
        print("Adding Dislike")
        try:
            Dlike.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteDisLikeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("About to delete dislike for video PK",pk)
        t = get_object_or_404(Video, id=pk)
        try:
            Dlik = VidDislikes.objects.get(user=request.user, video=t).delete()
        except VidLikes.DoesNotExist as e:
            pass

        return HttpResponse()
