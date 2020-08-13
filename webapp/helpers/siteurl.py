from django.urls import reverse
from django.utils.functional import cached_property


class BaseURLHelper:

    def __init__(self, modelsite):
        self.modelsite = modelsite
        self.model = modelsite.model
        self.opts = modelsite.opts

    @cached_property
    def create_url_name(self):
        return self.get_url_name('create')

    @cached_property
    def inspect_url_name(self):
        return self.get_url_name('inspect')

    @cached_property
    def edit_url_name(self):
        return self.get_url_name('edit')

    @cached_property
    def delete_url_name(self):
        return self.get_url_name('delete')

    def get_url_pattern(self, action, specific=False):
        raise NotImplementedError

    def get_url_name(self, action):
        raise NotImplementedError

    def get_url(self, action, specific, *args, **kwargs):
        raise NotImplementedError


class SiteURLHelper(BaseURLHelper):

    def get_url_pattern(self, action, specific=False):
        if action == 'index':
            return '%s/' % self.opts.model_name
        if specific:
            return '%s/%s/<str:instance_pk>/' % (self.opts.model_name, action)
        return '%s/%s/' % (self.opts.model_name, action)

    def get_url_name(self, action):
        return '%s_%s_%s' % (
            self.opts.app_label,
            self.opts.model_name,
            action
        )

    def get_url(self, action, specific, *args, **kwargs):
        url_name = self.get_url_name(action)
        return reverse(url_name, args=args, kwargs=kwargs)


class InlineSiteURLHelper(BaseURLHelper):

    def get_url_pattern(self, action, specific=False):
        if action == 'index':
            return '%s/' % self.opts.model_name
        if specific:
            return '%s_%s/<str:instance_pk>/' % (self.opts.model_name, action)
        return '%s_%s/' % (self.opts.model_name, action)

    def get_url_name(self, action):
        return '%s_%s_%s_inline' % (
            self.opts.app_label,
            self.opts.model_name,
            action
        )

    def get_url(self, action, specific, *args, **kwargs):
        url_name = self.get_url_name(action)
        return reverse(url_name, args=args, kwargs=kwargs)
