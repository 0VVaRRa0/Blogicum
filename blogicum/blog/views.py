from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Category, Post

POSTS = Post.objects.select_related('category', 'location', 'author')


class HomepageListView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now(),
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(
            Post.objects.filter(is_published=True, id=self.kwargs['pk'])
        )
        return context


class CategoryPostsListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.filter(
                slug=self.kwargs['category_slug'], is_published=True
            )
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            pub_date__lte=timezone.now(),
        )


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects.filter(username=self.kwargs['username'])
        )
        return context

    def get_queryset(self):
        return Post.objects.filter(
            author__username=self.kwargs.get('username'),
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
