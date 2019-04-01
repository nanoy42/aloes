from django.urls import path

from . import views

app_name = "gestion"

urlpatterns = [
    path('createRenovation', views.RenovationCreate.as_view(), name="createRenovation"),
    path('editRenovation/<int:pk>', views.RenovationEdit.as_view(), name="editRenovation"),
    path('deleleRenovation/<int:pk>', views.RenovationDelete.as_view(), name="deleteRenovation"),
    path('indexRenovation', views.renovationIndex, name="indexRenovation"),
    path('gestionIndex', views.gestionIndex, name="indexGestion"),
    path('tenantProfile/<int:pk>', views.tenantProfile, name="tenantProfile"),
    path('createTenant', views.TenantCreate.as_view(), name="createTenant"),
    path('createSchool', views.SchoolCreate.as_view(), name="createSchool"),
    path('editSchool/<int:pk>', views.SchoolEdit.as_view(), name="editSchool"),
    path('deleleSchool/<int:pk>', views.SchoolDelete.as_view(), name="deleteSchool"),
    path('indexSchool', views.schoolIndex, name="indexSchool"),
    path('createRent', views.RentCreate.as_view(), name="createRent"),
    path('editRent/<int:pk>', views.RentEdit.as_view(), name="editRent"),
    path('deleleRent/<int:pk>', views.RentDelete.as_view(), name="deleteRent"),
    path('indexRent', views.rentIndex, name="indexRent"),
    path('roomProfile/<int:pk>', views.roomProfile, name="roomProfile"),
    path('createRoom', views.RoomCreate.as_view(), name="createRoom"),
    path('leasingProfile/<int:pk>', views.leasingProfile, name="leasingProfile"),
    path('addOneYear', views.addOneYear, name="addOneYear"),
    path('leave/<int:pk>', views.leave, name="leave"),
    path('moveIn/<str:mode>/<int:pk>', views.moveIn, name="moveIn"),
    path('moveOut/<str:mode>/<int:pk>', views.moveOut, name="moveOut"),
    path('addNextTenant/<int:pk>', views.addNextTenant, name="addNextTenant"),
    path('addNextRoom/<int:pk>', views.addNextRoom, name="addNextRoom"),
    path('cancelNextRoom/<str:mode>/<int:pk>', views.cancelNextRoom, name="cancelNextRoom"),
    path('tenantMoveInDirect/<int:pk>', views.tenantMoveInDirect, name="tenantMoveInDirect"),
    path('roomMoveInDirect/<int:pk>', views.roomMoveInDirect, name="roomMoveInDirect"),
    path('createMap', views.MapCreate.as_view(), name="createMap"),
    path('editMap/<int:pk>', views.MapEdit.as_view(), name="editMap"),
    path('deleleMap/<int:pk>', views.MapDelete.as_view(), name="deleteMap"),
    path('indexMap', views.mapIndex, name="indexMap"),
    path('changeRoomMap/<int:pk>', views.ChangeRoomMap.as_view(), name="changeRoomMap"),
    path('exportCSV', views.export_csv, name="exportCSV"),
    path('homeless_tenants', views.homeless_tenants, name="homelessTenants"),
]
