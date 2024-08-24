from django.contrib import admin
from .models import Post, Comment, Image, Category


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'user')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [ImageInline, CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'uploaded_at')