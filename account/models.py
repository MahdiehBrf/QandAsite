from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from notifications.signals import notify
from polymorphic.models import PolymorphicModel
from django.urls import reverse

from QandAsite import settings

DEGREE_CHOICES = (
    ('A.A.', 'دانشیار هنر'),
    ('A.S.', 'دانشیار علوم'),
    ('B.A.', 'لیسانس هنر'),
    ('B.S.', 'لیسانس علوم'),
    ('M.A.', 'فوق لیسانس هنر'),
    ('M.S.', 'فوق لیسانس علوم'),
    ('Ph.D.', 'دکترا'),
)

NOTIF_TYPE = ['question', 'answer', 'comment', 'edit', 'follow', 'request', 'vote']


class Topic(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='topic_images/', default='avatars/default-image.png', null=True, blank=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default-image.png', null=True, blank=True)
    bio = RichTextField(null=True)
    first_login = models.BooleanField(default=True)

    followees = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    topics = models.ManyToManyField(Topic, related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Credential(PolymorphicModel):
    pass


class MainCredential(Credential):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    text = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = (('user'),)

    def __str__(self):
        return self.text


class Employment(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    position = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(null=True)
    is_current_job = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'company_name', 'position', 'start_year'),)

    def __str__(self):
        return ('(شغل فعلی) ' if self.is_current_job else '') + self.position + ' در ' + self.company_name + ' (' + str(self.start_year) + '-' + str(self.end_year) + ')'


class Educational(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    school = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    degree = models.CharField(max_length=5, choices=DEGREE_CHOICES, default='1', blank=False)
    graduation_year = models.IntegerField(blank=False)

    class Meta:
        unique_together = (('user', 'school', 'field', 'degree'),)

    def __str__(self):
        return self.get_degree_display() + ' ' + self.field + ' در ' + self.school + (' (' + str(self.graduation_year) + ') ' if self.graduation_year is not None else '')


class Language(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = (('user', 'name'),)

    def __str__(self):
        return 'آشنایی با ' + self.name


class Location(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=30)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(null=True)
    is_current_location = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'name', 'start_year'),)

    def __str__(self):
        return ('(مکان فعلی) ' if self.is_current_location else '') + 'سکونت در ' + self.name + ' (' + str(self.start_year) + '-' + str(self.end_year) + ')'


class Experience(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=False)

    class Meta:
        unique_together = (('user', 'topic'),)

    def __str__(self):
        return 'تجربه در موضوع ' + str(self.topic) + ' : ' + self.description


class Question(models.Model):
    asker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    description = RichTextField(null=True, blank=False)
    title = models.CharField(max_length=1000, blank=False, unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_followees')
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='edits')
    topics = models.ManyToManyField(Topic, related_name='questions')

    def __str__(self):
        return self.title


@receiver(post_save, sender=Question)
def question_handler(sender, instance, created, **kwargs):
    instance.followers.add(instance.asker)


@receiver(post_save, sender=Question)
def question_notifier(sender, instance, created, **kwargs):
    if created:
        for follower in instance.asker.followers.all():
            notify.send(sender= instance.asker, recipient=follower, verb=" پرسید سوال ", target=instance, href=reverse('account:question', args={instance.id}), sender_href=reverse('account:profile', args={instance.asker.id}), type='questions')


@receiver(m2m_changed, sender=Question.editors.through)
def question_edit_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        editor = User.objects.get(id=pk_set.pop())
        if editor != instance.asker:
            notify.send(sender=editor, recipient=instance.asker, verb=" ویرایش کرد سوال ", target=instance, href=reverse('account:question', args={instance.id}), sender_href=reverse('account:profile', args={editor.id}), type='edits')


@receiver(m2m_changed, sender=Question.followers.through)
def question_follow_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        follower = User.objects.get(id=pk_set.pop())
        if follower != instance.asker:
            notify.send(sender=follower, recipient=instance.asker, verb=" پیروی کرد سوال ", target=instance, href=reverse('account:question', args={instance.id}), sender_href=reverse('account:profile', args={follower.id}), type='follows')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False)
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    text = RichTextField(blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    credential = models.ForeignKey(Credential, on_delete=models.CASCADE, null=True)
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
                notify.send(sender=instance.responder, recipient=follower, verb=" پاسخ داد به ", action_object=instance, target=instance.question, href=reverse('account:question', args={instance.question.id}) + "#a-" + str(instance.id), sender_href=reverse('account:profile', args={instance.responder.id}), type='answers')


@receiver(m2m_changed, sender=Answer.voters.through)
def answer_vote_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        voter = User.objects.get(id=pk_set.pop())
        if voter != instance.responder:
            notify.send(sender=voter, recipient=instance.responder, verb=" رای داد به پاسخ شما به ", target=instance.question, href=reverse('account:question', args={instance.question.id}) + "#a-" + str(instance.id), sender_href=reverse('account:profile', args={voter.id}), type='votes')


@receiver(m2m_changed, sender=Answer.shareholders.through)
def answer_share_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        shareholder = User.objects.get(id=pk_set.pop())
        if shareholder != instance.responder:
            notify.send(sender=shareholder, recipient=instance.responder, verb=" به اشتراک گذاشت پاسخ شما را به سوال ", target=instance.question, href=reverse('account:question', args={instance.question.id}) + "#a-" + str(instance.id), sender_href=reverse('account:profile', args={shareholder.id}), type='votes')


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
        notify.send(sender=instance.asker, recipient=instance.askee, verb=" درخواست پاسخ فرستاد برای شما برای سوال ", target=instance.question, href=reverse('account:question', args={instance.question.id}), sender_href=reverse('account:profile', args={instance.asker.id}), type='requests')


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
            notify.send(sender=instance.commenter, recipient=instance.answer.responder, verb=" نظر داد به پاسخ شما به سوال ", target=instance.answer.question, href=reverse('account:question', args={instance.answer.question.id}) + "#c-" + str(instance.id), sender_href=reverse('account:profile', args={instance.commenter.id}), type='comments')


@receiver(m2m_changed, sender=AnswerComment.voters.through)
def answer_comment_vote_notifier(sender, action, instance, pk_set, **kwargs):
    if action == "post_add" and pk_set != set():
        voter = User.objects.get(id=pk_set.pop())
        if voter != instance.commenter:
            notify.send(sender=voter, recipient=instance.commenter, verb=" رای داد به نظر شما به پاسخ سوال ", target=instance.answer.question, href=reverse('account:question', args={instance.answer.question.id}) + "#c-" + str(instance.id), sender_href=reverse('account:profile', args={voter.id}), type='votes')
