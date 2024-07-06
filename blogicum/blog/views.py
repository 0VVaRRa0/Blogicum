from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .constants import POSTS_PER_PAGE, USER
from .forms import CommentForm, PostForm
from .mixins import OnlyAuthorMixin, PostsQuerySetMixin
from .models import Category, Comment, Post


class HomepageListView(PostsQuerySetMixin, ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = "blog/index.html"


class CategoryPostsListView(PostsQuerySetMixin, ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/category.html'

    def get_queryset(self):
        category_obj = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug']
        )
        qs = super().get_queryset()
        return qs.filter(category=category_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.only('is_published', 'slug'),
            is_published=True, slug=self.kwargs['category_slug']
        )
        return context


class ProfileListView(PostsQuerySetMixin, ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            USER,
            username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        user_obj = get_object_or_404(
            USER,
            username=self.kwargs['username']
        )
        if user_obj == self.request.user:
            return (
                Post.objects
                .annotate(comment_count=Count('comments'))
                .filter(author=user_obj)
                .order_by('-pub_date')
                .select_related('category', 'location')
            )
        else:
            qs = super().get_queryset()
            return qs.filter(author=user_obj)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name', 'username', 'email')
    model = USER
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.object.username}
        )

    def get_object(self):
        return self.request.user


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user == Post.objects.get(id=self.kwargs['post_id']).author:
            post_obj = get_object_or_404(
                Post,
                id=self.kwargs['post_id']
            )
        else:
            post_obj = get_object_or_404(
                Post,
                id=self.kwargs['post_id'],
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True
            )
        context['post'] = post_obj
        context['comments'] = post_obj.comments.all()
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    fields = ('text',)
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
    fields = ('text',)
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
