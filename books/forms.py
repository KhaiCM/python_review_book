from django import forms
from .models import Comment, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'})
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'})
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'}))
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class BookSearchForm(forms.Form):
    text = forms.CharField(min_length=1, max_length=200)


class AddBookComment(forms.Form):
    comment = forms.Textarea()
    book_id = forms.IntegerField(min_value=1)
