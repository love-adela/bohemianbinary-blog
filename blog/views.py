from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Tag, Comment, Revision
from .forms import PostForm, CommentForm
import logging
from difflib import Differ


class IndexView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.posts()


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        return Post.objects.detail_post(self.kwargs.get('post_id'))


class PostCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.draft = True
        post.save()
        revision = Revision.objects.create(title=post.title,
                                           post=post,
                                           author=post.author,
                                           text=post.text,
                                           created_date=post.created_date,
                                           )

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
        last_revision = Revision.objects.filter(post_id=post.pk) \
                                .order_by('-revision_id').first()
        new_revision_id = last_revision.revision_id + 1
        post.draft = True
        Revision.objects.create(revision_id=new_revision_id,
                                title=post.title,
                                post=post,
                                author=post.author,
                                text=post.text,
                                created_date=timezone.now())
        return redirect('post_detail', post_id=post.uuid)

    def get_object(self):
        post = Post.objects.filter(uuid=self.kwargs.get('post_id')).first()
        if len(post.revisions.all()) == 0:
            Revision.objects.create(post=post,
                                    author=post.author,
                                    text=post.text,
                                    created_date=post.created_date)
        return post


class DraftIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(draft=True) \
                .order_by('-created_date')
        return posts


class PostPublishRedriectView(LoginRequiredMixin, generic.base.RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'post_publish'

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.filter(uuid=kwargs.get('post_id')).first()
        post.draft = False
        post.publish()
        return reverse_lazy('post_detail', args=(post.uuid,))


class PostRemoveRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.filter(uuid=kwargs.get('post_id')).first()
        post.delete()
        return reverse_lazy('post_list')


class RevisionIndexView(generic.ListView):
    template_name = 'blog/revision_list.html'
    context_object_name = 'revisions'

    def get_queryset(self):
        post = Post.objects.filter(uuid=self.kwargs.get('post_id')).first()
        revisions = Revision.objects.filter(post=post).order_by('-created_date')
        return revisions


# def diff(original_text, current_text):
#     original = original_text.splitlines(keepends=True)
#     current = current_text.splitlines(keepends=True)
#     d = Differ()
#     return '\n'.join(d.compare(original, current))


class RevisionDetailView(generic.DetailView):
    model = Revision
    template_name = 'blog/revision_detail.html'
    context_object_name = 'current'


    def get_object(self):
        post = Post.objects.filter(uuid=self.kwargs.get('post_id')).first()
        post_revisions = Revision.objects.filter(post=post)
        current = post_revisions.filter(revision_id=self.kwargs.get('revision_id')).first()
        # manager로 빼기
        # self.previous = post_revisions.filter(created_date__lt=current.created_date).filter().order_by('-created_date').first()
        # previous_text = self.previous.text if self.previous is not None else ''
        # self.diff = diff(previous_text, current.text)
        return current

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['previous'] = self.previous
    #     context['diff'] = self.diff
    #     return context


class CommentCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Comment
    fields = ('author', 'text')
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = Post.objects.filter(uuid=self.kwargs.get('post_id')).first()
        comment.post = post
        comment.save()
        return redirect('post_detail', post_id=post.uuid)


class CommentApproveRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        post = comment.post
        comment.approve()
        return reverse_lazy('post_detail', args=(post.uuid,))


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
