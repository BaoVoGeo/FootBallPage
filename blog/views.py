

from django.forms.utils import ErrorList
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify

from django.views.generic import ListView
from django.http import HttpResponseRedirect

from django.db.models import Count,Exists   
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q

from .models import *
from .cmtforms import CommentForm
from intern.models import ReviewRating
from intern.forms import *

def show_blog(request):
    #show top views (posts)
    posts_date_main = Post.objects.all().order_by('-date')[:5]
    posts_date = Post.objects.all().order_by('-date')[5:]
    hot_view = PostViewsCount.objects.values('post_id').annotate(dcount = Count('post_id')).order_by('-dcount')[:5]
    if (hot_view.count() > 0):
        posts_hot_views = Post.objects.filter(id = hot_view[0]["post_id"])
        if (hot_view.count() < 5 ):
            
            for  i in range(1,hot_view.count()):
                posts_hot_views = posts_hot_views.union(Post.objects.filter(id = hot_view[i]["post_id"]))
        else: 
            for  i in range(1,5):
                posts_hot_views = posts_hot_views.union(Post.objects.filter(id = hot_view[i]["post_id"]))
    else:
        posts_hot_views = posts_date_main   
    context = {'posts_hot_views':posts_hot_views,
                'Posts_main': posts_date_main,
                'Posts_date': posts_date,
                }
    return render(request, 'blog/blog.html', context)

