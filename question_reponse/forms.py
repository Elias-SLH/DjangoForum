from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Question, Answer


class CustomUserCreationForm(UserCreationForm):
    """User's registering form based on User model + styling for bootstrap"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'width:300px'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['style'] = 'width:300px'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['style'] = 'width:300px'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['style'] = 'width:300px'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password confirmation'


class QuestionForm(forms.ModelForm):
    """Question form based on question model + styling for bootstrap"""
    class Meta:
        model = Question
        fields = ['topic', 'description']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title of your question'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                'placeholder': 'Detailed description of your question'}),
        }


class AnswerForm(forms.ModelForm):
    """Answer form based on Answer model + styling for bootstrap"""
    class Meta:
        model = Answer
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'You can answer the question here'}),
        }
