from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def currency(value):
    try:
        return f"{float(value):,.2f} TL"
    except (ValueError, TypeError):
        return "0,00 TL"
