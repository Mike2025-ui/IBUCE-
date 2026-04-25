/* ============================================================
   IBUCE s.a.r.l – SCRIPT PRINCIPAL
   ============================================================ */

let projets = [];
let projetActif = null;
let galerieImages = [];
let galerieIndex = 0;
let whatsappNumero1 = "2250757090714";
let whatsappNumero2 = "2250574002019";

const projetsStatiques = [
    {
        id: "1",
        titre: "Projet Bingerville",
        lieu: "Bingerville, Côte d'Ivoire",
        description: "Aménagement de voirie et lotissement résidentiel de grand standing. Travaux de topographie et construction de routes d'accès.",
        annee: "2024",
        categorie: "amenagement",
        image_principale: "/static/annonces/images/projet_bingerville.jpg",
        images: ["/static/annonces/images/projet_bingerville.jpg"]
    },
    {
        id: "2",
        titre: "Résidence Kitty – Bouaké 2023",
        lieu: "Bouaké, Côte d'Ivoire",
        description: "Construction d'une résidence moderne avec aménagements extérieurs, voiries et réseaux divers.",
        annee: "2023",
        categorie: "construction",
        image_principale: "/static/annonces/images/projet_bouake2023.jpg",
        images: ["/static/annonces/images/projet_bouake2023.jpg"]
    },
    {
        id: "3",
        titre: "Villa 3P – Songon 2023",
        lieu: "Songon, Côte d'Ivoire",
        description: "Construction d'une villa de 3 pièces avec finitions haut de gamme.",
        annee: "2023",
        categorie: "construction",
        image_principale: "/static/annonces/images/projet_songon2023.jpg",
        images: ["/static/annonces/images/projet_songon2023.jpg"]
    },
    {
        id: "4",
        titre: "Centre Commercial",
        lieu: "Abidjan, Côte d'Ivoire",
        description: "Construction d'un centre commercial moderne avec parking et aménagements extérieurs.",
        annee: "2024",
        categorie: "construction",
        image_principale: "/static/annonces/images/projet_centre_commercial.jpg",
        images: ["/static/annonces/images/projet_centre_commercial.jpg"]
    },
    {
        id: "5",
        titre: "Supermarché – Yakro",
        lieu: "Yamoussoukro, Côte d'Ivoire",
        description: "Construction d'un supermarché de grande surface avec zones de stationnement.",
        annee: "2023",
        categorie: "construction",
        image_principale: "/static/annonces/images/projet_supermaket3.jpg",
        images: ["/static/annonces/images/projet_supermaket3.jpg"]
    },
    {
        id: "6",
        titre: "Projet Supermarché",
        lieu: "Abidjan, Côte d'Ivoire",
        description: "Aménagement et construction d'un supermarché avec voiries et réseaux.",
        annee: "2023",
        categorie: "construction",
        image_principale: "/static/annonces/images/projet_supermarket.jpg",
        images: ["/static/annonces/images/projet_supermarket.jpg"]
    },
    {
        id: "7",
        titre: "Terrain – Action 4",
        lieu: "Abidjan, Côte d'Ivoire",
        description: "Travaux de topographie et aménagement de terrain. Relevés précis et bornage.",
        annee: "2024",
        categorie: "topographie",
        image_principale: "/static/annonces/images/action_terrain4.jpg",
        images: ["/static/annonces/images/action_terrain4.jpg"]
    },
    {
        id: "8",
        titre: "Terrain – Action 6",
        lieu: "Abidjan, Côte d'Ivoire",
        description: "Relevés topographiques et étude de sol pour projet de construction.",
        annee: "2024",
        categorie: "topographie",
        image_principale: "/static/annonces/images/actionterrain6.jpg",
        images: ["/static/annonces/images/actionterrain6.jpg"]
    }
];

