# Roughly a copy of django.contrib.session.middleware; 
#  Trimmed where cookie-based stuff didn't make sense.
import time

from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from django_lean.conf import settings

class SessionMiddleware(object):
    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.GET.get(settings.LEAN_QUERYSTRING_NAME, None)
        request.lean_url_session = engine.SessionStore(session_key)

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.lean_url_session.accessed
            modified = request.lean_url_session.modified
        except AttributeError:
            pass
        else:
            if modified:
                request.lean_url_session.save()
        return response
