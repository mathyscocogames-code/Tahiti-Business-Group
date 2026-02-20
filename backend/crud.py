import json
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

import models
import schemas
from auth import get_password_hash


# ============================================================
#  USERS
# ============================================================

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, data: schemas.UserRegister) -> models.User:
    role = data.role if data.role in ("personnel", "pro") else "personnel"
    db_user = models.User(
        email=data.email,
        password_hash=get_password_hash(data.password),
        nom=data.nom,
        role=role,
        tel=data.tel,
        whatsapp=data.whatsapp,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User, data: schemas.UserUpdate) -> models.User:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user: models.User) -> models.User:
    user.is_active = False
    db.commit()
    return user


# ============================================================
#  ANNONCES
# ============================================================

def get_annonces(
    db: Session,
    categorie: Optional[str] = None,
    localisation: Optional[str] = None,
    prix_min: Optional[float] = None,
    prix_max: Optional[float] = None,
    search: Optional[str] = None,
    statut: str = "active",
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Annonce]:
    q = db.query(models.Annonce)

    if statut:
        q = q.filter(models.Annonce.statut == statut)
    if user_id is not None:
        q = q.filter(models.Annonce.user_id == user_id)
    if categorie:
        q = q.filter(models.Annonce.categorie == categorie)
    if localisation:
        q = q.filter(models.Annonce.localisation.ilike(f"%{localisation}%"))
    if prix_min is not None:
        q = q.filter(models.Annonce.prix >= prix_min)
    if prix_max is not None:
        q = q.filter(models.Annonce.prix <= prix_max)
    if search:
        term = f"%{search}%"
        q = q.filter(
            or_(
                models.Annonce.titre.ilike(term),
                models.Annonce.description.ilike(term),
            )
        )

    # Annonces boostées en premier, puis les plus récentes
    q = q.order_by(models.Annonce.boost.desc(), models.Annonce.created_at.desc())
    return q.offset(skip).limit(limit).all()


def get_annonce(db: Session, annonce_id: int) -> Optional[models.Annonce]:
    return db.query(models.Annonce).filter(models.Annonce.id == annonce_id).first()


def create_annonce(
    db: Session, data: schemas.AnnonceCreate, user_id: int
) -> models.Annonce:
    db_ann = models.Annonce(
        titre=data.titre,
        description=data.description,
        prix=data.prix,
        prix_label=data.prix_label,
        categorie=data.categorie,
        localisation=data.localisation,
        user_id=user_id,
        specs=json.dumps(data.specs or {}),
        photos="[]",
    )
    db.add(db_ann)
    db.commit()
    db.refresh(db_ann)
    return db_ann


def update_annonce(
    db: Session, annonce: models.Annonce, data: schemas.AnnonceUpdate
) -> models.Annonce:
    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "specs" and isinstance(value, dict):
            value = json.dumps(value)
        setattr(annonce, field, value)
    db.commit()
    db.refresh(annonce)
    return annonce


def delete_annonce(db: Session, annonce: models.Annonce) -> None:
    db.delete(annonce)
    db.commit()


def add_photo(db: Session, annonce: models.Annonce, photo_url: str) -> models.Annonce:
    photos = json.loads(annonce.photos or "[]")
    photos.append(photo_url)
    annonce.photos = json.dumps(photos)
    db.commit()
    db.refresh(annonce)
    return annonce


def remove_photo(db: Session, annonce: models.Annonce, photo_url: str) -> models.Annonce:
    photos = json.loads(annonce.photos or "[]")
    photos = [p for p in photos if p != photo_url]
    annonce.photos = json.dumps(photos)
    db.commit()
    db.refresh(annonce)
    return annonce


def increment_views(db: Session, annonce: models.Annonce) -> None:
    annonce.views += 1
    db.commit()


def set_boost(db: Session, annonce: models.Annonce, boost: bool) -> models.Annonce:
    annonce.boost = boost
    db.commit()
    db.refresh(annonce)
    return annonce


# ============================================================
#  MESSAGES
# ============================================================

def create_message(
    db: Session,
    annonce_id: int,
    to_user_id: int,
    data: schemas.MessageCreate,
    from_user_id: Optional[int] = None,
) -> models.Message:
    msg = models.Message(
        annonce_id=annonce_id,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        content=data.content,
        contact_email=data.contact_email,
        contact_tel=data.contact_tel,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_messages_for_user(db: Session, user_id: int) -> List[models.Message]:
    return (
        db.query(models.Message)
        .filter(models.Message.to_user_id == user_id)
        .order_by(models.Message.created_at.desc())
        .all()
    )


def get_messages_for_annonce(db: Session, annonce_id: int) -> List[models.Message]:
    return (
        db.query(models.Message)
        .filter(models.Message.annonce_id == annonce_id)
        .order_by(models.Message.created_at.desc())
        .all()
    )


def mark_message_read(db: Session, msg: models.Message) -> models.Message:
    msg.is_read = True
    db.commit()
    return msg
