from django.shortcuts import render, redirect, get_object_or_404
from mountains.forms import FilterForm
from mountains.models import Mountain
from django.core.paginator import Paginator

def infopage(request): 
    form = FilterForm(request.GET or None)
    mountains = Mountain.objects.all()
    location = request.GET.get("location", None)
    difficulty = request.GET.get("height", None)
    leadtime = request.GET.get("leadtime", None)
    if location:
        mountains = mountains.filter(location__contains=location)
    if difficulty:
        height = int(difficulty) 
        mountains = mountains.filter(height__gte=height - 500, height__lt=height) 
    if leadtime: 
        mountains = mountains.filter(leadtime=leadtime)
    mountains = mountains.distinct() 

    if not mountains.exists():
        message = "검색 결과가 없습니다."
    else:
        message = None

    # 페이지네이션 설정: 한 페이지에 9개씩
    paginator = Paginator(mountains, 9)  # 한 페이지에 9개씩
    page_number = request.GET.get('page')  # 페이지 번호
    page_obj = paginator.get_page(page_number)
    context = {
        "form" : form, 
        "mountains" : mountains, 
        "message": message,
        "page_obj": page_obj,
    }
    return render(request, "mountains/infopage.html", context)

def mountain_detail(request, mountain_id): 
    mountain = get_object_or_404(Mountain, id = mountain_id) 
    context = {"mountain" : mountain}
    return render(request, "mountains/mountain_detail.html", context)

