from django.core.management.base import BaseCommand#, CommandError
from personnel.models import PersonnelPermission

perms = {}
perms['group_add_personnel'] = 'Can add a personnel to a group'
perms['group_remove_personnel'] = 'Can remove a personnel from a group'
perms['permission_grant'] = 'Can grant a permission'
perms['permission_revoke'] = 'Can revoke a permission'
perms['grant_multiple_permissions'] = 'Can grant multiple permissions'
perms['view_permission_index'] = 'Can view permission index'
perms['view_personnel_index'] = 'Can personnel index'
perms['view_group_index'] = 'Can view group index'
perms['create_new_user'] = 'Can add a new user to the system'
perms['activate_deactivate_personnel_account'] = 'Can activate or deactivate a user'
perms['change_branch_manager'] = 'Can change a branch manager'

perms['create_expenditure'] = 'Can create expenditure'
perms['authorize_expenditure'] = 'Can authorize an expenditure'
perms['unauthorize_expenditure'] = 'Can unauthorize an expenditure'
perms['view_expenditure_index'] = 'Can view expenditure index'

perms['view_expenditure_type_index'] = 'Can view expenditure types'
perms['create_expendituretype'] = 'Can create expenditure type'

perms['create_debt'] = 'Can create debt'
perms['view_debt_index'] = 'Can view debt index'

perms['view_remit_index'] = 'Can view remit index'

perms['create_remuneration'] = 'Can create a remuneration'
perms['view_remuneration_index'] = 'Can view remuneration index'
perms['view_remuneration_type_index'] = 'Can view remuneration types'

perms['view_access_code_index'] = 'Can view branch access codes'

perms['view_asset_index'] = 'Can view assets'
perms['view_asset_type_index'] = 'Can view asset types'

perms['view_branch_index'] = 'Can view branches'
perms['create_branch'] = 'Can create a branch'
perms['edit_branch'] = 'Can edit a branch'
perms['delete_branch'] = 'Can delete a branch'
perms['switch_branch'] = 'Can switch branch'

perms['view_department_index'] = 'Can view departments'

perms['view_cashier_index'] = 'Can view cashier index'
perms['create_cashier'] = 'Can create a cashier'
perms['edit_cashier'] = 'Can edit a cashier'
perms['delete_cashier'] = 'Can delete a cashier'

perms['view_product_index'] = 'Can view product index'
perms['create_product'] = 'Can create a product'
perms['edit_product'] = 'Can edit a product'
perms['delete_product'] = 'Can delete a product'

perms['create_department'] = 'Can create a department'
perms['edit_department'] = 'Can edit a department'
perms['delete_department'] = 'Can delete a department'
perms['add_access_code_to_branch'] = 'Can create branch access code'
perms['delete_access_code'] = 'Can delete branch access code'

perms['create_asset'] = 'Can create asset'
perms['create_assettype'] = 'Can create asset type'
perms['edit_asset'] = 'Can edit asset'
perms['delete_asset'] = 'Can delete asset'
perms['view_asset_receipt'] = 'Can view asset receipt'

perms['create_sale'] = 'Can create sale'
perms['view_sales_index'] = 'Can view sales index'

perms['view_cash_pay_index'] = 'Can view cash payment index'
perms['view_bank_pay_index'] = 'Can view bank payment index'
perms['view_pos_pay_index'] = 'Can view POS payment index'
perms['view_winning_pay_index'] = 'Can view winning payment index'

perms['view_gameremit_index'] = 'Can view game remits'
perms['create_gameremit'] = 'Can create game remit'

perms['view_viewcenterremit_index'] = 'Can view viewcenter remit'
perms['create_viewcenterremit'] = 'Can create viewcenter remit'

perms['create_team'] = 'Can create a team'
perms['create_division'] = 'Can create a division'

perms['create_service'] = 'Can create a service'
perms['view_services_index'] = 'Can view services'


class Command(BaseCommand):
    help = 'Create all permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start creating permissions'))
        for key, value in perms.items():
            PersonnelPermission.objects.get_or_create(name=value.strip(), code_name=key.strip())
            self.stdout.write(key)
        self.stdout.write(self.style.SUCCESS('Finish creating permissions'))
