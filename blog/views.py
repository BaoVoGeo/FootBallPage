

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, PostViewsCount
from .cmtforms import CommentForm
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from intern.models import ReviewRating
class PostListView(ListView):
    
    queryset = Post.objects.all().order_by('-date')
    reviews = ReviewRating.objects.all().order_by('-created_at')
    template_name = 'blog/blog.html'
    context_object_name = 'Posts'
    paginate_by = 5
    

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.user.is_authenticated:

        try:
            postview = PostViewsCount()
            postview.post = post
            postview.user = request.user
            postview.save()
        except:
            return render(request, "blog/post.html", {"post": post, "form": form})
        
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
        except:
            return render(request, "blog/post.html", {"post": post, "form": form})

    return render(request, "blog/post.html", {"post": post, "form": form})


def visitor_ip_address(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def accounts(request):
    return render(request, "accounts/login.html", {"account"})
