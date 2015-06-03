from django import template
from django.template.defaultfilters import stringfilter
from tecnoservicio.ordenes.models import *

register = template.Library()

@register.filter
@stringfilter
def y(a,b):
		return "#"


		