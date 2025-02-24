from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile", blank=True)
    short_description = models.TextField("소개글", blank=True)
    like_posts = models.ManyToManyField(
        "community.Post",
        verbose_name="좋아요 누른 Post 목록",
        related_name="like_users",
        blank=True,
    )
    comment_posts = models.ManyToManyField(
        "community.Post",
        verbose_name="댓글 단 Post 목록",
        related_name="comment_users",
        blank=True,
    )
    save_posts = models.ManyToManyField(
        "community.Post",
        verbose_name="저장한 Post 목록",
        related_name="save_users",
        blank=True,
    )
    following = models.ManyToManyField(
        "self",
        verbose_name="팔로우 중인 사용자들",
        related_name="followers",
        symmetrical=False,
        through="users.Relationship",
    )
    block_flag = models.BooleanField("정지된 사용자", default=False)
    report_count = models.PositiveIntegerField("신고 횟수", default=0)
    experienced_mountains = models.ManyToManyField(
        "mountains.Mountain", 
        verbose_name="등산해 본 Mountain 목록", 
        related_name="experienced_users", 
        blank=True, 
    )
    wish_mountains = models.ManyToManyField(
        "mountains.Mountain", 
        verbose_name="등산해 보고 싶은 Mountain 목록", 
        related_name="wish_users", 
        blank=True, 
    )

    def __str__(self):
        return self.username
    
    def report_user(self): 
        self.report_count += 1 
        if self.report_count >= 5: 
            self.block_flag = True
        self.save() 
    
class Relationship(models.Model):
    from_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우를 요청한 사용자",
        related_name="following_relationships",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 요청의 대상",
        related_name="follower_relationships",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"관계 ({self.from_user} -> {self.to_user})"