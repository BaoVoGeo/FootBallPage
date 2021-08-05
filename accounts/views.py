from re import split
import re
# from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from .forms import RegistrationForm
from .utils import token_generator
from accounts.models import Account

import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context = {'has_error': False, 'data': request.POST}
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if len(password) < 6:
                print(password)
                messages.add_message(request, messages.ERROR,
                                 'Password should be at least 6 characters')
                context['has_error'] = True

            if password != confirm_password:
                messages.add_message(request, messages.ERROR,
                                    'Password mismatch')
                context['has_error'] = True

            if not validate_email(email):
                messages.add_message(request, messages.ERROR,
                                    'Enter a valid email address')
                context['has_error'] = True
            

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password)
            user.set_password(password)
            user.save()
            if not context['has_error']:
                current_site = get_current_site(request=request)
                mail_subject ='Activate your account.'
                
                message = render_to_string('pages/active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user)
                })
                
                send_email = EmailMessage(subject = mail_subject, body = message, to=[email])
                send_email.send()
                messages.SUCCESS(
                    request=request,
                    message="Please confirm your email address to complete the registration")
                
            return redirect('register')
        else:
            messages.add_message(request, messages.ERROR,"Register failed!")
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request, 'pages/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        # if (user is None):
        #      user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            # try:
            #     cart = Cart.objects.get(cart_id=_cart_id(request))
            #     cart_items = CartItem.objects.filter(cart=cart)
            #     if cart_items.exists():
            #         product_variation = []
            #         for cart_item in cart_items:
            #             variations = cart_item.variations.all()
            #             product_variation.append(list(variations))
            #             # cart_item.user = user
            #             # cart_item.save()
            #         cart_items = CartItem.objects.filter(user=user)
            #         existing_variation_list = [list(item.variations.all()) for item in cart_items]
            #         id = [item.id for item in cart_items]

            #         for product in product_variation:
            #             if product in existing_variation_list:
            #                 index = existing_variation_list.index(product)
            #                 item_id = id[index]
            #                 item = CartItem.objects.get(id=item_id)
            #                 item.quantity += 1
            #                 item.user = user
            #                 item.save()
            #             else:
            #                 cart_items = CartItem.objects.filter(cart=cart)
            #                 for item in cart_items:
            #                     item.user = user
            #                     item.save()
            # except Exception:
            #     pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('blog')
        else:
            messages.error(request=request, message="Login failed!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'pages/login.html', context=context)



@login_required(login_url="login")
def logout(request):
    print(auth.logout(request))
    messages.success(request=request, message="You are logged out!")
    return redirect('login')


def activate( request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None
    
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,"Your account is activated, please login!")
        return render(request, 'pages/login.html')
    else:
        messages.add_message(request, messages.ERROR,"Activation link is invalid! Please use another email!")
        return redirect('register')


def forgotPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Account.objects.get(email__exact=email)
            
            current_site = get_current_site(request=request)
            mail_subject = 'Reset your password'
            message = render_to_string('pages/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request=request, message="Password reset email has been sent to your email address")
    except Exception:
        messages.error(request=request, message="Account does not exist!")
    finally:
        context = {
            'email': email if 'email' in locals() else '',
        }
        return render(request, "pages/forgotPassword.html", context=context)


def reset_password_validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None
        
    if user is not None and token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request=request, message='Please reset your password')
        return redirect('reset_password')
    else:
        messages.info(request=request, message="This link has been expired!")
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Password reset successful!")
            return redirect('login')
        else:
            messages.error(request, message="Password do not match!")
    return render(request, 'pages/reset_password.html')