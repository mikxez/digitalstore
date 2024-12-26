from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CartForAuthenticatedUser
from django.utils.translation import activate
from django.http import HttpResponse
from store1 import settings
from store1.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
import stripe
from .forms import *


# Create your views here.


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'digitalstore1/index.html'
    extra_context = {
        'title': 'Digitalstore'
    }
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


class MoreProductView(ListView):
    model = Product
    template_name = 'digitalstore1/more_product.html'
    extra_context = {
        'title': 'Больше товаров'
    }
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'digitalstore1/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=product.category)
        products = [i for i in products if i != product]
        context['products'] = products
        context['title'] = product.title
        return context


def product_by_color(request, color_code, category, modal):
    product = Product.objects.get(color_code=color_code,
                                  category__title=category,
                                  modal__title=modal)
    products = Product.objects.filter(category=product.category)
    products = [i for i in products if i != product]
    context = {
        'title': product.title,
        'products': products,
        'product': product
    }
    return render(request, 'digitalstore1/product_detail.html', context)


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digitalstore1/category_page.html'
    paginate_by = 1

    def get_queryset(self):
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        memory = self.request.GET.get('memory')
        price_from = self.request.GET.get('from')
        price_till = self.request.GET.get('till')
        category = Category.objects.get(slug=self.kwargs['slug'])
        brands = category.brand.all()
        products = Product.objects.filter(category__in=brands)
        if brand:
            products = products.filter(category__title=brand)
        if color:
            products = products.filter(color=color)
        if memory:
            products = products.filter(memory=memory)
        if price_from:
            products = [i for i in products if int(i.price) >= int(price_from)]
        if price_till:
            products = [i for i in products if int(i.price) <= int(price_till)]
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = category.title
        context['category'] = category
        brands = category.brand.all()
        products = Product.objects.filter(category__in=brands)
        context['colors'] = list(set([i.color for i in products]))
        context['memories'] = list(set([i.memory for i in products]))
        context['brands'] = list(set(brands))
        context['prices'] = [i for i in range(500000, 100000000, 500000)]
        context['brand'] = self.request.GET.get('brand')
        context['color'] = self.request.GET.get('color')
        context['memory'] = self.request.GET.get('memory')
        context['price_from'] = self.request.GET.get('from')
        context['price_till'] = self.request.GET.get('till')

        return context


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            form = LoginForm()

    context = {
        'title': 'Авторизация',
        'login_form': form
    }

    return render(request, 'digitalstore1/login.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('main')
    else:
        return redirect('main')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
            else:
                return redirect('register')
        else:
            form = RegisterForm()

        context = {
            'title': 'Регистарция',
            'register_form': form
        }

        return render(request, 'digitalstore1/register.html', context)


def add_to_favorite_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user
        product = Product.objects.get(slug=slug)
        favorite_products = FavoriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorite_products]:
                fav_product = FavoriteProduct.objects.get(product=product, user=user)
                fav_product.delete()
            else:
                FavoriteProduct.objects.create(product=product, user=user)

        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


class FavoriteListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'digitalstore1/favorite.html'
    login_url = 'login'
    extra_context = {
        'title': 'Моё избранное'
    }

    def get_queryset(self):
        favorite = FavoriteProduct.objects.filter(user=self.request.user)
        favorite = [i.product for i in favorite]
        return favorite


