import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
#    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    nicevotes = models.IntegerField(default=0)

    def __str__(self):
        return self.tweet_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Connection(models.Model):
    follower = models.ForeignKey(get_user_model(), related_name='conn_follower', on_delete=models.CASCADE)
    following = models.ForeignKey(get_user_model(), related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)
