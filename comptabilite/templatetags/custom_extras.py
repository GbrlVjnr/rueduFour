from django import template

register = template.Library()

@register.filter(name="blackandwhite")
def blackandwhite(value):
    return value.get(type="B&W").amount

@register.filter(name="color")
def color(value):
    return value.get(type="C").amount

@register.filter(name="getVAT")
def getVAT(value):
    return value-(value/(1+0.2))

@register.filter(name="getvalue")
def getvalue(value, key):
    return value[key]

@register.filter(name="previous")
def previous(value):
    return int(value) - 1