# -*- coding: utf-8 -*-
'''
Created on 06/07/18
'''

from __future__ import absolute_import, print_function, unicode_literals
import logging

from django.utils.translation import ugettext_lazy as _
from .sanitizer import AllowTokenParser


class DataAttributeParser(AllowTokenParser):

    def parse(self, attribute, val):
        return attribute.startswith('data-')