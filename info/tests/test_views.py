"""
Tests for the info app's team page.
"""
from django.test import TestCase
from django.urls import reverse


class TestInfoView(TestCase):
    """
    Testing info views
    """
    def test_info_page(self):
        """
        The team page loads successfully.
        """
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)
