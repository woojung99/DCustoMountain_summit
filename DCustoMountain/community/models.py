from django.db import models

# Create your models here.
class PostManager(models.Manager): 
    def get_queryset(self):
        return super().get_queryset().exclude(user__block_flag=True) 

class Post(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    content = models.TextField("내용", blank=True)
    created_at = models.DateTimeField("작성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)
    tags = models.ManyToManyField("community.Hashtag", verbose_name="해시태그 목록", blank=True)
    report_count = models.PositiveIntegerField("신고 횟수", default=0)

    def __str__(self):
        return f"{self.user.username}의 게시글 (id: {self.id})"
    
    def report_post(self): 
        self.report_count += 1 
        if self.report_count >= 3: 
            self.delete()
        else:
            self.save()
    
    def cancel_report_post(self):
        self.report_count -= 1
        self.save()
    
class PostImage(models.Model):
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)
    photo = models.ImageField("사진", upload_to="community/photo/%Y/%m/%d/")
    created_at = models.DateTimeField("업로드일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    created_at = models.DateTimeField("작성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

class Hashtag(models.Model):
    name = models.CharField("태그명", max_length=50)

    def __str__(self):
        return self.name