from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, Form

from account.models import User, Question, Answer, Employment, Educational, Language, Location, Experience, Topic



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


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ('image', )


class EmploymentForm(ModelForm):
    class Meta:
        model = Employment
        exclude = ['user']


class EducationForm(ModelForm):
    class Meta:
        model = Educational
        exclude = ['user']


class LocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ['user']


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        exclude = ['user']


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ['user']


