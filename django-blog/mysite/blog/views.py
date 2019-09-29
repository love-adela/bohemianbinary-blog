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

    def get_object(self):
        post = Post.objects.filter(uuid=self.kwargs.get('post_id'))[0]
        return post


class PostCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect('post_detail', post_id=post.uuid)


class PostUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        # TODO : self.request.user != author일 경우 에러 발생시키기
        post.save()
        return redirect('post_detail', pk=post.pk)


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
    pattern_name = 'post_publish'

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.filter(uuid=kwargs.get('post_id'))[0]
        post.publish()
        return reverse_lazy('post_detail', args=(post.uuid,))


class PostRemoveRedirectView(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.filter(uuid=kwargs.get('post_id'))[0]
        post.delete()
        return reverse_lazy('post_list')


class CommentCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Comment
    fields = ('author', 'text')
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = Post.objects.filter(uuid=self.kwargs.get('post_id'))[0]
        comment.post = post
        comment.save()
        return redirect('post_detail', post_id=post.uuid)


class CommentApproveRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        comment.approve()
        return reverse_lazy('post_detail', args=(comment.post.pk,))


class CommentRemoveRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        post = comment.post
        comment.delete()
        return reverse_lazy('post_detail', args=(post.uuid,))


class TagIndexView(generic.ListView):
    template_name = 'blog/tag_list.html'
    context_object_name = 'tag'

    def get_queryset(self):
        return get_object_or_404(Tag, title=self.kwargs['tag_name'])
