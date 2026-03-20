from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Review


class RecipeModelTest(TestCase):
    """Tests for the Recipe model."""

    def setUp(self):
        """Create a test user and recipe for use in tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            author=self.user,
            description='A test description',
            ingredients='Ingredient 1\nIngredient 2',
            instructions='Step 1\nStep 2',
            cooking_time=30,
            servings=4,
            status=1,
        )

    def test_recipe_str_returns_title(self):
        """Test that the string representation returns the title."""
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_recipe_slug_is_auto_generated(self):
        """Test that a slug is automatically created from the title."""
        self.assertEqual(self.recipe.slug, 'test-recipe')

    def test_recipe_ordering_is_newest_first(self):
        """Test that recipes are ordered by newest first."""
        second_recipe = Recipe.objects.create(
            title='Second Recipe',
            author=self.user,
            description='Another test',
            ingredients='Ingredient',
            instructions='Step',
            cooking_time=15,
            servings=2,
            status=1,
        )
        recipes = Recipe.objects.all()
        self.assertEqual(recipes[0], second_recipe)
        self.assertEqual(recipes[1], self.recipe)

    def test_recipe_default_status_is_published(self):
        """Test that new recipes default to published status."""
        self.assertEqual(self.recipe.status, 1)


class ReviewModelTest(TestCase):
    """Tests for the Review model."""

    def setUp(self):
        """Create a test user, recipe, and review."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            author=self.user,
            description='A test description',
            ingredients='Ingredient 1',
            instructions='Step 1',
            cooking_time=30,
            servings=4,
            status=1,
        )
        self.review = Review.objects.create(
            recipe=self.recipe,
            author=self.user,
            rating=5,
            body='Great recipe!',
        )

    def test_review_str(self):
        """Test the string representation of a review."""
        self.assertIn('testuser', str(self.review))
        self.assertIn('5/5', str(self.review))

    def test_review_unique_together(self):
        """Test that a user cannot review the same recipe twice."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                recipe=self.recipe,
                author=self.user,
                rating=3,
                body='Second review attempt',
            )

    def test_review_ordering_is_newest_first(self):
        """Test that reviews are ordered newest first."""
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        second_review = Review.objects.create(
            recipe=self.recipe,
            author=user2,
            rating=4,
            body='Also good!',
        )
        reviews = Review.objects.all()
        self.assertEqual(reviews[0], second_review)
        self.assertEqual(reviews[1], self.review)


class RecipeListViewTest(TestCase):
    """Tests for the home page / recipe list view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Published Recipe',
            author=self.user,
            description='Visible recipe',
            ingredients='Ingredient',
            instructions='Step',
            cooking_time=20,
            servings=2,
            status=1,
        )
        self.draft_recipe = Recipe.objects.create(
            title='Draft Recipe',
            author=self.user,
            description='Hidden recipe',
            ingredients='Ingredient',
            instructions='Step',
            cooking_time=20,
            servings=2,
            status=0,
        )

    def test_home_page_returns_200(self):
        """Test that the home page loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Test that the home page uses the recipe list template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'recipe/recipe_list.html')

    def test_only_published_recipes_shown(self):
        """Test that draft recipes are not shown on the home page."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Published Recipe')
        self.assertNotContains(response, 'Draft Recipe')


class RecipeDetailViewTest(TestCase):
    """Tests for the recipe detail view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Detail Test Recipe',
            author=self.user,
            description='Test description',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=45,
            servings=4,
            status=1,
        )

    def test_detail_page_returns_200(self):
        """Test that the detail page loads for a valid recipe."""
        response = self.client.get(
            reverse('recipe_detail', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_page_shows_recipe_title(self):
        """Test that the recipe title appears on the detail page."""
        response = self.client.get(
            reverse('recipe_detail', kwargs={'slug': self.recipe.slug})
        )
        self.assertContains(response, 'Detail Test Recipe')

    def test_detail_page_shows_reviews(self):
        """Test that reviews are passed to the detail template."""
        response = self.client.get(
            reverse('recipe_detail', kwargs={'slug': self.recipe.slug})
        )
        self.assertIn('reviews', response.context)


class RecipeCreateViewTest(TestCase):
    """Tests for creating a recipe."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_logged_out_user_cannot_create(self):
        """Test that anonymous users are redirected from the create page."""
        response = self.client.get(reverse('recipe_create'))
        self.assertNotEqual(response.status_code, 200)

    def test_logged_in_user_can_access_create(self):
        """Test that logged-in users can access the create form."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipe_create'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_create_recipe(self):
        """Test that a logged-in user can submit a new recipe."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('recipe_create'), {
            'title': 'New Recipe',
            'description': 'A new test recipe',
            'ingredients': 'New ingredients',
            'instructions': 'New instructions',
            'cooking_time': 25,
            'servings': 3,
            'status': 1,
        })
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.first().title, 'New Recipe')


