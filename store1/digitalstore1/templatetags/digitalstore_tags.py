from digitalstore1.models import Category, Product, FavoriteProduct
from django import template

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)

@register.filter
def reverse(value):
    try:
        return value[::-1]
    except TypeError:
        return value

@register.simple_tag()
def get_colors_product(modal, category):
    products = Product.objects.filter(modal=modal, category=category)
    colors = [i.color_code for i in products]
    return colors

@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()
@register.simple_tag()
def get_favorites(user):
    favorites = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in favorites]
    return products

@register.simple_tag()
def get_discount_price(price, discount):
    if discount > 0:
        procent = (price * discount) / 100
        price = price - procent
    return price
@register.simple_tag()
def installment(price):
    if price:
        a = price / 12
    return f'{a:.2f}'

@register.simple_tag()
def get_price(price):
    return f'{price:_}'.replace('_', ' ')

