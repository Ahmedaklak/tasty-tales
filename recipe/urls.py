from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.RecipeList.as_view(),
        name='home'
    ),
        path(
        'recipe/new/',
        views.RecipeCreate.as_view(),
        name='recipe_create'
    ),
    path(
        'recipe/<slug:slug>/',
        views.RecipeDetail.as_view(),
        name='recipe_detail'
    ),
    path(
        'recipe/<slug:slug>/edit/',
        views.RecipeEdit.as_view(),
        name='recipe_edit'
    ),
    path(
        'recipe/<slug:slug>/delete/',
        views.RecipeDelete.as_view(),
        name='recipe_delete'
    ),
    path(
        'recipe/<slug:slug>/review/',
        views.review_create,
        name='review_create'
    ),
    path(
        'recipe/<slug:slug>/review/<int:review_id>/delete/',
        views.review_delete,
        name='review_delete'
    ),
]