from django.contrib import admin

from .models import (
    ApplianceType, Workshop, Customer, RepairStatus, RepairOrder
)


@admin.register(ApplianceType)
class ApplianceTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('name', 'address', 'phone')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('created_at',)


@admin.register(RepairStatus)
class RepairStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'appliance_type', 'appliance_brand',
        'status', 'master', 'workshop', 'final_cost', 'created_at'
    )
    list_filter = (
        'status', 'appliance_type', 'workshop', 'master',
        'is_published', 'created_at'
    )
    search_fields = (
        'customer__name', 'customer__phone', 'appliance_brand',
        'appliance_model', 'description'
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('customer', 'appliance_type', 'appliance_brand', 'appliance_model')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Организация', {
            'fields': ('workshop', 'master', 'status')
        }),
        ('Стоимость', {
            'fields': ('estimated_cost', 'final_cost')
        }),
        ('Даты', {
            'fields': ('created_at', 'accepted_at', 'completed_at')
        }),
        ('Настройки', {
            'fields': ('is_published',)
        }),
    )
