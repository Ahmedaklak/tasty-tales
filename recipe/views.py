from django.http import HttpResponse
from django.views import generic
from .models import Recipe


def home_page_view(_request):
    return HttpResponse("Recipe Home Page")


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1)
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 6


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"
    slug_field = "slug"
    slug_url_kwarg = "slug"


def recipe_edit(_request, slug):
    return HttpResponse(f"Edit page for {slug} (not implemented yet)")


def recipe_delete(_request, slug):
    return HttpResponse(f"Delete page for {slug} (not implemented yet)")