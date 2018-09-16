from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, Form

from account.models import User, Question, Answer


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']


class QForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title']


class AForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('avatar', )

