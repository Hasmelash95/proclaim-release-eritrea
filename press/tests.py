from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article, Comment, Picture
from django.urls import reverse
from .filters import ArticleFilter


class TestingPressViews(TestCase):
    """
    Testing press views
    """

    # Setting up data to test
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(username='smiletest')
        self.user.set_password('iliketosmile')
        self.user.save()

        self.super_user = User.objects.create_superuser(username='super')
        self.super_user.set_password('superuserpass')
        self.super_user.save()

        self.article = Article.objects.create(
                       title='test title',
                       slug='test-title',
                       author=self.super_user,
                       content='test content',
                       excerpt='test excerpt',
                       tags=1,
                       )
        self.comment = Comment.objects.create(
                       article=self.article,
                       user=self.user,
                       subject='test subject',
                       content='test content',
                       approved=True
                       )
        self.picture = Picture.objects.create(
                       title='test picture title',
                       slug='test-picture-title',
                       alt='test-alt-desc'
                       )

    # Retrieving and testing home page
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'includes/messages.html')

    # Retrieving and testing article detail page
    def test_article_detail(self):
        response = self.client.get(reverse('article-detail',
                                   args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'article-detail.html')
        self.assertTemplateUsed(response, 'includes/messages.html')

    # Retrieving and testing article filter page
    def test_article_filter(self):
        response = self.client.get(reverse('filter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'article-filter.html')

    # Retrieving and testing favorites page
    def test_favorites(self):
        # User log in is needed to access page
        self.client.login(username='smiletest', password='iliketosmile')
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'favorites.html')

    # Retrieving and testing the crud pages which need admin login
    def test_crud_view(self):
        self.client.login(username='super', password='superuserpass')
        # Retrieving post article page
        response = self.client.get(reverse('post-article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'post-article.html')
        self.assertTemplateUsed(response, 'includes/messages.html')

        # Retrieving edit article page
        response_two = self.client.get(reverse('edit-article',
                                       args=[self.article.slug]))
        self.assertEqual(response_two.status_code, 200)
        self.assertTemplateUsed(response_two, 'base.html')
        self.assertTemplateUsed(response_two, 'edit-article.html')
        self.assertTemplateUsed(response, 'includes/messages.html')

        # Retrieving delete article page
        response_three = self.client.get(reverse('delete',
                                         args=[self.article.slug]))
        self.assertEqual(response_three.status_code, 200)
        self.assertTemplateUsed(response_three, 'base.html')
        self.assertTemplateUsed(response_three, 'delete.html')

    # Retrieving add article to favorites page
    def test_add_to_favorites_page(self):
        self.client.login(username='smiletest', password='iliketosmile')
        response = self.client.get(reverse('fave-add',
                                           args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'fave-add.html')

    # Testing whether a user can comment on a post
    def test_comment_post(self):
        self.client.login(username='smiletest', password='iliketosmile')
        response = self.client.post(reverse('article-detail',
                                            args=[self.article.slug]),
                                    data={'subject': 'new subject',
                                          'content': 'new comment body'})
        self.assertRedirects(response, reverse('article-detail',
                                               args=[self.article.slug]))

    # Testing whether staff can post an article
    def test_post_article(self):
        self.client.login(username='super', password='superuserpass')
        response = self.client.post(reverse('post-article'),
                                    data={'title': 'new title',
                                          'content': 'new content',
                                          'tags': 0,
                                          'excerpt': 'new excerpt'})
        self.assertRedirects(response, reverse('article-detail',
                                               args=['new-title']))

    # Testing whether staff can edit an article
    def test_edit_article(self):
        self.client.login(username='super', password='superuserpass')
        response = self.client.post(reverse('edit-article',
                                    args=[self.article.slug]),
                                    data={'title': 'update title',
                                          'content': 'update content',
                                          'tags': 1,
                                          })
        self.assertRedirects(response, reverse('article-detail',
                             args=['update-title']))

    # Testing whether staff can delete an article
    def test_delete_article(self):
        self.client.login(username='super', password='superuserpass')
        response = self.client.post(reverse('delete',
                                    args=[self.article.slug]))
        self.assertRedirects(response, '/#press')
        remaining_article = Article.objects.filter(slug=self.article.slug)
        self.assertEqual(len(remaining_article), 0)

    # Testing the add or remove from favorites function
    def test_add_to_favorites(self):
        self.client.login(username='smiletest', password='iliketosmile')
        response = self.client.post(reverse('fave-add',
                                    args=[self.article.slug]))
        self.assertRedirects(response, reverse('article-detail',
                             args=[self.article.slug]))
        num_fave_articles = self.article.favorites.count()
        self.assertEqual(self.article.favorites.count(), 1)
        response = self.client.post(reverse('fave-add',
                                    args=[self.article.slug]))
        self.assertRedirects(response, reverse('article-detail',
                             args=[self.article.slug]))
        self.assertEqual(self.article.favorites.count(), 0)
