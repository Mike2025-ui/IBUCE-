from django.contrib import admin
from .models import Projet, Image, Commentaire, DemandeContact

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('id_projet', 'titre', 'lieu', 'annee', 'categorie', 'est_publie')
    list_filter = ('categorie', 'est_publie', 'annee')
    search_fields = ('titre', 'lieu', 'id_projet', 'description')
    readonly_fields = ('id_projet', 'date_creation')
    inlines = [ImageInline]
    fieldsets = (
        ('Identification', {'fields': ('id_projet', 'titre', 'categorie')}),
        ('Localisation', {'fields': ('lieu',)}),
        ('Détails', {'fields': ('annee', 'description', 'image_principale')}),
        ('Publication', {'fields': ('est_publie',)}),
    )

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'projet', 'note', 'date')
    list_filter = ('projet', 'note')

@admin.register(DemandeContact)
class DemandeContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'projet', 'date')
    list_filter = ('date',)