from django.db import models
from django.apps import apps
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.urls import reverse

from notifications.signals import notify
from ckeditor.fields import RichTextField

from QandAsite import settings

# User = apps.get_model('account', 'User')
# Credential = apps.get_model('account', 'Credential')


class Question(models.Model):
    asker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    description = RichTextField(null=True, blank=False)
    title = models.CharField(max_length=1000, blank=False, unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_followees')
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='edits')
    topics = models.ManyToManyField('account.Topic', related_name='questions')

    def __str__(self):
        return self.title


@receiver(post_save, sender=Question)
def question_handler(sender, instance, created, **kwargs):
    instance.followers.add(instance.asker)


@receiver(post_save, sender=Question)
def question_notifier(sender, instance, created, **kwargs):
    if created:
        for follower in instance.asker.followers.all():
            notify.send(sender= instance.asker, recipient=follower, verb=" پرسید سوال ", target=instance, href=reverse('QandA:question', args={instance.id}), sender_href=reverse('account:profile', args={instance.asker.id}), type='questions')


@receiver(m2m_changed, sender=Question.editors.through)
def question_edit_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        editor = apps.get_model('account', 'User').objects.get(id=pk_set.pop())
        if editor != instance.asker:
            notify.send(sender=editor, recipient=instance.asker, verb=" ویرایش کرد سوال ", target=instance, href=reverse('QandA:question', args={instance.id}), sender_href=reverse('account:profile', args={editor.id}), type='edits')


@receiver(m2m_changed, sender=Question.followers.through)
def question_follow_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        follower = apps.get_model('account', 'User').objects.get(id=pk_set.pop())
        if follower != instance.asker:
            notify.send(sender=follower, recipient=instance.asker, verb=" پیروی کرد سوال ", target=instance, href=reverse('QandA:question', args={instance.id}), sender_href=reverse('account:profile', args={follower.id}), type='follows')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False)
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    text = RichTextField(blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    credential = models.ForeignKey('account.Credential', on_delete=models.CASCADE, null=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='votes')
    bookmarkers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarks')
    shareholders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shares')

    def __str__(self):
        return str(self.responder) + " به: " + str(self.question)


@receiver(post_save, sender=Answer)
def answer_notifier(sender, instance, created, **kwargs):
    if created:
        for follower in instance.question.followers.all():
            if instance.responder != follower:
                notify.send(sender=instance.responder, recipient=follower, verb=" پاسخ داد به ", action_object=instance, target=instance.question, href=reverse('QandA:question', args={instance.question.id}) + "#a-" + str(instance.id), sender_href=reverse('account:profile', args={instance.responder.id}), type='answers')


@receiver(m2m_changed, sender=Answer.voters.through)
def answer_vote_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        voter = apps.get_model('account', 'User').objects.get(id=pk_set.pop())
        if voter != instance.responder:
            notify.send(sender=voter, recipient=instance.responder, verb=" رای داد به پاسخ شما به ", target=instance.question, href=reverse('QandA:question', args={instance.question.id}) + "#a-" + str(instance.id), sender_href=reverse('account:profile', args={voter.id}), type='votes')


@receiver(m2m_changed, sender=Answer.shareholders.through)
def answer_share_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        shareholder = apps.get_model('account', 'User').objects.get(id=pk_set.pop())
        if shareholder != instance.responder:
            notify.send(sender=shareholder, recipient=instance.responder, verb=" به اشتراک گذاشت پاسخ شما را به سوال ", target=instance.question, href=reverse('QandA:question', args={instance.question.id}) + "#a-" + str(instance.id), sender_href=reverse('account:profile', args={shareholder.id}), type='votes')


class AnswerRequest(models.Model):
    asker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='asks', on_delete=models.CASCADE, blank=False)
    askee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='is_asked', on_delete=models.CASCADE, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.asker.get_full_name() + " asks " + str(self.question) + " from " + self.askee.get_full_name()

    class Meta:
        unique_together = (('asker', 'askee', 'question'),)


@receiver(post_save, sender=AnswerRequest)
def answer_request_notifier(sender, instance, created, **kwargs):
    if created:
        notify.send(sender=instance.asker, recipient=instance.askee, verb=" درخواست پاسخ فرستاد برای شما برای سوال ", target=instance.question, href=reverse('QandA:question', args={instance.question.id}), sender_href=reverse('account:profile', args={instance.asker.id}), type='requests')


class AnswerComment(models.Model):
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=False)

    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_votes')

    def __str__(self):
        return str(self.commenter) + "'s comment on " + str(self.answer)


@receiver(post_save, sender=AnswerComment)
def answer_comment_notifier(sender, instance, created, **kwargs):
    if created:
        if instance.commenter != instance.answer.responder:
            notify.send(sender=instance.commenter, recipient=instance.answer.responder, verb=" نظر داد به پاسخ شما به سوال ", target=instance.answer.question, href=reverse('QandA:question', args={instance.answer.question.id}) + "#c-" + str(instance.id), sender_href=reverse('account:profile', args={instance.commenter.id}), type='comments')


@receiver(m2m_changed, sender=AnswerComment.voters.through)
def answer_comment_vote_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        voter = apps.get_model('account', 'User').objects.get(id=pk_set.pop())
        if voter != instance.commenter:
            notify.send(sender=voter, recipient=instance.commenter, verb=" رای داد به نظر شما به پاسخ سوال ", target=instance.answer.question, href=reverse('QandA:question', args={instance.answer.question.id}) + "#c-" + str(instance.id), sender_href=reverse('account:profile', args={voter.id}), type='votes')
