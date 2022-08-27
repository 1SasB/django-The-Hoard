from django.urls import path,reverse_lazy
from . import views

from .views import *
#, VideoView, CreateCommentView,CommentDeleteView,DeleteReplyView,ReplyCreateView


app_name = 'commentR'

urlpatterns = [
   
    path('video/comment/create',CreateComment.as_view(),name='create_comment'),
    path('video/comment/update',UpdateComment.as_view(),name='update_comment'),
    path('video/comment/delete',DeleteComment.as_view(),name='delete_comment'),
    path('comment/reply/create',CreateReply.as_view(),name='create_reply'),
    path('comment/reply/update',UpdateReply.as_view(),name='update_reply'),
    path('comment/reply/delete',DeleteReply.as_view(),name='delete_reply'),

]