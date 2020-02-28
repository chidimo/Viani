from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

from constants.banner import BANNER

class PermissionBackend():
    def authenticate(self, *args, **kwargs):
        return None

    def has_permission(self, perm, request, *args, **kwargs):
        try:
            user_perms = request.user.personnel.personnel_permissions()
            print('user_perms', user_perms)
            return perm in user_perms
        except:
            logout(request)
            redirect('personnel:login')

vianirules = PermissionBackend()
