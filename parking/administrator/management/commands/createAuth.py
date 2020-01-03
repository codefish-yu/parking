from django.core.management.base import BaseCommand, CommandError

from administrator.models import AdminUser, Menu, Operation, Role


'''系统部署时初始化权限菜单, 运行一次'''

class Command(BaseCommand):

    def handle(self, *args, **options):

        Operations = {
            '查询': 'search',
            '新增': 'add',
            '修改': 'update',
            '删除': 'delete',
            '导出': 'export'
        }
        Menus = [{
                '系统配置': [
                    ['系统参数配置', ['查询', '新增', '修改', '删除'], '/administrator/settings/'],
                    ['系统类别明细', ['查询', '新增', '修改', '删除'], '/administrator/options/'], 
                    ['角色管理',    ['查询', '新增', '修改', '删除'], '/administrator/role/'], 
                    ['操作日志',    ['查询', '删除'], '/administrator/log/']
            ]},
            {
                '用户管理':[
                    ['用户列表', ['查询', '新增', '修改', '删除'], '/administrator/user/'],
                    ['个人资料', ['修改'], '/administrator/personal/']
            ]},
            {
                '商家管理':[
                    ['商家列表',[], '/company/list/'],
                    ['商家充值明细', [], '/company/bill/'],
                    ['商家车牌充值明细', [], '/company/bill2/'],
                    ['折扣券管理', [], '/company/ticket/']
            ]},
            {
                '停车场管理':[
                    ['出入口管理',[], '/parking/entry/'],
                    ['区域管理', [], '/parking/area/'],
                    ['泊位管理', [], '/parking/port/'],
                    ['收费站管理', [], '/parking/station/'],
                    ['摄像头管理', [], '/parking/carema/'],
                    ['LED管理', [], '/parking/led/'],
                    ['人员管理', [], '/parking/workman/']
            ]},
            {
                '内部车管理':[
                    ['内部车列表',[], '/specialcar/list/'],
                    ['充值明细', [], '/specialcar/bill/'],
                    ['充值规则配置', [], '/specialcar/rule/'],
                    ['黑名单管理', [], '/specialcar/bad/'],
            ]},
            {
                '报表管理':[
                    ['停车场支付方式日报表',[], '/data/pay-inner/'],
                    ['终端支付明细', [], '/data/pay-phone/'],
                    ['岗亭收费明细报表', [], '/data/pay-pass/'],
            ]},
        ]

        for i in Menus:
            for k,v in i.items():
                menu = Menu.objects.filter(menu_name=k)
                if menu.exists():
                    menu = menu.first()
                else:
                    menu = Menu.objects.create(menu_name=k)

                for child in v:
                    child_menu = Menu.objects.filter(menu_name=child[0])
                    if child_menu.exists():
                        child_menu = child_menu.first()
                    else:
                        child_menu = Menu.objects.create(menu_name=child[0], parent=menu, url=child[2])

                    for op in child[1]:
                        operation = Operation.objects.create(operation_name=op, action=Operations[op])

                        child_menu.operation.add(operation)
 
        if not AdminUser.objects.exists():
            if not Role.objects.exists():
                role = Role.objects.create(role_name='Admin', detail='系统默认管理员角色')
            else:
                role = Role.objects.filter(role_name='Admin').first()

            AdminUser.objects.create(user_name='admin', user_pass='admin', role_name=role, remark='系统默认管理员')

