from django import template

register = template.Library()

@register.filter(name="getvalue")
def getvalue(value, key):
    return value[key]