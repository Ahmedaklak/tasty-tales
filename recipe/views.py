from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Recipe, Review
from .forms import RecipeForm, ReviewForm


class RecipeList(generic.ListView):
    """Display all published recipes on the home page."""

    model = Recipe
    queryset = Recipe.objects.filter(status=1)  # status=1 is "Published", so drafts stay hidden from public listing.
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6


class RecipeDetail(generic.DetailView):
    """Display a single recipe's full details and its reviews."""

    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        # Only show the form if user is logged in and hasn't already reviewed
        if self.request.user.is_authenticated:
            has_reviewed = self.object.reviews.filter(
                author=self.request.user
            ).exists()
            if not has_reviewed:
                context['review_form'] = ReviewForm()  # UI guard for one-review-per-user; DB constraint still enforces it.
        return context


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    """Allow logged-in users to create a new recipe."""

    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/recipe_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Never trust client input for ownership.
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
        return self.request.user == recipe.author  # UserPassesTestMixin returns 403 when this fails.

    def get_success_url(self):
        return reverse_lazy(
            'recipe_detail', kwargs={'slug': self.object.slug}  # Redirect to canonical detail URL after edit.
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


@login_required
def review_create(request, slug):
    """Allow logged-in users to submit a review for a recipe."""

    recipe = get_object_or_404(Recipe, slug=slug)

    # Prevent duplicate reviews
    if Review.objects.filter(recipe=recipe, author=request.user).exists():
        messages.warning(request, 'You have already reviewed this recipe.')
        return redirect(reverse('recipe_detail', kwargs={'slug': slug}))  # Early exit avoids duplicate validation/save work.

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Need recipe/author first since they aren't form fields.
            review.recipe = recipe
            review.author = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.error(request, 'Error submitting review. Please check your input.')

    return redirect(reverse('recipe_detail', kwargs={'slug': slug}))


@login_required
def review_delete(request, slug, review_id):
    """Allow review authors to delete their own review."""

    review = get_object_or_404(Review, id=review_id)

    # Only the review author can delete it
    if request.user != review.author:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect(reverse('recipe_detail', kwargs={'slug': slug}))

    if request.method == 'POST':
        review.delete()  # Keep destructive action POST-only to avoid accidental deletes from link prefetch/crawlers.
        messages.success(request, 'Review deleted successfully!')

    return redirect(reverse('recipe_detail', kwargs={'slug': slug}))