from django.core.exceptions import ImproperlyConfigured
from importlib import import_module

try:
    from django.utils.encoding import force_text
except ImportError:
    try:
        from django.utils.encoding import force_unicode as force_text
    except ImportError:
        from django.utils.encoding import force_str as force_text
from django.utils.functional import Promise

import json
import os
import re
from collections import OrderedDict
from functools import wraps

from django.core.files.storage import get_storage_class
from django.template.defaultfilters import force_escape
from django.template.loader import render_to_string
from django.utils.functional import LazyObject

def import_class(path):
    path_bits = path.split('.')

    if len(path_bits) < 2:
        message = "'{0}' is not a complete Python path.".format(path)
        raise ImproperlyConfigured(message)

    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = import_module(module_path)

    if not hasattr(module_itself, class_name):
        message = "The Python module '{0}' has no '{1}' class.".format(
            module_path,
            class_name
        )
        raise ImportError(message)

    return getattr(module_itself, class_name)


def is_module_image_installed():
    try:
        from PIL import Image
        from PIL import ImageFile
    except ImportError:
        try:
            import Image
            import ImageFile
        except ImportError:
            return False
    return True


class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


def json_dumps(data):
    return json.dumps(data, cls=LazyEncoder)


def random_comment_exempt(view_func):
    # Borrowed from
    # https://github.com/lpomfrey/django-debreach/blob/f778d77ffc417/debreach/decorators.py#L21
    # This is a no-op if django-debreach is not installed
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response._random_comment_exempt = True
        return response
    return wraps(view_func)(wrapped_view)


"""
The following class is taken from https://github.com/jezdez/django/compare/feature/staticfiles-templatetag
and should be removed and replaced by the django-core version in 1.4
"""
default_storage = 'django.contrib.staticfiles.storage.StaticFilesStorage'


class ConfiguredStorage(LazyObject):

    def _setup(self):
        from django.conf import settings
        self._wrapped = get_storage_class(getattr(settings, 'STATICFILES_STORAGE', default_storage))()


configured_storage = ConfiguredStorage()


def static_url(path):
    '''
    Helper that prefixes a URL with STATIC_URL and cms
    '''
    if not path:
        return ''
    return configured_storage.url(os.path.join('', path))
