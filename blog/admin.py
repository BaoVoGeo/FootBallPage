from django.contrib import admin



from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    list_filter = ['name']
    search_fields = ['name','slug']
    prepopulated_fields = {'slug': ('name',)}
    
class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author', 'date']
    list_filter = ['date']
    search_fields = ['title','author']
    inlines = [CommentInline]
    prepopulated_fields = {'slug': ('title',)}

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

class PostInteractAdmin(admin.ModelAdmin):
    list_display = ['post','views']
    list_filter = ['views']
    search_fields = ['post']
    
admin.site.register(PostInteract, PostInteractAdmin)
admin.site.register(Category, CategoryAdmin)    
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

# admin.site.register(Like)