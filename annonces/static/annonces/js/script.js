let projets = [];
let projetActif = null;
let galerieImages = [];
let galerieIndex = 0;
let whatsappNumero1 = "2250757090714";
let whatsappNumero2 = "2250574002019";

function getMediaUrl(path) {
    if (!path) return '/static/annonces/images/logoibuce.jpg';
    if (path.startsWith('http')) return path;
    if (path.startsWith('/media/')) return path;
    if (path.startsWith('/static/')) return path;
    return `/static/annonces/images/${path}`;
}

function showPage(nom) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const page = document.getElementById('page-' + nom);
    if (page) page.classList.add('active');
    const navLinks = document.getElementById('navLinks');
    if (navLinks) navLinks.classList.remove('open');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (nom === 'admin') renderAdminList();
}

function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('open');
}

function retourRealisations() {
    showPage('realisations');
}

async function chargerProjets() {
    try {
        const response = await fetch('/api/projets/');
        const data = await response.json();
        projets = data;
        renderRealisationsAccueil();
        renderRealisationsFull();
        if (document.getElementById('adminList')) renderAdminList();
        console.log('✅ IBUCE - Projets chargés depuis Django');
    } catch (error) {
        console.error('Erreur chargement projets:', error);
    }
}

function creerCarteRealisation(p) {
    const imgUrl = getMediaUrl(p.image_principale);
    const categorieFr = {
        'construction': 'Construction', 'topographie': 'Topographie',
        'amenagement': 'Aménagement', 'forage': 'Forage',
        'hydraulique': 'Hydraulique', 'cartographie': 'Cartographie',
        'juridique': 'Juridique foncier'
    }[p.categorie] || 'Réalisation';
    
    return `
        <div class="realisation-card" onclick="voirDetail('${p.id}')">
            <div class="card-img">
                <img src="${imgUrl}" alt="${p.titre}" onerror="this.src='/static/annonces/images/logoibuce.jpg'">
                <span class="card-badge">${p.annee}</span>
            </div>
            <div class="card-content">
                <h3>${p.titre}</h3>
                <div class="card-location"><i class="fas fa-map-marker-alt"></i> ${p.lieu}</div>
                <div class="card-desc">${p.description.substring(0, 100)}${p.description.length > 100 ? '...' : ''}</div>
                <button class="btn-detail-modern" onclick="event.stopPropagation(); voirDetail('${p.id}')">
                    Voir le projet <i class="fas fa-arrow-right"></i>
                </button>
            </div>
        </div>
    `;
}

function renderRealisationsAccueil() {
    const grid = document.getElementById('realisationsGrid');
    if (!grid) return;
    grid.innerHTML = projets.slice(0, 3).map(creerCarteRealisation).join('');
}

function renderRealisationsFull() {
    const grid = document.getElementById('realisationsGridFull');
    if (!grid) return;
    grid.innerHTML = projets.map(creerCarteRealisation).join('');
}

function voirDetail(id) {
    const p = projets.find(x => x.id == id);
    if (!p) return;
    projetActif = p;
    
    const imagesListe = p.images && p.images.length ? p.images : [p.image_principale];
    const thumbsHTML = imagesListe.map((img, i) => {
        const imgUrl = getMediaUrl(img);
        return `<div class="detail-thumb-modern ${i === 0 ? 'active' : ''}" onclick="changerImgDetail(this,'${imgUrl}',${i})">
                    <img src="${imgUrl}" alt="Photo ${i+1}">
                </div>`;
    }).join('');
    
    const imgUrl = getMediaUrl(p.image_principale);
    
    document.getElementById('detailContent').innerHTML = `
        <div class="detail-layout-modern">
            <div>
                <div class="detail-img-main-modern" onclick="ouvrirGalerie('${p.id}', 0)">
                    <img src="${imgUrl}" alt="${p.titre}" id="detailImgPrincipale">
                </div>
                <div class="detail-thumbs-modern">${thumbsHTML}</div>
                <div class="detail-info-modern">
                    <h2>${p.titre}</h2>
                    <div class="detail-meta-row"><i class="fas fa-map-marker-alt"></i> ${p.lieu}</div>
                    <div class="detail-meta-row"><i class="fas fa-calendar-alt"></i> Année : ${p.annee}</div>
                    <p class="detail-desc">${p.description}</p>
                </div>
            </div>
            <div class="detail-sidebar-modern">
                <div class="sidebar-card-modern">
                    <h3><i class="fas fa-hard-hat"></i> IBUCE s.a.r.l</h3>
                    <p>Expertise en topographie, construction, aménagement, hydraulique, cartographie, juridique foncier.</p>
                    <a href="https://wa.me/${whatsappNumero1}?text=Bonjour%20IBUCE,%20devis%20pour%20${encodeURIComponent(p.titre)}" 
                       class="btn-primary-full" style="text-decoration:none; margin-top:16px; display:flex;" target="_blank">
                        <i class="fab fa-whatsapp"></i> Demander un devis
                    </a>
                </div>
            </div>
        </div>
    `;
    showPage('detail');
}

