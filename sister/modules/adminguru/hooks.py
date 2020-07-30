from django.shortcuts import reverse
from sister.core import hooks
from sister.admin.blocks import AdminBlockItem
from sister.admin.menus import MenuItem

from sister.modules.pembelajaran.models import Kelas

class GuruMenuItem(MenuItem):

    def is_shown(self, request):
        return request.user.is_superuser


class KelasBlockItem(AdminBlockItem):
    template = 'admin/kelas_block.html'

    def get_context(self, request):
        context = super().get_context(request)
        context.update({
            'kelas_list': Kelas.objects.filter(guru_kelas=request.user.profile.guru)
        })
        return context

    def is_shown(self, request):
        if not hasattr(request.user, 'profile'):
            return False
        return True if hasattr(request.user.profile, 'guru') else False


@hooks.register('admin_menu_item')
def register_guru_kelas_menu(request):
    return GuruMenuItem('Kelas', reverse('admin:guruadmin_kelas_index'), icon='teach' )


@hooks.register('admin_homepage_block_item')
def register_guru_kelas_block(request):
    return KelasBlockItem('Kelas')