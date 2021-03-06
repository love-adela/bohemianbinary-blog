from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='post_list'),
    path('post/<uuid:post_id>/', views.DetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<uuid:post_id>/edit/',
         views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<uuid:post_id>/publish/',
         views.PostPublishRedriectView.as_view(), name='post_publish'),
    path('post/<uuid:post_id>/remove/',
         views.PostRemoveRedirectView.as_view(), name='post_remove'),
    path('post/<uuid:post_id>/comment/',
         views.CommentCreateView.as_view(), name='add_comment_to_post'),
    path('post/<uuid:post_id>/revision/',
         views.RevisionIndexView.as_view(), name='revision_list'),
    path('post/<uuid:post_id>/revision/<int:revision_id>',
         views.RevisionDetailView.as_view(), name='revision_detail'),
    path('drafts/', views.DraftIndexView.as_view(), name='post_draft_list'),
    path('comment/<int:pk>/approve/',
         views.CommentApproveRedirectView.as_view(), name='comment_approve'),
    path('comment/<int:pk>/remove/',
         views.CommentRemoveRedirectView.as_view(), name='comment_remove'),
    path('tag/<str:tag_name>/', views.TagIndexView.as_view(), name='tag_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
