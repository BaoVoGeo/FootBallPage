from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .cmtforms import CommentForm
from django.views.generic import ListView
from django.http import HttpResponseRedirect

class PostListView(ListView):
    
    queryset = Post.objects.all().order_by('-date')
    template_name = 'blog/blog.html'
    context_object_name = 'Posts'
    paginate_by = 5
    

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST, author=request.user, post=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(request, "blog/post.html", {"post": post, "form": form})

def accounts(request):
    return render(request, "accounts/login.html", {"account"})
