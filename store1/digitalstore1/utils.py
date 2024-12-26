from .models import *


class CartForAuthenticatedUser:
    def __init__(self, request, product_slug=None, action=None):
        self.user = request.user

        if product_slug and action:
            self.add_or_delete(product_slug, action)

    def get_cart_info(self):
        customer, _created = Customer.objects.get_or_create(user=self.user)
        order, _created = Order.objects.get_or_create(customer=customer, payment=False)
        order_products = order.orderproduct_set.all()
        order_total_price = order.get_order_total_price
        order_total_quantity = order.get_order_total_products

        return {
            'order_total_price': order_total_price,
            'order_total_quantity': order_total_quantity,
            'order': order,
            'order_products': order_products
        }

    def add_or_delete(self, product_slug, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(slug=product_slug)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0 and order_product.quantity < product.quantity:
            order_product.quantity += 1
        elif action == 'delete':
            order_product.quantity -= 1

        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def create_payment(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for item in order_products:
            product = Product.objects.get(pk=item.product.pk)
            product.quantity -= item.quantity
            product.save()

        order.payment = True
        order.save()
