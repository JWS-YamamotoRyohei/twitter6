from django.contrib import admin
from .models import Tweet

# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweet_text', 'pub_date', 'was_published_recently', 'nicevotes')

admin.site.register(Tweet, TweetAdmin)