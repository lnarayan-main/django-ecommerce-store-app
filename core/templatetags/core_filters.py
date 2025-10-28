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