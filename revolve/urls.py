from django.urls import path
from . import views

app_name = 'revolve'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<int:category_id>/', views.category_list, name='post_by_category'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('blog-posts/', views.blog_posts, name='blog_posts'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category-posts/', views.category_posts, name='category_posts'),
    path('all-posts/', views.all_posts, name='all_posts'),
    path('contact/', views.contact_view, name='contact'),
]
