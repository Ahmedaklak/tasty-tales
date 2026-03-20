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
        default=1  # Defaults to published so new recipes show up unless explicitly saved as draft.
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']  # Newest-first ordering is relied on by list/detail tests and UI expectations.

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Only auto-generate once so edited titles don't break existing URLs.
        super().save(*args, **kwargs)


class Review(models.Model):
    """Model representing a user review/rating for a recipe."""

    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        help_text='Rate the recipe from 1 to 5'
    )
    body = models.TextField(
        help_text='Write your review here'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        # Prevent a user from reviewing the same recipe twice
        unique_together = ('recipe', 'author')  # DB-level guard to stop duplicate reviews even if view checks are bypassed.

    def __str__(self):
        return f'{self.author.username} rated {self.recipe.title} - {self.rating}/5'