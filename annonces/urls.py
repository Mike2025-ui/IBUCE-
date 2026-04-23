from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('IbucClaude-admin-access/', views.page_login, name='page_login'),
    path('admin-ibuce-panel/', views.admin_panel, name='admin_panel'),
    path('logout/', views.force_logout, name='logout'),
    
    # API Projets
    path('api/projets/', views.api_projets, name='api_projets'),
    path('api/projet/<str:id_projet>/', views.api_projet_detail, name='api_projet_detail'),
    path('api/projets/creer/', views.creer_projet, name='creer_projet'),
    path('api/projets/<str:id_projet>/supprimer/', views.supprimer_projet, name='supprimer_projet'),
    path('api/projets/<str:id_projet>/modifier/', views.modifier_projet, name='modifier_projet'),
    path('api/projet/<str:id_projet>/commentaire/', views.ajouter_commentaire, name='ajouter_commentaire'),
    path('api/contact/interesse/', views.contacter_interesse, name='contacter_interesse'),
]