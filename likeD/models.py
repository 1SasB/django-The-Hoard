from django.db import models
from videos.models import Video
# Create your models here.
class VidLikes(models.Model):
    video = models.ForeignKey('videos.video',on_delete=models.CASCADE,related_name="liked_video")
    user =  models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video','user')

    def __str__(self):
        return '%s likes %s'%(self.user.username,self.video.title)


class VidDislikes(models.Model):
    video = models.ForeignKey('videos.Video',on_delete=models.CASCADE,related_name="disliked_video")
    user =  models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video','user')

    def __str__(self):
        return '%s dislikes %s'%(self.user.username,self.video.title)