from django.contrib.staticfiles.storage import CachedFilesMixin
from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class UrlCorrectedS3BotoStorage(S3BotoStorage):
    """
    Overrides the url() method to readd a trailing slash if it was removed by
    the base class.
    """

    def url(self, name):
        url = super(UrlCorrectedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url


class S3PipelineStorage(PipelineMixin, CachedFilesMixin, UrlCorrectedS3BotoStorage):
    pass
