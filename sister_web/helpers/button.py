from django.utils.translation import ugettext as _


class ButtonHelperBase:
    exclude = ['create']
    default_classnames = ['btn btn-sm']
    add_classnames = ['btn-success']
    inspect_classnames = ['btn-info']
    edit_classnames = ['btn-warning']
    delete_classnames = ['btn-danger']

    add_button_icon = 'plus'
    inspect_button_icon = 'eye'
    edit_button_icon = 'pencil'
    delete_button_icon = 'trash-can'

    def __init__(self, view, request):
        self.view = view
        self.request = request
        self.model = view.model
        self.opts = view.model._meta
        self.permission_helper = view.permission_helper
        self.url_helper = view.url_helper

    def finalise_classname(self, classnames=None):
        combined = self.default_classnames + classnames
        return ' '.join(combined)

    def get_create_url(self, **kwargs):
        return NotImplementedError

    def get_edit_url(self, **kwargs):
        return NotImplementedError

    def get_inspect_url(self, **kwargs):
        return NotImplementedError

    def get_delete_url(self, **kwargs):
        return NotImplementedError

    def get_buttons_for_obj(self, obj, exclude=None, classnames=None):
        return NotImplementedError

    def create_button(self, classnames=None, **kwargs):
        classnames = classnames or []
        all_classnames = self.add_classnames + classnames
        cn = self.finalise_classname(all_classnames)
        return {
            'url': self.get_create_url(**kwargs),
            'label': _('Add %s') % self.opts.verbose_name,
            'classname': cn,
            'icon': self.add_button_icon,
            'title': _('Add a new %s') % self.opts.verbose_name,
        }

    def inspect_button(self, classnames=None, **kwargs):
        classnames = classnames or []
        all_classnames = self.inspect_classnames + classnames
        cn = self.finalise_classname(all_classnames)
        return {
            'url': self.get_inspect_url(**kwargs),
            'label': _('Inspect'),
            'classname': cn,
            'icon': self.inspect_button_icon,
            'title': _('Inspect this %s') % self.opts.verbose_name,
        }

    def edit_button(self, classnames=None, **kwargs):
        classnames = classnames or []
        all_classnames = self.edit_classnames + classnames
        cn = self.finalise_classname(all_classnames)
        return {
            'url': self.get_edit_url(**kwargs),
            'label': _('Edit'),
            'classname': cn,
            'icon': self.edit_button_icon,
            'title': _('Edit this %s') % self.opts.verbose_name,
        }

    def delete_button(self, classnames=None, **kwargs):
        classnames = classnames or []
        all_classnames = self.delete_classnames + classnames
        cn = self.finalise_classname(all_classnames)
        return {
            'url': self.get_delete_url(**kwargs),
            'label': _('Delete'),
            'classname': cn,
            'icon': self.delete_button_icon,
            'title': _('Delete this %s') % self.opts.verbose_name,
        }


class ButtonHelper(ButtonHelperBase):

    def get_create_url(self, **kwargs):
        return self.url_helper.get_url('create', False)

    def get_edit_url(self, **kwargs):
        return self.url_helper.get_url('edit', True, **kwargs)

    def get_inspect_url(self, **kwargs):
        return self.url_helper.get_url('inspect', True, **kwargs)

    def get_delete_url(self, **kwargs):
        return self.url_helper.get_url('delete', True, **kwargs)

    def get_buttons_for_obj(self, obj, exclude=None, classnames=None):
        exclude = exclude or []
        classnames = classnames or []
        ph = self.permission_helper
        usr = self.request.user
        btns = []

        inspect_enabled = self.view.modelsite.inspect_view_enabled
        inspect_excluded = 'inspect' in exclude
        user_can_inspect = ph.user_can_inspect_obj(usr, obj)
        if inspect_enabled and not inspect_excluded and user_can_inspect:
            btns.append(
                self.inspect_button(classnames=classnames, instance_pk=obj.pk)
            )

        edit_enabled = self.view.modelsite.edit_view_enabled
        edit_excluded = 'edit' in exclude
        user_can_edit = ph.user_can_edit_obj(usr, obj)
        if edit_enabled and not edit_excluded and user_can_edit:
            btns.append(
                self.edit_button(classnames=classnames, instance_pk=obj.pk)
            )

        delete_enabled = self.view.modelsite.delete_view_enabled
        delete_excluded = 'delete' in exclude
        user_can_delete = ph.user_can_delete_obj(usr, obj)
        if delete_enabled and not delete_excluded and user_can_delete:
            btns.append(
                self.delete_button(classnames=classnames, instance_pk=obj.pk)
            )
        return btns


class InlineButtonHelper(ButtonHelperBase):

    def get_create_url(self, **kwargs):
        return self.url_helper.get_url('create', False, **kwargs)

    def get_edit_url(self, **kwargs):
        return self.url_helper.get_url('edit', True, **kwargs)

    def get_inspect_url(self, **kwargs):
        return self.url_helper.get_url('inspect', True, **kwargs)

    def get_delete_url(self, **kwargs):
        return self.url_helper.get_url('delete', True, **kwargs)

    def get_buttons_for_obj(self, obj, exclude=None, classnames=None):
        exclude = exclude or []
        classnames = classnames or []
        ph = self.permission_helper
        usr = self.request.user
        parent = self.view.parent
        btns = []

        # create_enabled = self.view.modelsite.create_view_enabled
        # create_excluded = 'create' in exclude
        # user_can_create = ph.user_can_create_obj(usr, obj)
        # if create_enabled and not create_excluded and user_can_create:
        #     btns.append(
        #         self.create_button(
        #             classnames=classnames, parent_pk=parent.id)
        #     )

        inspect_enabled = self.view.modelsite.inspect_view_enabled
        inspect_excluded = 'inspect' in exclude
        user_can_inspect = ph.user_can_inspect_obj(usr, obj)
        if inspect_enabled and not inspect_excluded and user_can_inspect:
            btns.append(
                self.inspect_button(
                    classnames=classnames,
                    parent_pk=parent.pk,
                    instance_pk=obj.pk)
            )

        edit_enabled = self.view.modelsite.edit_view_enabled
        edit_excluded = 'edit' in exclude
        user_can_edit = ph.user_can_edit_obj(usr, obj)
        if edit_enabled and not edit_excluded and user_can_edit:
            btns.append(
                self.edit_button(
                    classnames=classnames,
                    parent_pk=parent.pk,
                    instance_pk=obj.pk)
            )

        delete_enabled = self.view.modelsite.delete_view_enabled
        delete_excluded = 'delete' in exclude
        user_can_delete = ph.user_can_delete_obj(usr, obj)
        if delete_enabled and not delete_excluded and user_can_delete:
            btns.append(
                self.delete_button(
                    classnames=classnames,
                    parent_pk=parent.pk,
                    instance_pk=obj.pk)
            )
        return btns
