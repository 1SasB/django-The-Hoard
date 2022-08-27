from django.db import models
# Create your models here.

class Comment(models.Model):
    c_text = models.TextField(verbose_name='', max_length=1000)
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE)

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
