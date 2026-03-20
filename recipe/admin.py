# Register your models here.
from django.contrib import admin
from .models import Recipe, Review

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ('title', 'description',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'author', 'rating', 'created_on')
    list_filter = ('rating', 'created_on')
    search_fields = ('author__username', 'body')