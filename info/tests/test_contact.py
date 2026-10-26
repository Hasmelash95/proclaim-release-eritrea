from django.test import TestCase
from django.urls import reverse
from ..models import ContactMessage


class TestContactForm(TestCase):
    """
    Testing the contact form
    """

    def setUp(self):
        self.message = {'name': 'Test Sender',
                        'email': 'sender@example.com',
                        'subject': 'Getting involved',
                        'message': 'How can I help?'}

    # Retrieving the contact page
    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'info/contact.html')

    # Testing a sent message is saved and a thank you is shown
    def test_send_message(self):
        response = self.client.post(reverse('contact'), self.message,
                                    follow=True)
        self.assertRedirects(response, reverse('contact'))
        self.assertContains(response, 'Thank you for your message')
        saved = ContactMessage.objects.get()
        self.assertEqual(saved.email, 'sender@example.com')
        self.assertEqual(saved.message, 'How can I help?')
        self.assertFalse(saved.handled)

    # Testing missing fields and a bad email are not saved
    def test_invalid_message(self):
        response = self.client.post(reverse('contact'),
                                    {**self.message, 'email': 'not-an-email',
                                     'message': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['contact_form'].errors)
        self.assertEqual(ContactMessage.objects.count(), 0)

    # Testing spam bots that fill in the hidden field are not saved
    def test_spam_is_not_saved(self):
        response = self.client.post(reverse('contact'),
                                    {**self.message,
                                     'website': 'http://spam.example.com'},
                                    follow=True)
        self.assertContains(response, 'Thank you for your message')
        self.assertEqual(ContactMessage.objects.count(), 0)

    # The team page links to the contact page instead of the offices
    def test_team_page_links_to_contact(self):
        response = self.client.get(reverse('info'))
        self.assertContains(response, reverse('contact'))
        self.assertNotContains(response, 'Our Offices')
