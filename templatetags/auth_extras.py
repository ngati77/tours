from django import template
from django.contrib.auth.models import Group 

from django.template.defaultfilters import register

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()



@register.filter
def DayEn2Heb(text): # Only one argument.
    """Translate Day name from English to Hebrew"""
    # Dictionary to convert English to Hebrew 
    hebdict = {'Sunday':'ראשון', 'Monday':'שני', 'Tuesday':'שלישי', 'Wednesday':'רביעי', 'Thursday':'חמישי', 'Friday':'שישי', 'Saturday':'שבת'}

    return hebdict[text]