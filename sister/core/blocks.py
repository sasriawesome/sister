from django.forms import Media, MediaDefiningClass
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from sister.core import hooks


class BlockItem(metaclass=MediaDefiningClass):
    template = 'block_item.html'

    def __init__(self, label, icon='', name=None, classnames='', attrs=None, order=1000):
        self.label = label
        self.name = (name or slugify(str(label)))
        self.classnames = classnames
        self.order = order
        self.icon = icon

        if attrs:
            self.attr_string = flatatt(attrs)
        else:
            self.attr_string = ""

    def is_shown(self, request):
        """
        Whether this menu item should be shown for the given request; permission
        checks etc should go here. By default, menu items are shown all the time
        """
        return True

    def get_context(self, request):
        """Defines context for the template, overridable to use more data"""
        return {
            'name': self.name,
            'classnames': self.classnames,
            'attr_string': self.attr_string,
            'label': self.label,
            'icon': self.icon
        }

    def render_html(self, request):
        context = self.get_context(request)
        return render_to_string(self.template, context, request=request)


class Block:

    hook_name = None

    def __init__(self, hook_name):
        if not isinstance(hook_name, str):
            return ValueError('Hookname must be a string')
        self._registered_block_items = []
        self.hook_name = hook_name

    @property
    def registered_block_items(self):
        if not bool(self._registered_block_items):
            self._registered_block_items = hooks.get_hooks(self.hook_name)
        return self._registered_block_items

    def block_items_for_request(self, request):
        items = [ item(request) for item in self.registered_block_items ]
        return [ item for item in items if item.is_shown(request)]

    @property
    def media(self):
        media = Media()
        for item in self.registered_block_items:
            media += item.media
        return media

    def render_html(self, request):
        block_items = self.block_items_for_request(request)

        # provide a hook for modifying the block, if construct_hook_name has been set

        rendered_block_items = []
        for item in sorted(block_items, key=lambda i: i.order):
            rendered_block_items.append(item.render_html(request))
        return mark_safe(''.join(rendered_block_items))


homepage_block = Block(hook_name='homepage_block_item')