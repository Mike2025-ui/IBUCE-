from django.contrib import admin
from .models import Projet, Image, Commentaire, DemandeContact

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['id_projet', 'titre', 'lieu', 'annee', 'categorie', 'est_publie', 'date_creation']
    list_filter = ['categorie', 'est_publie', 'annee']
    search_fields = ['titre', 'lieu', 'id_projet', 'description']
    readonly_fields = ['id_projet', 'date_creation']
    fieldsets = (
        ('Identification', {
            'fields': ('id_projet', 'titre', 'categorie')
        }),
        ('Localisation', {
            'fields': ('lieu',)
        }),
        ('Informations', {
            'fields': ('annee', 'description', 'image_principale')
        }),
        ('Statut', {
            'fields': ('est_publie',)
        }),
    )

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'projet', 'ordre']
    list_filter = ['projet']
    search_fields = ['projet__titre']

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'auteur', 'projet', 'note', 'date']
    list_filter = ['projet', 'note', 'date']
    search_fields = ['auteur', 'texte', 'projet__titre']

@admin.register(DemandeContact)
class DemandeContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'telephone', 'projet', 'date']
    list_filter = ['date']
    search_fields = ['nom', 'telephone', 'email', 'message']