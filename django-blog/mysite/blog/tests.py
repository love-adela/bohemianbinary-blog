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
        Image.objects.create(file='img/pig1.jpg')
        i1 = Image.objects.first()
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
        Tag.objects.create(title='java')
        t1 = Tag.objects.first()
        self.assertEquals(t1.title, 'java')
        self.assertNotEquals(t1.title, 'python3')


def create_user():
    """
    author 초기화
    """
    author = User.objects.create(username='testuser')
    author.set_password('1234')
    author.save()
    return User.objects.first()


# test_user = create_user()
def create_post(title=None, text=None, days=None):
    """
    post 초기화
    """
    # TODO : create_user 독립
    author = create_user()
    post = Post.objects.create(author=author)
    if title is not None:
        post.title = title
    if text is not None:
        post.text = text
    if days is not None:
        post.created_date = days
    return post
    # time = timezone.now() + datetime.timedelta(days=days)


class PostModelTests(TestCase):
    # method 테스트
    def test_publish(self):
        """
        post에서 publish되는 시간대가 현재시간보다 뒤에 있는지 테스트
        """
        now = timezone.now()
        post = create_post()
        post.publish()
        self.assertLess(now, post.published_date)

    def test_formatted_text(self):
        post = create_post()
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
        post = create_post()
        c1 = post.comments.create(author='test', text='와아 축하해요!')
        c1.approve()
        post.save()
        c2 = post.approved_comments().first()
        self.assertEqual(c2.text, '와아 축하해요!')

    def test_is_contained(self):
        """
        string 포함 테스트
        """
        Image.objects.create(file='img/pig1.jpg')
        i1 = Image.objects.first()
        self.assertIn(str(i1), '/Users/adela/workspace/bohemian-binary/django-blog/mysite/media/img/pig1.jpg')
        Tag.objects.create(title='java')
        t1 = Tag.objects.first()
        self.assertIn(str(t1), 'java')
        post = create_post(title='이거슨 테스트')
        p1 = Post.objects.first()
        self.assertIn(str(p1), '이거슨 테스트')
        c1 = post.comments.create(author='test', text='이거슨 댓글테스트')
        self.assertIn(str(c1), '이거슨 댓글테스트')


class PostIndexViewTests(TestCase):
    def test_is_post(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])


class PostDetailViewTests(TestCase):
    def test_is_post(self):
        """
        """
        post = create_post(title='테스트 포스트 1.')
        post = Post.objects.filter(uuid=post.uuid).first()
        response = self.client.get(
            reverse('post_detail', args=(post.uuid,)))
        self.assertEqual(
            response.context['post'], post)


def create_user_and_sign_in(client):
    create_user()
    credential = {
        'username': 'testuser',
        'password': '1234'
    }
    response = client.post('/accounts/login/', credential, follow=True)


# TODO: Login 해주는 method 별도로 만들고
class LoginTestCase(TestCase):
    def test_login(self):
        create_user()
        credential = {
            'username': 'testuser',
            'password': '1234'
        }
        response = self.client.get(reverse('post_new'))
        self.assertRedirects(response, '/accounts/login/?next=/post/new/')
        response = self.client.post('/accounts/login/', credential, follow=True)
        response = self.client.get(reverse('post_new'))
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)


class PostCreateViewTests(TestCase):
    def test_is_form_valid(self):
        create_user_and_sign_in(self.client)
        form_data = {
            'title': 'test용 title',
            'text': '음하하하 이것은 테스트입니다.'
        }
        response = self.client.post(
            reverse('post_new'), form_data, follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'].title, form_data['title'])


class PostUpdateViewTests(TestCase):
    def test_is_form_valid(self):
        create_user_and_sign_in(self.client)
        form_data = {
            'title': 'test용 title',
            'text': '음하하하 이것은 테스트입니다.'
        }
        response = self.client.post(
            reverse('post_new'), form_data, follow=True
            )
        uuid = response.context['post'].uuid
        form_data = {
            'title': '수정 test용 title',
            'text': '음하하하 이것은 수정 테스트입니다.'
        }
        response = self.client.post(
            reverse('post_edit', args=(uuid,)), form_data, follow=True
            )
        logging.error(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'].title, form_data['title'])


class DraftIndexViewTests(TestCase):
    def test_is_draft(self):
        create_user_and_sign_in(self.client)
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(response.status_code, 200)

        # draft에 글 없는지 검사
        self.assertQuerysetEqual(response.context['posts'], [])

        # draft 글 생성
        form_data = {
            'title': 'draft test용 title',
            'text': '음하하하 이것은 draft 테스트입니다.'
        }
        response = self.client.post(
            reverse('post_new'), form_data, follow=True
        )

        # draft에 글 있는지 검사 && post_list에는 없는지 검사
        response = self.client.get(reverse('post_draft_list'))
        post = response.context['posts'].first()
        self.assertEqual(post.title, form_data['title'])
        self.assertEqual(post.text, form_data['text'])
        uuid = post.uuid

        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

        # publish
        response = self.client.get(
            reverse('post_publish', args=(uuid,)), follow=True
            )  # Redirect 되기 때문에
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.title, form_data['title'])
        self.assertEqual(post.text, form_data['text'])

        # draft에는 글 없는지 검사 && post_list에는 있는지 검사
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        post = response.context['posts'].first()
        self.assertEqual(post.title, form_data['title'])
        self.assertEqual(post.text, form_data['text'])
