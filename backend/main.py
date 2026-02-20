"""
TAHITI BUSINESS GROUPE — FastAPI Backend
Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

import io
import json
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import (
    Depends, FastAPI, File, Form, HTTPException, UploadFile, status
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from PIL import Image
from sqlalchemy.orm import Session

import auth
import crud
import models
import schemas
from database import engine, get_db

# ---- Bootstrap ----
models.Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Tahiti Business Groupe API",
    description="Plateforme d'annonces gratuites — Polynésie française",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # En prod : remplacer par le domaine exact
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================
#  HELPERS
# ============================================================

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMG_SIZE = (800, 600)


async def save_photo(upload: UploadFile, annonce_id: int) -> str:
    """Lit, redimensionne et sauvegarde une photo. Retourne l'URL relative."""
    ext = Path(upload.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Format non supporté : {ext}. Acceptés : jpg, png, webp.",
        )
    content = await upload.read()
    img = Image.open(io.BytesIO(content)).convert("RGB")
    img.thumbnail(MAX_IMG_SIZE, Image.LANCZOS)

    filename = f"{annonce_id}_{uuid.uuid4().hex[:10]}{ext}"
    filepath = UPLOAD_DIR / filename
    img.save(filepath, quality=85, optimize=True)
    return f"/static/uploads/{filename}"


def serialize_annonce(ann: models.Annonce) -> dict:
    """Convertit un objet Annonce SQLAlchemy en dict JSON-compatible."""
    return {
        "id": ann.id,
        "titre": ann.titre,
        "description": ann.description,
        "prix": ann.prix,
        "prix_label": ann.prix_label,
        "categorie": ann.categorie,
        "localisation": ann.localisation,
        "statut": ann.statut,
        "photos": json.loads(ann.photos or "[]"),
        "specs": json.loads(ann.specs or "{}"),
        "boost": ann.boost,
        "views": ann.views,
        "created_at": ann.created_at.isoformat(),
        "owner": {
            "id": ann.owner.id,
            "nom": ann.owner.nom,
            "email": ann.owner.email,
            "tel": ann.owner.tel,
            "whatsapp": ann.owner.whatsapp,
            "role": ann.owner.role,
        } if ann.owner else None,
    }


def user_dict(user: models.User) -> dict:
    return {
        "id": user.id,
        "nom": user.nom,
        "email": user.email,
        "role": user.role,
        "tel": user.tel,
        "whatsapp": user.whatsapp,
        "created_at": user.created_at.isoformat(),
    }


# ============================================================
#  AUTH ROUTES
# ============================================================

@app.post("/auth/register", response_model=schemas.TokenData, status_code=201,
          summary="Créer un compte")
def register(data: schemas.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, data.email):
        raise HTTPException(400, "Cet email est déjà utilisé.")
    user = crud.create_user(db, data)
    token = auth.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user": user_dict(user)}


@app.post("/auth/login", response_model=schemas.TokenData,
          summary="Connexion (JSON body)")
def login_json(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, data.email)
    if not user or not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Email ou mot de passe incorrect.")
    if not user.is_active:
        raise HTTPException(403, "Compte désactivé.")
    token = auth.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user": user_dict(user)}


