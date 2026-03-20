from django import forms
from .models import Recipe, Review


class RecipeForm(forms.ModelForm):
    """Form for creating and editing recipes."""

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
            'instructions',
            'cooking_time',
            'servings',
            'status',  # Exposed so authors can intentionally save drafts instead of auto-publishing.
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 6}),  # Bigger textarea makes multiline ingredient lists usable.
            'instructions': forms.Textarea(attrs={'rows': 8}),
        }


class ReviewForm(forms.ModelForm):
    """Form for submitting a review on a recipe."""

    class Meta:
        model = Review
        fields = ['rating', 'body']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),  # Forces Bootstrap styling since crispy config can vary by template.
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts on this recipe...',
            }),
        }
        labels = {
            'rating': 'Your Rating',
            'body': 'Your Review',  # Friendlier labels read better than raw model field names.
        }