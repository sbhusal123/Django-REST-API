from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

"""
Django admin site : https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#module-django.contrib.admin
Reversing admin URLs : https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#reversing-admin-urls
""" # noqa


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()

        # create super user
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@surya.com",
            password="test123"
        )

        # log in user through django test client
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='test2@surya.com',
            password="testpassword",
            name="Test user full name"
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""

        # defined in the django admin as {app_name}_{model_name}_{}
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """Test that user edit page works"""
        # /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
