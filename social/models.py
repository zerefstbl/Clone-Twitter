from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.dispatch import receiver


class Post(models.Model):
    body = models.TextField()
    create_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    deslikes = models.ManyToManyField(
        User, blank=True, related_name='deslikes')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    image = models.ImageField(
        upload_to='media/posts_photos', blank=True, null=True)


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name='user', related_name='profile')
    name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(
        upload_to='media/profile_pictures', default='media/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(
        User, related_name='followers', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notification(models.Model):
    # 1 = Like, 2 = Comment, 3 = Follow
    notification_type = models.IntegerField(null=True, blank=True)
    to_user = models.ForeignKey(
        User, related_name='notification_to', on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        User, related_name='notification_from', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='+',
                             on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
