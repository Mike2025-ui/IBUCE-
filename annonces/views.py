from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Projet, Image, Commentaire, DemandeContact
import json
import os

# ============================================================
# PAGES HTML
# ============================================================

def index(request):
    return render(request, 'annonces/index.html')


@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('/IbucClaude-admin-access/')
    return render(request, 'annonces/index.html', {'show_admin': True})


def page_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin-ibuce-panel/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/admin-ibuce-panel/')
        else:
            return render(request, 'annonces/login.html', {'error': True})
    
    return render(request, 'annonces/login.html')


def force_logout(request):
    logout(request)
    return redirect('/')


# ============================================================
# API PROJETS
# ============================================================

def api_projets(request):
    projets = Projet.objects.filter(est_publie=True)
    data = []
    for p in projets:
        images_urls = [img.image.url for img in p.images.all() if img.image]
        data.append({
            'id': p.id_projet,
            'titre': p.titre,
            'lieu': p.lieu,
            'annee': p.annee,
            'categorie': p.categorie,
            'description': p.description,
            'image_principale': p.image_principale.url if p.image_principale else '/static/annonces/images/logoibuce.jpg',
            'images': images_urls,
            'commentaires': []
        })
    return JsonResponse(data, safe=False)


def api_projet_detail(request, id_projet):
    try:
        projet = Projet.objects.get(id_projet=id_projet, est_publie=True)
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)
    
    images_urls = [img.image.url for img in projet.images.all() if img.image]
    data = {
        'id': projet.id_projet,
        'titre': projet.titre,
        'lieu': projet.lieu,
        'annee': projet.annee,
        'categorie': projet.categorie,
        'description': projet.description,
        'image_principale': projet.image_principale.url if projet.image_principale else '/static/annonces/images/logoibuce.jpg',
        'images': images_urls,
        'commentaires': []
    }
    return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
def creer_projet(request):
    try:
        titre = request.POST.get('titre')
        lieu = request.POST.get('lieu')
        annee = request.POST.get('annee')
        categorie = request.POST.get('categorie')
        description = request.POST.get('description')
        
        if not all([titre, lieu, annee, description]):
            return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)
        
        projet = Projet(
            titre=titre, lieu=lieu, annee=annee,
            categorie=categorie, description=description, est_publie=True
        )
        
        if request.FILES.get('image_principale'):
            projet.image_principale = request.FILES['image_principale']
        
        projet.save()
        
        for img_file in request.FILES.getlist('images'):
            Image.objects.create(projet=projet, image=img_file, ordre=0)
        
        return JsonResponse({'success': True, 'id': projet.id_projet})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
def supprimer_projet(request, id_projet):
    try:
        projet = Projet.objects.get(id_projet=id_projet)
        projet.delete()
        return JsonResponse({'success': True})
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)


@require_http_methods(["POST"])
def modifier_projet(request, id_projet):
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


@require_http_methods(["POST"])
def contacter_interesse(request):
    try:
        data = json.loads(request.body)
        prenom = data.get('prenom')
        nom = data.get('nom')
        telephone = data.get('telephone')
        message = data.get('message', '')
        
        if not all([prenom, nom, telephone]):
            return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)
        
        DemandeContact.objects.create(
            nom=f"{prenom} {nom}",
            telephone=telephone,
            message=message
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)