import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now



class CustomUserManager(UserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_stuff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_ADMIN = 'Admin'
    ROLE_SUPPORT = 'Support'
    ROLE_CUSTOMER = 'Customer'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SUPPORT, 'Support'),
        (ROLE_CUSTOMER, 'Customer'),
    )

    email = models.EmailField('Email address', unique=True, blank=False)
    first_name = models.TextField('First name', max_length=30, blank=False)
    last_name = models.TextField('Last name', max_length=30, blank=False)
    create_date = models.DateTimeField('Create date', default=now, editable=False)
    role = models.TextField('Role', choices=ROLE_CHOICES, max_length=8, default='Customer', blank=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super(CustomUser, self)

    def save(self, *args, **kwargs):
        self.update_date = now()
        return super(CustomUser, self).save(*args, **kwargs)



class Ticket(models.Model):

    DEPARTAMENT_SUPPORT = 'Support'
    DEPARTAMENT_BILLING = 'Billing'
    DEPARTAMENT_SALES = 'Sales'

    DEPARTAMENT_CHOICES = (
        (DEPARTAMENT_SUPPORT, 'Support'),
        (DEPARTAMENT_BILLING, 'Billing'),
        (DEPARTAMENT_SALES, 'Sales'),
    )

    STATUS_ACTIVE = 'Active'
    STATUS_CLOSED = 'Closed'
    STATUS_PENDING = 'Pending'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_PENDING, 'Pending'),
    )

    PRIORITY_LOW = 'Low'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_HIGH = 'High'

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    )

    uuid = models.UUIDField('Public ID', default=uuid.uuid4, editable=False, unique=True)
    subject = models.TextField('Subject', max_length=100, blank=False)
    departament = models.TextField('Departament', max_length=7, choices=DEPARTAMENT_CHOICES, blank=False)
    status = models.TextField('Status', max_length=7, choices=STATUS_CHOICES, blank=False)
    priority = models.TextField('Priority', max_length=6, choices=PRIORITY_CHOICES, blank=False)

    create_date = models.DateTimeField('Create date', default=now, editable=False)
    update_date = models.DateTimeField('Last update date', default=now, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        ordering = ['-create_date']

    def clean(self):
        super(Ticket, self)

    def save(self, *args, **kwargs):
        self.update_date = now()

        super(Ticket, self).save(*args, **kwargs)



class Message(models.Model):

    DIRECTION_INCOMING = 'Incoming'
    DIRECTION_OUTGOING = 'Outgoing'

    DIRECTION_CHOICES = (
        (DIRECTION_INCOMING, 'Incoming'),
        (DIRECTION_OUTGOING, 'Outgoing'),
    )

    uuid = models.UUIDField('Message ID', default=uuid.uuid4, editable=False, unique=True)
    text = models.TextField()
    direction = models.CharField('Direction', max_length=8, choices=DIRECTION_CHOICES, blank=False)

    create_date = models.DateTimeField('Create date', default=now, editable=False)

    ticket = models.ForeignKey(Ticket, default=None, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name='messages')

    def clean(self):
        super(Message, self)

    def save(self, *args, **kwargs):
        self.create_date = now()
        return super(Message, self).save(*args, **kwargs)