class DiscountProduct(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digitalstore1/favorite.html'
    extra_context = {
        'title': 'Товары по акции'
    }

    def get_queryset(self):
        products = Product.objects.all()
        products = [i for i in products if i.discount > 0]
        return products


def add_product_to_cart(request, slug, action):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = CartForAuthenticatedUser(request, slug, action)
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


def my_cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart = CartForAuthenticatedUser(request)
        order_info = cart.get_cart_info()
        order_products = order_info['order_products']
        products = Product.objects.all()[::-1][:8]

        context = {
            'title': 'Моя корзина',
            'order': order_info['order'],
            'order_products': order_products,
            'products': products
        }

        return render(request, 'digitalstore1/my_cart.html', context)


def delete_products_from_cart(request, order):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order_product = OrderProduct.objects.filter(order=order)
        order_product.delete()
        return redirect('my_cart')


def change_language(request, lang_code):
    if lang_code in dict(settings.LANGUAGES).keys():
        activate(lang_code)
        request.session['django_language'] = lang_code

    return redirect(request.META.get('HTTP_REFERER', '/'))


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart = CartForAuthenticatedUser(request)
        if cart.get_cart_info()['order_products']:
            regions = Region.objects.all()
            dict_city = {i.pk: [[j.title, j.pk] for j in i.cities.all()] for i in regions}

            context = {
                'title': 'Оформление заказа',
                'order': cart.get_cart_info()['order'],
                'order_products': cart.get_cart_info()['order_products'],
                'customer_form': CustomerForm(instance=request.user.customer),
                'shipping_form': ShippingForm(),
                'dict_city': dict_city
            }
            return render(request, 'digitalstore1/checkout.html', context)
        else:
            next_page = request.META.get('HTTP_REFERER', 'main')
            return redirect(next_page)


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        if request.method == 'POST':
            cart = CartForAuthenticatedUser(request)
            order_info = cart.get_cart_info()

            customer_form = CustomerForm(data=request.POST)
            shipping_form = ShippingForm(data=request.POST)
            ship_address = ShippingAddress.objects.all()
            if customer_form.is_valid() and shipping_form.is_valid():
                customer = Customer.objects.get(user=request.user)
                customer.first_name = customer_form.cleaned_data['first_name']
                customer.last_name = customer_form.cleaned_data['last_name']
                customer.telegram = customer_form.cleaned_data['telegram']
                customer.save()
                address = shipping_form.save(commit=False)
                address.customer = customer
                address.order = order_info['order']
                if order_info['order'] not in [i.order for i in ship_address]:
                    address.save()
            else:
                return redirect('checkout')

            total_price = order_info['order_total_price']
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'rub',
                        'product_data': {'name': 'Товары магазна LOFT'},
                        'unit_amount': int(total_price) * 100
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('checkout'))
            )

            return redirect(session.url, 303)


def success_payment(request):
    if not request.user.is_authenticated:
        return redirect('main')
    else:
        cart = CartForAuthenticatedUser(request)
        cart.create_payment()

        context = {
            'title': 'Успешная оплата'
        }

        return render(request, 'digitalstore1/success.html', context)


class SearchResult(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digitalstore1/favorite.html'

    def get_queryset(self):
        word = self.request.GET.get('q', '').strip()
        products = Product.objects.filter(title__iregex=word)
        return products


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user
        if not Profiles.objects.filter(user=user).exists():
            Profiles.objects.create(user=user)
        if user:
            profile = Profiles.objects.get(user=user)
            context = {
                'title': f'Профиль {user.username}',
                'profile': profile,
            }
            return render(request, 'digitalstore1/profile.html', context)


def edit_account_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            profile = Profiles.objects.get(user=request.user)
        except Profiles.DoesNotExist:
            return redirect('login')

        user = request.user
        account_form = EditAccountForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

        context = {
            'title': f'Изменения данных {request.user.username}',
            'account_form': account_form,
            'profile_form': profile_form
        }
        return render(request, 'digitalstore1/edit.html', context)


def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            edit_profile = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if edit_profile.is_valid():
                edit_profile.save()
                return redirect('profile')
            else:
                return redirect('change')


def edit_account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            edit_account_form = EditAccountForm(request.POST, instance=request.user)
            if edit_account_form.is_valid():
                edit_account_form.save()
                return redirect('profile')
            else:
                return redirect('change')


def order_list(request):
    if not request.user.is_authenticated:
        return redirect('main')

    try:
        customer = Customer.objects.get(user=request.user)
        goods = Order.objects.filter(customer=customer, payment=True)
    except ObjectDoesNotExist:
        goods = None

    if goods.exists():
        context = {
            'items': goods,
            'title': 'Мои заказы'
        }
        return render(request, 'digitalstore1/my_orders.html', context)

    return render(request, 'digitalstore1/my_orders.html', {
        'items': goods,
        'title': 'Мои заказы'
    })
