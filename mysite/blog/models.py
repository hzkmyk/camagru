from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    num_likes = models.IntegerField(default=0)
    caption = models.CharField(max_length=100, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return "{} uploaded on {}".format(
            self.user.username,
            str(self.uploaded_at),
        )

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    posted_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(to=Image, related_name='comments', on_delete=models.CASCADE)
    def __str__(self):
        return (
            self.text,
            self.user.username,
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.BooleanField(default=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
