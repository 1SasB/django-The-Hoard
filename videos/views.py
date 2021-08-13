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
from .forms import NewVideoForm, CreateHordF,CommentForm,ReplyForm
from django.contrib.auth import update_session_auth_hash,login,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .models import Video, Comment,Reply,Hord
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.conf import settings

from moviepy.editor import *

from PIL import Image

class Home(View):
    template_name = 'videos/home.html'

    def get(self, request):
        # fetch video from DB
        videos = Video.objects.order_by('-date_uploaded')
        for obj in videos:
            obj.natural_updated = naturaltime(obj.date_updated)
            print(obj.path)

        return render(request, self.template_name, {'videos': videos})


class NewVideo(LoginRequiredMixin,View):
    template_name = 'videos/upload.html'
    success_url = reverse_lazy('videos:home')

    def get(self, request):
        # print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            # return HttpResponse('You have to be logged in, in order to upload a video.')
            return HttpResponseRedirect('/account/login')

        form = NewVideoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):  # pass filled out HTML-Form from View to NewVideoForm()
        form = NewVideoForm(request.POST, request.FILES)

        # print(form)
        # print(request.POST)
        # print(request.FILES)
        my_file = request.FILES['path']
        if form.is_valid():
            # create a new Video Entry
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['path']
            # print(file)
            # random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            # path = random_char + file.name

            # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # fs = FileSystemStorage(location=os.path.join(BASE_DIR, '/videos'))
            # fs = FileSystemStorage()
            # filename = fs.save(my_file.name,my_file)
            # file_url = fs.url(filename)
            # print(file_url)
            # heads up, code for thumnail video duration below

            # clip = VideoFileClip(my_file)
            # frame = clip.reader.fps
            # duration = clip.duration
            # print(duration)

            # max_duration = int(duration)+1
            # i = max_duration//2

            # frame = clip.get_frame(i)
            # thumbnail_dir = os.path.join(settings.MEDIA_ROOT,'thumbnails')

            # thumbnail_name = str(random_char)+".jpg"

            # new_thumbnail_file = os.path.join(thumbnail_dir,thumbnail_name)

            # new_thumbnail = Image.fromarray(frame)

            # new_thumbnail.save(new_thumbnail_file)



            
            hord = get_object_or_404(Hord,owner=request.user)
            new_video = Video(title=title,
                              description=description,
                              user=request.user,
                            #   thumbnail=thumbnail_name,
                            #   duration=duration, 
                              path=file,
                              hord=hord
                              )
            new_video.save()
            

            # clip = VideoFileClip(file_url)
            # frame = clip.reader.fps
            # duration = clip.duration
            # print(clip.duration)

            # redirect to detail view template of a Video
            return redirect(self.success_url)
        else:
            messages.info(request, 'Form not valid. Try again')
            return HttpResponse('/upload/')




class VideoView(View):
    template_name = 'videos/video.html'

    def get(self, request, id):
        # fetch video from DB by ID
        video_list = Video.objects.order_by('date_uploaded').exclude(id=id)[:3]
        video_by_id = get_object_or_404(Video,id=id)
        print(video_list)
        context = { 'video': video_by_id, 
                    'video_list': video_list }
        # DoesNotExist
        print(request.user)
        if request.user.is_authenticated:
            print('user signed in')
            comment_form = CommentForm()
            reply_form = ReplyForm()
            context['comment_form'] = comment_form

        comments = Comment.objects.filter(video__id=id).order_by('-date_uploaded')[:5]
        print(comments)
        context['comments'] = comments
        return render(request, self.template_name, context)



class HordPage(View):
    template_name = 'videos/hord_page.html'

    def get(self,request,hord_name):
        hord = get_object_or_404(Hord,Name=hord_name)
        hord_videos = Video.objects.filter(hord=hord)
        ctx = {'hord':hord, 'videos':hord_videos}
        return render(request,self.template_name,ctx)


class HordProfile(LoginRequiredMixin,View):
    template_name = 'videos/hord_page.html'

    def get(self,request):
        hord = get_object_or_404(Hord,owner=request.user)
        hord_videos = Video.objects.filter(hord=hord)

        return render(request,self.template_name)











class Register(View):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('videos:create_hord')

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
        print(request.POST)
        user_name = request.POST.get('username',False)
        print(user_name)
        password = request.POST.get('password1',False)
        print(password)
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