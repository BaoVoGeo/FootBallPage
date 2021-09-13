from django.core import paginator
from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect 

from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from blog.models import Post, PostInteract
from accounts.models import Account
from .forms import UpdateProfile, ReviewForm
from .models import ReviewRating

@login_required

def index(request):
    return render(request, 'blog/blog.html')
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
        user = Account.objects.get(id=request.user.id,)
        form = UpdateProfile(request.POST, request.FILES, instance = user)
        if form.is_valid():
            # upload(request.FILES['file'])
            print(request.FILES)
            if request.user.is_authenticated:
                form.save()
                notifi = form.instance
                messages.success(request, "Updated successful")
                return render(request,'pages/change_info.html', {'form':form, 'notifi': notifi})
        else:
            messages.success(request, "Updated not successful")
            
    
    form = UpdateProfile()
    return render(request, 'pages/change_info.html', {'form':form})

# def upload(f): 
#     file = open(f.name, 'wb+') 
#     for chunk in f.chunks():
#         file.write(chunk)
        
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
class SearchList(ListView):

    def get(self,request,*args,**kwargs):
        """
        Return the list of all the active employee data.
        """
        search_filter = self.request.GET.get('q')
        click = self.request.GET.get('click')
        sort_value = '-date'
        if not search_filter:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(Q(title__icontains=search_filter) | Q(content__icontains=search_filter)).order_by(sort_value)
        post_count = queryset.count()
        paginator = Paginator(queryset, 5)
        try:
            page = int(self.request.GET.get('page', '1'))
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
class FilterList(ListView):
    
    def get(self,request,*args,**kwargs):
        """
        Return the list of all the active employee data.
        """
        search_filter = self.request.GET.get('q')
        click = self.request.GET.get('click')
        sort_value = '-date'
        print("FilterList")
        print(click)
        print(search_filter)
        if click=='1':
            sort_value = self.request.GET.get('sorttitle')
        if click=='2':
            sort_value = self.request.GET.get('sortviews')
        if click=='3':
            sort_value = self.request.GET.get('sortdate')
        
        print(sort_value)
        if click=='2':
            if not search_filter:
                queryset = Post.objects.all()
            else:
                queryset_filter = Post.objects.filter(Q(title__icontains=search_filter) | Q(content__icontains=search_filter))
                queryset_interact = PostInteract.objects.filter(post_id__in = queryset_filter).order_by(sort_value)
                queryset = Post.objects.filter(id=queryset_interact[0].post_id)
                
                for i in range(1,queryset_interact.count()):
                    queryset = queryset.union(Post.objects.filter(id=queryset_interact[i].post_id))
                
        else: 
            if not search_filter:
                queryset = Post.objects.all()
            else:
                queryset = Post.objects.filter(Q(title__icontains=search_filter) | Q(content__icontains=search_filter)).order_by(sort_value)
        
        
        print(queryset)
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
        
        return render(request, "pages/filter_search_results.html", context)
