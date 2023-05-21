from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post
from slugify import slugify
import os


# Create your views here.
class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Список постов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        post.increment_count_view()
        return post


class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('blog:post_list')
    extra_context = {
        'title': 'Создать пост'
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.save()
        return redirect(reverse('blog:post_item', kwargs={'slug': post.slug}))


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content', 'preview', 'slug', 'date_of_creation', 'is_published', 'number_of_views')
    success_url = reverse_lazy('blog:post_list')
    extra_context = {
        'title': 'Редактирование'
    }


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
