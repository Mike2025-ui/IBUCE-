from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ============================================================
# MODÈLES POUR IBUCE
# ============================================================

class Annonce(models.Model):
    """Modèle pour les projets IBUCE"""
    
    TYPE_CHOICES = [
        ('terrain', 'Terrain'),
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('commercial', 'Commercial'),
        ('Lotissement', 'Lotissement'),
        ('Amenagement', 'Aménagement'),
        ('Financement', 'Financement'),
        ('construction', 'Construction'),
        ('topographie', 'Topographie'),
        ('forage', 'Forage'),
        ('second_oeuvre', 'Second Œuvre'),
    ]
    
    id_annonce = models.CharField(max_length=10, unique=True, editable=False)
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    prix = models.CharField(max_length=50)
    surface = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    img_principale = models.ImageField(upload_to='annonces/images/', blank=True, null=True)
    note = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_publie = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id_annonce} - {self.titre}"
    
    def sauvegarder_avec_id(self):
        if not self.id_annonce:
            dernier = Annonce.objects.all().order_by('id').last()
            if dernier and dernier.id_annonce:
                try:
                    num = int(dernier.id_annonce[1:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.id_annonce = f"A{num:03d}"
        self.save()


class Image(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='annonces/images/')
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return f"Image pour {self.annonce.id_annonce}"


class Document(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='documents')
    nom = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='annonces/documents/')
    
    def __str__(self):
        return f"{self.nom} - {self.annonce.id_annonce}"


class Commentaire(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.CharField(max_length=100)
    note = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    texte = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.auteur} - {self.annonce.id_annonce} ({self.note}/5)"


class DemandeContact(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='demandes')
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.annonce.id_annonce}"