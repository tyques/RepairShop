from django.test import TestCase, Client
from django.urls import reverse


class PagesURLTests(TestCase):
    def setUp(self):
        # Создаем клиент для имитации запросов неавторизованного пользователя
        self.guest_client = Client()

    def test_about_page_exists_at_desired_location(self):
        """Проверка доступности страницы 'О нас' по прямому URL."""
        response = self.guest_client.get('/pages/about/')
        self.assertEqual(response.status_code, 200)

    def test_rules_page_exists_at_desired_location(self):
        """Проверка доступности страницы 'Правила' по прямому URL."""
        response = self.guest_client.get('/pages/rules/')
        self.assertEqual(response.status_code, 200)

    def test_pages_use_correct_template(self):
        """Проверка использования правильных шаблонов для страниц."""
        templates_pages_names = {
            'pages/about.html': reverse('pages:about'),
            'pages/rules.html': reverse('pages:rules'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)