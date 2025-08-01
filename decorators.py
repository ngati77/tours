from functools import wraps

from django.conf import settings
from django.contrib import messages
from datetime import date
from django.core.exceptions import PermissionDenied



from django.contrib.auth.decorators import login_required, user_passes_test

import requests

def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        request.recaptcha_is_valid = None
        if request.method == 'POST':
        
            #print(request)
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success'] and result['score'] > 0.6:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

''' Check if user has permition to edit blog'''
def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

def group_required_in_date(*group_names):
    """
    Requires user membership in at least one of the groups passed in.
    """
    def in_groups(user):
        today = date.today()
        if user.is_authenticated:
            if user.is_superuser:
                return True

            if bool(user.groups.filter(name__in=group_names)):
                year,month,day = user.first_name.split('-')
                last_date = date(int(year), int(month), int(day))
                if today <= last_date:
                    return True
        raise PermissionDenied("You do not have permission to access this resource.")
    return user_passes_test(in_groups)
