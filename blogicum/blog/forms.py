from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), label='Текст комментария'
    )

    class Meta:
        model = Comment
        fields = ('text',)
