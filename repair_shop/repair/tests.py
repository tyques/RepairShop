from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from repair_shop.repair.models import (
    ApplianceType, Workshop, Customer, RepairStatus, RepairOrder
)

User = get_user_model()


class RepairModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестовые данные, общие для всех тестов класса
        cls.customer = Customer.objects.create(
            name='Тестовый Клиент',
            phone='+79990000000'
        )
        cls.appliance_type = ApplianceType.objects.create(
            title='Тестовый Тип',
            slug='test-type',
            description='Описание типа'
        )
        cls.workshop = Workshop.objects.create(
            name='Тестовая Мастерская',
            address='Адрес'
        )
        cls.status = RepairStatus.objects.create(
            name='Новый',
            order=1
        )
        cls.order = RepairOrder.objects.create(
            customer=cls.customer,
            appliance_type=cls.appliance_type,
            appliance_brand='BrandX',
            description='Сломалось',
            workshop=cls.workshop,
            status=cls.status
        )

    def test_models_have_correct_object_names(self):
        """Проверка того, что у моделей корректно работает __str__."""
        order = RepairModelTest.order
        expected_object_name = f"Заказ #{order.id} - {order.customer.name} ({order.appliance_brand})"
        self.assertEqual(expected_object_name, str(order))

        self.assertEqual(str(RepairModelTest.customer), 'Тестовый Клиент (+79990000000)')
        self.assertEqual(str(RepairModelTest.appliance_type), 'Тестовый Тип')
        self.assertEqual(str(RepairModelTest.workshop), 'Тестовая Мастерская')
        self.assertEqual(str(RepairModelTest.status), 'Новый')


class RepairViewsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='master')

        # Создаем основные данные
        self.customer = Customer.objects.create(name='Ivan', phone='123')
        self.appliance_type = ApplianceType.objects.create(
            title='Fridge',
            slug='fridge',
            is_published=True
        )
        self.workshop = Workshop.objects.create(name='Main Shop', is_published=True)
        self.status = RepairStatus.objects.create(name='In Progress', order=1)

        # Создаем публичный заказ
        self.order = RepairOrder.objects.create(
            customer=self.customer,
            appliance_type=self.appliance_type,
            appliance_brand='Samsung',
            description='Broken',
            workshop=self.workshop,
            status=self.status,
            is_published=True
        )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'repair/index.html': reverse('repair:index'),
            'repair/detail.html': reverse('repair:order_detail', kwargs={'order_id': self.order.id}),
            'repair/category.html': reverse('repair:appliance_type_orders',
                                            kwargs={'appliance_type_slug': self.appliance_type.slug}),
            'repair/workshop.html': reverse('repair:workshop_orders', kwargs={'workshop_id': self.workshop.id}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, 200)

    def test_index_page_show_correct_context(self):
        """На главную страницу передается список заказов."""
        response = self.guest_client.get(reverse('repair:index'))
        first_object = response.context['order_list'][0]
        self.assertEqual(first_object.appliance_brand, 'Samsung')
        self.assertEqual(first_object.customer.name, 'Ivan')
        self.assertEqual(first_object.status.name, 'In Progress')

    def test_order_detail_page_show_correct_context(self):
        """На страницу заказа передается правильный заказ."""
        response = self.guest_client.get(
            reverse('repair:order_detail', kwargs={'order_id': self.order.id})
        )
        self.assertEqual(response.context['order'].description, 'Broken')

    def test_category_page_show_correct_context(self):
        """На странице категории отображаются заказы только этой категории."""
        # Создадим второй тип техники и заказ для него
        other_type = ApplianceType.objects.create(title='Oven', slug='oven')
        RepairOrder.objects.create(
            customer=self.customer,
            appliance_type=other_type,
            appliance_brand='Bosch',
            description='Oven broken',
            is_published=True
        )

        response = self.guest_client.get(
            reverse('repair:appliance_type_orders', kwargs={'appliance_type_slug': 'fridge'})
        )
        # В контексте должен быть только 1 заказ (холодильник), а не 2
        self.assertEqual(len(response.context['order_list']), 1)
        self.assertEqual(response.context['appliance_type'], self.appliance_type)

    def test_404_if_order_does_not_exist(self):
        """Проверка возврата 404 для несуществующего заказа."""
        response = self.guest_client.get(
            reverse('repair:order_detail', kwargs={'order_id': 999})
        )
        self.assertEqual(response.status_code, 404)


class RepairLogicTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.customer = Customer.objects.create(name='Test', phone='000')
        self.appliance_type = ApplianceType.objects.create(
            title='TV', slug='tv', is_published=True
        )

    def test_unpublished_order_not_shown(self):
        """Скрытый заказ (is_published=False) не должен отображаться на главной."""
        RepairOrder.objects.create(
            customer=self.customer,
            appliance_type=self.appliance_type,
            appliance_brand='Sony',
            description='Hidden',
            is_published=False  # Скрыт
        )

        response = self.guest_client.get(reverse('repair:index'))
        self.assertEqual(len(response.context['order_list']), 0)

    def test_order_with_unpublished_category_not_shown(self):
        """Заказ, у которого скрыт тип техники, не должен отображаться."""
        hidden_type = ApplianceType.objects.create(
            title='Hidden Type', slug='hidden', is_published=False
        )
        RepairOrder.objects.create(
            customer=self.customer,
            appliance_type=hidden_type,  # Тип скрыт
            appliance_brand='LG',
            description='Hidden by category',
            is_published=True
        )

        response = self.guest_client.get(reverse('repair:index'))
        self.assertEqual(len(response.context['order_list']), 0)

    def test_unpublished_order_detail_404(self):
        """Страница деталей скрытого заказа должна возвращать 404."""
        hidden_order = RepairOrder.objects.create(
            customer=self.customer,
            appliance_type=self.appliance_type,
            appliance_brand='Sony',
            description='Hidden',
            is_published=False
        )
        response = self.guest_client.get(
            reverse('repair:order_detail', kwargs={'order_id': hidden_order.id})
        )
        self.assertEqual(response.status_code, 404)