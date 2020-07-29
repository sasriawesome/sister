from django.utils import timezone
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from constance import config
from wkhtmltopdf.views import PDFTemplateView


class AdminBaseView(TemplateView):

    admin_site = None
    cacheable = True
    url_path = NotImplemented
    url_name = NotImplemented
    template_name = 'admin/base_site.html'
    page_title = ''

    def has_permission(self, request):
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request):
            raise PermissionError("You don’t have permission to view or edit this page")
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        super().__init__(*args, **kwargs)

    def get_extra_context(self):
        return {}

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            **self.admin_site.each_context(self.request),
            'title': self.get_page_title(),
            **self.get_extra_context()
        })
        return kwargs


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

    def get_settings(self, request):
        return PrintPDFSetting.for_site(request.site)

    def apply_settings(self, request):
        pass # use default settings

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
        options = {
            'margin-top': config.PDF_MARGIN_TOP,
            'margin-left': config.PDF_MARGIN_LEFT,
            'margin-right': config.PDF_MARGIN_RIGHT,
            'margin-bottom': config.PDF_MARGIN_BOTTOM,
            'orientation': config.PDF_ORIENTATION
        }
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