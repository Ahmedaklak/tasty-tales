from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Recipe
from .forms import RecipeForm


class RecipeList(generic.ListView):
    """Display all published recipes on the home page."""

    model = Recipe
    queryset = Recipe.objects.filter(status=1)
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6


class RecipeDetail(generic.DetailView):
    """Display a single recipe's full details."""

    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    """Allow logged-in users to create a new recipe."""

    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/recipe_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, 'Recipe created successfully!'
        )
        return super().form_valid(form)


class RecipeEdit(LoginRequiredMixin, UserPassesTestMixin,
                 generic.UpdateView):
    """Allow recipe authors to edit their own recipes."""

    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/recipe_form.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def get_success_url(self):
        return reverse_lazy(
            'recipe_detail', kwargs={'slug': self.object.slug}
        )

    def form_valid(self, form):
        messages.success(
            self.request, 'Recipe updated successfully!'
        )
        return super().form_valid(form)


class RecipeDelete(LoginRequiredMixin, UserPassesTestMixin,
                   generic.DeleteView):
    """Allow recipe authors to delete their own recipes."""

    model = Recipe
    template_name = 'recipe/recipe_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Recipe deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)