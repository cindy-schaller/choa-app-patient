from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='days_ago')
def days_ago(value):
    return str((datetime.now().date() - value.date()).days) + " days ago"

@register.filter(name='tab_title')
def tab_title(value):
    return value.replace("Questionnaire", " ")