class RecipeEditDeleteViewTest(TestCase):
    """Tests for editing and deleting recipes."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Edit Test Recipe',
            author=self.user,
            description='Original description',
            ingredients='Original ingredients',
            instructions='Original instructions',
            cooking_time=30,
            servings=4,
            status=1,
        )

    def test_author_can_access_edit(self):
        """Test that the recipe author can access the edit page."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('recipe_edit', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_non_author_cannot_edit(self):
        """Test that a different user cannot edit someone else's recipe."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('recipe_edit', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 403)

    def test_author_can_delete(self):
        """Test that the recipe author can delete their recipe."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('recipe_delete', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(Recipe.objects.count(), 0)

    def test_non_author_cannot_delete(self):
        """Test that a different user cannot delete someone else's recipe."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(
            reverse('recipe_delete', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(Recipe.objects.count(), 1)


class ReviewViewTest(TestCase):
    """Tests for review creation and deletion."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Review Test Recipe',
            author=self.user,
            description='Test',
            ingredients='Test',
            instructions='Test',
            cooking_time=30,
            servings=4,
            status=1,
        )

    def test_logged_in_user_can_submit_review(self):
        """Test that a logged-in user can submit a review."""
        self.client.login(username='otheruser', password='testpass123')
        self.client.post(
            reverse('review_create', kwargs={'slug': self.recipe.slug}),
            {'rating': 4, 'body': 'Nice recipe!'}
        )
        self.assertEqual(Review.objects.count(), 1)

    def test_logged_out_user_cannot_review(self):
        """Test that anonymous users cannot submit a review."""
        self.client.post(
            reverse('review_create', kwargs={'slug': self.recipe.slug}),
            {'rating': 4, 'body': 'Nice recipe!'}
        )
        self.assertEqual(Review.objects.count(), 0)

    def test_user_cannot_review_twice(self):
        """Test that a user cannot submit two reviews on the same recipe."""
        self.client.login(username='otheruser', password='testpass123')
        self.client.post(
            reverse('review_create', kwargs={'slug': self.recipe.slug}),
            {'rating': 4, 'body': 'First review'}
        )
        self.client.post(
            reverse('review_create', kwargs={'slug': self.recipe.slug}),
            {'rating': 5, 'body': 'Second review'}
        )
        self.assertEqual(Review.objects.count(), 1)

    def test_review_author_can_delete_review(self):
        """Test that a review author can delete their own review."""
        self.client.login(username='otheruser', password='testpass123')
        review = Review.objects.create(
            recipe=self.recipe,
            author=self.other_user,
            rating=4,
            body='Nice!',
        )
        self.client.post(
            reverse('review_delete', kwargs={
                'slug': self.recipe.slug,
                'review_id': review.id,
            })
        )
        self.assertEqual(Review.objects.count(), 0)

    def test_non_author_cannot_delete_review(self):
        """Test that a user cannot delete someone else's review."""
        review = Review.objects.create(
            recipe=self.recipe,
            author=self.other_user,
            rating=4,
            body='Nice!',
        )
        self.client.login(username='testuser', password='testpass123')
        self.client.post(
            reverse('review_delete', kwargs={
                'slug': self.recipe.slug,
                'review_id': review.id,
            })
        )
        self.assertEqual(Review.objects.count(), 1)