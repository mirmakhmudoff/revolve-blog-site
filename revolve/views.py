from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, TemplateView
from taggit.models import Tag
from .forms import CommentForm, ContactForm
from .models import Post, Category
from django.db import models
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings


def post_list(request, tag_slug=None, category_id=None):
    posts_list = Post.published.all()
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts_list = posts_list.filter(category=category)

    unique_tags = Tag.objects.filter(post__in=posts_list).annotate(post_count=Count('post')).distinct()
    categories = Category.objects.all()

    paginator = Paginator(posts_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    template_name = 'list.html' if tag_slug or category_id else 'index.html'

    return render(request, template_name, {
        'categories': categories,
        'posts': posts,
        'tag': tag,
        'category': category,
        'unique_tags': unique_tags
    })


def blog_posts(request, tag_slug=None, category_id=None):
    posts_list = Post.published.all()
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts_list = posts_list.filter(category=category)

    unique_tags = Tag.objects.filter(post__in=posts_list).annotate(post_count=Count('post')).distinct()

    categories = Category.objects.annotate(
        post_count=Count('posts', filter=models.Q(posts__status=Post.Status.PUBLISHED)))

    paginator = Paginator(posts_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog-posts.html', {
        'categories': categories,
        'posts': posts,
        'tag': tag,
        'category': category,
        'unique_tags': unique_tags,
        'user': request.user,
        'trending_posts': Post.published.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4],
    })


def category_posts(request, tag_slug=None, category_id=None):
    posts_list = Post.published.all()
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts_list = posts_list.filter(category=category)

    unique_tags = Tag.objects.filter(post__in=posts_list).annotate(post_count=Count('post')).distinct()

    categories = Category.objects.annotate(
        post_count=Count('posts', filter=models.Q(posts__status=Post.Status.PUBLISHED)))

    paginator = Paginator(posts_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'category-posts.html', {
        'categories': categories,
        'posts': posts,
        'tag': tag,
        'category': category,
        'unique_tags': unique_tags,
        'user': request.user,
        'trending_posts': Post.published.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4],
    })


def all_posts(request, tag_slug=None, category_id=None):
    posts_list = Post.published.all()
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts_list = posts_list.filter(category=category)

    unique_tags = Tag.objects.filter(post__in=posts_list).annotate(post_count=Count('post')).distinct()

    categories = Category.objects.annotate(
        post_count=Count('posts', filter=models.Q(posts__status=Post.Status.PUBLISHED)))

    paginator = Paginator(posts_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'all-posts.html', {
        'categories': categories,
        'posts': posts,
        'tag': tag,
        'category': category,
        'unique_tags': unique_tags,
        'user': request.user,
        'trending_posts': Post.published.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4],
    })


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('revolve:post_detail', year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'form': form})


class PostDetailView(DetailView, FormView):
    model = Post
    template_name = 'post-detail.html'
    context_object_name = 'detail'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CommentForm'] = self.get_form()

        post = self.get_object()

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        trending_posts = Post.published.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4]
        categories = Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')

        context['similar_posts'] = similar_posts
        context['trending_posts'] = trending_posts
        context['categories'] = categories

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('revolve:post_detail', kwargs={
            'year': post.publish.year,
            'month': post.publish.month,
            'day': post.publish.day,
            'slug': post.slug
        })


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts_list = category.posts.filter(status=Post.Status.PUBLISHED)

    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    trending_posts = Post.published.annotate(num_comments=Count('comments')).order_by('-num_comments')[:4]
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')

    return render(request, 'category-list.html', {
        'category': category,
        'posts': posts,
        'trending_posts': trending_posts,
        'categories': categories,
        'user': request.user,
    })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"New Contact Form Submission from {name}"
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            send_mail(subject, email_message, from_email, recipient_list)

            return redirect('revolve:contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


class AboutView(TemplateView):
    template_name = 'about.html'
