from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from django.utils import timezone
from tkinter import messagebox


from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, ListView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404

from .models import Connection

def index(request):
    latest_tweet_list = Tweet.objects.all().order_by('-pub_date')[:5]
    context = {'latest_tweet_list': latest_tweet_list}
    return render(request, 'twitter/index.html', context)

@login_required
def tweetlist(request):
    latest_tweet_list = Tweet.objects.all().order_by('-pub_date')[:5]
    context = {'latest_tweet_list': latest_tweet_list}
    return render(request, 'twitter/tweetlist.html', context)

@login_required
def detail(request, tweet_id):
    user = request.user
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.method == 'POST':
            tweet.nicevotes += 1
            tweet.save()
            context = {'user':user,'tweet': tweet}
            return render(request, 'twitter/detail.html', context)

    context = {'user':user,'tweet': tweet}
    return render(request, 'twitter/detail.html', context)


# def results(request, tweet_id):
#     tweet = get_object_or_404(Tweet, pk=tweet_id)
#     return render(request, 'twitter/results.html', {'tweet': tweet})

@login_required
def tweet_new(request):
     if request.method == "POST":
         form = TweetForm(request.POST)
         if form.is_valid():
             tweet = form.save(commit=False)
             tweet.author = request.user
             tweet.pub_date =timezone.now()
             tweet.save()
             return redirect('twitter:detail',tweet_id=tweet.pk)
     else:
         form = TweetForm()
     return render(request, 'twitter/tweet_new.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('twitter:tweetlist')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'twitter/signup.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
     model = User
     template_name = "twitter/profile.html"
     slug_field = 'username'
     slug_url_kwarg = 'username'

     def get_context_data(self, **kwargs):
         context = super(ProfileDetailView, self).get_context_data(**kwargs)
         username = self.kwargs['username']
         context['username'] = username
         context['user'] = self.request.user
         context['following_count'] = Connection.objects.filter(follower__username=username).count()
         context['followers_count'] = Connection.objects.filter(following__username=username).count()

         if username != context['user'].username:
             context['connected'] = True if Connection.objects.exists() else False

         return context

@login_required
def follow_view(request, *args, **kwargs):
     try:
         follower = User.objects.get(username=request.user)
         following = User.objects.get(username=kwargs['username'])
     except User.DoesNotExist:
         messages.warning(request, '{}は存在しません'.format(kwargs['username']))
         return HttpResponseRedirect(reverse('twitter:index'))

     if follower == following:
         messages.warning(request, '自分自身はフォローできませんよ')
     else:
         _, created = Connection.objects.get_or_create(follower=follower, following=following)

         if (created):
             messages.success(request, '{}をフォローしました'.format(following.username))
         else:
             messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))

     return HttpResponseRedirect(reverse('twitter:profile', kwargs={'username': following.username}))

@login_required
def unfollow_view(request, *args, **kwargs):
     try:
         follower = User.objects.get(username=request.user)
         following = User.objects.get(username=kwargs['username'])
         if follower == following:
             messages.warning(request, '自分自身のフォローを外せません')
         else:
             unfollow = Connection.objects.get(follower=follower, following=following)
             unfollow.delete()
             messages.success(request, 'あなたは{}のフォローを外しました'.format(following.username))
     except User.DoesNotExist:
         messages.warning(request, '{}は存在しません'.format(kwargs['username']))
         return HttpResponseRedirect(reverse('twitter:index'))
     except Connection.DoesNotExist:
         messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(following.username))

     return HttpResponseRedirect(reverse('twitter:profile', kwargs={'username': following.username}))