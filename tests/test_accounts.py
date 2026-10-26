from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestingAccounts(TestCase):
    """
    Testing the allauth sign in, sign up and sign out pages
    """

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(username='smiletest')
        self.user.set_password('iliketosmile')
        self.user.save()

    # Retrieving the styled account pages
    def test_account_pages(self):
        pages = [('account_login', 'account/login.html'),
                 ('account_signup', 'account/signup.html')]
        for url_name, template in pages:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'base.html')
            self.assertTemplateUsed(response, template)

        self.client.login(username='smiletest', password='iliketosmile')
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/logout.html')

    # Testing whether a user can sign in
    def test_sign_in(self):
        response = self.client.post(reverse('account_login'),
                                    data={'login': 'smiletest',
                                          'password': 'iliketosmile'})
        self.assertRedirects(response, reverse('home'))
        self.assertIn('_auth_user_id', self.client.session)

    # Testing that a wrong password does not sign in
    def test_sign_in_wrong_password(self):
        response = self.client.post(reverse('account_login'),
                                    data={'login': 'smiletest',
                                          'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    # Testing whether a new user can sign up and is signed in
    def test_sign_up(self):
        response = self.client.post(reverse('account_signup'),
                                    data={'username': 'newmember',
                                          'password1': 'Blue-Kettle-73',
                                          'password2': 'Blue-Kettle-73'})
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newmember').exists())
        self.assertIn('_auth_user_id', self.client.session)

    # Testing whether a user can sign out
    def test_sign_out(self):
        self.client.login(username='smiletest', password='iliketosmile')
        response = self.client.post(reverse('account_logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)
