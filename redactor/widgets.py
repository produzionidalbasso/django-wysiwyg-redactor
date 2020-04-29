import logging
from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.conf import settings
try:
    from django.urls import reverse_lazy
except ImportError:  # Django < 1.10 pragma: no cover
    from django.core.urlresolvers import reverse_lazy


from redactor.utils import json_dumps

logger = logging.getLogger(__name__)


class RedactorEditor(widgets.Textarea):
    def __init__(self, *args, **kwargs):
        upload_to = kwargs.pop('upload_to', 'redactor')
        self.options = dict(getattr(settings, 'REDACTOR_OPTIONS', {}))
        self.options.update(kwargs.pop('redactor_options', {}))

        if kwargs.pop('allow_file_upload', True):
            self.options['fileUpload'] = reverse_lazy(
                'redactor_upload_file', kwargs={'upload_to': upload_to}
            )
        if kwargs.pop('allow_image_upload', True):
            self.options['imageUpload'] = reverse_lazy(
                'redactor_upload_image', kwargs={'upload_to': upload_to}
            )

        widget_attrs = {'class': 'redactor-box'}
        widget_attrs.update(kwargs.get('attrs', {}))
        widget_attrs.update({'data-redactor-options': self.options})

        kwargs['attrs'] = widget_attrs
        super(RedactorEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        """
        Must parse self.options with json_dumps on self.render.
        Because at some point Django calls RedactorEditor.__init__ before
        loading the urls, and it will break.
        """
        attrs['data-redactor-options'] = json_dumps(self.options)
        html = super(RedactorEditor, self).render(name, value, attrs, renderer)
        return mark_safe(html)

    def _media(self):
        _min = '' if settings.DEBUG else '.min'
        js = (
            'admin/js/jquery.init.js',
            'django-wysiwyg-redactor/jquery.redactor.init.js',
            'redactor/redactor{}.js'.format(_min),
            'redactor/langs/{}.js'.format(self.options.get('lang', 'en')),
        )

        if 'plugins' in self.options:
            plugins = self.options.get('plugins')
            for plugin in plugins:
                js = js + (
                    'redactor/plugins/{}.js'.format(plugin),
                )

        css = {
            'all': (
                'redactor/redactor{}.css'.format(_min),
                'django-wysiwyg-redactor/django_admin.css',
            )
        }

        if 'plugins' in self.options:
            plugins = self.options.get('plugins')
            for plugin in plugins:
                try:
                    from django.contrib.staticfiles import finders
                    result = finders.find('redactor/plugins/{}.css'.format(plugin))
                    if result is not None:
                        css['all'] = css['all'] + (
                            'redactor/plugins/{}.css'.format(plugin),
                        )
                except:
                    logger.exception("An error has occurred on load plugins css")

        return forms.Media(css=css, js=js)

    media = property(_media)
