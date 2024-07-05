from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('login')


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
