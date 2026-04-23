from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Projet(models.Model):
    CATEGORIE_CHOICES = [
        ('topographie', 'Topographie'),
        ('travaux_publics', 'Travaux Publics'),
        ('construction', 'Construction'),
        ('hydraulique', 'Hydraulique'),
        ('cartographie', 'Cartographie'),
        ('juridique', 'Juridique foncier'),
        ('amenagement', 'Aménagement'),
        ('formation', 'Formation'),
        ('vente', 'Vente matériel'),
        ('import_export', 'Import-Export'),
        ('informatique', 'Informatique'),
        ('bathymetrie', 'Bathymétrie'),
        ('minier', 'Minier'),
    ]
    
    id_projet = models.CharField(max_length=10, unique=True, editable=False)
    titre = models.CharField(max_length=200)
    lieu = models.CharField(max_length=200)
    annee = models.CharField(max_length=10)
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES, default='construction')
    description = models.TextField()
    image_principale = models.ImageField(upload_to='projets/', null=True, blank=True)
    est_publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.id_projet:
            dernier = Projet.objects.all().order_by('-id_projet').first()
            if dernier and dernier.id_projet.startswith('P'):
                try:
                    num = int(dernier.id_projet[1:]) + 1
                    self.id_projet = f"P{num:03d}"
                except:
                    self.id_projet = "P001"
            else:
                self.id_projet = "P001"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id_projet} - {self.titre}"


class Image(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projets/images/')
    ordre = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Image pour {self.projet.titre}"


class Commentaire(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.CharField(max_length=100)
    note = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    texte = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.auteur} - {self.projet.titre}"


class DemandeContact(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} - {self.telephone}"