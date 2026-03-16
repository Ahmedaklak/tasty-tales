from django.urls import path
from .views import (
    home_page_view,
    RecipeList,
    RecipeDetail,
    recipe_edit,
    recipe_delete,
)

urlpatterns = [
    path("", home_page_view, name="home"),
    path("recipes/", RecipeList.as_view(), name="recipe_list"),
    path("recipes/<slug:slug>/", RecipeDetail.as_view(), name="recipe_detail"),
    path("recipes/<slug:slug>/edit/", recipe_edit, name="recipe_edit"),
    path("recipes/<slug:slug>/delete/", recipe_delete, name="recipe_delete"),
]