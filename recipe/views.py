from django.http import HttpResponse


# Create your views here.
def home_page_view(_request):
    return HttpResponse("Recipe Home Page")
