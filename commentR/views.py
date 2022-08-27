from django.shortcuts import render
# from videos.owner import OwnerListView,OwnerCreateView,OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse
from .forms import CommentForm,ReplyForm
from django.contrib.auth import update_session_auth_hash,login,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .models import  Comment,Reply
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from django.apps import apps

Video = apps.get_model('videos','Video')
Hord = apps.get_model('account','Hord')
Subscribers = apps.get_model('account','Subscribers')

@method_decorator(csrf_exempt, name='dispatch')
class CreateComment(LoginRequiredMixin,View):
    def post(self,request):
        print("Inside Comment Create View")
        comment = request.POST.get('comment',None)
        video_id = request.POST.get('vid_id',None)
        video = get_object_or_404(Video,pk=int(video_id))

        comment_obj = Comment.objects.create(c_text=comment,video=video,user=request.user)
        res_comment = {
            'id': comment_obj.id,
            'comment_text': comment_obj.c_text,
            'uploaded_date': comment_obj.date_uploaded,
            'user': comment_obj.user.username
        }

        data = {
            'comment': render_to_string("videos/comment_template.html",res_comment)
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateComment(LoginRequiredMixin,View):
    def post(self,request):
        print("Inside Comment Update View")
        comment_text = request.POST.get('comment',None)
        comment_id = request.POST.get('id',None)
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
            'reply': render_to_string("videos/reply_template.html",reply)
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateReply(LoginRequiredMixin,View):
    def post(self,request):
        reply_text = request.POST.get('reply',None)
        reply_id = request.POST.get('id',None)
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
        reply = get_object_or_404(Reply,pk=int(reply_id))
        reply_text = reply.r_text
        reply.delete()

        data = {
            'comment_id': reply_id,
            'success_message': 'You have succesfuly deleted comment'+"_"+reply_text[:35]
        }

        return JsonResponse(data)
