from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginForm, SignupForm, ProfileForm 
from users.models import User 
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from cal.utils import Calendar 
from cal.models import Event 
from mountains.forms import FilterForm 
from mountains.models import Mountain

# Create your views here.
def login_view(request): 
    if request.user.is_authenticated: 
        return redirect("community:feeds")
    if request.method == "POST": 
        form = LoginForm(data = request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user: 
                login(request, user) 
                return redirect("community:feeds")
            else: 
                form.add_error(None, "User information incorrect.")
        context = {"form" : form}
        return render(request, "users/login.html", context)
    else: 
        form = LoginForm() 
        context = {"form" : form}
        return render(request, "users/login.html", context)

def logout_view(request): 
    logout(request) 
    return redirect("users:login")

def signup(request): 
    if request.method == "POST": 
        form = SignupForm(data = request.POST, files = request.FILES) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user) 
            return redirect("community:feeds")
        context = {"form" : form}
        return render(request, "users/signup.html", context)
    else: 
        form = SignupForm() 
        context = {"form" : form}
        return render(request, "users/signup.html", context)
    
def mypage(request, user_id): 
    user = get_object_or_404(User, id = user_id)
    if not request.user.is_authenticated: 
        return redirect("users:login")
    elif user != request.user: 
        url_next = request.GET.get("next") or reverse("users:mypage", args=[request.user.id])
        return redirect(url_next)
    user_events = Event.objects.filter(user=request.user)
    cal = Calendar() 
    total_distance = cal.total_distance(contents=user_events) 
    total_duration = cal.total_duration(contents=user_events) 
    context = {
        "user" : user, 
        "total_distance" : total_distance, 
        "total_duration" : total_duration, 
    }
    return render(request, "users/mypage.html", context)

def profile(request, user_id):
    user = get_object_or_404(User, id = user_id)
    context = {
        "user" : user, 
        "request_user" : request.user, 
    }
    return render(request, "users/profile.html", context)

def edit_profile(request, user_id): 
    if request.method == "POST": 
        form = ProfileForm(request.POST, request.FILES, instance=request.user) 
        if form.is_valid(): 
            form.save() 
            return redirect("users:profile", user_id=request.user.id)
    else: 
        form = ProfileForm(instance=request.user)
    context = {"form" : form}
    return render(request, "users/edit_profile.html", context)

def like_list(request): 
    user = request.user
    posts = user.like_posts.all() 
    context = { 
        "posts" : posts, 
    }
    return render(request, "users/like_list.html", context)

def comment_list(request): 
    user = request.user 
    posts = user.comment_posts.all()
    context = {
        "posts" : posts, 
    }
    return render(request, "users/comment_list.html", context)

def save_list(request): 
    user = request.user 
    posts = user.save_posts.all() 
    context = {
        "posts" : posts, 
    }
    return render(request, "users/save_list.html", context)

def followers(request, user_id):
    user = get_object_or_404(User, id = user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user" : user,
        "title" : "Followers",
        "relationships" : relationships,
    }
    return render(request, "users/followers.html", context)

def following(request, user_id):
    user = get_object_or_404(User, id = user_id)
    relationships = user.following_relationships.all()
    context = {
        "user" : user,
        "title" : "Following",
        "relationships" : relationships,
    }
    return render(request, "users/following.html", context)

def short_description(request, user_id): 
    user = get_object_or_404(User, id = user_id)
    context = {"user" : user}
    return render(request, "users/short_description.html", context)

def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id = user_id)
    if target_user in user.following.all():
        user.following.remove(target_user)
    else:
        user.following.add(target_user)
    url_next = request.GET.get("next") or reverse("users:profile", args=[user.id])
    return redirect(url_next)

# def follow_me(request, target_user_id): 
#     user = request.user 
#     target_user = get_object_or_404(User, id = target_user_id)
#     if user in target_user.following.all(): 
#         target_user.following.remove(user) 
#     return redirect(reverse("users:followers", args=[user.id]))

def report_user(request, user_id): 
    reported_user = get_object_or_404(User, id = user_id)
    reported_user.report_user() 
    messages.success(request, f"{reported_user.username} 님을 신고했습니다.")
    return redirect("users:profile", user_id=user_id)

def experienced(request, mountain_id): 
    mountain = Mountain.objects.get(id = mountain_id)
    user = request.user 
    if user.experienced_mountains.filter(id = mountain.id).exists(): 
        user.experienced_mountains.remove(mountain) 
    else: 
        user.experienced_mountains.add(mountain) 
    url_next = request.GET.get("next") or reverse("mountains:filter")
    return redirect(url_next)

def wish(request, mountain_id): 
    mountain = Mountain.objects.get(id = mountain_id)
    user = request.user 
    if user.wish_mountains.filter(id = mountain.id).exists(): 
        user.wish_mountains.remove(mountain) 
    else: 
        user.wish_mountains.add(mountain) 
    url_next = request.GET.get("next") or reverse("mountains:filter")
    return redirect(url_next)

def experienced_list(request): 
    user = request.user 
    mountains = user.experienced_mountains.all() 
    context = {
        "mountains" : mountains, 
    }
    return render(request, "users/experienced_list.html", context)

def wish_list(request): 
    user = request.user 
    mountains = user.wish_mountains.all() 
    context = {
        "mountains" : mountains, 
    }
    return render(request, "users/wish_list.html", context)

def add_experienced(request):
    form = FilterForm(request.GET or None)
    mountains = Mountain.objects.all()
    location = request.GET.get("location", None)
    difficulty = request.GET.get("difficulty", None)
    leadtime = request.GET.get("leadtime", None)
    if location:
        mountains = mountains.filter(location__contains=location)
    if difficulty:
        height = int(difficulty) 
        mountains = mountains.filter(height__gte=height - 500, height__lt=height) 
    if leadtime: 
        mountains = mountains.filter(leadtime=leadtime)
    context = {
        "form" : form, 
        "mountains" : mountains, 
    }
    return render(request, "users/add_experienced.html", context)

def add_wish(request):
    form = FilterForm(request.GET or None)
    mountains = Mountain.objects.all()
    location = request.GET.get("location", None)
    difficulty = request.GET.get("difficulty", None)
    leadtime = request.GET.get("leadtime", None)
    if location:
        mountains = mountains.filter(location__contains=location)
    if difficulty:
        height = int(difficulty) 
        mountains = mountains.filter(height__gte=height - 500, height__lt=height) 
    if leadtime: 
        mountains = mountains.filter(leadtime=leadtime)
    context = {
        "form" : form, 
        "mountains" : mountains, 
    }
    return render(request, "users/add_wish.html", context)

def distance_list(request): 
    user_events = Event.objects.filter(user=request.user).order_by('-hikedate')
    context = {"user_events" : user_events}
    return render(request, "users/distance_list.html", context)

def duration_list(request): 
    user_events = Event.objects.filter(user=request.user).order_by('-hikedate')
    context = {"user_events" : user_events}
    return render(request, "users/duration_list.html", context)
