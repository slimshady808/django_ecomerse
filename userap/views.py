from django.shortcuts import render,redirect
import json
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.cache import cache_control
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .models import UserDetails, Address
from .forms import UserDetailsForm, AddressForm
from .forms import UserRegisterForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import UserDetails, Address
from .forms import UserDetailsForm, AddressForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Address
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from orderap.models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Address
from .forms import AddressForm
# Create your views here.

#log-in user by email and password
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request=request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('log_in')
    
    else:
        return render(request, 'user/login.html')

#sign-up user
def sign_up(request):
    if request.user.is_authenticated:
        return render(request,'products/index.html')
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']

        if password1==password2:
            #change
            if User.objects.filter(email=email).exists():
                messages.info(request,'email takken')
                return redirect('sign_up')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email)
                user.is_active=False
                user.save()
                email_subject='Activate your Account'
                message=render_to_string('email_signup/activate.html',{
                    'user':user,
                    'domain': '//127.0.0.1:8000/',
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user)
                })
                email_message =EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,
                [email])
                email_message.send()

                messages.success(request,'activate your account clicking link')
                return redirect('log_in')



 
        else:
            messages.info(request,'password not matching')
            return redirect('sign_up')
      
 
    else:
        return render(request,'user/register.html')
  
  
#email activation
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,'Account activated sucesfully')
            return redirect ('log_in')
        return render (request,'activatefail.html')
#=========================================================================  
# user sign-out
def sign_out(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')
#=====================================================================

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'user/request-reset-email.html')

    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
           # current_site=get_current_site(request)
            email_subject='[reset your password]'
            message=render_to_string('user/reset-user-password.html',{
                'domain':'//127.0.0.1:8000/',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])

            })
            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.info(request,'we send you an email ')
            return render(request,'user/request-reset-email.html')
        else:
            messages.error(request,'There is no user with that email address.')
            return render(request,'user/request-reset-email.html')
        
            
#====================================================================
class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,'password reset link is invalid')
                return render(request,'user/request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass
        return render(request,'user/set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token': token
        }
        password=request.POST['password1']
        confirm_password=request.POST['password2']
        if password != confirm_password:
            messages.warning(request,'password is not matching')
            return render(request,'user/set-new-password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successful')
            return redirect('log_in')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,'something went wrong')
            return render(request,'user/set-new-password.html',context)

        return render(request,'user/set-new-password.html',context)

#====================================================================
def user_dashboard(request):
    if request.user.is_authenticated:
          
        user_form = UserRegisterForm()
        user_details_form = UserDetailsForm()
        address_form = AddressForm()
        context = {'user_form': user_form, 'user_details_form': user_details_form, 'address_form': address_form}
        return render(request, 'user/user_details.html', context)
    else:
        return redirect('home')
#======================================================
def user_profile(request):
    try:
        user_details = request.user.userdetails
        address = user_details.address_set.first()
    except UserDetails.DoesNotExist:
        user_details = None
        address = None
    context = {
        'user_details': user_details,
        'address': address
    }
    return render(request, 'user/user_profile.html', context)

#=================================================

#============================================

def edit_user_profile(request):
    user_details = UserDetails.objects.filter(user=request.user).first()
    if user_details:
        address = user_details.address_set.first()
    else:
        user_details = UserDetails(user=request.user)
        address = None

    if request.method == 'POST':
        user_details_form = UserDetailsForm(request.POST, instance=user_details)
        address_form = AddressForm(request.POST, instance=address)
        if user_details_form.is_valid() and address_form.is_valid():
            user_details = user_details_form.save(commit=False)
            address = address_form.save(commit=False)
            user_details.user = request.user
            user_details.save()
            if not address:
                address = Address(user_details=user_details)
            address.user_details = user_details
            address.save()
            return redirect('user_profile')
    else:
        user_details_form = UserDetailsForm(instance=user_details)
        if not address:
            address = Address(user_details=user_details)
        address_form = AddressForm(instance=address)

    context = {
        'user_details_form': user_details_form,
        'address_form': address_form
    }

    return render(request, 'user/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})

#=========================================
@login_required
def user_address(request):
    user_details = UserDetails.objects.get(user=request.user)
    addresses = Address.objects.filter(user_details=user_details)
    return render(request, 'user/user_address.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            user_details = UserDetails.objects.get(user=request.user)
            address.user_details = user_details
            address.save()
            return redirect('user_address')
    else:
        form = AddressForm()
    return render(request, 'user/add_address.html', {'form': form})


@require_POST
def delete_address(request, address_id):
    try:
        # Get the address object and check if it belongs to the current user
        address = Address.objects.get(id=address_id, user_details__user=request.user)
    except Address.DoesNotExist:
        # Return a 404 response if the address object does not exist or does not belong to the current user
        return HttpResponseNotFound()

    # Delete the address object and redirect to the address list page
    address.delete()
    return redirect('user_address')
  

# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-id')

#     context = {
#         'orders': orders
#     }
#     return render(request, 'order_history.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render





import json

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # convert shipping_address JSONField data to dictionary
    for order in orders:
        order.shipping_address = json.loads(order.shipping_address)

   

        context = {
            'orders': page_obj,
            
          }
    return render(request, 'order_history.html', context)





def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('check_out')
    else:
        form = AddressForm(instance=address)
    return render(request, 'edit_address.html', {'form': form})