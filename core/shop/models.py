from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from decimal import Decimal
import uuid


User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=191, unique=True)    

    image  = models.ImageField(upload_to='category/imgs', blank=True,null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):

    TAGS = (
        ('Special', 'Special'),
        ('Best-Seller', 'Best-Seller')
    )

    title = models.CharField(max_length=110)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    description = HTMLField()
    image = models.ImageField(upload_to='product/imgs')

    price = models.DecimalField(max_digits=15, decimal_places=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.0"))

    added_at = models.DateTimeField(auto_now_add=True)

    stock = models.PositiveBigIntegerField(default=0)

    tag = models.CharField(max_length=11, choices=TAGS, blank=True, null=True)

    slug = models.CharField(max_length=191, blank=True, null=True, unique=True)

    @property
    def is_exist(self):
        return self.stock > 0

    @property
    def is_offed(self):
        return self.discount > 0
    
    @property
    def offed_price(self):
        return self.price - ((self.price * self.discount) / 100)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        if self.slug is None:
            self.slug = "product-" + str(uuid.uuid4())[:5] + str(timezone.now().microsecond)
        
        super().save(*args, **kwargs)

    def get_absolute_api_url(self):
        return reverse("shop:api-v1:product-detail", kwargs={"slug": self.slug})
    
    

class ImageProduct(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='galary')

    img = models.ImageField(upload_to='product/imgs')

class CharacteristicProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Specifications')
    
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Comment(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    rating = models.IntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)\
    
    def __str__(self):
        return f"{self.user.phone} - > {self.product.title}"
    

class SpecialSuggestion(models.Model):
    
    start_at = models.DateTimeField(default=timezone.now);
    end_at = models.DateTimeField()

    is_active = models.BooleanField(default=False);

    products = models.ManyToManyField(Product, through="SpecialSuggestionProduct", related_name="suggestion_products")

    @property
    def remaining(self):

        now = timezone.now()

        return self.end_at - now if self.end_at > now else 0


class SpecialSuggestionProduct(models.Model):
    suggestion = models.ForeignKey(
        SpecialSuggestion,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

