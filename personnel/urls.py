"""Urls"""

from django.urls import reverse_lazy, path, re_path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'personnel'

urlpatterns = []

urlpatterns += [
    re_path(r'^report/(?P<out_format>[\w]+)/$', views.report, name='report'),
]

urlpatterns += [
    path('', views.PersonnelIndex.as_view(), name='index'),
    path('staff/', views.PersonnelPublicIndex.as_view(), name='staffers'),
    path('groups/', views.GroupIndex.as_view(), name='groups'),
    path('permissions/', views.PersonnelPermissionIndex.as_view(), name='permissions'),
    path('permission-detail/<int:pk>/', views.PersonnelPermissionDetail.as_view(), name='permission_detail'),
    path('designations/', views.DesignationIndex.as_view(), name='designations'),
]


urlpatterns += [
    path('new/', views.new_personnel, name='new'),
    path('welcome/<str:display_name>/', views.welcome_personnel, name='create_success'),
    path('activate/<int:pk>/<str:display_name>/', views.activate_personnel, name='create_activate'),
    path('edit/<int:pk>/<slug:slug>', views.PersonnelEdit.as_view(), name='edit'),
    path('edit/manager/<int:pk>/<slug:slug>/', views.PersonnelEditByManager.as_view(), name='edit_by_manager'),
    path('edit/avatar/<int:pk>/', views.PersonnelAvatarEdit.as_view(), name='edit_avatar'),
]

urlpatterns += [
    path('new/avatar/<int:pk>/', views.PersonnelAvatarCreate.as_view(), name='new_avatar'),
    path('new/group/', views.new_group, name='new_group'),
    path('new/designation/', views.NewDesignation.as_view(), name='new_designation'),
    path('activate-deactivate/<int:pk>/<slug:slug>/', views.activate_deactivate_personnel_account, name='activate_deactivate_personnel_account'),
    path('detail/<int:pk>/<slug:slug>', views.PersonnelDetail.as_view(), name='detail'),
    path('add-personnels-to-group/<int:pk>/', views.add_personnels_to_group, name='add_personnels_to_group'),
    path('remove-personnels-from-group/<int:pk>/', views.remove_personnel_from_group, name='remove_personnel_from_group'),
]

urlpatterns += [
    path('set_permission/<int:pk>/', views.make_staff, name='make_staff'),
    path('personnel-branch/', views.BranchPersonnel.as_view(), name='branch_staff'),
    path('grant-permisson/<int:pk>/', views.grant_permission, name='grant_permission'),
    path('revoke-permisson/<int:pk>/', views.revoke_permission, name='revoke_permission'),
    path('multiple-permisson/', views.grant_multiple_permissions, name='grant_multiple_permissions'),
]

urlpatterns += [
    path('remunerations/<int:pk>/<slug:slug>/', views.personnel_remunerations, name='personnel_remunerations'),
    path('sales/<int:pk>/<slug:slug>/', views.personnel_sales, name='personnel_sales'),
    path('sale-filter/', views.PersonnelSaleFilterView.as_view(), name='personnel_sale_filter'),
    path('remits/<int:pk>/<slug:slug>/', views.personnel_remits, name='personnel_remits'),
    path('debts/<int:pk>/<slug:slug>/', views.personnel_debts, name='personnel_debts'),
    path('expenditures/<int:pk>/<slug:slug>/', views.personnel_expenditures, name='personnel_expenditures'),
    path('games-remit/<int:pk>/<slug:slug>/', views.personnel_gameremits, name='personnel_gameremits'),
    path('viewcenter-remits/<int:pk>/<slug:slug>/', views.personnel_viewcenterremits, name='personnel_viewcenterremits'),
]

urlpatterns += [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-manager/', views.dashboard_manager, name='dashboard_manager'),
    path('dashboard-ceo/', views.dashboard_ceo, name='dashboard_ceo'),
]

urlpatterns += [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('personnel:password_change_done')), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('personnel:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('personnel:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
