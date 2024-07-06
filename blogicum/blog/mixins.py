from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import redirect
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


class OnlyProfileOwnerMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user.username
        return user == self.kwargs['username']

    def handle_no_permission(self):
        return redirect('blog:profile', username=self.kwargs['username'])


class AdminZoneShortNamesMixin:

    def short_title(self, obj):
        return Truncator(obj.title).chars(TITLE_DISPLAY_LIMIT)
    short_title.short_description = 'Заголовок'

    def short_text(self, obj):
        return Truncator(obj.text).chars(TITLE_DISPLAY_LIMIT)
    short_text.short_description = 'Текст'

    def short_name(self, obj):
        return Truncator(obj.name).chars(TITLE_DISPLAY_LIMIT)
    short_name.short_description = 'Название'
