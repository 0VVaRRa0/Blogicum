from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomepageView.as_view(), name='index'),
    path(
        'posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsView.as_view(), name='category_posts'
    ),
]
