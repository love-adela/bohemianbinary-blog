from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.template.loader import render_to_string
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

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

    title = Sequence(lambda n: 'Post Title %d ' % n)
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
        self.view = DetailView.as_view()
        self.request = HttpRequest()
        setattr(self.request, 'method', 'GET')
        setattr(self.request, 'user', AnonymousUser())

    def test_get_with_anonymous(self):
        post = PostFactory.create()
        response = self.view(self.request, post_id=post.uuid)
        self.assertEqual(response.status_code, 200)
        # self.assertIn('/accounts/login/', response[])

    def test_get_with_author(self):
        user = UserFactory.create()
        post = PostFactory.create(author=user)

        setattr(self.request, 'user', user)
        response = self.view(self.request, post_id=post.uuid).render()
        # rendered = render_to_string('post_detail.html', {'post':post}) # TODO: Add more request dict items
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.content.decode('utf-8'), rendered)

    def test_get_with_some_dude(self):
        user = UserFactory.create()
        post = PostFactory.create()

        setattr(self.request, 'user', user)
        response = self.view(self.request, post_id = post.uuid).render()

        # rendered = render_to_string(
        #     'post_detail.html',
        #     {'error': 'The book was not found or you do not have permission to access the post.'}
        #     )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(respone.content.decode('utf-8'), rendered)