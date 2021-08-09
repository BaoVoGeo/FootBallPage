from django import forms
from intern.models import ReviewRating
class UploadFileForm(forms.Form):
    file = forms.FileField()
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']