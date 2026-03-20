# Testing

This document describes all testing performed on the Tasty Tales application.

## Table of Contents

- [Automated Testing](#automated-testing)
- [Manual Testing](#manual-testing)
- [Validator Testing](#validator-testing)
- [Browser Compatibility](#browser-compatibility)
- [Responsiveness Testing](#responsiveness-testing)
- [Bugs](#bugs)

---

## Automated Testing

24 automated tests were written using Django's built-in `TestCase` framework. They are located in `recipe/tests.py`.

To run all tests:
```
python manage.py test
```

### Test Results

All 24 tests pass with no errors.

### Tests Breakdown

#### Recipe Model Tests (4 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_recipe_str_returns_title | The string representation of a recipe returns its title | Pass |
| test_recipe_slug_is_auto_generated | A slug is automatically generated from the recipe title | Pass |
| test_recipe_ordering_is_newest_first | Recipes are ordered with the newest first | Pass |
| test_recipe_default_status_is_published | New recipes default to published status (1) | Pass |

#### Review Model Tests (3 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_review_str | The string representation includes the username and rating | Pass |
| test_review_unique_together | A user cannot review the same recipe twice (IntegrityError raised) | Pass |
| test_review_ordering_is_newest_first | Reviews are ordered with the newest first | Pass |

#### Recipe List View Tests (3 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_home_page_returns_200 | The home page loads successfully with a 200 status code | Pass |
| test_home_page_uses_correct_template | The home page uses the recipe_list.html template | Pass |
| test_only_published_recipes_shown | Only published recipes appear on the home page; drafts are hidden | Pass |

#### Recipe Detail View Tests (3 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_detail_page_returns_200 | The detail page loads for a valid recipe slug | Pass |
| test_detail_page_shows_recipe_title | The recipe title appears on the detail page | Pass |
| test_detail_page_shows_reviews | The reviews context variable is passed to the template | Pass |

#### Recipe Create View Tests (3 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_logged_out_user_cannot_create | Anonymous users are redirected away from the create page | Pass |
| test_logged_in_user_can_access_create | Logged-in users can access the create recipe form | Pass |
| test_logged_in_user_can_create_recipe | A logged-in user can successfully submit a new recipe | Pass |

#### Recipe Edit/Delete View Tests (4 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_author_can_access_edit | The recipe author can access the edit page | Pass |
| test_non_author_cannot_edit | A different user receives a 403 when trying to edit | Pass |
| test_author_can_delete | The recipe author can delete their own recipe | Pass |
| test_non_author_cannot_delete | A different user cannot delete someone else's recipe | Pass |

#### Review View Tests (5 tests)

| Test | Description | Result |
|------|-------------|--------|
| test_logged_in_user_can_submit_review | A logged-in user can submit a review with a rating | Pass |
| test_logged_out_user_cannot_review | Anonymous users cannot submit reviews | Pass |
| test_user_cannot_review_twice | A user is prevented from reviewing the same recipe twice | Pass |
| test_review_author_can_delete_review | A review author can delete their own review | Pass |
| test_non_author_cannot_delete_review | A user cannot delete someone else's review | Pass |

---

## Manual Testing

Manual testing was performed on every user-facing feature of the application.

### Navigation

| Test | Steps | Expected Result | Actual Result | Pass |
|------|-------|-----------------|---------------|------|
| Logo link | Click "Tasty Tales" in navbar | Redirects to home page | Home page loads | ✅ |
| Login link (logged out) | Click "Login" in navbar | Redirects to login page | Login page loads | ✅ |
| Register link (logged out) | Click "Register" in navbar | Redirects to signup page | Signup page loads | ✅ |
| Add Recipe link (logged in) | Click "+ Add Recipe" in navbar | Redirects to create form | Create form loads | ✅ |
| Logout link (logged in) | Click "Logout" in navbar | Redirects to logout confirmation | Confirmation page loads | ✅ |

### Authentication

| Test | Steps | Expected Result | Actual Result | Pass |
|------|-------|-----------------|---------------|------|
| Register new account | Fill in username and password, click Register | Account created, redirected to home | Account created successfully | ✅ |
| Login with valid credentials | Enter correct username/password, click Login | Logged in, redirected to home with success message | Logged in successfully | ✅ |
| Login with wrong password | Enter incorrect password, click Login | Error message shown, not logged in | Error message displayed | ✅ |
| Logout | Click Logout, confirm on logout page | Logged out, redirected to home | Logged out successfully | ✅ |
| Navbar shows username when logged in | Log in and check navbar | "Hello, [username]" appears | Username displayed | ✅ |

### Recipe CRUD

| Test | Steps | Expected Result | Actual Result | Pass |
|------|-------|-----------------|---------------|------|
| View recipe list | Go to home page | Published recipes shown as cards | Recipes displayed correctly | ✅ |
| View recipe detail | Click a recipe title | Full recipe details shown | All details displayed | ✅ |
| Create recipe | Fill in form, click Create | Recipe created, redirected to home with success message | Recipe created successfully | ✅ |
| Create recipe with empty fields | Submit form with missing required fields | Validation errors shown | Form errors displayed | ✅ |
| Edit own recipe | Click Edit on own recipe, change fields, click Update | Recipe updated with success message | Recipe updated successfully | ✅ |
| Edit button only shown to author | View a recipe you did not create | No Edit/Delete buttons visible | Buttons hidden correctly | ✅ |
| Delete own recipe | Click Delete, confirm on confirmation page | Recipe deleted with success message | Recipe deleted successfully | ✅ |
| Cannot edit other user's recipe | Try accessing /recipe/slug/edit/ for another user's recipe | 403 Forbidden page shown | Access denied correctly | ✅ |
| Cannot delete other user's recipe | Try accessing /recipe/slug/delete/ for another user's recipe | 403 Forbidden page shown | Access denied correctly | ✅ |

### Reviews

| Test | Steps | Expected Result | Actual Result | Pass |
|------|-------|-----------------|---------------|------|
| Submit a review | Fill in rating and body, click Submit | Review appears below recipe with success message | Review displayed correctly | ✅ |
| Star rating displays correctly | Submit a review with rating 4 | Four filled stars and one empty star shown | Stars display correctly | ✅ |
| Cannot review twice | Submit a review then check the form | "You have already reviewed this recipe" shown instead of form | Message displayed correctly | ✅ |
| Delete own review | Click Delete on own review, confirm | Review removed with success message | Review deleted successfully | ✅ |
| Cannot delete other's review | View a review by another user | No Delete button shown | Button hidden correctly | ✅ |
| Review form hidden when logged out | View recipe detail while logged out | "Log in to leave a review" shown instead of form | Login prompt displayed | ✅ |

### Pagination

| Test | Steps | Expected Result | Actual Result | Pass |
|------|-------|-----------------|---------------|------|
| Pagination appears with 7+ recipes | Add more than 6 recipes | Next/Previous buttons appear | Pagination working | ✅ |
| Next page loads correctly | Click "Next" | Page 2 of recipes loads | Second page loads | ✅ |

---

## Validator Testing

### HTML Validation

All pages were tested using the [W3C HTML Validator](https://validator.w3.org/).

| Page | Result |
|------|--------|
| Home page | No errors |
| Recipe detail | No errors |
| Add recipe | No errors |
| Edit recipe | No errors |
| Delete recipe | No errors |
| Register | No errors |
| Login | No errors |
| Logout | No errors |

### CSS Validation

CSS was tested using the [W3C CSS Validator (Jigsaw)](https://jigsaw.w3.org/css-validator/).

| File | Result |
|------|--------|
| style.css | No errors |

### Python Validation

All Python files were checked for PEP8 compliance using the [CI Python Linter](https://pep8ci.herokuapp.com/).

| File | Result |
|------|--------|
| models.py | No errors |
| views.py | No errors |
| forms.py | No errors |
| urls.py | No errors |
| admin.py | No errors |
| tests.py | No errors |
| settings.py | No errors |

### Lighthouse

Lighthouse testing was performed using Chrome DevTools.

| Page | Performance | Accessibility | Best Practices | SEO |
|------|-------------|---------------|----------------|-----|
| Home page | 90+ | 90+ | 90+ | 90+ |
| Recipe detail | 90+ | 90+ | 90+ | 90+ |

---

## Browser Compatibility

The application was tested on the following browsers:

| Browser | Version | Result |
|---------|---------|--------|
| Google Chrome | Latest | All features work correctly |
| Mozilla Firefox | Latest | All features work correctly |
| Microsoft Edge | Latest | All features work correctly |

---

## Responsiveness Testing

The application was tested for responsiveness at the following breakpoints:

| Device / Width | Result |
|----------------|--------|
| Mobile (320px) | Layout stacks to single column, navbar collapses to hamburger menu |
| Tablet (768px) | Cards display in two columns, all elements properly sized |
| Desktop (1200px+) | Cards display in three columns, full navbar visible |

Testing was performed using Chrome DevTools device emulation.

---

## Bugs

### Fixed Bugs

| Bug | Description | Fix |
|-----|-------------|-----|
| Static files not loading on Heroku | CSS returned 404 on production. WhiteNoise was installed but collectstatic was not running during deployment. | Added a `release` phase to the Procfile to run collectstatic automatically on each deploy. |
| Review model indentation error | The Review class was accidentally indented inside the Recipe model's save method, causing an IndentationError. | Moved the Review class to the correct indentation level at the top level of the file. |

### Unfixed Bugs

There are no known unfixed bugs.