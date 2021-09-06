from django import forms
from blog.models import Rating
from intern.models import ReviewRating
class UploadFileForm(forms.Form):
    file = forms.FileField()
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        
class RatePostForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['subject', 'review', 'rating']
        

