from django.contrib import admin
from .models import ReviewRating
# Register your models here.
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['user','subject', 'review', 'created_at']
    list_filter = ['created_at']
    search_fields = ['subject','user']
    
admin.site.register(ReviewRating, ReviewRatingAdmin)