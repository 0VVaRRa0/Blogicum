from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomepageListView.as_view(), name='index'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        'posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(), name='category_posts'
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileListView.as_view(), name='profile'
    )
]
