from django import forms
from django.utils import timezone, translation
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import redirect, get_object_or_404, Http404

from wkhtmltopdf.views import PDFTemplateView


_ = translation.ugettext_lazy


class AdminContextMixin:

    page_title = ''
    context = None
    extra_context = {}

    def get_page_title(self):
        return self.page_title

    def get_extra_context(self):
        return self.extra_context

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            **self.admin_site.each_context(self.request),
            'title': self.get_page_title(),
            **self.get_extra_context()
        })
        return kwargs


class AdminMultipleObjectMixin(AdminContextMixin, MultipleObjectMixin):
    pass


class AdminSingleObjectMixin(AdminContextMixin, SingleObjectMixin):

    pk_url_kwarg = 'object_id'
    context_object_name = 'instance'


class FormMixin(AdminContextMixin):
    """Provide a way to show and handle a form in a request."""
    initial = {}
    form_class = None
    success_url = None
    prefix = None

    @property
    def media(self):
        js = [
            'vendor/jquery/jquery.js',
            'jquery.init.js',
            'core.js',
            'admin/RelatedObjectLookups.js',
            'actions.min.js',
            'urlify.js',
            'prepopulate.js',
            'vendor/xregexp/xregexp.js',
        ]
        return forms.Media(js=['admin/js/%s' % url for url in js])

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix

    def get_form_class(self):
        """Return the form class to use."""
        return self.form_class

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured(
                    "No URL to redirect to. Provide a success_url."
                    )
        return str(self.success_url)  # success_url may be lazy

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_extra_context(self):
        return {'media': self.media}

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)


class AdminViewMixin:

    admin_site = None
    cacheable = True
    url_path = NotImplemented
    url_name = NotImplemented

    def __init__(self, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        super().__init__(*args, **kwargs)

    def has_permission(self, request):
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request):
            raise PermissionError(
                "You don’t have permission to view or edit this page"
                )
        return super().dispatch(request, *args, **kwargs)


class AdminView(AdminViewMixin, TemplateResponseMixin, View):

    template_name = 'admin/base_site.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ModelFormMixin(FormMixin, AdminSingleObjectMixin):
    """Provide a way to show and handle a ModelForm in a request."""
    fields = None

    def get_form_class(self):
        """Return the form class to use in this view."""
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif getattr(self, 'object', None) is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model

            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." %
                    self.__class__.__name__
                )

            return modelform_factory(model, fields=self.fields)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class ProcessFormView(AdminView):

    """Render a form on GET and processes it on POST."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseDetailView(AdminSingleObjectMixin, AdminView):
    """A base view for displaying a single object."""
    pass


class BaseListView(MultipleObjectMixin, AdminView):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            has_object_list = hasattr(self.object_list, 'exists')
            has_paginate_by = self.get_paginate_by(
                    self.object_list
                ) is not None
            if has_paginate_by and has_object_list:
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                msg = _('Empty list and “%(cls_name)s.allow_empty” is False.')
                raise Http404(msg % {
                    'cls_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)


class AdminListView(BaseListView):
    pass


class AdminDetailView(BaseDetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AdminCreateView(ModelFormMixin, ProcessFormView):

    cacheable = False

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class AdminUpdateView(ModelFormMixin, ProcessFormView):

    cacheable = False

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class AdminDeleteView(AdminSingleObjectMixin, AdminView):

    cacheable = False

    def get_success_url(self):
        raise NotImplementedError('Delete view need success url')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object.delete()
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.delete(request, *args, **kwargs)


class PDFViewMixin:
    title = None
    filename = None
    show_content_in_browser = True

    template_name = 'admin/print/content.html'
    cover_template = 'admin/print/cover.html'
    header_template = 'admin/print/header.html'
    footer_template = 'admin/print/footer_with_page_number.html'

    cmd_options = {
        'orientation': 'portrait',
        'margin-top': 40,
        'margin-left': 25,
        'margin-right': 25,
        'margin-bottom': 25,
    }

    def get_settings(self, request):
        return None

    def apply_settings(self, request):
        pass

    def get_title(self):
        return self.title

    def get_extra_context(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            **self.get_extra_context(),
            'title': self.get_title()
        })
        return context

    def get_filename(self):
        return self.__class__.__name__ if not self.filename else self.filename

    def get_cmd_options(self):
        return self.cmd_options


class ModelPDFTemplateView(PDFViewMixin, PDFTemplateView):
    model = None

    @property
    def opts(self):
        return self.model._meta

    def get_title(self):
        return self.title or self.opts.verbose_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'opts': self.opts,
        })
        return context

    def get_filename(self):
        if not self.filename:
            filename = '%s_%s_%s' % (
                self.opts.app_label,
                self.opts.model_name,
                timezone.now().strftime('%d%m%Y')
            )
            return filename
        return self.filename + '_' + timezone.now().strftime('%d%m%Y')

    def get(self, request, *args, **kwargs):
        """ Render PDF Response """
        self.apply_settings(request)
        return super().get(request, *args, **kwargs)


class AdminPDFTemplateView(AdminViewMixin, ModelPDFTemplateView):
    pass


class ModelAdminPDFViewBase(PDFTemplateView):
    title = None
    modeladmin = None
    filename = None
    show_content_in_browser = True
    template_name = 'admin/print/content.html'
    cover_template = 'admin/print/cover.html'
    header_template = 'admin/print/header.html'
    footer_template = 'admin/print/footer.html'

    cmd_options = {
        'margin-top': 40,
        'margin-left': 25,
        'margin-right': 25,
        'margin-bottom': 25,
    }

    def __init__(self, modeladmin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modeladmin = modeladmin
        self.model = modeladmin.model
        self.opts = self.model._meta

    def get(self, request, *args, **kwargs):
        self.apply_settings(request)
        return super().get(request, *args, **kwargs)

    def apply_settings(self, request):
        pass

    def get_title(self):
        return self.title or self.opts.verbose_name

    def get_context_data(self, **kwargs):
        context = {
            'title': self.get_title(),
            'opts': self.opts,
        }
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_filename(self):
        if not self.filename:
            filename = '%s_%s_%s' % (
                self.opts.app_label,
                self.opts.model_name,
                timezone.now().strftime('%d%m%Y')
            )
            return filename
        return self.filename + '_' + timezone.now().strftime('%d%m%Y')

    def get_cmd_options(self):
        return self.cmd_options


class PDFPrintDetailView(ModelAdminPDFViewBase):
    instance = None
    instance_pk = None

    def __init__(self, modeladmin, instance_pk, *args, **kwargs):
        super().__init__(modeladmin, *args, **kwargs)
        self.instance_pk = instance_pk
        self.instance = get_object_or_404(self.model, pk=instance_pk)

    def get_title(self):
        return self.modeladmin.document_title or super().get_title()

    def apply_settings(self, request):
        if not self.modeladmin.document_show_cover:
            self.cover_template = None
        if not self.modeladmin.document_show_header:
            self.headertemplate = None
        if not self.modeladmin.document_show_footer:
            self.footer_template = None

    def get_context_data(self, **kwargs):
        context = {'instance': self.instance}
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        app_label = self.opts.app_label.lower()
        model_name = self.opts.model_name.lower()
        return self.modeladmin.print_template or [
                'admin/print/%s/%s/content.html' % (app_label, model_name),
                'admin/print/%s/content.html' % (model_name),
                'admin/print/%s/content.html' % (app_label),
                'admin/print/content.html',
            ]
