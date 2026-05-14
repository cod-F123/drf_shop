from django.contrib import admin
from .models import Category, Product, ImageProduct, CharacteristicProduct, Comment

# Register your models here.

class ImageProductInlineAdmin(admin.StackedInline):
    model = ImageProduct
    extra = 1

class  CharacteristicProductInlineAdmin(admin.StackedInline):
    verbose_name_plural = 'Specifications'
    
    model = CharacteristicProduct
    extra = 1

class CommentAdminInline(admin.StackedInline):
    model = Comment
    extra = 1
    readonly_fields = ['created_at']
    verbose_name_plural = 'comments'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category__name', 'price', 'discount','is_offed', 'is_exist', 'added_at']
    search_fields = ['title', 'category']

    readonly_fields = ['added_at']

    list_editable = ['price', 'discount']

    list_filter = ['category__name']
    inlines = [ImageProductInlineAdmin, CharacteristicProductInlineAdmin, CommentAdminInline]