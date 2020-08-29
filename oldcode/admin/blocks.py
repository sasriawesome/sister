from sister.core.blocks import Block, BlockItem


class AdminBlockItem(BlockItem):
    template = 'admin/block_item.html'


admin_homepage_block = Block(hook_name='admin_homepage_block_item')
