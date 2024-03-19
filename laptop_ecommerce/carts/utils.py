from django.utils import timezone
from offer_management.models import CategoryOffer, ProductOffer

def get_category_offer(category):
    today = timezone.now().date()
    try:
        category_offer = CategoryOffer.objects.get(
            category=category,
            expire_date__gte=today,
            is_active=True
        )
        return category_offer.discount_rate
    except CategoryOffer.DoesNotExist:
        return 0

def get_product_offer(product):
    today = timezone.now().date()
    try:
        product_offer = ProductOffer.objects.get(
            products=product,
            expire_date__gte=today,
            is_active=True
        )
        return product_offer.discount_rate
    except ProductOffer.DoesNotExist:
        return 0

def apply_offers(cart_items, grand_total):
    max_offer = 0
    has_offer = False

    for cart_item in cart_items:
        product = cart_item.product
        category = product.category
        variations = cart_item.variations.all()
        category_offer = get_category_offer(category)
        product_offer = get_product_offer(product)

        for variation in variations:
            variation_category_offer = get_category_offer(variation.product.category)
            variation_product_offer = get_product_offer(variation.product)

            if variation_category_offer or variation_product_offer:
                offer = max(variation_category_offer, variation_product_offer)
                max_offer = max(max_offer, offer)
                has_offer = True

    if has_offer:
        grand_total -= max_offer
        applied_offer = max_offer
    else:
        applied_offer = None
        if category_offer:
            grand_total -= category_offer
            has_offer = True
        elif product_offer:
            grand_total -= product_offer
            has_offer = True

    if not has_offer:
        pass

    return grand_total, applied_offer