@app.post("/auth/token", include_in_schema=False)
def login_form(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2 form endpoint — utilisé par Swagger UI."""
    user = crud.get_user_by_email(db, form.username)
    if not user or not auth.verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Identifiants invalides.")
    token = auth.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


# ============================================================
#  USER ROUTES
# ============================================================

@app.get("/me", summary="Profil utilisateur connecté")
def get_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return user_dict(current_user)


@app.put("/me", summary="Mettre à jour le profil")
def update_me(
    data: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    updated = crud.update_user(db, current_user, data)
    return user_dict(updated)


@app.get("/mes-annonces", summary="Mes annonces")
def mes_annonces(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    annonces = crud.get_annonces(db, user_id=current_user.id, statut=None)
    return [serialize_annonce(a) for a in annonces]


@app.get("/messages", summary="Mes messages reçus")
def mes_messages(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    msgs = crud.get_messages_for_user(db, current_user.id)
    return [
        {
            "id": m.id,
            "annonce_id": m.annonce_id,
            "annonce_titre": m.annonce.titre if m.annonce else "",
            "content": m.content,
            "contact_email": m.contact_email,
            "contact_tel": m.contact_tel,
            "from_user": user_dict(m.sender) if m.sender else None,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat(),
        }
        for m in msgs
    ]


# ============================================================
#  ANNONCES — ROUTES PUBLIQUES
# ============================================================

@app.get("/annonces", summary="Liste des annonces (filtrable)")
def list_annonces(
    categorie: Optional[str] = None,
    localisation: Optional[str] = None,
    prix_min: Optional[float] = None,
    prix_max: Optional[float] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    annonces = crud.get_annonces(
        db,
        categorie=categorie,
        localisation=localisation,
        prix_min=prix_min,
        prix_max=prix_max,
        search=search,
        skip=skip,
        limit=limit,
    )
    return [serialize_annonce(a) for a in annonces]


@app.get("/annonces/{annonce_id}", summary="Détail d'une annonce")
def get_annonce(annonce_id: int, db: Session = Depends(get_db)):
    ann = crud.get_annonce(db, annonce_id)
    if not ann or ann.statut not in ("active", "sold"):
        raise HTTPException(404, "Annonce introuvable.")
    crud.increment_views(db, ann)
    return serialize_annonce(ann)


# ============================================================
#  ANNONCES — ROUTES AUTHENTIFIÉES
# ============================================================

@app.post("/annonces", status_code=201, summary="Déposer une annonce (multipart/form-data)")
async def create_annonce(
    titre: str = Form(...),
    description: Optional[str] = Form(None),
    prix: Optional[float] = Form(None),
    prix_label: Optional[str] = Form(None),
    categorie: str = Form(...),
    localisation: str = Form(...),
    specs: str = Form("{}"),
    photos: List[UploadFile] = File(default=[]),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    real_photos = [p for p in photos if p.filename]
    if len(real_photos) > 5:
        raise HTTPException(400, "Maximum 5 photos par annonce.")

    try:
        specs_dict = json.loads(specs)
    except json.JSONDecodeError:
        specs_dict = {}

    ann_data = schemas.AnnonceCreate(
        titre=titre,
        description=description,
        prix=prix,
        prix_label=prix_label,
        categorie=categorie,
        localisation=localisation,
        specs=specs_dict,
    )
    annonce = crud.create_annonce(db, ann_data, current_user.id)

    for photo in real_photos:
        photo_url = await save_photo(photo, annonce.id)
        crud.add_photo(db, annonce, photo_url)

    return serialize_annonce(annonce)


@app.post("/annonces/{annonce_id}/photos", summary="Ajouter des photos à une annonce")
async def upload_photos(
    annonce_id: int,
    photos: List[UploadFile] = File(...),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    if ann.user_id != current_user.id:
        raise HTTPException(403, "Non autorisé.")

    existing = json.loads(ann.photos or "[]")
    real_photos = [p for p in photos if p.filename]
    if len(existing) + len(real_photos) > 5:
        raise HTTPException(400, f"Maximum 5 photos. Déjà {len(existing)} sur cette annonce.")

    added = []
    for photo in real_photos:
        url = await save_photo(photo, annonce_id)
        crud.add_photo(db, ann, url)
        added.append(url)

    return {"added": added, "total": len(json.loads(ann.photos))}


@app.put("/annonces/{annonce_id}", summary="Modifier une annonce")
def update_annonce(
    annonce_id: int,
    data: schemas.AnnonceUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    if ann.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Non autorisé.")
    return serialize_annonce(crud.update_annonce(db, ann, data))


@app.delete("/annonces/{annonce_id}", summary="Supprimer une annonce")
def delete_annonce(
    annonce_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    if ann.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Non autorisé.")
    crud.delete_annonce(db, ann)
    return {"success": True}


@app.post("/annonces/{annonce_id}/boost", summary="Booster une annonce (PRO)")
def boost_annonce(
    annonce_id: int,
    current_user: models.User = Depends(auth.require_pro_or_admin),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    if ann.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Non autorisé.")
    crud.set_boost(db, ann, True)
    return {"success": True, "boost": True}


# ============================================================
#  CONTACT
# ============================================================

@app.post("/annonces/{annonce_id}/contact", status_code=201,
          summary="Envoyer un message au propriétaire")
def contact_annonce(
    annonce_id: int,
    data: schemas.MessageCreate,
    current_user: Optional[models.User] = Depends(auth.get_optional_user),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann or ann.statut != "active":
        raise HTTPException(404, "Annonce introuvable.")
    if not data.content.strip():
        raise HTTPException(400, "Le message ne peut pas être vide.")

    msg = crud.create_message(
        db,
        annonce_id=annonce_id,
        to_user_id=ann.user_id,
        data=data,
        from_user_id=current_user.id if current_user else None,
    )
    return {"success": True, "message_id": msg.id}


@app.get("/annonces/{annonce_id}/messages",
         summary="Messages reçus pour une annonce (propriétaire)")
def annonce_messages(
    annonce_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    if ann.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Non autorisé.")
    msgs = crud.get_messages_for_annonce(db, annonce_id)
    return [
        {
            "id": m.id,
            "content": m.content,
            "contact_email": m.contact_email,
            "contact_tel": m.contact_tel,
            "from_user": user_dict(m.sender) if m.sender else None,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat(),
        }
        for m in msgs
    ]


# ============================================================
#  PRO STATS
# ============================================================

@app.get("/pro/stats", summary="Statistiques PRO")
def pro_stats(
    current_user: models.User = Depends(auth.require_pro_or_admin),
    db: Session = Depends(get_db),
):
    annonces = crud.get_annonces(db, user_id=current_user.id, statut=None)
    return {
        "total_annonces": len(annonces),
        "total_views": sum(a.views for a in annonces),
        "total_messages": sum(len(a.messages) for a in annonces),
        "annonces": [
            {
                "id": a.id,
                "titre": a.titre,
                "statut": a.statut,
                "views": a.views,
                "boost": a.boost,
                "messages_count": len(a.messages),
            }
            for a in annonces
        ],
    }


# ============================================================
#  ADMIN ROUTES
# ============================================================

@app.get("/admin/stats", summary="[ADMIN] Statistiques globales")
def admin_stats(
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    total_users = db.query(models.User).count()
    total_ann = db.query(models.Annonce).count()
    active_ann = db.query(models.Annonce).filter(models.Annonce.statut == "active").count()
    pending_ann = db.query(models.Annonce).filter(models.Annonce.statut == "pending").count()
    total_msgs = db.query(models.Message).count()
    return {
        "total_users": total_users,
        "total_annonces": total_ann,
        "active_annonces": active_ann,
        "pending_annonces": pending_ann,
        "total_messages": total_msgs,
    }


@app.get("/admin/annonces", summary="[ADMIN] Toutes les annonces")
def admin_list_annonces(
    statut: Optional[str] = None,
    categorie: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    annonces = crud.get_annonces(db, categorie=categorie, statut=statut, skip=skip, limit=limit)
    return [serialize_annonce(a) for a in annonces]


@app.put("/admin/annonces/{annonce_id}/statut", summary="[ADMIN] Changer le statut d'une annonce")
def admin_update_statut(
    annonce_id: int,
    statut: str,
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    allowed = ("active", "pending", "rejected", "sold")
    if statut not in allowed:
        raise HTTPException(400, f"Statut invalide. Valeurs : {allowed}")
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    crud.update_annonce(db, ann, schemas.AnnonceUpdate(statut=statut))
    return {"success": True, "statut": statut}


@app.delete("/admin/annonces/{annonce_id}", summary="[ADMIN] Supprimer une annonce")
def admin_delete_annonce(
    annonce_id: int,
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    ann = crud.get_annonce(db, annonce_id)
    if not ann:
        raise HTTPException(404, "Annonce introuvable.")
    crud.delete_annonce(db, ann)
    return {"success": True}


@app.get("/admin/users", summary="[ADMIN] Liste des utilisateurs")
def admin_list_users(
    skip: int = 0,
    limit: int = 100,
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return [user_dict(u) for u in users]


@app.put("/admin/users/{user_id}/role", summary="[ADMIN] Changer le rôle d'un utilisateur")
def admin_update_role(
    user_id: int,
    role: str,
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    allowed = ("personnel", "pro", "admin")
    if role not in allowed:
        raise HTTPException(400, f"Rôle invalide. Valeurs : {allowed}")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur introuvable.")
    user.role = role
    db.commit()
    return {"success": True, "role": role}


@app.delete("/admin/users/{user_id}", summary="[ADMIN] Désactiver un utilisateur")
def admin_deactivate_user(
    user_id: int,
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur introuvable.")
    crud.deactivate_user(db, user)
    return {"success": True}


# ============================================================
#  HEALTH CHECK
# ============================================================

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "app": "Tahiti Business Groupe API", "version": "1.0.0"}
