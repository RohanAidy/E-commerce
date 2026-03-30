from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import category, product, Cart, CartItem, Order, OrderItem, Review, Wishlist

# CustomUser forms temporarily commented out
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     phone = forms.CharField(max_length=20, required=False)
#     address = forms.CharField(widget=forms.Textarea, required=False)
#     city = forms.CharField(max_length=100, required=False)
#     postal_code = forms.CharField(max_length=20, required=False)
#     country = forms.CharField(max_length=100, required=False)
#     date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
#                   'phone', 'address', 'city', 'postal_code', 'country', 'date_of_birth')

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(label='Email')
    
#     class Meta:
#         fields = ('username', 'password')

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'country', 'date_of_birth')
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'})
#         }
