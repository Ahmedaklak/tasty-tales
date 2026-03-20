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
            'status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 6}),
            'instructions': forms.Textarea(attrs={'rows': 8}),
        }


class ReviewForm(forms.ModelForm):
    """Form for submitting a review on a recipe."""

    class Meta:
        model = Review
        fields = ['rating', 'body']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts on this recipe...',
            }),
        }
        labels = {
            'rating': 'Your Rating',
            'body': 'Your Review',
        }