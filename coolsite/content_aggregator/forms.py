from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField
from django.template.defaultfilters import register

from .models import *


class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 20:
            raise ValidationError('Слишком длинное название статьи')
        return title


class RegistrationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }



class LoginUserForm(AuthenticationForm):
    pass


class UserCategoriesForm(forms.ModelForm):
    user_category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                   widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = UserProfile
        fields = ('user_category',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'email': 'Email'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'profile__input'}),
            'last_name': forms.TextInput(attrs={'class': 'profile__input'}),
            'email': forms.EmailInput(attrs={'class': 'profile__input'}),
        }