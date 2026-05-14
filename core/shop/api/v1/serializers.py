from rest_framework import serializers
from shop.models import Product,  ImageProduct, CharacteristicProduct, Comment, Category


class CategorySerialzier(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name', 'image']
    

class ImageProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageProduct
        fields = ['id', 'img']  


class CharacteristicProductSrializer(serializers.ModelSerializer):
    
    class Meta:
        model = CharacteristicProduct
        fields = ['id', 'key', 'value']


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerialzier(read_only=True)
    
    galary = ImageProductSerializer(read_only=True, many=True)

    Specifications = CharacteristicProductSrializer(read_only=True, many=True)

    def to_representation(self, instance):
        rep =  super().to_representation(instance)

        request = self.context.get("request")

        if request.parser_context.get("kwargs").get("slug"):
            pass 

        else:
            rep.pop('galary')
            rep.pop('Specifications')
            rep.pop('description')

        return rep

    class Meta:
        model = Product

        fields = "__all__"


