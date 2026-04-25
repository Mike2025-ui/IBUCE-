from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Projet, Image, DemandeContact
import json
from django.conf import settings
import os

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
        if user and user.is_staff:
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

def api_projets(request):
    projets = Projet.objects.filter(est_publie=True)
    data = []
    for p in projets:
        images = [img.image.url for img in p.images.all()]
        data.append({
            'id': p.id_projet,
            'titre': p.titre,
            'lieu': p.lieu,
            'annee': p.annee,
            'categorie': p.categorie,
            'description': p.description,
            'image_principale': p.image_principale.url if p.image_principale else '',
            'images': images,
        })
    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
def creer_projet(request):
    titre = request.POST.get('titre')
    lieu = request.POST.get('lieu')
    annee = request.POST.get('annee')
    categorie = request.POST.get('categorie')
    description = request.POST.get('description')
    if not all([titre, lieu, annee, description]):
        return JsonResponse({'error': 'Champs requis manquants'}, status=400)
    projet = Projet(
        titre=titre, lieu=lieu, annee=annee,
        categorie=categorie, description=description, est_publie=True
    )
    if request.FILES.get('image_principale'):
        projet.image_principale = request.FILES['image_principale']
    projet.save()
    # Génération de l'ID
    if not projet.id_projet:
        dernier = Projet.objects.order_by('-id_projet').first()
        num = 1
        if dernier and dernier.id_projet.startswith('P'):
            try:
                num = int(dernier.id_projet[1:]) + 1
            except:
                num = 1
        projet.id_projet = f"P{num:03d}"
        projet.save()
    for img in request.FILES.getlist('images'):
        Image.objects.create(projet=projet, image=img)
    return JsonResponse({'success': True, 'id': projet.id_projet})

@require_http_methods(["DELETE"])
def supprimer_projet(request, id_projet):
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

def envoyer_contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        tel = request.POST.get('telephone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if nom and tel and message:
            DemandeContact.objects.create(
                nom=nom, telephone=tel, email=email, message=message
            )
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Champs requis'}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)