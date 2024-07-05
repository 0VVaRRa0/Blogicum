from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from .models import Post


class PostsQuerySet:

    def get_queryset(self):
        return (
            Post.objects
            .annotate(comment_count=Count('comment'))
            .filter(
                category__is_published=True,
                is_published=True,
                pub_date__lte=timezone.localtime()
            )
            .order_by('-pub_date')
            .select_related('author', 'category')
        )


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect(
            reverse(
                'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
            )
        )


class OnlyProfileOwnerMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user.username
        return user == self.kwargs['username']

    def handle_no_permission(self):
        return redirect(
            reverse(
                'blog:profile', kwargs={'username': self.kwargs['username']}
            )
        )