function changerImgDetail(thumbEl, imgSrc, index) {
    document.getElementById('detailImgPrincipale').src = imgSrc;
    document.querySelectorAll('.detail-thumb-modern').forEach(t => t.classList.remove('active'));
    thumbEl.classList.add('active');
    galerieIndex = index;
}

function ouvrirGalerie(id, indexDep) {
    const p = projets.find(x => x.id == id);
    if (!p) return;
    galerieImages = (p.images && p.images.length ? p.images : [p.image_principale]).map(img => getMediaUrl(img));
    galerieIndex = indexDep;
    if (galerieImages.length === 0) return;
    document.getElementById('galerieImg').src = galerieImages[galerieIndex];
    document.getElementById('galerieCount').textContent = `${galerieIndex+1}/${galerieImages.length}`;
    document.getElementById('modalGalerie').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function galeriePrev() {
    if (galerieImages.length === 0) return;
    galerieIndex = (galerieIndex - 1 + galerieImages.length) % galerieImages.length;
    document.getElementById('galerieImg').src = galerieImages[galerieIndex];
    document.getElementById('galerieCount').textContent = `${galerieIndex+1}/${galerieImages.length}`;
}

function galerieNext() {
    if (galerieImages.length === 0) return;
    galerieIndex = (galerieIndex + 1) % galerieImages.length;
    document.getElementById('galerieImg').src = galerieImages[galerieIndex];
    document.getElementById('galerieCount').textContent = `${galerieIndex+1}/${galerieImages.length}`;
}

function fermerGalerie() {
    document.getElementById('modalGalerie').classList.add('hidden');
    document.body.style.overflow = '';
}

document.addEventListener('keydown', function(e) {
    const modal = document.getElementById('modalGalerie');
    if (!modal || modal.classList.contains('hidden')) return;
    if (e.key === 'ArrowRight') galerieNext();
    if (e.key === 'ArrowLeft') galeriePrev();
    if (e.key === 'Escape') fermerGalerie();
});

function envoyerContact(event) {
    event.preventDefault();
    const nom = document.getElementById('cNom').value.trim();
    const tel = document.getElementById('cTel').value.trim();
    const email = document.getElementById('cEmail').value.trim();
    const message = document.getElementById('cMessage').value.trim();
    
    if (!nom || !tel || !message) {
        afficherToast('Veuillez remplir tous les champs obligatoires', 'error');
        return;
    }
    
    const msgWA = encodeURIComponent(`Bonjour IBUCE,\n\nNom: ${nom}\nTél: ${tel}\nEmail: ${email || 'Non renseigné'}\n\nMessage: ${message}`);
    window.open(`https://wa.me/${whatsappNumero1}?text=${msgWA}`, '_blank');
    document.getElementById('contactForm').reset();
    afficherToast('Message préparé ! WhatsApp va s\'ouvrir', 'success');
}

function afficherToast(message, type) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3500);
}

document.addEventListener('DOMContentLoaded', async function() {
    await chargerProjets();
    console.log('✅ IBUCE - Site chargé');
});