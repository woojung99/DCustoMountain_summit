from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginForm, SignupForm, ProfileForm 
from users.models import User 
from mountains.models import Mountain
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.urls import reverse

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
    context = {
        "user" : user, 
    }
    return render(request, "users/mypage.html", context)

def profile(request, user_id):
    user = get_object_or_404(User, id = user_id)
    context = {
        "user" : user, 
        "request_user" : request.user, 
    }
    return render(request, "users/profile.html", context)

@login_required 
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

def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id = user_id)
    if target_user in user.following.all():
        user.following.remove(target_user)
    else:
        user.following.add(target_user)
    url_next = request.GET.get("next") or reverse("users:profile", args=[user.id])
    return redirect(url_next)

@login_required 
def report_user(request, user_id): 
    reported_user = get_object_or_404(User, id = user_id)
    reported_user.report_user() 
    messages.success(request, f"{reported_user.username} 님을 신고했습니다.")
    return redirect("users:profile", user_id=user_id)

