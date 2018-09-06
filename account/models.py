from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from QandAsite import settings

DEGREE_CHOICES = (
    ('A.A.', 'Associate of Arts'),
    ('A.S.', 'Associate of Science'),
    ('B.A.', 'Bachelor of Arts'),
    ('B.S.', 'Bachelor of Science'),
    ('M.A.', 'Master of Arts'),
    ('M.S.', 'Master of Science'),
    ('Ph.D.', 'Doctoral'),
)


class Topic(models.Model):
    name = models.CharField(max_length=30)

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
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    followers = models.ManyToManyField('self', related_name='followees')
    topics = models.ManyToManyField(Topic, related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Question(models.Model):
    asker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    description = RichTextField(blank=False, unique=True)
    title = models.CharField(max_length=1000, blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followees')
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='edits')
    topics = models.ManyToManyField(Topic, related_name='questions')

    def __str__(self):
        return "سوال " + str(self.asker) + " درمورد: " + self.title


@receiver(post_save, sender=Question)
def my_handler(sender, instance, created, **kwargs):
    instance.followers.add(instance.asker)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False)
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    text = RichTextField(blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='votes')
    bookmarkers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarks')
    shareholders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shares')

    def __str__(self):
        return "پاسخ " + str(self.responder) + " به: " + str(self.question)


@receiver(post_save, sender=Answer)
def my_handler(sender, instance, created, **kwargs):
    for follower in instance.question.followers.all():
        notify.send(sender= instance.responder, recipient=follower, verb=" پاسخ داد به ", action_object=instance, target=instance.question)


class AnswerRequest(models.Model):
    asker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='asks', on_delete=models.CASCADE, blank=False)
    askee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='is_asked', on_delete=models.CASCADE, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.asker.get_full_name() + " asks " + self.question + " from " + self.askee.get_full_name()

    class Meta:
        unique_together = (('asker', 'askee', 'question'),)


class AnswerComment(models.Model):
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=False)

    text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.commenter) + "'s comment on " + str(self.answer)


class Credential(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)

    class Meta:
        abstract = True


class Employment(Credential):
    position = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(null=True)
    is_current_job = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'company_name', 'position', 'start_year'),)


class Educational(Credential):
    school = models.CharField(max_length=30)
    field = models.CharField(max_length=30)
    degree = models.CharField(max_length=5, choices=DEGREE_CHOICES, default='1', blank=False)
    graduation_year = models.IntegerField(blank=False)

    class Meta:
        unique_together = (('user', 'school', 'field', 'degree'),)


class Language(Credential):
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = (('user', 'name'),)


class Location(Credential):
    name = models.CharField(max_length=30)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(null=True)
    is_current_location = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'name', 'start_year'),)


class Experience(Credential):
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=False)

    class Meta:
        unique_together = (('user', 'topic'),)
