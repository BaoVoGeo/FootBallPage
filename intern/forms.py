from django import forms
from blog.models import Rating
from accounts.models import Account
from intern.models import ReviewRating
class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name","last_name","email","phone_number",'profile_avt']
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        
class RatePostForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['subject', 'review', 'rating']
        
        

