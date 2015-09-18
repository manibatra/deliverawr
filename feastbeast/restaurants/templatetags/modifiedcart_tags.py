from django import template

from restaurants.mycart import ModifiedCart


register = template.Library()


def get_modifiedcart(context, session_key=None, cart_class=ModifiedCart):
    """
    Make the cart object available in template.
    Sample usage::
        {% load carton_tags %}
        {% get_cart as cart %}
        {% for product in cart.products %}
            {{ product }}
        {% endfor %}
    """
    request = context['request']
    return cart_class(request.session, session_key=session_key)

register.assignment_tag(takes_context=True, name='get_modifiedcart')(get_modifiedcart)