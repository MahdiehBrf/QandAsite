from django.forms import ModelForm

from account.models import User


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

