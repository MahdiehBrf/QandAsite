from django.forms import ModelForm

from account.models import User, Employment, Educational, Language, Location, Experience, Topic


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('avatar', )


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


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ('image', )
