from rest_framework import serializers

from Stripe.models import Order, ItemOrder, Item


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ('id',)


class ItemOrderSerializer(serializers.ModelSerializer):
    # item_id = serializers.StringRelatedField()
    item_name = serializers.CharField(source="item_id.name", read_only=True)

    class Meta:
        model = ItemOrder
        fields = ['item_id', 'item_name', 'quantity', ]
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    order = ItemOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ('id',)

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        order = super().create(validated_data)
        for element in range(len(order_data)):
            ItemOrder.objects.create(order_id=order, **order_data[element])
        return order

    def update(self, instance, validated_data):
        order_data = validated_data.pop('order')
        order = super().update(instance, validated_data)
        for value in order_data:
            ItemOrder.objects.update_or_create(
                order_id=order,
                item_id=value.get('item_id'),
                defaults={
                    'quantity': value.get('quantity'),
                })
        return order
