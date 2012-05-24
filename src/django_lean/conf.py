from .datastructures import ConfigurationView, DictAttribute
from django.conf import settings as dj_settings

defaults = {
    'LEAN_QUERYSTRING_NAME': 'dlid',
    'LEAN_AUTOCREATE_GOAL_TYPES': False,
    'LEAN_ENGAGEMENT_CALCULATOR': None,
    'LEAN_ANALYTICS': [],
    'LEAN_ANALYTICS_FOR_EXPERIMENTS': False,
    'LEAN_SEGMENTS': [],
}



settings = ConfigurationView(DictAttribute(dj_settings), [defaults])
