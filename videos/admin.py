from django.contrib import admin

# Register your models here.
from .models import Video
from account.models import Hord
from commentR.models import Comment,Reply


admin.site.register([Video,Comment,Reply,Hord])
