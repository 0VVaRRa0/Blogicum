from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm
from .models import Category, Comment, Post


class HomepageListView(ListView):
    model = Post
    paginate_by = 10
    template_name = "blog/index.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now(),
        )


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(
            Post.objects.filter(is_published=True, id=self.kwargs['post_id'])
        )
        context['comments'] = Comment.objects.filter(
            post=self.kwargs['post_id']
        )
        context['form'] = CommentForm
        return context


class CategoryPostsListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/category.html'

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
    paginate_by = 10
    template_name = 'blog/profile.html'

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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        object = self.get_object()
        redirect_url = reverse_lazy(
            'blog:post_detail', kwargs={'post_id': object.pk}
        )
        return redirect(redirect_url)


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')
    template_name = "blog/create.html"


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    post_obj = None

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.pk}
        )


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.id}
        )


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.id}
        )
