from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment, PostImage, Hashtag
from users.models import User
from community.forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts":posts,
        "comment_form":comment_form,
    }
    return render(request, "community/feeds.html", context)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    context = {
        "post":post,
        "comment_form":comment_form,
    }
    return render(request, "community/post_detail.html", context)

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
<<<<<<< HEAD

            # 전송된 이미지들을 순회하며 PostImage 객체 생성
            for image_file in request.FILES.getlist("images"):
=======
            for image_file in request.FILES.getlist("photo"):
>>>>>>> origin/new_mypage
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )
<<<<<<< HEAD
                print(image_file)
            
            # 문자열로 전달된 해시태그들로 Hashtag 객체 생성하고 post 객체에 추가
=======
>>>>>>> origin/new_mypage
            tag_string = request.POST.get("tags")
            if tag_string:
                tag_name_list = [tag_name.strip() for tag_name in tag_string.split(",")]
                for tag_name in tag_name_list:
                    tag, _ = Hashtag.objects.get_or_create(
                        name=tag_name,
                    )
                    post.tags.add(tag)
            return redirect(reverse("community:post_detail", kwargs={"post_id":post.id}))
    else:
        form = PostForm()
    context = {"form":form}
    return render(request, "community/add_post.html", context)

def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        if post.user == request.user:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                edited_post = form.save()
                return redirect(reverse("community:post_detail", kwargs={"post_id":edited_post.id}))
        else:
            return HttpResponseForbidden("이 게시글을 수정할 권한이 없습니다.")
    else:
        form = PostForm(instance=post)
<<<<<<< HEAD


    context = {
        "form":form,
    }
=======
    context = {"form":form}
>>>>>>> origin/new_mypage
    return render(request, "community/add_post.html", context)

@require_POST
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect("community:feeds")
    else:
        return HttpResponseForbidden("이 게시글을 삭제할 권한이 없습니다.")

@require_POST   
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        url = reverse("community:post_detail", kwargs={"post_id":comment.post.id}) + f"#comment-{comment.id}"
        return redirect(url)

def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST":
        if comment.user == request.user:
            edit_comment_form = CommentForm(request.POST, instance=comment)
            if edit_comment_form.is_valid():
                edited_comment = edit_comment_form.save()
                url = reverse("community:post_detail", kwargs={"post_id":edited_comment.post.id}) + f"#comment-{edited_comment.id}"
                return redirect(url)
        else:
            return HttpResponseForbidden("이 게시글을 수정할 권한이 없습니다.")
    else:
        edit_comment_form = CommentForm(instance=comment)
    post = comment.post
    comment_form = CommentForm()
    context = {
        "post":post,
        "comment":comment,
        "comment_form":comment_form,
        "edit_comment_form":edit_comment_form,
        }
    return render(request, "community/edit_comment.html", context)

@require_POST
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return redirect(reverse("community:post_detail", kwargs={"post_id":comment.post.id}))
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다.")

def tags(request, tag_name):
    try:
        tag = Hashtag.objects.get(name=tag_name)
    except Hashtag.DoesNotExist:
        posts = Post.objects.none()
    else:
        posts = Post.objects.filter(tags=tag)
    context = {
        "tag_name":tag_name,
        "posts":posts,
    }
    return render(request, "community/search_tags.html", context)

def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user.like_posts.filter(id=post.id).exists():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)
    url = reverse("community:feeds") + f"#post-{post.id}"
    return redirect(url)

def save_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user.save_posts.filter(id=post_id).exists():
        user.save_posts.remove(post)
    else:
        user.save_posts.add(post)
    url = reverse("community:feeds") + f"#post-{post.id}"
    return redirect(url)

def report_post(request, post_id): 
    post = Post.objects.get(id=post_id)
    user = request.user
    reported_user = get_object_or_404(User, id = post.user.id)
    if user.report_posts.filter(id=post.id).exists():
        user.report_posts.remove(post)
        post.cancel_report_post()
        reported_user.cancel_report_user()
        messages.success(request, f"{reported_user.username} 님의 게시글의 신고를 취소하였습니다.")
        print(post.report_count)
        print(reported_user.report_count)

    else:
        user.report_posts.add(post)
        post.report_post()
        reported_user.report_user()
        messages.success(request, f"{reported_user.username} 님의 게시글을 신고하였습니다.")
        print(post.report_count)
        print(reported_user.report_count)

    url = reverse("community:feeds") + f"#post-{post.id}"
    return redirect(url)

def search_results(request):
    search_string = request.GET.get("search_string", None)
    if search_string:
        if search_string[0] == "@":
            user_name = search_string[1:].strip()
            target_user = User.objects.get(username=user_name)
            context = {
                "search_string":search_string,
                "target_user":target_user,
            } 
        elif search_string[0] == "#":
            tag_name = search_string[1:].strip()
            return redirect(reverse("community:tags", kwargs={"tag_name":tag_name}))
        else:
            posts = Post.objects.filter(content__contains = search_string)
            context = {
                "search_string":search_string,
                "posts":posts,
            }
    else:
        return HttpResponseForbidden("하단의 검색 방법을 참고하여 검색하세요")
<<<<<<< HEAD
    
    return render(request, "community/search_results.html", context)

def trending(request):
    posts = Post.objects.all()
    likes_count = [post.like_users.count() for post in posts]
    posts_dict = dict(zip(posts, likes_count))
    posts_rank_list = sorted(posts_dict.items(), key=lambda x: (-x[1], -x[0].id))
    top5_list = [i[0] for i in posts_rank_list[:5]]
    context = {
        "top5_list":top5_list,
    }
    return render(request, "community/trending.html", context)



=======
    return render(request, "community/search_result.html", context)
>>>>>>> origin/new_mypage
    

    