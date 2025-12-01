from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class ApplianceType(models.Model):
    """Тип бытовой техники"""
    title = models.CharField(
        'Название типа техники',
        max_length=256
    )
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )
    is_published = models.BooleanField(
        'Активен',
        default=True,
        help_text='Снимите галочку, чтобы скрыть тип техники.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'тип техники'
        verbose_name_plural = 'Типы техники'

    def __str__(self):
        return self.title


class Workshop(models.Model):
    """Мастерская/филиал"""
    name = models.CharField('Название мастерской', max_length=256)
    address = models.CharField('Адрес', max_length=512, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    is_published = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'мастерская'
        verbose_name_plural = 'Мастерские'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Клиент мастерской"""
    name = models.CharField('Имя', max_length=256)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адрес', max_length=512, blank=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.name} ({self.phone})"


class RepairStatus(models.Model):
    """Статус ремонта"""
    name = models.CharField('Название статуса', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'статус ремонта'
        verbose_name_plural = 'Статусы ремонта'
        ordering = ['order']

    def __str__(self):
        return self.name


class RepairOrder(models.Model):
    """Заказ на ремонт"""
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='orders'
    )
    appliance_type = models.ForeignKey(
        ApplianceType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип техники',
        related_name='orders'
    )
    appliance_brand = models.CharField('Марка техники', max_length=100)
    appliance_model = models.CharField('Модель техники', max_length=100, blank=True)
    description = models.TextField('Описание неисправности')
    master = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Мастер',
        related_name='repair_orders'
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Мастерская'
    )
    status = models.ForeignKey(
        RepairStatus,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Статус ремонта'
    )
    estimated_cost = models.DecimalField(
        'Предварительная стоимость',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    final_cost = models.DecimalField(
        'Финальная стоимость',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    accepted_at = models.DateTimeField('Дата принятия', null=True, blank=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)
    is_published = models.BooleanField('Отображать', default=True)

    class Meta:
        verbose_name = 'заказ на ремонт'
        verbose_name_plural = 'Заказы на ремонт'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.customer.name} ({self.appliance_brand})"
