"""Urls of gestion app."""
from django.urls import path

from . import views

app_name = "gestion"

urlpatterns = [
    path('createRenovation', views.RenovationCreate.as_view(),
         name="createRenovation"),
    path('editRenovation/<int:pk>',
         views.RenovationEdit.as_view(), name="editRenovation"),
    path('deleleRenovation/<int:pk>',
         views.RenovationDelete.as_view(), name="deleteRenovation"),
    path('indexRenovation', views.renovations_index, name="indexRenovation"),
    path('gestionIndex', views.gestion_index, name="indexGestion"),
    path('tenantProfile/<int:pk>', views.tenant_profile, name="tenantProfile"),
    path('editTenant/<int:pk>', views.edit_tenant, name="editTenant"),
    path('createTenant', views.TenantCreate.as_view(), name="createTenant"),
    path('createSchool', views.SchoolCreate.as_view(), name="createSchool"),
    path('editSchool/<int:pk>', views.SchoolEdit.as_view(), name="editSchool"),
    path('deleleSchool/<int:pk>', views.SchoolDelete.as_view(),
         name="deleteSchool"),
    path('indexSchool', views.schools_index, name="indexSchool"),
    path('createRent', views.RentCreate.as_view(), name="createRent"),
    path('editRent/<int:pk>', views.RentEdit.as_view(), name="editRent"),
    path('deleleRent/<int:pk>', views.RentDelete.as_view(), name="deleteRent"),
    path('indexRent', views.rents_index, name="indexRent"),
    path('roomProfile/<int:pk>', views.room_profile, name="roomProfile"),
    path('editRoom/<int:pk>', views.edit_room, name="editRoom"),
    path('createRoom', views.RoomCreate.as_view(), name="createRoom"),
    path('leasingProfile/<int:pk>', views.leasing_profile,
         name="leasingProfile"),
    path('editLeasing/<int:pk>', views.edit_leasing, name="editLeasing"),
    path('addOneYear', views.add_one_year, name="addOneYear"),
    path('leave/<int:pk>', views.leave, name="leave"),
    path('moveIn/<str:mode>/<int:pk>', views.move_in, name="moveIn"),
    path('moveOut/<str:mode>/<int:pk>', views.move_out, name="moveOut"),
    path('addNextTenant/<int:pk>', views.add_next_tenant, name="addNextTenant"),
    path('addNextRoom/<int:pk>', views.add_next_room, name="addNextRoom"),
    path('cancelNextRoom/<str:mode>/<int:pk>',
         views.cancel_next_room, name="cancelNextRoom"),
    path('tenantMoveInDirect/<int:pk>',
         views.tenant_move_in_direct, name="tenantMoveInDirect"),
    path('roomMoveInDirect/<int:pk>',
         views.room_move_in_direct, name="roomMoveInDirect"),
    path('createMap', views.MapCreate.as_view(), name="createMap"),
    path('editMap/<int:pk>', views.MapEdit.as_view(), name="editMap"),
    path('deleleMap/<int:pk>', views.MapDelete.as_view(), name="deleteMap"),
    path('indexMap', views.map_index, name="indexMap"),
    path('changeRoomMap/<int:pk>',
         views.ChangeRoomMap.as_view(), name="changeRoomMap"),
    path('exportCSV', views.export_xls, name="exportCSV"),
    path(
        'emptyRoomAutocomplete',
        views.EmptyRoomAutocomplete.as_view(),
        name="emptyRoomAutocomplete"
    ),
    path(
        'noNextTenantRoomAutocomplete',
        views.NoNextTenantRoomAutomplete.as_view(),
        name="noNextTenantRoomAutocomplete"
    ),
    path(
        'tenantWNRAutocomplete',
        views.TenantWNRAutocomplete.as_view(),
        name="tenantWNRAutocomplete"
    ),
    path(
        'tenantWithoutRoomAutocomplete',
        views.TenantWithoutRoomAutocomplete.as_view(),
        name="tenantWithoutRoomAutocomplete"
    ),
    path('backup', views.backup, name="backup"),
    path('mailTenants', views.mail_tenants, name="mailTenants"),
    path('homelessTenants', views.homeless_tenants, name="homelessTenants"),
    path('roomSwitchActivate/<int:pk>', views.room_switch_activate, name="roomSwitchActivate"),
    path('inactiveRooms', views.inactive_rooms, name="inactiveRooms"),
    path('importTenant', views.import_tenant, name="importTenant"),
]
