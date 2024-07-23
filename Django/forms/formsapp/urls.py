
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('add/', views.add_view, name='add'),
    path('prospect_form/', views.prospect_view, name='prospect_form'),
    path('success/', views.success_view, name='success'),
    path('prospect/', views.prospect_list_view, name='prospect_list'),
    path('prospects/edit/<int:id>/', views.prospect_edit_view, name='prospect_edit'),
    path('prospects/delete/<int:id>/', views.prospect_delete_view, name='prospect_delete'),
]