class ListViewLeague(ListView):
    
    template_name = "blog/base_blog.html"
        
    def get_queryset(self):
        
        post_filter_date = Post.objects.filter(tags__slug=self.kwargs.get("slug")).all()
        posts_date_main =post_filter_date.order_by('-date')[:5]
        posts_date = post_filter_date.order_by('-date')[5:]
        hot_view = PostViewsCount.objects.filter(post__in = post_filter_date).values('post_id').annotate(dcount = Count('post_id')).order_by('-dcount')[:5]
        
        if (hot_view.count() > 0):
            posts_hot_views = Post.objects.filter(id = hot_view[0]["post_id"])
            if (hot_view.count() < 5 ):
                
                for  i in range(1,hot_view.count()):
                    posts_hot_views = posts_hot_views.union(Post.objects.filter(id = hot_view[i]["post_id"]))
            else: 
                for  i in range(1,5):
                    posts_hot_views = posts_hot_views.union(Post.objects.filter(id = hot_view[i]["post_id"]))
        else:
            posts_hot_views = posts_date_main
        
        return (posts_hot_views, posts_date_main, posts_date, self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super(ListViewLeague, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        context["posts"] = self.get_queryset()
        context = {
            'tags': self.kwargs.get("slug"),
            'Posts_hot_views': self.get_queryset()[0],
            'Posts_main': self.get_queryset()[1],
            'Posts_date': self.get_queryset()[2],
            'title_page': self.get_queryset()[3],
        }
        return context

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    # Number of Interacts on each post
    if (PostInteract_detail.objects.filter(post = post).exists()):
        pass
    else:
        add = PostInteract_detail(post = post)   
        add.save()
    if (PostInteract.objects.filter(post = post).exists()):
        total_views =  PostInteract.objects.get(post = post).views
    else:
        total_views = 0
    if (PostInteract.objects.filter(post = post).exists()):
        total_likes = PostInteract_detail.objects.get(post = post).user_likes.count()
        total_dislikes = PostInteract_detail.objects.get(post =post).user_dislikes.count()
        total_shares = PostInteract_detail.objects.get(post = post).user_shares.count()
    else:
        total_likes = total_dislikes = total_shares = 0
    # tags
    tags = post.tags.all()
    similar_books = Post.objects.filter(
        tags__in=tags
    ).exclude(
        id=post.id
    ).distinct()
    
    context ={
        "post": post, 
        "form": form, 
        "total_likes": total_likes,
        "total_dislikes": total_dislikes,
        "total_shares": total_shares,
        "total_views" :total_views,
        "similar_books": similar_books,
    }
    if request.user.is_authenticated:
        try:
            postview = PostViewsCount()
            postview.post = post
            postview.user = request.user
            if(postview.save() == None):
                
                if (PostInteract.objects.filter(post = post).exists()):
                    postinteract = PostInteract.objects.get(post = post)
                    
                    postinteract.views += 1
                    postinteract.save()
                else:
                    
                    postinteract = PostInteract()
                    postinteract.post = post
                    postinteract.views = 1
                    postinteract.save()
        except:
            
            if request.method == "POST":
                form = CommentForm(request.POST, author=request.user, post=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.path)
            else:
                form = CommentForm()
            return render(request, "blog/post.html", context)
        if request.method == "POST":
            form = CommentForm(request.POST, author=request.user, post=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.path)
        else:
            form = CommentForm()
    else:
        try:
            user_ip = visitor_ip_address(request)
            postview = PostViewsCount()
            postview.post = post
            postview.ip = user_ip
            postview.save()
            if (PostInteract.objects.filter(post = post).exists()):
                postinteract = PostInteract.objects.get(post = post)
                
                postinteract.views += 1
                postinteract.save()
            else:
                postinteract = PostInteract()
                postinteract.post = post
                postinteract.views = 1
                postinteract.save()
        except:
            return render(request, "blog/post.html", context)

    return render(request, "blog/post.html", context)

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def accounts(request):
    return render(request, "accounts/login.html", {"account"})

def like_post(request, pk):
    post_pk = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if (PostInteract_detail.objects.filter(post = post_pk).exists()):
            post_detail = PostInteract_detail.objects.get(post = post_pk)
            if post_detail.user_likes.filter(id = request.user.id).exists():
                    del_post = post_detail.user_likes.get(id = request.user.id)
                    post_detail.user_likes.remove(del_post)
            else:
                if post_detail.user_dislikes.filter(id = request.user.id).exists():
                    del_post = post_detail.user_dislikes.get(id = request.user.id)
                    post_detail.user_dislikes.remove(del_post)
                post_detail.user_likes.add(request.user)
            return HttpResponseRedirect(reverse('post', args = [str(pk)]))
        else:
            add = PostInteract_detail(post = post_pk)
            add.save()
            add.user_likes.add(request.user)
            add.save()
            return HttpResponseRedirect(reverse('post', args = [str(pk)]))
    else:
        return HttpResponseRedirect(reverse('post', args = [str(pk)]))

def dislike_post(request, pk):
    post_pk = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if (PostInteract_detail.objects.filter(post = post_pk).exists()):
            post_detail = PostInteract_detail.objects.get(post = post_pk)
            if post_detail.user_dislikes.filter(id = request.user.id).exists():
                    del_post = post_detail.user_dislikes.get(id = request.user.id)
                    post_detail.user_dislikes.remove(del_post)
            else:
                if post_detail.user_likes.filter(id = request.user.id).exists():
                    del_post = post_detail.user_likes.get(id = request.user.id)
                    post_detail.user_likes.remove(del_post)
                post_detail.user_dislikes.add(request.user)
            return HttpResponseRedirect(reverse('post', args = [str(pk)]))
        else:
            add = PostInteract_detail(post = post_pk)
            add.save()
            add.user_dislikes.add(request.user)
            add.save()
            return HttpResponseRedirect(reverse('post', args = [str(pk)]))
    else:
        return HttpResponseRedirect(reverse('post', args = [str(pk)]))
    
def share_post(request, pk):
    post_pk = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
    
        if (PostInteract_detail.objects.filter(post = post_pk).exists()):
            post_detail = PostInteract_detail.objects.get(post = post_pk)
            if post_detail.user_shares.filter(id = request.user.id).exists():
                    del_post = post_detail.user_shares.get(id = request.user.id)
                    post_detail.user_shares.remove(del_post)
            else:
                    post_detail.user_shares.add(request.user)
            return HttpResponseRedirect(reverse('post', args = [str(pk)]))
        else:
            add = PostInteract_detail(post = post_pk)
            add.save()
            add.user_shares.add(request.user)
            add.save()
            return HttpResponseRedirect(reverse('post', args = [str(pk)]))
    else:
        return HttpResponseRedirect(reverse('post', args = [str(pk)]))
    

def rate_post(request, pk):
    
    url = request.META.get('HTTP_REFERER')
    print(url)
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            try:   
                print(Rating.objects.filter(post__id=pk).exists())
                # if Rating.objects.filter(users=request.user.id,post=post).exists():
                review = Rating.objects.get(users__id=request.user.id,post__id=pk)
                form = RatePostForm(request.POST, instance=review)
                form.save()
                messages.success(request, "Thanks for rating")
  
            except Rating.DoesNotExist:
                form = RatePostForm(request.POST)
                if form.is_valid():
                    data = Rating()
                    data.post = post 
                    data.subject = form.cleaned_data['subject']
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.save()
                    data.users.add(request.user)
                    data.save()
                    messages.success(request, "Thanks for rating, it saved")
            
        return redirect(url)
    else:
        return redirect(url)
