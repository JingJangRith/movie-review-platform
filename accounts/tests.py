from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass!9284",
        )

    def test_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass!9284",
            "password2": "StrongPass!9284",
        })

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "StrongPass!9284",
        })

        self.assertRedirects(response, reverse("dashboard"))

    def test_profile_update(self):
        self.client.login(username="testuser", password="StrongPass!9284")

        response = self.client.post(reverse("profile"), {
            "username": "updateduser",
            "email": "updated@example.com",
            "first_name": "Test",
            "last_name": "User",
        })

        self.assertRedirects(response, reverse("profile"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updated@example.com")

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}"
        )

    def test_logout_requires_post(self):
        self.client.login(username="testuser", password="StrongPass!9284")

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_post(self):
        self.client.login(username="testuser", password="StrongPass!9284")

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_account_deletion(self):
        self.client.login(username="testuser", password="StrongPass!9284")

        response = self.client.post(reverse("delete_account"))

        self.assertRedirects(response, reverse("login"))
        self.assertFalse(User.objects.filter(username="testuser").exists())