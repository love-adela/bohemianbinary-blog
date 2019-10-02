import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Tag, Post, Comment

from .utils import FormatterMistune


class TagModelTests(TestCase):
    # Tag 모델 가져오는지 테스트 .. 현재(2019-10-02) 모델 중 가장 작은 단위기 때문에.
    def test_with_title(self):
        Tag.objects.create(title='java')
        t1 = Tag.objects.first()
        self.assertEquals(t1.title, 'java')
        self.assertNotEquals(t1.title, 'python3')


class PostModelTests(TestCase):
    # author 초기화
    def create_user(self):
        author = User.objects.create(username='testuser')
        author.set_password('1234')
        author.save()
        return User.objects.first()

    # method 테스트
    def test_publish(self):
        author = self.create_user()

        # post에서 publish되는 시간대가 현재시간보다 뒤에 있는지 테스트
        now = timezone.now()
        post = Post(author=author)  # author이 필수값이라서 설정함.
        post.publish()
        self.assertLess(now, post.published_date)

    def test_formatted_text(self):
        author = self.create_user()

        post = Post.objects.create(author=author)
        post.text = '**Java가 좋아요**'
        # import한 mistune 포매트가 동작하는지 테스트
        # ... 만일 mistune라이브러리가 모든 text를 1로 format해도 정상으로 나오면?
        #     -> formatted_another_text로 검사
        formatted_text = FormatterMistune().format(post.text)
        self.assertEquals(formatted_text, post.formatted_text())

        # import한 mistune포매터를 믿을 수 없는 상황 대비해서 테스트
        formatted_another_text = '<p><strong>Java가 좋아요</strong></p>\n'
        self.assertEquals(formatted_another_text, post.formatted_text())

    def test_approved_comments(self):
        author = self.create_user()
        post = Post.objects.create(author=author)

        c1 = post.comments.create(author='test', text='와아 축하해요!')
        c1.approve()
        post.save()
        c2 = post.approved_comments().first()
        self.assertEqual(c2.text, '와아 축하해요!')
