from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "category",
    )
    filter_horizontal = ('genre',)
    search_fields = ("name", "year", "genre", "category")
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name", "slug")


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "pub_date",
        "title",
        "score"
    )
    search_fields = ("author", "text", "pub_date", "title", "score")


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "pub_date",
        "review",
    )
    search_fields = ("author", "text", "pub_date", "review")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name", "slug")


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
