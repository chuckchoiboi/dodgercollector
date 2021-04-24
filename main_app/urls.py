from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # dodger urls
    path('dodgers/', views.dodgers_index, name='index'),
    path('dodgers/<int:dodger_id>/', views.dodgers_detail, name='detail'),
    path('dodgers/create/', views.DodgerCreate.as_view(), name='dodgers_create'),
    path('dodgers/<int:pk>/update/',
         views.DodgerUpdate.as_view(), name='dodgers_update'),
    path('dodgers/<int:pk>/delete/',
         views.DodgerDelete.as_view(), name='dodgers_delete'),
    path('dodgers/<int:dodger_id>/add_training/',
         views.add_training, name='add_training'),
    path('dodgers/<int:dodger_id>/assoc_equipment/<int:equipment_id>/',
         views.assoc_equipment, name='assoc_equipment'),
    path('dodgers/<int:dodger_id>/dissoc_equipment/<int:equipment_id>/',
         views.dissoc_equipment, name='dissoc_equipment'),
    path('dodgers/<int:dodger_id>/add_photo/',
         views.add_photo, name='add_photo'),

    # equipment urls
    path('equipments/', views.equipments_index, name='equipments_index'),
    path('equipments/<int:equipment_id>/',
         views.equipment_detail, name='equipment_detail'),
    path('equipments/create/', views.Create_Equipment.as_view(),
         name='equipments_create'),
    path('equipments/<int:pk>/update/',
         views.Update_equipment.as_view(), name='update_equipment'),
    path('equipments/<int:pk>/delete/',
         views.Delete_equipment.as_view(), name='delete_equipment'),

    # account urls
    path('accounts/signup/', views.signup, name='signup'),

]
