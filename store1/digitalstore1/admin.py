from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from .forms import CategoryForm


from .models import *
# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(ImageProduct)
admin.site.register(ModalProduct)
admin.site.register(FavoriteProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Profiles)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'parent', 'get_icon_admin']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {'slug': ('title',)}
    form = CategoryForm

    def get_icon_admin(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30">')
            except:
                return '-'
        else:
            return '-'

    get_icon_admin.short_description = 'Иконка'


class ImageProductInline(admin.TabularInline):
    fk_name = 'product'
    model = ImageProduct
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'category', 'quantity', 'color', 'discount', 'created_at', 'get_img_admin')
    list_display_links = ['pk', 'title']
    inlines = [ImageProductInline]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['price', 'quantity', 'discount', 'category']

    def get_img_admin(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="50">')
            except:
                return '-'
        else:
            return '-'