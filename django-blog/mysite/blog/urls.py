from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.DetailView.as_view(), name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/publish/', views.PostPublishRedriectView.as_view(), name='post_publish'),
    # path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('drafts/', views.DraftIndexView.as_view(), name='post_draft_list'),
    path('comment/<int:pk>/approve/', views.CommentApproveRedirectView.as_view(), name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('tag/<str:tag_name>/', views.TagIndexView.as_view(), name='tag_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
