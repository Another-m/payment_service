import stripe
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from rest_framework import viewsets

from Payment_service.settings import HOST, API_KEY
from Stripe.models import Item, Order, ItemOrder
from Stripe.serializers import OrderSerializer, ItemOrderSerializer, ItemSerializer

stripe.api_key = API_KEY


# Главная страница
def index(request):
    template = 'index.html'
    data = request_params(request)
    products = Item.objects.all()
    context = dict(products=products,
                   title='Страница товаров',
                   quan_items=data['count'],
                   order_sum=data['order_sum'],
                   )
    return render(request, template, context)


# Страница описания товара
def item(request, item):
    template = 'item.html'
    products = Item.objects.get(pk=item)
    data = request_params(request)
    context = dict(item=products,
                   title='Описание товара',
                   quan_items=data['count'],
                   order_sum=data['order_sum'],
                   )
    return render(request, template, context)


# Корзина
def basket(request):
    template = 'order.html'
    data = request_params(request)
    products = get_items(data['order_id'])

    context = dict(products=products,
                   title='Корзина',
                   quan_items=data['count'],
                   order_sum=data['order_sum'],
                   order_id=data['order_id'],
                   )
    return render(request, template, context)


# Страница оплаты
def payment(request, order_id):
    products = get_items(order_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': i['items'].currency,
                'product_data': {
                    'name': i['items'].name,
                },
                'unit_amount': i['items'].price * 100,
            },
            'quantity': i['quantity'],
        } for i in products],
        mode='payment',
        success_url='{}/success'.format(HOST),
        cancel_url='{}/order'.format(HOST),
    )
    return redirect(session.url, code=303)


# Страница успеха
def success(request):
    template = 'success.html'
    data = request_params(request)
    products = get_items(data['order_id'])

    context = dict(products=products,
                   title='Завершение оплаты',
                   quan_items=data['count'],
                   order_sum=data['order_sum'],
                   order_id=data['order_id'],
                   )
    return render(request, template, context)


# Выйти из сессии
def clear_order(request):
    del request.session['order']
    return redirect('order')


class ItemViewSet(viewsets.ModelViewSet):
    """
    Класс для просмотра всех товаров через API
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Класс для просмотра всех заказов через API
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ItemOrderViewSet(viewsets.ModelViewSet):
    """
    Класс для связующей таблицы многие ко многим
    """
    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer


# Добавление, изменение данных при наличии параметров в запросе
def request_params(request):
    page_params = request.GET.get("choose")
    page_params1 = request.GET.get("quantity")
    order_id = 0
    if 'order' in request.session:
        order = request.session.get('order')
        order_id = Order.objects.get(id=order)
    if page_params:
        if not order_id:
            order_id = Order.objects.create()
            request.session['order'] = order_id.id
        if "del" in request.GET:
            dell_item(order_id, page_params)
        # elif page_params == 'clear':
        #     clear_order(request)
        else:
            choose_items(order_id, page_params, page_params1)
    count = count_items(order_id)
    return dict(order_id=order_id, count=count['count'], order_sum=count['main_sum'])


# Выбор товаров и добвление в корзину либо изменение количества, если товар есть в корзине
def choose_items(order_id, page_params, page_params1):
    item_id = Item.objects.get(pk=page_params)
    order = ItemOrder(order_id=order_id,
                      item_id=item_id,
                      quantity=page_params1,
                      )
    try:
        order.save()
    except:
        order = ItemOrder.objects.get(order_id=order_id, item_id=item_id)
        order.quantity = page_params1
        order.save()


# Удаление товара из корзины
def dell_item(order_id, page_params):
    item = ItemOrder.objects.get(order_id=order_id, item_id=page_params)
    item.delete()


# Счетчик количества товаров в корзине и общей суммы заказа
def count_items(order_id):
    if not order_id:
        return dict(count=0, main_sum=0)
    count = ItemOrder.objects.filter(order_id=order_id).aggregate(Sum('quantity'))
    main_sum = ItemOrder.objects.filter(order_id=order_id).aggregate(total=Sum(F('item_id__price') * F('quantity')))[
        'total']
    check_currency = ItemOrder.objects.filter(order_id=order_id).distinct('item_id__currency').count()
    if check_currency == 1:
        currency = ItemOrder.objects.filter(order_id=order_id).first().item_id.currency
        main_sum = f"Сумма заказа: {main_sum} {currency}"
    else:
        main_sum = "Заказ невозможен! В корзине товары в разных валютах."
    return dict(count=count['quantity__sum'], main_sum=main_sum)


# Получить из базы товары для оплты по id заказа из сессии
def get_items(order_id):
    items = ItemOrder.objects.filter(order_id=order_id).select_related('item_id')
    return [dict(items=i.item_id, quantity=i.quantity) for i in items]
