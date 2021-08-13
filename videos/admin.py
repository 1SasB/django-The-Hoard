from django.contrib import admin

# Register your models here.
from .models import Video,Comment,Reply,Hord


admin.site.register([Video,Comment,Reply,Hord])
