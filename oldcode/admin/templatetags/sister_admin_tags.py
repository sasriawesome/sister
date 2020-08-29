from django import template
from sister.admin.menus import admin_menu
from sister.admin.blocks import admin_homepage_block

register = template.Library()


@register.inclusion_tag('admin/sidenav_main.html', takes_context=True)
def admin_sidenav(context):
    request = context['request']
    return {
        'menu_html': admin_menu.render_html(request),
        'request': request,
    }


@register.inclusion_tag('admin/index_blocks.html', takes_context=True)
def admin_homepage_blocks(context):
    request = context['request']
    return {
        'blocks_html': admin_homepage_block.render_html(request),
        'request': request,
    }
