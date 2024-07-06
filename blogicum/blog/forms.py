from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), label='Текст комментария'
    )

    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'category',
            'location',
            'image'
        )
