from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


STATUS = ((0, 'Draft'), (1, 'Published'))


class Recipe(models.Model):
    """Model representing a recipe shared by a user."""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    description = models.TextField(
        help_text='A short summary of the recipe'
    )
    ingredients = models.TextField(
        help_text='List ingredients, one per line'
    )
    instructions = models.TextField(
        help_text='Step-by-step cooking instructions'
    )
    cooking_time = models.PositiveIntegerField(
        help_text='Cooking time in minutes'
    )
    servings = models.PositiveIntegerField(
        help_text='Number of servings'
    )
    status = models.IntegerField(
        choices=STATUS,
        default=1
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)