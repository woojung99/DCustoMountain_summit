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
#    keyword = request.GET.get("keyword", None)
#    print(keyword)
#    print(request.GET) # request.GET으로 전달된 데이터를 출력
    mtn_difficulty = request.GET.get("mtn_difficulty", None) # 난이도 intermediate
    location = request.GET.get("location", None) # 지역 Seoul
    leadtime = request.GET.get("leadtime", None) # 소요시간 3to5
    mtn_name = request.GET.get("mtn_name", None) # 산이름 산이름오나7

    # Mountain 테이블에서 모든 데이터를 가져온 후 필터링 적용
    query = Mountain.objects.all()

    # 난이도 필터
    if mtn_difficulty and mtn_difficulty != '상관없음':
        query = query.filter(mtn_difficulty=mtn_difficulty)

    # 지역 필터
    if location and location != '00':  # '00'은 선택 안 함
        query = query.filter(location__icontains=location)

    # 소요시간 필터
    if leadtime and leadtime != 'no_matter':  # 'no_matter'는 선택 안 함
        query = query.filter(leadtime=leadtime)

    # 산 이름 필터
    if mtn_name:
        query = query.filter(mtn_name__icontains=mtn_name)

    # 최종 검색 결과
    search_result_list = query.distinct()  # 중복 제거

    print('----- 검색 결과 -----')
    print(search_result_list)
    print(len(search_result_list))
    print(search_result_list[0].mtn_difficulty)

    return render(request, "mountains/search_mtn_info.html")

def search_mtn_details(request, pk):


    return render(request, "mountains/search_mtn_details.html")