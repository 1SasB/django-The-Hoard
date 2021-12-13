from django.core.files import storage
from django.db import models
import os
from django.conf import settings
# from account.models import Hord
from django.core.validators import MinLengthValidator
from django.db.models.base import Model
from django.core.files.storage import FileSystemStorage

vid_path = FileSystemStorage(location='/media/videos')

visibilty = (
    ('Public','Public'),
    ('Private','Private'),
    ('Draft','Draft'),
    ('None','None')
)




class Hord(models.Model):
    Name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    profile_image = models.ImageField(upload_to='images/profile/')
    wall_paper = models.ImageField(upload_to='images/wall/')
    owner = models.OneToOneField('auth.user',on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    

class SubHord(models.Model):
    Name = models.CharField(max_length=200,
            validators=[MinLengthValidator(5, "Title must be greater than 5 characters")])
    hord = models.ForeignKey(Hord,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    # duration = models.DurationField()
    path = models.FileField(upload_to='videos/', null=False, verbose_name="PATH")
    thumbnail = models.FileField(upload_to='thumbnails/',blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    date_updated = models.DateTimeField(auto_now=True)
    hord = models.ForeignKey(Hord,on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    likes = models.ManyToManyField('auth.User', through='VidLikes' ,related_name='video_likes')
    dislikes = models.ManyToManyField('auth.User', through='VidDislikes', related_name='video_dislikes')
    visibilty = models.CharField(max_length=15,choices=visibilty)

    def __str__(self):
        return str(self.title) + ": " + str(self.path)
    
    def delete(self,*args,**kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT,self.path.name))
        super(Video,self).delete(*args,**kwargs)


class VidLikes(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    user = user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video','user')

    def __str__(self):
        return '%s likes %s'%(self.user.username,self.video.title)


class VidDislikes(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    user = user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video','user')

    def __str__(self):
        return '%s dislikes %s'%(self.user.username,self.video.title)




class Playlist(models.Model):
    Name = models.CharField(max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
            )
    description = models.CharField(max_length=750)
    date_created = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    hord = models.ForeignKey(Hord,on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Draft(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    hord = models.ForeignKey(Hord,on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Comment(models.Model):
    c_text = models.TextField(verbose_name='', max_length=1000)
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.c_text

class Reply(models.Model):
    r_text = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user',on_delete=models.CASCADE)

    def __str__(self):
        return self.r_text





# from django.db.models.signals import post_save, post_delete
# from moviepy.editor import *


# def create_profile(sender,instance,created,*args,**kwargs):
#     print(instance)
#     clip = VideoFileClip(instance.path.file)
#     # frame = clip.reader.fps
#     duration = clip.duration
#     print(duration)

# # def create_pharmacist_profile(sender,instance,created,*args,**kwargs):
# #     if created:
# #         instance.profile = Pharmacist.objects.create()
# #         instance.save()

# post_save.connect(create_profile,sender=Video)
# # post_save.connect(create_pharmacist_profile,sender=Pharmacist)