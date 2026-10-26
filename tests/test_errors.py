from django.test import TestCase


class TestingErrorPages(TestCase):
    """
    Testing the custom error pages
    """

    # A page that does not exist shows the custom 404 page
    def test_404_page(self):
        response = self.client.get('/this-page-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error404.html')
