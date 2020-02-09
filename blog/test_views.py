from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, RequestFactory

import factory

from .views import *
import logging


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User 

    username = Sequence(lambda n: 'User_%s' % n)
    email = Sequence(lambda n: 'email_%s@example.com' % n)
    password = ''
    is_active = True
    is_superuser = False


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = sequence(lambda n: 'Post Title %d ' % n)
    author = SubFactory(UserFactory)


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class PostIndexViewTest(TestCase):
    # All of the teset cases should be accessible to this request factory
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_index_view_requires_session_middleware(self):
        """ 
        Test that index view returns a 200 response and uses the correct template
        """
        request = self.factory.get('post_list')
        request = add_middleware_to_request(request, SessionMiddleware)
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.view = PostFactory.as_view()
        self.request = HttpRequest()
        setattr(self.request, 'method', 'GET')
        setattr(self.request, 'user', AnonymousUser())

    def test_get_with_anonymous(self):
        post = PostFactory.create()

        response = self.view(self.request, post_id=post.id)
        self.assertEqual(response.status_code, 302)
        # self.assertIn('/accounts/login/', response[])

    def test_get_with_author(self):
        user = UserFactory.create()
        post = PostFactory.create(author=user)

        setattr(self.request, 'user', user)
        response = self.view(self.request, post_id=post.id).render()
        rendered = render_to_string('post_detail.html', {'post':post}) # TODO: Add more request dict items
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), rendered)

    def test_get_with_some_dude(self):
        user = UserFactory.create()
        post = PostFactory.create()

        setattr(self.request, 'user', user)
        response = self.view(self.request, post_id = post.id).render()

        rendered = render_to_string(
            'post_detail.html',
            {'error': 'The book was not found or you do not have permission to access the post.'}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(respone.content.decode('utf-8'), rendered)
# class DraftIndexViewTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_draft_index_view_requires_session_middleware(self):
#         request = self.factory.get('post_draft_list')
#         request.user = AnonymousUser()
#         request = add_middleware_to_request(request, SessionMiddleware)
#         response = DraftIndexView.as_view()(request)
#         self.assertEqual(response.status_code, 302)

    # def test_draft(self):
    #     """
    #     Test correctly posting to the draft index view
    #     """
    #     # TODO: create anonymous object tobe login
    #     request = self.factory.post(
    #         reverse_lazy('post_draft_list'),
    #         {
    #             'title': 'This is the draft post title for unittest',
    #             'text': 'If life gives you lemons, make lemonade.'}
    #     )
    #     request.session = {}
    #     response = DraftIndexView.as_view()(request)
    #     self.assertEqual(response.status_code, 302)

    # def test_is_draft_when_create_post(self):
    #     create_user_and_sign_in(self.client)
    #     response = self.client.get(reverse('post_draft_list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context['posts'], [])

    # def test_is_draft_when_create_and_edit_post(self):
    #     create_user_and_sign_in(self.client)
    #     form_data = {
    #         'title': 'draft test용 title',
    #         'text': '음하하하 이것은 draft 테스트입니다.',
    #     }
    #     response = self.client.post(
    #         reverse('post_new'), form_data, follow=True)
    #     response = self.client.get(reverse('post_draft_list'))
    #     post = response.context['posts'].first()
    #     self.assertEqual(post.draft, True)

    # def test_is_not_draft_when_publish_post(self):
    #     create_user_and_sign_in(self.client)
    #     form_data = {
    #         'title': 'draft test용 title',
    #         'text': '음하하하 이것은 draft 테스트입니다.'
    #     }
    #     response = self.client.post(
    #         reverse('post_new'), form_data, follow=True)
    #     uuid = response.context['post'].uuid
    #     response = self.client.get(
    #         reverse('post_publish', args=(uuid,)), follow=True)
    #     response = self.client.get(reverse('post_draft_list'))
    #     draft = response.context['posts'].first()
    #     self.assertEqual(draft, None)

    # def test_is_not_draft_when_publish_and_edit(self):
    #     create_user_and_sign_in(self.client)
    #     form_data = {
    #         'title': 'draft test용 타이틀입니다. 플스 타이틀 아님.',
    #         'text': '여기는 테라로사. 건조하다. 춥고.'
    #     }
    #     response = self.client.post(
    #         reverse('post_new'), form_data, follow=True)
    #     uuid = response.context['post'].uuid
    #     response = self.client.get(
    #         reverse('post_publish', args=(uuid,)), follow=True)
    #     form_data = {
    #         'title': '수정된 draft test용 타이틀',
    #         'text': '여기는 테라로사. 건조하다. 춥고. 레모네이드를 시켰다. 얼어죽어도 아이슨가.'
    #     }
    #     response = self.client.post(
    #         reverse('post_edit', args=(uuid,)), form_data, follow=True)
    #     response = self.client.get(
    #         reverse('post_publish', args=(uuid,)), follow=True)
    #     response = self.client.get(reverse('post_draft_list'))
    #     draft = response.context['posts'].first()
    #     self.assertEqual(draft, None)