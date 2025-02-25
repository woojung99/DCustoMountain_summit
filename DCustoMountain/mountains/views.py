from django.shortcuts import render, redirect
from mountains.forms import FilterForm
from mountains.models import Mountain
from django.urls import reverse

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

def experienced(request, mountain_id): 
    mountain = Mountain.objects.get(id = mountain_id)
    print(mountain) 
    user = request.user 
    if user.experienced_mountains.filter(id = mountain.id).exists(): 
        user.experienced_mountains.remove(mountain) 
    else: 
        user.experienced_mountains.add(mountain) 
    url_next = request.GET.get("next") or reverse("mountains:filter")
    return redirect(url_next)

def search_mtn_info(request):
    return render(request, "mountains/search_mtn_info.html")