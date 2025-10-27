from django import template

register = template.Library()

# @register.simple_tag(takes_context=True)
# def is_active_nav(context, url_name):
#     """
#     Compares the current resolved URL name with the provided url_name.
#     Returns the string 'active' if they match, otherwise returns an empty string.
    
#     Usage: {% is_active_nav 'seller_dashboard' %}
#     """
#     try:
#         current_url_name = context['request'].resolver_match.url_name
#         if current_url_name == url_name:
#             return 'active'
#     except Exception:
#         pass
        
#     return ''


@register.simple_tag(takes_context=True)
def is_active_nav(context, *url_names):
    """
    Returns 'active' if the current resolved URL name matches any of the given names.
    
    Usage:
        {% is_active_nav 'seller_dashboard' 'products_list' 'create_product' %}
    """
    try:
        current_url_name = context['request'].resolver_match.url_name
        if current_url_name in url_names:
            return 'active'
    except Exception:
        pass

    return ''