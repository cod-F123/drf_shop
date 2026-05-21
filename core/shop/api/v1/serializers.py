from rest_framework import serializers
from django.contrib.auth import get_user_model
from shop.models import Product,  ImageProduct, CharacteristicProduct, Comment, Category, SpecialSuggestion



class UserAuthorCommentSerializer(serializers.ModelSerializer):
    full_name  = serializers.SerializerMethodField('get_full_name', read_only=True)

    def get_full_name(self, obj):

        full_name = obj.profile.full_name if obj.profile.full_name else 'کاربر بی نام'

        return full_name

    class Meta:
        model = get_user_model()
        fields = ['full_name']


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


class CommentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only=True)
    user = UserAuthorCommentSerializer(read_only=True)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user 

        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'rating', 'created_at', 'product']
        read_only_fields = ['id', 'created_at', 'user']

class RelatedProductSerializer(serializers.ModelSerializer):
    category = CategorySerialzier(read_only=True)

    image = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)

    class Meta:
        model = Product
        fields = ["id","slug", "image", "title", "category","is_exist", "is_offed", "discount", "price", "offed_price","stock", "tag"]


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerialzier(read_only=True)
    
    galary = ImageProductSerializer(read_only=True, many=True)

    Specifications = CharacteristicProductSrializer(read_only=True, many=True)

    comments = CommentSerializer(read_only=True, many=True)

    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField('get_absolute_url', read_only=True)

    def get_absolute_url(self, obj):
        request = self.context.get("request")

        absolute_url = request.build_absolute_uri(obj.get_absolute_api_url())

        return absolute_url
    

    def to_representation(self, instance):
        rep =  super().to_representation(instance)

        request = self.context.get("request")

        if request.parser_context.get("kwargs").get("slug"):
            rep.pop('relative_url')
            rep.pop('absolute_url')
            rep["related_products"] = RelatedProductSerializer(Product.objects.filter(category__name = rep.get("category").get("name"))[:10], many=True, context={"request":request}).data

        else:
            rep.pop('galary')
            rep.pop('Specifications')
            rep.pop('description')
            rep.pop('comments')

        return rep

    class Meta:
        model = Product

        fields = ["id","title", "image", "description", "category", "is_exist", "is_offed", "discount", "price", "offed_price","stock", "tag", "slug", "relative_url", "absolute_url", "galary", "Specifications", "comments"]



class SpecialSuggestionSerilaizer(serializers.ModelSerializer):

    products = ProductSerializer(many=True, read_only=True)
    remaining_sconds = serializers.SerializerMethodField("get_remaining_seconds")

    def get_remaining_seconds(self, obj):
        
        return int(obj.remaining.total_seconds()) if obj.remaining != 0 else 0

    class Meta:
        model = SpecialSuggestion
        fields = ["start_at", "end_at", "products","is_active","remaining_sconds"]