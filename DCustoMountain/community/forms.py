from django import forms
from community.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
        ]
        widgets = {
            "content":forms.Textarea(
                attrs={
                    "placeholder":"문구 입력...",
                }
            ),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "post",
            "content",
        ]
        widgets = {
            "content":forms.Textarea(
                attrs={
                    "placeholder":"댓글 달기..."
                }
            ) 
        }


