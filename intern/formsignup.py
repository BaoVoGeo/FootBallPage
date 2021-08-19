from django import forms
import re
from django.contrib.auth.models import User
from accounts.models import MyAccountManager
class RegistrationForm(forms.Form):
    first_name = forms.CharField(label = 'Họ', max_length = 50, min_length = 8 )
    last_name = forms.CharField(label = 'Tên', max_length = 50, min_length = 8 )
    username = forms.CharField(label = 'Tên đăng nhập', max_length = 50, min_length = 8 )
    email = forms.EmailField(label='Email')
    password_1 = forms.CharField(label = 'Nhập mật khẩu', max_length = 30, min_length = 8, widget = forms.PasswordInput())
    password_2 = forms.CharField(label = 'Nhập lại mật khẩu', max_length =30, min_length =8, widget = forms.PasswordInput())
    
    
    def clean_password2(self):
        if 'password_1' in self.cleaned_data:
            password_1 = self.cleaned_data['password_1']
            password_2 = self.cleaned_data['password_2']
            if password_1 == password_2 and password_1:
                return password_2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+&', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
    
    
    
    def save(self):
        MyAccountManager.create_user(
                            first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'],
                            username=self.cleaned_data['username'], password=self.cleaned_data['password_1'], 
                            email =  self.cleaned_data['email'] )
        