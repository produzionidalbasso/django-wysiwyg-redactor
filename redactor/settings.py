# -*- coding: utf-8 -*-
try:
    from urllib.parse import urljoin
except ImportError:
    # Python 2
    from urlparse import urljoin

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


ALLOW_TOKEN_PARSERS = (
    'redactor.attribute_parsers.DataAttributeParser',
)
