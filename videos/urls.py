from django.urls import path,reverse_lazy
from . import views

from .views import CreateComment, CreateReply, DeleteComment, DeleteReply,AddLikeView,DeleteLikeView, HordPage, HordProfile, NewVideo, Home, Register, CreateHord, UpdateComment, UpdateReply, VideoDelete,VideoView
#, VideoView, CreateCommentView,CommentDeleteView,DeleteReplyView,ReplyCreateView


app_name = 'videos'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('upload',NewVideo.as_view(),name='upload'),
    path('register',Register.as_view(),name='register'),
    path('create_hord', CreateHord.as_view(), name='create_hord'),
    path('video/<int:id>', VideoView.as_view(), name='video_detail'),
    path('hoard/<slug:hord_name>',HordPage.as_view(),name='hord_page'),
    path('hoard/profile',HordProfile.as_view(),name='hord_profile'),
    path('video/delete',VideoDelete.as_view(),name='video_delete'),
    path('video/<int:pk>/like',AddLikeView.as_view(),name='video_like'),
    path('video/<int:pk>/unlike',DeleteLikeView.as_view(),name='video_unlike'),
    path('video/comment/create',CreateComment.as_view(),name='create_comment'),
    path('video/comment/update',UpdateComment.as_view(),name='update_comment'),
    path('video/comment/delete',DeleteComment.as_view(),name='delete_comment'),
    path('comment/reply/create',CreateReply.as_view(),name='create_reply'),
    path('comment/reply/update',UpdateReply.as_view(),name='update_reply'),
    path('comment/reply/delete',DeleteReply.as_view(),name='delete_reply'),

]