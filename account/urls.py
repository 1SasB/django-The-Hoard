from django.urls import path,reverse_lazy
from . import views

from .views import *
#, VideoView, CreateCommentView,CommentDeleteView,DeleteReplyView,ReplyCreateView


app_name = 'account'

urlpatterns = [

    path('register',Register.as_view(),name='register'),
    path('create_hord', CreateHord.as_view(), name='create_hord'),
    

    # HOard
    path('hoard/<slug:hord_name>',HordPage.as_view(),name='hord_page'),
    path('hoard/profile',HordProfile.as_view(),name='hord_profile'),
    path('hoard/<int:pk>/subscribe',AddSubscribeView.as_view(),name='hord_subscribe'),
    path('hoard/<int:pk>/unsubscribe',RemoveSubscribeView.as_view(),name='hord_unsubscribe'),

    
   

]