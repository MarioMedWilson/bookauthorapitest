from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Author(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)


class Page(models.Model):
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    content = models.TextField()

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Page.objects.all().aggregate(largest=models.Max('number'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.number = last_id + 1

        super(Page, self).save(*args, **kwargs)

