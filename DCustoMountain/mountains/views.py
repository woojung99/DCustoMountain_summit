from django.shortcuts import render
from .forms import FilterForm
from .models import Mountain

def filter(request):
    form = FilterForm(request.GET or None)
    mountains = Mountain.objects.all()
    location = request.GET.get("location")
    height = request.GET.get("height")
    if location:
        mountains = mountains.filter(location__icontains=location)
    if height:
        height = int(height) 
        mountains = mountains.filter(height__gte=height - 500, height__lt=height) 
    context = {
        "form" : form, 
        "mountains" : mountains, 
    }
    return render(request, "mountains/filter.html", context)