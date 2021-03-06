from functools import wraps

import requests

from django.conf import settings

# check recaptcha for forms
def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            res = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = res.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
        return view_func(request, *args, **kwargs)
    return _wrapped_view
