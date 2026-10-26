from django.test import TestCase
from django.urls import reverse
from ..models import ContactMessage


class TestContactForm(TestCase):
    """
    Testing the contact form on the team page
    """

    def setUp(self):
        self.url = reverse('info')
        self.message = {'name': 'Test Sender',
                        'email': 'sender@example.com',
                        'subject': 'Getting involved',
                        'message': 'How can I help?'}

    # The team page shows the contact form
    def test_form_on_team_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/info.html')
        self.assertContains(response, 'id="contact"')
        self.assertContains(response, 'name="message"')
        self.assertNotContains(response, 'Our Offices')

    # Testing a sent message is saved and a thank you is shown
    def test_send_message(self):
        response = self.client.post(self.url, self.message, follow=True)
        self.assertRedirects(response, self.url + '#contact')
        self.assertContains(response, 'Thank you for your message')
        saved = ContactMessage.objects.get()
        self.assertEqual(saved.email, 'sender@example.com')
        self.assertEqual(saved.message, 'How can I help?')
        self.assertFalse(saved.handled)

    # Testing missing fields and a bad email are not saved
    def test_invalid_message(self):
        response = self.client.post(self.url,
                                    {**self.message, 'email': 'not-an-email',
                                     'message': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/info.html')
        self.assertTrue(response.context['contact_form'].errors)
        self.assertEqual(ContactMessage.objects.count(), 0)

    # Testing spam bots that fill in the hidden field are not saved
    def test_spam_is_not_saved(self):
        response = self.client.post(self.url,
                                    {**self.message,
                                     'website': 'http://spam.example.com'},
                                    follow=True)
        self.assertContains(response, 'Thank you for your message')
        self.assertEqual(ContactMessage.objects.count(), 0)
