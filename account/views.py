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
from .forms import CreateHordF
from django.contrib.auth import update_session_auth_hash,login,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .models import Subscribers,Hord
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.conf import settings

from moviepy.editor import *

from PIL import Image
# from videos.models import Video
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from django.apps import apps
Video = apps.get_model('videos','Video')
# account_models = apps.get_model('account')
# Create your views here.


class HordPage(View):
    template_name = 'videos/hord_page.html'

    def get(self,request,hord_name):
        hord = get_object_or_404(Hord,Name=hord_name)
        hord_videos = Video.objects.filter(hord=hord)
        ctx = {'hord':hord, 'videos':hord_videos}
        return render(request,self.template_name,ctx)


class HordProfile(LoginRequiredMixin,View):
    template_name = 'videos/hord_profile.html'

    def get(self,request):
        print(request.user)

        hord = get_object_or_404(Hord,owner=request.user)
        hord_videos = Video.objects.filter(hord=hord)
        ctx ={'videos': hord_videos}
        return render(request,self.template_name,ctx)

@method_decorator(csrf_exempt, name='dispatch')
class AddSubscribeView(LoginRequiredMixin,View):
    def post(self,request, pk):
        print("About to Add subscribe for video PK",pk)
        hord = get_object_or_404(Hord, id=pk)


        subs = Subscribers(user=request.user, hord=hord)
        try:
            subs.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class RemoveSubscribeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("About to delete subscribe for video PK",pk)
        hord = get_object_or_404(Hord, id=pk)
        try:
            Dlik = Subscribers.objects.get(user=request.user, hord=hord).delete()
        except Subscribers.DoesNotExist as e:
            pass

        return HttpResponse()


class Register(View):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:create_hord')

    def get(self,request):
        user_form = UserCreationForm()
        context = {'form':user_form}
        return render(request,self.template_name,context)

    def post(self,request):
        user_form = UserCreationForm(request.POST)
        if not user_form.is_valid():
            ctx = {'form': user_form}
            return render(request, self.template_name, ctx)

        user_form.save()
        user_name = request.POST.get('username',False)
        password = request.POST.get('password1',False)
        user = authenticate(request,username=user_name,password=password)
        if user is not None:
            login(request,user)
            return redirect(self.success_url)



class CreateHord(LoginRequiredMixin,View):
    template_name = 'videos/create_hord.html'
    success_url = reverse_lazy('videos:home')

    def get(self,request,pk=None):
        hord_form = CreateHordF()
        context = {'hord_form':hord_form}
        return render(request,self.template_name,context)

    def post(self,request,pk=None):
        hord_form = CreateHordF(request.POST)
        if not hord_form.is_valid():
            ctx = {'hord_form': hord_form}
            return render(request, self.template_name, ctx)
        hord = hord_form.save(commit=False)
        hord.owner = self.request.user
        hord.save()
        return redirect(self.success_url) 