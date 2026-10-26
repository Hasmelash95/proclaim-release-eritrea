from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ..models import Article


class TestPublishedDate(TestCase):
    """
    Testing the published date, which is shown, sorted and filtered on
    instead of the date an article was added to the site
    """

    @classmethod
    def setUpTestData(self):
        self.super_user = User.objects.create_superuser(username='super')
        self.super_user.set_password('superuserpass')
        self.super_user.save()

        # Added to the site first, but published most recently
        self.recent = Article.objects.create(
                      title='Recent release', slug='recent-release',
                      author=self.super_user, content='recent content',
                      excerpt='recent excerpt', tags=0,
                      published_on=date(2026, 3, 1))
        # Restored to the site later, with its original older date
        self.restored = Article.objects.create(
                        title='Restored release', slug='restored-release',
                        author=self.super_user, content='restored content',
                        excerpt='restored excerpt', tags=1,
                        published_on=date(2019, 5, 22))

    def setUp(self):
        self.client.login(username='super', password='superuserpass')

    # Articles are listed by published date, not when they were added
    def test_home_sorted_by_published_date(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(list(response.context['article']),
                         [self.recent, self.restored])

    # The article page shows the published date
    def test_detail_shows_published_date(self):
        response = self.client.get(reverse('article-detail',
                                   args=[self.restored.slug]))
        self.assertContains(response, 'Published on May 22, 2019')
        self.assertNotContains(response, 'Updated on')

    # Staff can give a new article its original published date
    def test_post_with_published_date(self):
        self.client.post(reverse('post-article'),
                         data={'title': 'old release', 'content': 'content',
                               'excerpt': 'excerpt', 'tags': 1,
                               'published_on': '2018-01-15'})
        article = Article.objects.get(slug='old-release')
        self.assertEqual(article.published_on, date(2018, 1, 15))

    # A new article without a date is published today
    def test_post_without_date_uses_today(self):
        self.client.post(reverse('post-article'),
                         data={'title': 'new release', 'content': 'content',
                               'excerpt': 'excerpt', 'tags': 0})
        article = Article.objects.get(slug='new-release')
        self.assertEqual(article.published_on, timezone.localdate())

    # Editing without a date keeps the article's existing date
    def test_edit_keeps_date(self):
        self.client.post(reverse('edit-article', args=[self.restored.slug]),
                         data={'title': 'Restored release',
                               'content': 'updated content', 'tags': 1})
        self.restored.refresh_from_db()
        self.assertEqual(self.restored.content, 'updated content')
        self.assertEqual(self.restored.published_on, date(2019, 5, 22))

    # The filter page searches and sorts by published date
    def test_filter_by_published_date(self):
        response = self.client.get(reverse('filter'),
                                   {'published_on_max': '2020-01-01'})
        self.assertEqual(list(response.context['filter'].qs),
                         [self.restored])
        response = self.client.get(reverse('filter'),
                                   {'ordering': 'published_on'})
        self.assertEqual(list(response.context['filter'].qs),
                         [self.restored, self.recent])
