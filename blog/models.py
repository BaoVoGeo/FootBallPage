from django.db import models
from django.db.models import Count
from django.conf import settings
from django.db.models.constraints import UniqueConstraint
from accounts.models import Account
import datetime
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length = 50)
    slug = models.SlugField(unique=True,blank=True,null=True)
    
    def save(self, *args, **kwargs):
         if not self.id:
                # Newly created object, so set slug
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)
    # def __str__(self):
    #     str(self.name)
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug  = models.SlugField(null=True,blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    author = models.CharField(max_length= 10)
    image = models.ImageField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    post_views=models.IntegerField(default = 0)
    
    def title_slug  (self):
        return slugify(self.title)
    
    def save(self, *args, **kwargs):
         if not self.id:
                # Newly created object, so set slug
            self.slug = slugify(self.title)
            super(Post, self).save(*args, **kwargs)
    def get_url(self):
        return reverse('post', args=[self.category.slug, self.slug])        


class PostViewsCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,db_index=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, db_index=False)
    ip = models.GenericIPAddressField(default=None, blank=True, null=True,db_index=False)
    date_view = models.DateField(("Date"), default=datetime.date.today)
    
    class Meta:
        unique_together = (['post','ip','date_view'],['post','user','date_view'])

class PostInteract(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,db_index=False)
    # likes = models.IntegerField(default = 0)
    # dislikes = models.IntegerField(default = 0)
    # shares  = models.IntegerField(default = 0)
    views= models.IntegerField( default= 0)
    
    def __str__(self):  
        
        return str(self.post)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)

class PostInteract_detail(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_likes =  models.ManyToManyField(Account, related_name='requirement_post_likes')
    user_dislikes =  models.ManyToManyField(Account, related_name='requirement_post_dislikes')
    user_shares =  models.ManyToManyField(Account, related_name='requirement_post_shares')
    
    def total_likes(self):
        self.user_likes.count()
    def total_dislikes(self):
        self.user_dislikes.count()
    def total_shares(self):
        self.user_shares.count()
    def __str__(self):
        str(self.post)
        
class Like(models.Model):
    ''' like  comment '''

    comment = models.OneToOneField(Comment, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(Account, related_name='requirement_comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.comment)[:30]

class DisLike(models.Model):
    ''' Dislike  comment '''

    comment = models.OneToOneField(Comment, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(Account, related_name='requirement_comment_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.comment)[:30]

