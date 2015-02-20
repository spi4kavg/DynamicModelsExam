from ..settings import CONFIG_FILE
import yaml
from django import template

register = template.Library()


@register.inclusion_tag("test_app/templatetags/dynamic_nav.html")
def dynamic_nav():
    stream = open(CONFIG_FILE, 'r')
    obj = yaml.load(stream)
    return {
        "obj": obj
    }