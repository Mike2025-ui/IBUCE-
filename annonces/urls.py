from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('IbucClaude-admin-access/', views.page_login, name='page_login'),
    path('admin-ibuce-panel/', views.admin_panel, name='admin_panel'),
    path('logout/', views.force_logout, name='logout'),
    
    path('api/projets/', views.api_projets, name='api_projets'),
    path('api/projets/creer/', views.creer_projet, name='creer_projet'),
    path('api/projets/<str:id_projet>/supprimer/', views.supprimer_projet, name='supprimer_projet'),
    path('api/projets/<str:id_projet>/modifier/', views.modifier_projet, name='modifier_projet'),
    path('api/contact/', views.contacter_interesse, name='contacter_interesse'),
]