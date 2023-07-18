from django.urls import path

from api.v1.manager import views


urlpatterns = [
    path('login/', views.login),

    path('category/', views.category),
    path('category/add/', views.category_add),
    path('category/edit/<int:pk>/', views.category_edit),
    path('category/delete/<int:pk>/', views.category_delete),

    path('item/', views.item),
    path('item/add/', views.item_add),
    path('item/edit/<int:pk>/', views.item_edit),
    path('item/delete/<int:pk>/', views.item_delete),

    path('franchise/', views.franchise),
    path('franchise/add/', views.franchise_add),
    path('franchise/edit/<int:pk>/', views.franchise_edit),
    path('franchise/delete/<int:pk>/', views.franchise_delete),

    path('franchise/user/', views.franchise_user),
    path('franchise/user/add/', views.franchise_user_add),
    # path('franchise/user/edit/<int:pk>/', views.franchise_user_edit),
    path('franchise/user/delete/<int:pk>/', views.franchise_user_delete),

    # path('item/assign/', views.item_assign),
    # path('item/assign/edit/<int:pk>/', views.item_assign_edit),
    # path('item/assign/delete/<int:pk>/', views.item_assign_delete),

]