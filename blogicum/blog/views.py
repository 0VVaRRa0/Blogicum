from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS = Post.objects.select_related('category', 'location', 'author')


def index(request):
    """View-функция, вызывающая главную страницу."""
    context = {
        'post_list': POSTS
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
        .order_by('-pub_date')[0:5]
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """View-функция, вызывающая страницу поста."""
    context = {
        'post': get_object_or_404(
            Post.objects.all().filter(
                id=post_id, is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            )
        )
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """View-функция, вызывающая страницу категории"""
    context = {
        'category': get_object_or_404(
            Category.objects
            .values('title', 'description', 'slug')
            .filter(
                slug=category_slug,
                is_published=True
            )
        ),
        'post_list': POSTS
        .filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lte=timezone.now()
        )
        .order_by('-pub_date')
    }
    return render(request, 'blog/category.html', context)
