from django import template
import json
register = template.Library()


@register.filter
def dict_merge(a, b):
    return a | b


@register.filter
def json_dumps(text):
    return json.dumps(text)
