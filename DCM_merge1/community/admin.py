from django.contrib import admin
from community.models import Post, PostImage, Comment, Hashtag
import admin_thumbnails

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin_thumbnails.thumbnail("photo")
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content",
        "created_at",
        "updated_at"
    ]
    inlines = [
        CommentInline,
        PostImageInline,
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    pass