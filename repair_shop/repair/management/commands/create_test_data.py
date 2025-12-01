"""
Команда для создания тестовых данных мастерской по ремонту.
Использование: python manage.py create_test_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from repair_shop.repair.models import (
    ApplianceType, Workshop, Customer, RepairStatus, RepairOrder
)
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовые данные для мастерской по ремонту'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        # Создание статусов ремонта
        statuses_data = [
            {'name': 'Принят', 'order': 1, 'description': 'Заказ принят в работу'},
            {'name': 'В работе', 'order': 2, 'description': 'Ремонт выполняется'},
            {'name': 'Готов', 'order': 3, 'description': 'Ремонт завершен'},
            {'name': 'Выдан', 'order': 4, 'description': 'Техника выдана клиенту'},
        ]
        
        statuses = {}
        for status_data in statuses_data:
            status, created = RepairStatus.objects.get_or_create(
                name=status_data['name'],
                defaults=status_data
            )
            statuses[status_data['name']] = status
            if created:
                self.stdout.write(f'  ✓ Создан статус: {status.name}')

        # Создание типов техники
        appliance_types_data = [
            {
                'title': 'Холодильник',
                'slug': 'refrigerator',
                'description': 'Ремонт холодильников всех марок и моделей'
            },
            {
                'title': 'Стиральная машина',
                'slug': 'washing-machine',
                'description': 'Ремонт стиральных машин, включая диагностику и замену запчастей'
            },
            {
                'title': 'Микроволновая печь',
                'slug': 'microwave',
                'description': 'Ремонт микроволновых печей'
            },
            {
                'title': 'Посудомоечная машина',
                'slug': 'dishwasher',
                'description': 'Ремонт посудомоечных машин'
            },
        ]

        appliance_types = {}
        for at_data in appliance_types_data:
            at, created = ApplianceType.objects.get_or_create(
                slug=at_data['slug'],
                defaults=at_data
            )
            appliance_types[at_data['slug']] = at
            if created:
                self.stdout.write(f'  ✓ Создан тип техники: {at.title}')

        # Создание мастерских
        workshops_data = [
            {
                'name': 'Мастерская на Ленина',
                'address': 'ул. Ленина, д. 10',
                'phone': '+7 (495) 123-45-67'
            },
            {
                'name': 'Мастерская на Пушкина',
                'address': 'ул. Пушкина, д. 25',
                'phone': '+7 (495) 234-56-78'
            },
        ]

        workshops = []
        for w_data in workshops_data:
            w, created = Workshop.objects.get_or_create(
                name=w_data['name'],
                defaults=w_data
            )
            workshops.append(w)
            if created:
                self.stdout.write(f'  ✓ Создана мастерская: {w.name}')

        # Создание мастера (если нет пользователей)
        if not User.objects.filter(is_staff=True).exists():
            master = User.objects.create_user(
                username='master',
                email='master@example.com',
                password='master123',
                first_name='Иван',
                last_name='Мастеров',
                is_staff=True
            )
            self.stdout.write(f'  ✓ Создан мастер: {master.username}')
        else:
            master = User.objects.filter(is_staff=True).first()

        # Создание клиентов
        customers_data = [
            {
                'name': 'Иванов Иван Иванович',
                'phone': '+7 (999) 111-22-33',
                'email': 'ivanov@example.com',
                'address': 'ул. Примерная, д. 1, кв. 10'
            },
            {
                'name': 'Петрова Мария Сергеевна',
                'phone': '+7 (999) 222-33-44',
                'email': 'petrova@example.com',
                'address': 'ул. Тестовая, д. 5, кв. 20'
            },
            {
                'name': 'Сидоров Петр Александрович',
                'phone': '+7 (999) 333-44-55',
                'email': '',
                'address': ''
            },
        ]

        customers = []
        for c_data in customers_data:
            c, created = Customer.objects.get_or_create(
                phone=c_data['phone'],
                defaults=c_data
            )
            customers.append(c)
            if created:
                self.stdout.write(f'  ✓ Создан клиент: {c.name}')

        # Создание заказов на ремонт
        orders_data = [
            {
                'customer': customers[0],
                'appliance_type': appliance_types['refrigerator'],
                'appliance_brand': 'Samsung',
                'appliance_model': 'RB33J3000SA',
                'description': 'Не морозит, не включается компрессор. Требуется диагностика.',
                'status': statuses['В работе'],
                'workshop': workshops[0],
                'master': master,
                'estimated_cost': 3500.00,
                'created_at': timezone.now() - timedelta(days=5),
            },
            {
                'customer': customers[1],
                'appliance_type': appliance_types['washing-machine'],
                'appliance_brand': 'LG',
                'appliance_model': 'F2J5HS4W',
                'description': 'Не отжимает, не сливает воду. Возможно засор сливного насоса.',
                'status': statuses['Готов'],
                'workshop': workshops[0],
                'master': master,
                'estimated_cost': 2500.00,
                'final_cost': 2800.00,
                'created_at': timezone.now() - timedelta(days=3),
                'completed_at': timezone.now() - timedelta(days=1),
            },
            {
                'customer': customers[2],
                'appliance_type': appliance_types['microwave'],
                'appliance_brand': 'Panasonic',
                'appliance_model': 'NN-ST45KW',
                'description': 'Не греет, но включается. Возможно проблема с магнетроном.',
                'status': statuses['Принят'],
                'workshop': workshops[1],
                'estimated_cost': 2000.00,
                'created_at': timezone.now() - timedelta(days=1),
            },
            {
                'customer': customers[0],
                'appliance_type': appliance_types['dishwasher'],
                'appliance_brand': 'Bosch',
                'appliance_model': 'SMS2IKI14R',
                'description': 'Не моет посуду, вода не нагревается. Требуется замена ТЭНа.',
                'status': statuses['Выдан'],
                'workshop': workshops[1],
                'master': master,
                'estimated_cost': 4000.00,
                'final_cost': 4200.00,
                'created_at': timezone.now() - timedelta(days=10),
                'completed_at': timezone.now() - timedelta(days=7),
            },
        ]

        created_orders = 0
        for order_data in orders_data:
            order, created = RepairOrder.objects.get_or_create(
                customer=order_data['customer'],
                appliance_brand=order_data['appliance_brand'],
                appliance_model=order_data['appliance_model'],
                created_at__date=order_data['created_at'].date(),
                defaults=order_data
            )
            if created:
                created_orders += 1
                self.stdout.write(
                    f'  ✓ Создан заказ #{order.id}: '
                    f'{order.appliance_brand} ({order.customer.name})'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Готово! Создано заказов: {created_orders}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                '\nДля входа в админ-панель используйте:\n'
                '  Логин: master\n'
                '  Пароль: master123\n'
            )
        )

