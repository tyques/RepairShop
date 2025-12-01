from django.shortcuts import get_object_or_404, render

from .models import ApplianceType, RepairOrder, Workshop


def index(request):
    """Главная страница - список заказов на ремонт"""
    order_list = RepairOrder.objects.select_related(
        'customer', 'appliance_type', 'workshop', 'master', 'status'
    ).filter(
        is_published=True,
        appliance_type__is_published=True
    ).order_by('-created_at')[:10]
    return render(request, 'repair/index.html', {'order_list': order_list})


def order_detail(request, order_id):
    """Детальная информация о заказе на ремонт"""
    order = get_object_or_404(
        RepairOrder.objects.select_related(
            'customer', 'appliance_type', 'workshop', 'master', 'status'
        ),
        pk=order_id,
        is_published=True,
        appliance_type__is_published=True
    )
    return render(request, 'repair/detail.html', {'order': order})


def appliance_type_orders(request, appliance_type_slug):
    """Заказы по типу техники"""
    appliance_type = get_object_or_404(
        ApplianceType,
        slug=appliance_type_slug,
        is_published=True
    )
    order_list = appliance_type.orders.select_related(
        'customer', 'workshop', 'master', 'status'
    ).filter(
        is_published=True
    ).order_by('-created_at')
    return render(
        request,
        'repair/category.html',
        {'appliance_type': appliance_type, 'order_list': order_list}
    )


def workshop_orders(request, workshop_id):
    """Заказы по мастерской"""
    workshop = get_object_or_404(
        Workshop,
        pk=workshop_id,
        is_published=True
    )
    order_list = RepairOrder.objects.select_related(
        'customer', 'appliance_type', 'master', 'status'
    ).filter(
        workshop=workshop,
        is_published=True,
        appliance_type__is_published=True
    ).order_by('-created_at')
    return render(
        request,
        'repair/workshop.html',
        {'workshop': workshop, 'order_list': order_list}
    )
