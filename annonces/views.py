from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Projet, Image, Commentaire, DemandeContact
import json
from django.conf import settings
import os

# ============================================================
# PAGES HTML
# ============================================================

def index(request):
    return render(request, 'annonces/index.html')


@csrf_exempt
def page_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_panel')
        else:
            return render(request, 'annonces/login.html', {'error': True})
    
    return render(request, 'annonces/login.html')


@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('page_login')
    return render(request, 'annonces/index.html', {'show_admin': True})


def force_logout(request):
    logout(request)
    return redirect('/')


# ============================================================
# API POUR LES PROJETS
# ============================================================

def api_projets(request):
    """API qui retourne TOUS les projets au format JSON"""
    projets = Projet.objects.filter(est_publie=True)
    
    data = []
    for p in projets:
        images_urls = [img.image.url if img.image else '' for img in p.images.all()]
        commentaires_list = [{
            'auteur': c.auteur,
            'date': c.date.strftime('%d %b. %Y'),
            'note': c.note,
            'texte': c.texte
        } for c in p.commentaires.all()]
        
        data.append({
            'id': p.id_projet,
            'titre': p.titre,
            'lieu': p.lieu,
            'annee': p.annee,
            'categorie': p.categorie,
            'description': p.description,
            'imgPrincipale': p.image_principale.url if p.image_principale else '',
            'images': images_urls,
            'note': 0,
            'commentaires': commentaires_list
        })
    
    return JsonResponse(data, safe=False)


def api_projet_detail(request, id_projet):
    """API qui retourne UN SEUL projet (par son ID)"""
    try:
        projet = Projet.objects.get(id_projet=id_projet, est_publie=True)
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)
    
    images_urls = [img.image.url if img.image else '' for img in projet.images.all()]
    commentaires_list = [{
        'auteur': c.auteur,
        'date': c.date.strftime('%d %b. %Y'),
        'note': c.note,
        'texte': c.texte
    } for c in projet.commentaires.all()]
    
    data = {
        'id': projet.id_projet,
        'titre': projet.titre,
        'lieu': projet.lieu,
        'annee': projet.annee,
        'categorie': projet.categorie,
        'description': projet.description,
        'imgPrincipale': projet.image_principale.url if projet.image_principale else '',
        'images': images_urls,
        'note': 0,
        'commentaires': commentaires_list
    }
    return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
def creer_projet(request):
    """Crée un nouveau projet avec upload de fichiers"""
    try:
        titre = request.POST.get('titre')
        lieu = request.POST.get('lieu')
        annee = request.POST.get('annee')
        categorie = request.POST.get('categorie')
        description = request.POST.get('description')
        
        if not all([titre, lieu, annee, description]):
            return JsonResponse({'error': 'Tous les champs obligatoires doivent être remplis'}, status=400)
        
        projet = Projet(
            titre=titre,
            lieu=lieu,
            annee=annee,
            categorie=categorie,
            description=description,
            est_publie=True
        )
        
        if request.FILES.get('image_principale'):
            projet.image_principale = request.FILES['image_principale']
        
        projet.save()
        
        # Générer l'ID après sauvegarde
        if not projet.id_projet:
            dernier = Projet.objects.all().order_by('-id_projet').first()
            if dernier and dernier.id_projet.startswith('P'):
                try:
                    num = int(dernier.id_projet[1:]) + 1
                    projet.id_projet = f"P{num:03d}"
                except:
                    projet.id_projet = "P001"
            else:
                projet.id_projet = "P001"
            projet.save()
        
        for img_file in request.FILES.getlist('images'):
            Image.objects.create(projet=projet, image=img_file, ordre=0)
        
        return JsonResponse({'success': True, 'id': projet.id_projet})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
def supprimer_projet(request, id_projet):
    """Supprime un projet"""
    try:
        projet = Projet.objects.get(id_projet=id_projet)
        if projet.image_principale:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(projet.image_principale)))
            except:
                pass
        projet.delete()
        return JsonResponse({'success': True})
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)


@require_http_methods(["POST"])
def modifier_projet(request, id_projet):
    """Modifie un projet (avec support upload image)"""
    try:
        projet = Projet.objects.get(id_projet=id_projet)
        
        projet.titre = request.POST.get('titre', projet.titre)
        projet.lieu = request.POST.get('lieu', projet.lieu)
        projet.annee = request.POST.get('annee', projet.annee)
        projet.categorie = request.POST.get('categorie', projet.categorie)
        projet.description = request.POST.get('description', projet.description)
        
        if request.FILES.get('image_principale'):
            if projet.image_principale:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(projet.image_principale)))
                except:
                    pass
            projet.image_principale = request.FILES['image_principale']
        
        projet.save()
        return JsonResponse({'success': True})
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def ajouter_commentaire(request, id_projet):
    """Ajoute un commentaire à un projet"""
    try:
        projet = Projet.objects.get(id_projet=id_projet)
        data = json.loads(request.body)
        
        Commentaire.objects.create(
            projet=projet,
            auteur=data['auteur'],
            note=data['note'],
            texte=data['texte']
        )
        
        return JsonResponse({'success': True})
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def contacter_interesse(request):
    """Formulaire de contact"""
    try:
        data = json.loads(request.body)
        projet_id = data.get('projet_id')
        prenom = data.get('prenom')
        nom = data.get('nom')
        telephone = data.get('telephone')
        message = data.get('message', '')
        
        if not all([prenom, nom, telephone]):
            return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)
        
        projet = None
        if projet_id:
            try:
                projet = Projet.objects.get(id_projet=projet_id)
            except Projet.DoesNotExist:
                pass
        
        DemandeContact.objects.create(
            projet=projet,
            nom=f"{prenom} {nom}",
            telephone=telephone,
            message=message
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)