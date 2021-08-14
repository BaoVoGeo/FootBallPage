from django.shortcuts import render

# Create your views here.
from blog.models import Post
from django.shortcuts import redirect, render
from intern.models import ReviewRating
from django.http import HttpResponse
from django.contrib import messages


from django.db.models import Q

from django.http import HttpResponseRedirect 
from django.contrib.auth.models import User
from .forms import UploadFileForm, ReviewForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
@login_required

def index(request):
    return render(request, 'blog/blog.html')
def contact(request):
    return render(request, 'pages/contact.html')
def showblog(request):
    return render(request, 'blog/blog.html')

def accounts(request):
    return render(request, 'accounts/login.html')

def error(request,exception):
    return render(request, 'pages/error.html', {'message': exception})

def profile(request):
    return render(request, 'pages/profile.html')

def fileUploaderView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload(request.FILES['file'])
            if request.user.is_authenticated:
                print('co nguoi dang nhap ne')
                print( request.user.username)
                print(form.data)
                p = User.objects.get(username = request.user.username)
                print(p.img_avt_id)
                p.img_avt_id = 2
                p.save()
                
        else:
            return HttpResponse("<h2>File uploaded not successful!</h2>")
    
    form = UploadFileForm()
    return render(request, 'pages/change_info.html', {'form':form})
  
def upload(f): 
    file = open(f.name, 'wb+') 
    for chunk in f.chunks():
        file.write(chunk)
        
        
def submit_review(request):
    url = request.META.get('HTTP_REFERER')
    
    if request.method == "POST":
        try:
           
            review = ReviewRating.objects.get(id=request.user.id,)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except Exception:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
class ReviewListView(ListView):
    
    queryset = ReviewRating.objects.all().order_by('-created_at')
    template_name = 'pages/base.html'
    context_object_name = 'Reviews'
    paginate_by = 5


def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        posts = Post.objects.order_by('-post_views','-date').filter(Q(title__icontains=q) | Q(content__icontains=q))
        post_count = posts.count()
    context = {
        'Posts': posts,
        'q': q,
        'Post_count': post_count,
    }
    return render(request, 'pages/search_posts.html', context=context)