function getMediaUrl(path) {
    if (!path) return 'https://via.placeholder.com/400x240?text=IBUCE';
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

function retourProjets() {
    showPage('projets');
}

async function chargerProjets() {
    projets = [...projetsStatiques];
    renderRealisationsAccueil();
    renderRealisationsFull();
    if (document.getElementById('adminList')) renderAdminList();
    console.log('✅ IBUCE - Projets chargés');
}

function creerCarteRealisation(p) {
    const imgUrl = getMediaUrl(p.image_principale);
    return `
        <div class="realisation-card" onclick="voirDetail('${p.id}')">
            <div class="card-img">
                <img src="${imgUrl}" alt="${p.titre}" onerror="this.src='https://via.placeholder.com/400x240?text=IBUCE'">
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
    
    const imagesListe = p.images || [p.image_principale];
    const thumbsHTML = imagesListe.map((img, i) => {
        const imgUrl = getMediaUrl(img);
        return `
            <div class="detail-thumb-modern ${i === 0 ? 'active' : ''}" onclick="changerImgDetail(this,'${imgUrl}',${i})">
                <img src="${imgUrl}" alt="Photo ${i+1}">
            </div>
        `;
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
                    <div class="detail-meta-row"><i class="fas fa-tag"></i> Catégorie : ${p.categorie}</div>
                    <p class="detail-desc">${p.description}</p>
                </div>
            </div>
            <div class="detail-sidebar-modern">
                <div class="sidebar-card-modern">
                    <h3><i class="fas fa-hard-hat"></i> IBUCE s.a.r.l</h3>
                    <p>Expertise en topographie, construction, aménagement, forage, transit et vente d'appareils topographiques. Devis gratuit sur demande.</p>
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
    galerieImages = (p.images || [p.image_principale]).map(img => getMediaUrl(img));
    galerieIndex = indexDep;
    document.getElementById('galerieImg').src = galerieImages[galerieIndex];
    document.getElementById('galerieCount').textContent = `${galerieIndex+1}/${galerieImages.length}`;
    document.getElementById('modalGalerie').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function galeriePrev() {
    galerieIndex = (galerieIndex - 1 + galerieImages.length) % galerieImages.length;
    document.getElementById('galerieImg').src = galerieImages[galerieIndex];
    document.getElementById('galerieCount').textContent = `${galerieIndex+1}/${galerieImages.length}`;
}

function galerieNext() {
    galerieIndex = (galerieIndex + 1) % galerieImages.length;
    document.getElementById('galerieImg').src = galerieImages[galerieIndex];
    document.getElementById('galerieCount').textContent = `${galerieIndex+1}/${galerieImages.length}`;
}

function fermerGalerie() {
    document.getElementById('modalGalerie').classList.add('hidden');
    document.body.style.overflow = '';
}

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
    
    const msgWA = encodeURIComponent(
        `Bonjour IBUCE s.a.r.l,\n\nNom: ${nom}\nTél: ${tel}\nEmail: ${email || 'Non renseigné'}\n\nMessage: ${message}`
    );
    
    const lienWA = `https://wa.me/${whatsappNumero1}?text=${msgWA}`;
    window.open(lienWA, '_blank');
    document.getElementById('contactForm').reset();
    afficherToast('Message préparé ! WhatsApp va s\'ouvrir', 'success');
}

function ajouterProjet(event) {
    event.preventDefault();
    const newId = String(projets.length + 1);
    const nouveauProjet = {
        id: newId,
        titre: document.getElementById('aTitle').value.trim(),
        lieu: document.getElementById('aLieu').value.trim(),
        annee: document.getElementById('aAnnee').value.trim(),
        categorie: document.getElementById('aCategorie').value,
        description: document.getElementById('aDesc').value.trim(),
        image_principale: '/static/annonces/images/placeholder.jpg',
        images: ['/static/annonces/images/placeholder.jpg']
    };
    
    const imgFile = document.getElementById('aImgMain').files[0];
    if (imgFile) {
        nouveauProjet.image_principale = URL.createObjectURL(imgFile);
        nouveauProjet.images = [URL.createObjectURL(imgFile)];
    }
    
    projets.push(nouveauProjet);
    renderRealisationsAccueil();
    renderRealisationsFull();
    renderAdminList();
    document.getElementById('adminForm').reset();
    afficherToast('Projet ajouté avec succès', 'success');
}

function renderAdminList() {
    const list = document.getElementById('adminList');
    if (!list) return;
    document.getElementById('nbProjets').textContent = projets.length;
    
    if (projets.length === 0) {
        list.innerHTML = '<p style="text-align:center;color:var(--gray-mid);padding:20px">Aucune réalisation</p>';
        return;
    }
    
    list.innerHTML = projets.map(p => `
        <div class="admin-row-modern">
            <img src="${getMediaUrl(p.image_principale)}" alt="${p.titre}">
            <div class="admin-info">
                <strong>#${p.id} – ${p.titre}</strong>
                <span>${p.lieu} · ${p.annee}</span>
            </div>
            <button class="btn-edit-modern" onclick="ouvrirEditProjet('${p.id}')"><i class="fas fa-edit"></i> Modifier</button>
            <button class="btn-suppr-modern" onclick="supprimerProjet('${p.id}')"><i class="fas fa-trash"></i> Supprimer</button>
        </div>
    `).join('');
}

function ouvrirEditProjet(id) {
    const p = projets.find(x => x.id == id);
    if (!p) return;
    document.getElementById('editId').value = p.id;
    document.getElementById('editTitre').value = p.titre;
    document.getElementById('editLieu').value = p.lieu;
    document.getElementById('editAnnee').value = p.annee;
    document.getElementById('editCategorie').value = p.categorie;
    document.getElementById('editDescription').value = p.description;
    document.getElementById('modalEditProjet').classList.remove('hidden');
}

function fermerEditProjet() {
    document.getElementById('modalEditProjet').classList.add('hidden');
}

function soumettreEditProjet(event) {
    event.preventDefault();
    const id = document.getElementById('editId').value;
    const index = projets.findIndex(x => x.id == id);
    
    if (index !== -1) {
        projets[index].titre = document.getElementById('editTitre').value;
        projets[index].lieu = document.getElementById('editLieu').value;
        projets[index].annee = document.getElementById('editAnnee').value;
        projets[index].categorie = document.getElementById('editCategorie').value;
        projets[index].description = document.getElementById('editDescription').value;
        
        const imgFile = document.getElementById('editImgPrincipale').files[0];
        if (imgFile) {
            projets[index].image_principale = URL.createObjectURL(imgFile);
            projets[index].images = [URL.createObjectURL(imgFile)];
        }
        
        renderRealisationsAccueil();
        renderRealisationsFull();
        renderAdminList();
        fermerEditProjet();
        afficherToast('Projet modifié avec succès', 'success');
    }
}

function supprimerProjet(id) {
    if (!confirm('Supprimer définitivement cette réalisation ?')) return;
    const index = projets.findIndex(x => x.id == id);
    if (index !== -1) {
        projets.splice(index, 1);
        renderRealisationsAccueil();
        renderRealisationsFull();
        renderAdminList();
        afficherToast('Projet supprimé avec succès', 'success');
    }
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
    console.log('✅ IBUCE s.a.r.l - Site chargé avec succès');
});

document.addEventListener('keydown', function(e) {
    const modal = document.getElementById('modalGalerie');
    if (modal.classList.contains('hidden')) return;
    if (e.key === 'ArrowRight') galerieNext();
    if (e.key === 'ArrowLeft') galeriePrev();
    if (e.key === 'Escape') fermerGalerie();
});