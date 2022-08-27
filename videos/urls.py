from django.urls import path,reverse_lazy
from . import views

from .views import *
#, VideoView, CreateCommentView,CommentDeleteView,DeleteReplyView,ReplyCreateView


app_name = 'videos'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('upload',NewVideo.as_view(),name='upload'),
    # path('register',Register.as_view(),name='register'),
    # path('create_hord', CreateHord.as_view(), name='create_hord'),
    

    # # HOard
    # path('hoard/<slug:hord_name>',HordPage.as_view(),name='hord_page'),
    # path('hoard/profile',HordProfile.as_view(),name='hord_profile'),
    # path('hoard/<int:pk>/subscribe',AddSubscribeView.as_view(),name='hord_subscribe'),
    # path('hoard/<int:pk>/unsubscribe',RemoveSubscribeView.as_view(),name='hord_unsubscribe'),

    # Videos
    path('video/<int:id>', VideoView.as_view(), name='video_detail'),
    path('video/delete',VideoDelete.as_view(),name='video_delete'),
    # path('video/<int:pk>/like',AddLikeView.as_view(),name='video_like'),
    # path('video/<int:pk>/unlike',DeleteLikeView.as_view(),name='video_unlike'),
    # path('video/<int:pk>/dislike',AddDisLikeView.as_view(),name='video_dislike'),
    # path('video/<int:pk>/undislike',DeleteDisLikeView.as_view(),name='video_undislike'),
    # path('video/comment/create',CreateComment.as_view(),name='create_comment'),
    # path('video/comment/update',UpdateComment.as_view(),name='update_comment'),
    # path('video/comment/delete',DeleteComment.as_view(),name='delete_comment'),
    # path('comment/reply/create',CreateReply.as_view(),name='create_reply'),
    # path('comment/reply/update',UpdateReply.as_view(),name='update_reply'),
    # path('comment/reply/delete',DeleteReply.as_view(),name='delete_reply'),

]