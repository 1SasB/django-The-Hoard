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
from .models import Subscribers, VidLikes,VidDislikes, Video, Comment,Reply,Hord
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
        print("im here")
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



            print("im here")
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
            print(new_video.pk)

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
        comments = Comment.objects.filter(video=video_by_id).order_by('-date_uploaded')

        if request.user.is_authenticated:

            like_rows = request.user.video_likes.values('id')
            likes = [row['id'] for row in like_rows]
            

            dislike_rows = request.user.video_dislikes.values('id')
            dislikes = [row['id'] for row in dislike_rows]
            

            subsc_rows = request.user.hoard_subscribers.values('id')
            subscribers = [row['id'] for row in subsc_rows]

            like_count = video_by_id.likes.all().count()
            dislike_count = video_by_id.dislikes.all().count()

            context = { 'video': video_by_id, 
                    'video_list': video_list,
                    'comments': comments,
                    'video_likes': likes,
                    'video_dislikes': dislikes,
                    'like_count': like_count,
                    'dislike_count': dislike_count,
                    'subscribers':subscribers }
        
        else:

        
            like_count = video_by_id.likes.all().count()
            dislike_count = video_by_id.dislikes.all().count()
            # subscribers = [row['id'] for row in subsc_rows]

            context = { 'video': video_by_id, 
                        'video_list': video_list,
                        'comments': comments,
                        'like_count': like_count,
                        'dislike_count': dislike_count
                        }

        

        return render(request, self.template_name, context)


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
        except VidLikes.DoesNotExist as e:
            pass

        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class CreateComment(LoginRequiredMixin,View):
    def post(self,request):
        print("Inside Comment Create View")
        comment = request.POST.get('comment',None)
        print(comment)
        video_id = request.POST.get('vid_id',None)
        print(video_id)
        video = get_object_or_404(Video,pk=int(video_id))

        comment_obj = Comment.objects.create(c_text=comment,video=video,user=request.user)
        res_comment = {
            'id': comment_obj.id,
            'comment_text': comment_obj.c_text,
            'uploaded_date': comment_obj.date_uploaded,
            'user': comment_obj.user.username
        }

        data = {
            'comment': res_comment
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateComment(LoginRequiredMixin,View):
    def post(self,request):
        print("Inside Comment Update View")
        comment_text = request.POST.get('comment',None)
        print(comment_text)
        comment_id = request.POST.get('id',None)
        print(comment_id)
        comment = get_object_or_404(Comment,pk=int(comment_id))
        comment.c_text = comment_text
        comment.save()
        res_comment = {
            'id': comment.id,
            'comment_text': comment.c_text,
            'updated_date': comment.date_updated,
            'user': comment.user.username
        }

        data = {
            'comment': res_comment
        }

        return JsonResponse(data)




@method_decorator(csrf_exempt, name='dispatch')
class DeleteComment(LoginRequiredMixin,View):
    def post(self,request):
        comment_id = request.POST.get('id',None)
        comment = get_object_or_404(Comment,pk=int(comment_id))
        comment_text = comment.c_text
        comment.delete()

        data = {
            'comment_id': comment_id,
            'success_message': 'You have succesfuly deleted comment'+"_"+comment_text[:35]
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class CreateReply(LoginRequiredMixin,View):
    def post(self,request):
        print("Inside CreateReply View")

        c_reply = request.POST.get('reply',None)
        comment_id = request.POST.get('comment_id',None)
        comment = get_object_or_404(Comment,pk=comment_id)
        

        reply_obj = Reply.objects.create(r_text=c_reply,comment=comment,user=request.user)
        reply = {
            'reply_id': reply_obj.id,
            'comment_id': comment.id,
            'reply': reply_obj.r_text,
            'uploaded_date': reply_obj.date_uploaded,
            'user': reply_obj.user.username
        }

        data = {
            'reply': reply
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateReply(LoginRequiredMixin,View):
    def post(self,request):
        print("Inside Reply Update View")
        reply_text = request.POST.get('reply',None)
        print(reply_text)
        reply_id = request.POST.get('id',None)
        print(reply_id)
        reply = get_object_or_404(Reply,pk=int(reply_id))
        reply.r_text = reply_text
        reply.save()
        res_reply = {
            'id': reply.id,
            'reply_text': reply.r_text,
            'updated_date': reply.date_updated,
            'user': reply.user.username
        }

        data = {
            'comment': res_reply
        }

        return JsonResponse(data)




@method_decorator(csrf_exempt, name='dispatch')
class DeleteReply(LoginRequiredMixin,View):
    def post(self,request):
        reply_id = request.POST.get('id',None)
        reply = get_object_or_404(Comment,pk=int(reply_id))
        reply_text = reply.r_text
        reply.delete()

        data = {
            'comment_id': reply_id,
            'success_message': 'You have succesfuly deleted comment'+"_"+reply_text[:35]
        }

        return JsonResponse(data)



class VideoDelete(LoginRequiredMixin,View):
    success_url = reverse_lazy('videos:hord_profile')
    def post(self,request):
        video_ids = request.POST.getlist('id[]')
        print(video_ids)
        for id in video_ids:
            video = Video.objects.get(pk=id)
            video.delete()
        return redirect(self.success_url)



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
        hord = get_object_or_404(Hord,owner=request.user)
        hord_videos = Video.objects.filter(hord=hord)
        ctx ={'videos': hord_videos}
        return render(request,self.template_name,ctx)











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