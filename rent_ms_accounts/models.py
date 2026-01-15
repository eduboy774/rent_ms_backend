import uuid
from django.db import models
from django.contrib.auth.models import User

PROFILE_LEVEL = (
    ('REGION',  'REGION'),
    ('DISTRICT', 'DISTRICT'),
)

USER_PROFILES_TYPES = (
    ('ADMIN_PROFILE', 'ADMIN_PROFILE'),
    ('NORMAL_PROFILE', 'NORMAL_PROFILE'),
)

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)


class UsersProfiles(models.Model):
    id = models.AutoField(primary_key=True)
    profile_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    profile_type = models.CharField(choices=USER_PROFILES_TYPES, max_length=9000, blank=True,null=True)
    profile_level = models.CharField(choices=PROFILE_LEVEL, max_length=9000, blank=True,null=True)
    profile_phone = models.CharField(default='', max_length=9000, blank=True,null=True)
    profile_title = models.CharField(default='', max_length=9000, blank=True,null=True)
    profile_photo = models.CharField(default='/profiles/user_profile.png', max_length=600, blank=True,null=True)
    profile_gender = models.CharField(max_length=100 , null=True , choices=GENDER_CHOICES)
    profile_user = models.ForeignKey(User, related_name='profile_user', on_delete=models.CASCADE, blank=True)
    profile_is_active = models.BooleanField(default=True)
    profile_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'vilcom_user_profiles'
        ordering = ['-id']
        verbose_name_plural = "USER PROFILES"

    def __str__(self):
        return "{}-{}".format(self.profile_title, self.profile_user)


class ForgotPasswordRequestUsers(models.Model):
    id = models.AutoField(primary_key=True)
    request_user = models.ForeignKey(User, related_name='request_profile', on_delete=models.CASCADE)
    request_token = models.CharField(max_length=300, editable=False, default=None)
    request_is_used = models.BooleanField(default=False)
    request_is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'vilcom_users_forgot_password_request'
        ordering = ['-id']
        verbose_name_plural = "FORGOT PASSWORD REQUESTS"

    def __str__(self):
        return "{} - {}".format(self.request_user, self.request_token)