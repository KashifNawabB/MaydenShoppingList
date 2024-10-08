from django import template

register = template.Library()

# custom tags for math operations inside templates
@register.filter
def multiply(value1, value2):
    return value1 * value2

@register.filter
def subtract(value1, value2):
    return value1 - value2
