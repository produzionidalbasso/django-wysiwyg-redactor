
from django.urls import path, re_path

from redactor.views import RedactorUploadView

urlpatterns = [
    re_path(r'^upload/image/(?P<upload_to>)',
        RedactorUploadView.as_view(),
        name='redactor_upload_image'),

    re_path(r'^upload/file/(?P<upload_to>)',
        RedactorUploadView.as_view(),
        name='redactor_upload_file'),
]
