from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class Recipe(models.Model):
    """The Recipe object"""

    # We use the settings to retieve our auth user model, since we created a custom one
    # Cascade makes sure this tag is also removed when user is gone
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Other required fields
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # Optional field
    link = models.CharField(max_length=255, blank=True)

    # A normal foreign key like user; only 1 user can be assigned to a recipe
    # ManyToMany -> Each ingredient and tag can also be assigned other recipes
    # Why use a string as modelname? Because else those models have to be declared above
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    # Representation when you call str(tag)
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)

    # We use the settings to retieve our auth user model, since we created a custom one
    # Cascade makes sure this tag is also removed when user is gone
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Representation when you call str(tag)
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)

    # We use the settings to retieve our auth user model, since we created a custom one
    # Cascade makes sure this tag is also removed when user is gone
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Representation when you call str(tag)
    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    # This overrides the BaseUserManager's create_user method
    # The **extra_fields are just any extra fields, so it's dynamic
    # The optional password=None is for when you want to create a user that is not active
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address..')

        # You access the User model with "self.model"
        # Here you add the email and all other extra fields, so it's dynamic
        # The "normalize_email" also is a Django build in method
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # You'll want to use build in method this since it encrypts the password
        user.set_password(password)

        # The "using=self.db" is required for when using multiple db's and,
        # therefore is good practise to add it.
        user.save(using=self.db)

        return user

    # Don't need to worry about extra fields since only using with command line
    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


# The AbstractBaseUser gives us all the functionality that come with Django's User model
# So we can build on top of them and customize it
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add the UserManager for our objects
    objects = UserManager()

    # Define which field will be used as "username" to login
    USERNAME_FIELD = 'email'
