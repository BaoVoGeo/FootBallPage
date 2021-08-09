from django.contrib import admin

from .models import Post,Comment

from .models import *



class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    list_filter = ['date']
    search_fields = ['title','author']
    inlines = [CommentInline]

class LikeInline(admin.TabularInline):
    model = Like

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'body','post','date']
    list_filter = ['date']
    search_fields = ['body','author','post']
    # actions =['approve_comments']
    # inlines = [LikeInline]
    # def approve_comments(self, request, queryset):
    #     queryset.update(active=True)
        
        
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

# admin.site.register(Like)