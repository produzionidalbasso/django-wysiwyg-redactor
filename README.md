# django-wysiwyg-redactor

(Version modified of django-redactorjs)

I modified things like:

* dyrectory static has been deleted
* method RedactorEditor.media has been fixed to import also css files of redactor plugins
* fix on url and view to upload images and files
* Created RedactorTextPlugin for integration with django-cms


What's that
-----------

*django-wysiwyg-redactor is a reusable application for Django, using WYSIWYG editor http://redactorjs.com/*

Dependence
-----------

- `Django >= 1.11`
- `PIL`

Getting started
---------------
* Install django-wysiwyg-redactor:

``pip install -e git+https://github.com/frankhood/django-wysiwyg-redactor.git#egg=django-wysiwyg-redactor``

* Add `'redactor'` to INSTALLED_APPS.

* Add `path('redactor/', include('redactor.urls')),` to urls.py

* Add default config in settings.py (more settings see: <https://github.com/douglasmiranda/django-wysiwyg-redactor/wiki/Settings>):


```python
REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'
```

* buy license here: http://redactorjs.com/download/ and copy redactor library under `/static/redactor/` directory of your project


Using in model
--------------

```python
from django.db import models
from redactor.fields import RedactorField

class Entry(models.Model):
    title = models.CharField(max_length=250, verbose_name=u'Title')
    short_text = RedactorField(verbose_name=u'Text')
```
or use custom parametrs:
```python
    short_text = RedactorField(
        verbose_name=u'Text',
        redactor_options={'lang': 'en', 'focus': 'true'},
        upload_to='tmp/'
    )
```
Using for only admin interface
-----------------------------
```python
from django import forms
from redactor.widgets import RedactorEditor
from blog.models import Entry

class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = Entry
        widgets = {
           'short_text': RedactorEditor(),
        }

class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm
```

`RedactorEditor` takes the same parameters as `RedactorField`


Using for django-cms
-----------------------------
```python
from redactor.cms_plugins import RedactorTextPlugin

class ArticlePlugin(RedactorTextPlugin):
    name = _('Article')
    render_template = "cms_plugins/article.html"

```


# Redactor-js version 
Tested with version 3.0.11 redactor-js

