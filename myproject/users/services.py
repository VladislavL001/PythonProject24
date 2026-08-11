import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(payment):
    """Создает продукт в Stripe."""

    product = stripe.Product.create(name=payment.course.name)

    return product


def create_price(payment, product):
    """Создает цену для продукта."""

    price = stripe.Price.create(
        unit_amount=int(payment.amount * 100),
        currency="rub",
        product=product.id,
    )

    return price


def create_session(price):
    """Создает ссылку на оплату."""

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ],
    )

    return session
