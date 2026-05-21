from rest_framework import serializers
from shop.models import Product
from payment.models import Order, OrderItem


class ProductOrderItemSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id","slug","title", "image",  "is_offed", "discount", "price", "offed_price", "tag"]

class OrderItemSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        product = attrs.get("product")
        
        if (product.stock - attrs.get("quantity", 1)) <= 0 :
            raise serializers.ValidationError({'product': f"Not enough stock for {product.title}"})

        return super().validate(attrs)
    
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        
        rep['product'] = ProductOrderItemSerialzier(instance = Product.objects.get(id = rep.get("product"))).data

        return rep

    class Meta:
        model = OrderItem
        fields = ["id",'product', 'amount', 'quantity']
        read_only_fields = ['amount', "id"]


class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True)

    created_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only = True)
    payed_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only = True)
    sent_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only=True)

    def validate(self, attrs):

        if len(attrs.get('items', 0)) < 1 :
            raise serializers.ValidationError(
                'Order must contain at least one item.'
            )
        
        return super().validate(attrs)
    

    def create(self, validated_data):

        validated_data['user'] = self.context['request'].user
        
        items_data = validated_data.pop("items")
        
        order = Order.objects.create(total_amount = 0, **validated_data)

        for item in items_data:

            OrderItem.objects.create(order = order, product = item.get("product") , quantity = item.get("quantity"))

        return order

    class Meta:

        model = Order

        fields = ["order_id", 'total_amount', 'status', 'created_at', 'payed_at', 'sent_at', 'items']

        read_only_fields = ['order_id', 'total_amount', 'status',]
