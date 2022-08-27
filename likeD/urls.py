from django.urls import path,reverse_lazy
from . import views

from .views import *
#, VideoView, CreateCommentView,CommentDeleteView,DeleteReplyView,ReplyCreateView


app_name = 'likeD'

urlpatterns = [
   

   
    path('video/<int:pk>/like',AddLikeView.as_view(),name='video_like'),
    path('video/<int:pk>/unlike',DeleteLikeView.as_view(),name='video_unlike'),
    path('video/<int:pk>/dislike',AddDisLikeView.as_view(),name='video_dislike'),
    path('video/<int:pk>/undislike',DeleteDisLikeView.as_view(),name='video_undislike'),
   

]