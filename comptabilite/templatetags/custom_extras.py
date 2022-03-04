from django import template

register = template.Library()

@register.filter(name="getvalue")
def getvalue(value, key):
    return value[key]

@register.filter(name="previous")
def previous(value):
    return int(value) - 1