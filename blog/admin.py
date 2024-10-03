from django.contrib import admin

from .mixins import AdminZoneShortNamesMixin
from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(AdminZoneShortNamesMixin, admin.ModelAdmin):
    list_display = ('short_title', 'is_published', 'slug')
    list_editable = ('is_published',)


@admin.register(Comment)
class CommentAdmin(AdminZoneShortNamesMixin, admin.ModelAdmin):
    list_display = ('author', 'post', 'short_text')
    search_fields = ('post__title',)


@admin.register(Location)
class LocationAdmin(AdminZoneShortNamesMixin, admin.ModelAdmin):
    list_display = ('short_name',)


@admin.register(Post)
class PostAdmin(AdminZoneShortNamesMixin, admin.ModelAdmin):
    list_display = ('short_title', 'is_published', 'category')
    list_editable = ('is_published', 'category')
    list_filter = ('category',)
    search_fields = ('title',)
