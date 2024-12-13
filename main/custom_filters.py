from django import template

register = template.Library()

@register.filter
def dict_item(dictionary, key):
    """Retrieve an item from a dictionary using a key."""
    return dictionary.get(key)