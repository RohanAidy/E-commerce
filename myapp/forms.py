from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import category, product, Cart, CartItem, Order, OrderItem, Review, Wishlist

# Enhanced User Creation Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=False, help_text='Optional. Enter your phone number.')
    address = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional. Enter your full address.')
    city = forms.CharField(max_length=100, required=False, help_text='Optional. Enter your city.')
    postal_code = forms.CharField(max_length=20, required=False, help_text='Optional. Enter your postal code.')
    country = forms.CharField(max_length=100, required=False, help_text='Optional. Enter your country.')
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), help_text='Optional. Select your date of birth.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                  'phone', 'address', 'city', 'postal_code', 'country', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and help text
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

# Enhanced Authentication Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})

# User Profile Form - Only available fields that exist in Django's default User model
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'})
        }
