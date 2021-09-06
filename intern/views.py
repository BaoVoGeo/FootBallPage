from django.core import paginator
from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect 
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from blog.models import Post
from .forms import UploadFileForm, ReviewForm
from intern.models import ReviewRating

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

# def search(request):
    
#     if 'q' in request.GET:
#         q = request.GET.get('q')
#         posts = Post.objects.order_by('-post_views','-date').filter(Q(title__icontains=q) | Q(content__icontains=q))
#         post_count = posts.count()
#         print(q)
#     paginator = Paginator(Post.objects.all(), 5)  
#     try:
#         page = int(request.GET.get('page', '1'))
#     except:
#         page = 1
    
#     try:
#         record_list = paginator.page(page)
#     except PageNotAnInteger:
#         record_list = paginator.page(1)
#     except EmptyPage:
#         record_list = paginator.page(1)
    
#     print(paginator.page(2).object_list)
#     index = record_list.number - 1
#     # This value is maximum index of pages, so the last page - 1
#     max_index = len(paginator.page_range)

#     # range of 7, calculate where to slice the list
#     start_index = index - 3 if index >= 3 else 0
#     end_index = index + 4 if index <= max_index - 4 else max_index

#     # new page range
#     page_range = paginator.page_range[start_index:end_index]


#     # showing first and last links in pagination
#     if index >= 4:
#         start_index = 1
#     if end_index - index >= 4 and end_index != max_index:
#         end_index = max_index
#     else:
#         end_index = None
            
#     context = {
#         # 'Posts': posts,
#         # 'q': q,
#         # 'Post_count': post_count,
#         'record_list': record_list,
#         'page_range': page_range,
#         'start_index': start_index,
#         'end_index': end_index,
#         'max_index':max_index,
#     }   
#     return render(request, 'pages/search_posts.html', context=context)


class EmployeeList(ListView):

    def get(self,request,*args,**kwargs):
        """
        Return the list of all the active employee data.
        """
        search_filter = request.GET.get('q')

        if not search_filter:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.order_by('-post_views','-date').filter(Q(title__icontains=search_filter) | Q(content__icontains=search_filter))
            
        post_count = queryset.count()
        paginator = Paginator(queryset, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        
        try:
            record_list = paginator.page(page)
        except PageNotAnInteger:
            record_list = paginator.page(1)
        except EmptyPage:
            record_list = paginator.page(paginator.num_pages)
            
        # Get the index of the current page
        index = record_list.number - 1

        # This value is maximum index of pages, so the last page - 1
        max_index = len(paginator.page_range)

        # range of 7, calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 4 if index <= max_index - 4 else max_index

        # new page range
        page_range = paginator.page_range[start_index:end_index]

        # showing first and last links in pagination
        if index >= 4:
            start_index = 1
        if end_index - index >= 4 and end_index != max_index:
            end_index = max_index
        else:
            end_index = None


        context = {
        'Post_count': post_count,
        'record_list': record_list,
        'page_range': page_range,
        'start_index': start_index,
        'end_index': end_index,
        'max_index':max_index,
        }   
        return render(request, 'pages/search_posts.html', context=context)
