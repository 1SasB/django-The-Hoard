from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Hord(models.Model):
    Name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    profile_image = models.ImageField(upload_to='images/profile/')
    wall_paper = models.ImageField(upload_to='images/wall/')
    subscribers  = models.ManyToManyField('auth.User', through='Subscribers',related_name='hoard_subscribers')
    owner = models.OneToOneField('auth.user',on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class Subscribers(models.Model):
    hord = models.ForeignKey(Hord,on_delete=models.CASCADE,related_name='subsc_hord')
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hord','user')

    def __str__(self):
        return '%s subscribed to %s'%(self.user.username,self.hord.Name)


class SubHord(models.Model):
    Name = models.CharField(max_length=200,
            validators=[MinLengthValidator(5, "Title must be greater than 5 characters")])
    hord = models.ForeignKey(Hord,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
