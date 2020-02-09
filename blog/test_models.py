import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import Image, Tag, Post, Comment, upload_to

from .utils import FormatterMistune
import logging


class ImageModelTests(TestCase):
    def test_is_image(self):
        i1 = Image.objects.create(file='img/pig1.jpg')
        i1.save()
        image = upload_to(i1, 'img/pig1.jpg')
        self.assertIn('img/', image)
        self.assertIn('.jpg', image)
        Tag.objects.create(title='이미지가아님')
        t1 = Tag.objects.first()
        try:
            fake_image = upload_to(t1, 'img/fake.jpg')
        except:
            pass


class TagModelTests(TestCase):
    # Tag 모델 가져오는지 테스트 .. 현재(2019-10-02) 모델 중 가장 작은 단위기 때문에.
    def test_with_title(self):
        t1 = Tag.objects.create(title='java')
        t1.save()
        self.assertEquals(t1.title, 'java')
        # 대소문자 통과되는지, 공백들어갈건지, '()', '#'가 들어가는지 model 코드에서 validation.
        self.assertNotEquals(t1.title, 'python3')


# def create_user():
#     """
#     author 초기화
#     """
#     author = User.objects.create(username='testuser')
#     author.set_password('1234')
#     author.save()
#     return author

#     # username 에 admin이 들어가있지 않는지 validation
#     # username 형식도 테스트 - URL에 쓸 수 있는 형식으로 이메일에 '/'가 들어가야하는지, username이 url의 일부로 쓰이는지.


# def create_post(title=None, text=None, days=None):
#     """
#     post 초기화
#     """
#     # TODO : create_user 독립
#     author = create_user()
#     post = Post.objects.create(author=author)
#     if title is not None:
#         post.title = title
#     if text is not None:
#         post.text = text
#     if days is not None:
#         post.created_date = days
#     return post


# class PostModelTests(TestCase):
#     # method 테스트
#     def test_publish(self):
#         """
#         post에서 publish되는 시간대가 현재시간보다 뒤에 있는지 테스트
#         """
#         now = timezone.now()
#         post = create_post()
#         post.publish()
#         self.assertLess(now, post.published_date)

#     def test_formatted_text(self):
#         post = create_post()
#         post.text = '**Java가 좋아요**'
#         # import한 mistune 포매트가 동작하는지 테스트
#         # ... 만일 mistune라이브러리가 모든 text를 1로 format해도 정상으로 나오면?
#         #     -> formatted_another_text로 검사
#         formatted_text = FormatterMistune().format(post.text)
#         self.assertEquals(formatted_text, post.formatted_text())

#         # import한 mistune포매터를 믿을 수 없는 상황 대비해서 테스트
#         formatted_another_text = '<p><strong>Java가 좋아요</strong></p>\n'
#         self.assertEquals(formatted_another_text, post.formatted_text())

#     def test_approved_comments(self):
#         post = create_post()
#         c1 = post.comments.create(author='test', text='와아 축하해요!')
#         c1.approve()
#         post.save()
#         c2 = post.approved_comments().first()
#         self.assertEqual(c2.text, '와아 축하해요!')

#     def test_is_contained(self):
#         """
#         string 포함 테스트
#         """
#         Image.objects.create(file='img/pig1.jpg')
#         i1 = Image.objects.first()
#         self.assertIn('img/pig1.jpg', str(i1))
#         Tag.objects.create(title='java')
#         t1 = Tag.objects.first()
#         self.assertIn(str(t1), 'java')
#         post = create_post(title='이거슨 테스트')
#         p1 = Post.objects.first()
#         self.assertIn(str(p1), '이거슨 테스트')
#         c1 = post.comments.create(author='test', text='이거슨 댓글테스트')
#         self.assertIn(str(c1), '이거슨 댓글테스트')