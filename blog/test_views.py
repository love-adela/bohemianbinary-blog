from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test import Client, TestCase, RequestFactory
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

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


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
        self.client = Client()
    
    def test_get_with_author(self):
        user = UserFactory.create(password='1234')
        post_1 = PostFactory.create(author=user)
        post_2 = PostFactory.create(author=user)
        post_3 = PostFactory.create()

        self.client.login(username=user.username, password='1234')
        response = self.client.get(reverse('post_list'))

        # rendered = render_to_string(
        #     'post_list.html',
        #     {'posts': [post_1, post_2]}
        # )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No posts found')
        # self.assertEqual(response.content.decode('utf-8'), rendered)

    def test_get_some_dude(self):
        user = UserFactory.create(password='1234')
        PostFactory.create_batch(3)

        self.client.login(username=user.username, password='1234')
        response = self.client.get(reverse('post_list'))

        # rendered = render_to_string('post_list.html', {posts: []})
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'No posts found')
        # self.assertEqual(response.content.decode('utf-8'), rendered)

    def test_get_with_anonymous(self):
        response = self.client.get(reverse('post_list'))

        self.assertEqual(response.status_code, 200)
        # self.assertIn(reverse('/accounts/login', response['']))


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_with_anonymous(self):
        post = PostFactory.create()
        response = self.client.get(reverse('post_detail', args=(post.uuid,)))
        
        self.assertEqual(response.status_code, 200)
        # self.assertIn('/accounts/login/', response[''])

    def test_get_with_author(self):
        user = UserFactory.create(password='1234')
        post = PostFactory.create(author=user)

        self.client.login(username=user.username, password='1234')
        response = self.client.get(reverse('post_detail', args=(post.uuid,)))

    def test_get_with_some_dude(self):
        user = UserFactory.create(password='1234')
        post = PostFactory.create()

        self.client.login(username=user.username, password='1234')
        response = self.client.get(reverse('post_detail', args=(post.uuid, )))

        # rendered = render_to_string(
        #     'post_detail.html',
        #     {'error': 'The book was not found or you do not have permission to access the post.'}
        #     )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.content.decode('utf-8'), rendered)