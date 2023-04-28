from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserDetails, Address


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['full_name', 'mobile_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
         }
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','mobile','house_name', 'street', 'district', 'state', 'pincode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
            'house_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your house name'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your street'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your district'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your state'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your pincode'}),
        }

class UserDashboardForm(forms.Form):
    full_name = forms.CharField(required=True)
    mobile_number = forms.CharField(required=True)
    house_name = forms.CharField(required=True)
    street = forms.CharField(required=True)
    district = forms.CharField(required=True)
    state = forms.CharField(required=True)
    pincode = forms.CharField(required=True)

    def save(self, user):
        address_form = AddressForm(self.cleaned_data)
        address = address_form.save()

        user_details_form = UserDetailsForm(self.cleaned_data)
        user_details_form.instance.user = user
        user_details_form.instance.address = address
        user_details = user_details_form.save()

        return user_details

    def update(self, user_details):
        address = user_details.address
        address_form = AddressForm(self.cleaned_data, instance=address)
        address = address_form.save()

        user_details_form = UserDetailsForm(self.cleaned_data, instance=user_details)
        user_details_form.instance.address = address
        user_details = user_details_form.save()

        return user_details
    




class CustomPasswordChangeForm(PasswordChangeForm):
   
    pass























"""from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserDetails, Address


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['full_name', 'mobile_number']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['house_name', 'street', 'district', 'state', 'pincode']"""