from django import template

register = template.Library()


@register.filter
def percentage_color(value):
    try:
        val = int(value)
    except (ValueError, TypeError):
        return 'danger'
    if val >= 80:
        return 'success'
    elif val >= 50:
        return 'warning'
    elif val >= 25:
        return 'info'
    return 'danger'


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0