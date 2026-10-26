from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Article


class TestingPermissions(TestCase):
    """
    Testing that only staff can manage articles and only
    logged in users can use favorites
    """

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(username='smiletest')
        self.user.set_password('iliketosmile')
        self.user.save()

        self.super_user = User.objects.create_superuser(username='super')
        self.article = Article.objects.create(
                       title='test title',
                       slug='test-title',
                       author=self.super_user,
                       content='test content',
                       excerpt='test excerpt',
                       tags=1,
                       )

    # Non staff users are sent to the admin login instead of the crud pages
    def test_crud_pages_need_staff(self):
        self.client.login(username='smiletest', password='iliketosmile')
        for url in [reverse('post-article'),
                    reverse('edit-article', args=[self.article.slug]),
                    reverse('delete', args=[self.article.slug])]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('admin:login'), response.url)

    # Logged out users cannot delete an article
    def test_delete_needs_staff(self):
        response = self.client.post(reverse('delete',
                                    args=[self.article.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(slug=self.article.slug).exists())

    # Logged out users cannot post an article
    def test_post_needs_staff(self):
        response = self.client.post(reverse('post-article'),
                                    data={'title': 'sneaky title',
                                          'content': 'sneaky content',
                                          'tags': 0,
                                          'excerpt': 'sneaky excerpt'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(slug='sneaky-title').exists())

    # Logged out users are sent to sign in before using favorites
    def test_favorites_need_login(self):
        for url in [reverse('favorites'),
                    reverse('fave-add', args=[self.article.slug])]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('account_login'), response.url)
