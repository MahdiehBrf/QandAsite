from django.db import models
from django.apps import apps
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel

from QandAsite import settings

# Topic = apps.get_model('QandA', 'Topic')

DEGREE_CHOICES = (
    ('D.', 'دیپلم'),
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
    image = models.ImageField(upload_to='topic_images/', default='topic_images/default_topic_image.png', null=True, blank=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user2(self, email, password, first_name, last_name, **kwargs):
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
        user = self.create_user2(
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

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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
    end_year = models.IntegerField(null=True, blank=True)
    is_current_job = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'company_name', 'position', 'start_year'),)

    def __str__(self):
        return ('(شغل فعلی) ' if self.is_current_job else '') + self.position + ' در ' + self.company_name + ' (' + str(self.start_year) + ('-' + str(self.end_year) if (self.end_year and self.end_year != self.start_year) else '')  + ')'


class Educational(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    school = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    degree = models.CharField(max_length=5, choices=DEGREE_CHOICES, default='1', blank=False)
    graduation_year = models.IntegerField(null=True, blank=True)

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
    end_year = models.IntegerField(null=True, blank=True)
    is_current_location = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'name', 'start_year'),)

    def __str__(self):
        return ('(مکان فعلی) ' if self.is_current_location else '') + 'سکونت در ' + self.name + ' (' + str(self.start_year) + ('-' + str(self.end_year) if (self.end_year and self.end_year != self.start_year) else '')  + ')'


class Experience(Credential):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    description = models.TextField(blank=False)

    class Meta:
        unique_together = (('user', 'topic'),)

    def __str__(self):
        return 'تجربه در موضوع ' + str(self.topic) + ' : ' + self.description


