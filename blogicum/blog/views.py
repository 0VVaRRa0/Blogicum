from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm
from .mixins import OnlyAuthorMixin
from .models import Category, Comment, Post


POSTS = (
    Post.objects
    .annotate(comment_count=Count('comment'))
    .filter(
        category__is_published=True,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    .order_by('-pub_date')
)
USER = get_user_model()


class HomepageListView(ListView):
    model = Post
    paginate_by = 10
    template_name = "blog/index.html"
    queryset = POSTS


class CategoryPostsListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, is_published=True,
            slug=self.kwargs['category_slug']
        )
        return context

    def get_queryset(self):
        return (
            POSTS.filter(
                category__slug=self.kwargs['category_slug']
            )
        )


class ProfileListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            USER.objects.filter(username=self.kwargs['username'])
        )
        return context

    def get_queryset(self):
        return (
            POSTS.filter(
                author__username=self.kwargs['username']
            )
        )


class ProfileUpdateView(UpdateView):
    fields = ('first_name', 'last_name', 'username', 'email')
    model = USER
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'registration/registration_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.kwargs['username']}
        )


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(
            Post, is_published=True, id=self.kwargs['post_id']
        )
        context['comments'] = Comment.objects.filter(
            post=self.kwargs['post_id']
        )
        context['form'] = CommentForm
        return context


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
