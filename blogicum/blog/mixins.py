from django.contrib import admin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.text import Truncator

from .constants import TITLE_DISPLAY_LIMIT
from .models import Post


class PostsQuerySetMixin:

    def get_queryset(self):
        return (
            Post.objects
            .annotate(comment_count=Count('comments'))
            .filter(
                category__is_published=True,
                is_published=True,
                pub_date__lte=timezone.localtime()
            )
            .order_by('-pub_date')
            .select_related('author', 'category', 'location')
        )


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class AdminZoneShortNamesMixin:

    @admin.display(description='Заголовок')
    def short_title(self, obj):
        return Truncator(obj.title).chars(TITLE_DISPLAY_LIMIT)

    @admin.display(description='Текст')
    def short_text(self, obj):
        return Truncator(obj.text).chars(TITLE_DISPLAY_LIMIT)

    @admin.display(description='Название')
    def short_name(self, obj):
        return Truncator(obj.name).chars(TITLE_DISPLAY_LIMIT)


class CommentSuccessUrlMixin:

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.post.id}
        )
