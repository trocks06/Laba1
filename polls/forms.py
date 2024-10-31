from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from .models import User
from .models import Question, Choice

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'avatar', 'password1', 'password2')

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'avatar')

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class QuestionForm(forms.ModelForm):
    choices = forms.CharField(widget=forms.Textarea, help_text="Введите варианты ответов, разделенные запятой.")

    class Meta:
        model = Question
        fields = ['question_text', 'question_desc_mini', 'question_desc_full', 'question_image']