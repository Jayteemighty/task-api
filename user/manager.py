from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy

class CustomUserManager(BaseUserManager):

    def create(self, email, password, **extras):
        if not email:
            raise ValueError(gettext_lazy('Email field cannot be empty'))

        email = self.normalize_email(email)

        user = self.model(email=email, **extras)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extras):
        
        extras.setdefault('is_active', True)
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)

        if extras.get('is_staff') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_admin=True'))

        if extras.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_superuser=True'))
        
        user = self.create(email, password, **extras)

        return user
        