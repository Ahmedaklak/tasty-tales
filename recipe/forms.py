from django import forms
from .models import Recipe


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