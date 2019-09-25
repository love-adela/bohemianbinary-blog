from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Tag, Comment
from .forms import PostForm, CommentForm
import logging


class IndexView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('published_date')
        return posts


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class DraftIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(
            published_date__isnull=True).order_by('created_date')
        return posts


class PostPublishRedriectView(LoginRequiredMixin, generic.base.RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'post-publish'

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
    # def post_publish(request, pk):
        # post = get_object_or_404(Post, pk=pk)
        post.publish()
        return reverse_lazy('post_detail', args=(post.pk,))
        # return super(PostPublishRedriectView, self).get_redirect_url(*args, **kwargs)
        # return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


class CommentApproveRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        comment.approve()
        return reverse_lazy('post_detail', args=(comment.post.pk,))


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


class TagIndexView(generic.ListView):
    template_name = 'blog/tag_list.html'
    context_object_name = 'tag'

    def get_queryset(self):
        return get_object_or_404(Tag, title=self.kwargs['tag_name'])
