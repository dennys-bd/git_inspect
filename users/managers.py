from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, github_id=None, username=None, avatar=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, github_id=github_id, username=username, avatar=avatar, **kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **kwargs):
        user = self.create_user(**kwargs)
        user.username = user.email
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
