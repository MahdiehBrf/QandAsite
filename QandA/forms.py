from django.forms import ModelForm

from QandA.models import Question, Answer


class QForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title']


class AForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
