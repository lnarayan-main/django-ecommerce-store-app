from django import template

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