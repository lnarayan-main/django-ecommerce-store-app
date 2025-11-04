from django import template
from cart.models import WishlistItem

register = template.Library()

@register.filter
def subtract(price, discount):
    """
    Returns the discounted price if discount is provided,
    otherwise returns the original price.
    """
    try:
        # Convert to float for safety in case of Decimal or None
        price = float(price)
        discount = float(discount) if discount not in [None, ""] else 0

        if discount > 0:
            return price - discount
        return price
    except (TypeError, ValueError):
        # Return original price if any issue occurs
        return price or 0
    
def currency(value):
    """Adds a currency symbol and formats the number to two decimal places and adds comma separators."""
    try:
        return f"${value:,.2f}" 
    except (ValueError, TypeError):
        return value


@register.filter
def mul(value, arg):
    try:
        return value * arg
    except:
        return ''


@register.filter
def split_description(value, word_count=5):
    """
    Splits text after a certain number of words and adds a <br> tag.
    Example:
        {{ category.description|split_description:5 }}
    """
    if not value:
        return ''
    words = value.split()
    if len(words) <= word_count:
        return value
    first_line = ' '.join(words[:word_count])
    second_line = ' '.join(words[word_count:])
    return f"{first_line}<br>{second_line}"


@register.filter
def break_after_words(value, count):
    """Inserts a <br> after the specified number of words."""
    words = str(value).split()
    if len(words) > count:
        first_line = " ".join(words[:count])
        second_line = " ".join(words[count:])
        return f"{first_line}<br>{second_line}"
    return value

@register.filter
def is_product_wishlisted(product, user):
    """
    Custom filter to check if a product is in the user's wishlist.
    
    WARNING: This causes an N+1 query problem if used inside a loop
    of products, as it hits the database for every single product.
    
    Usage in template: {% if product|is_product_wishlisted:request.user %}
    """
    # 1. Handle Anonymous/Unauthenticated Users
    if not user or not user.is_authenticated:
        return False
        
    # 2. Execute the Database Query (Inefficiently inside a loop)
    return WishlistItem.objects.filter(
        user=user, 
        product=product
    ).exists()