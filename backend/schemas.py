from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================
#  AUTH
# ============================================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    nom: str
    role: str = "personnel"     # personnel | pro
    tel: Optional[str] = None
    whatsapp: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


# ============================================================
#  USER
# ============================================================

class UserOut(BaseModel):
    id: int
    email: str
    nom: str
    role: str
    tel: Optional[str] = None
    whatsapp: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    tel: Optional[str] = None
    whatsapp: Optional[str] = None


# ============================================================
#  ANNONCE
# ============================================================

class AnnonceCreate(BaseModel):
    titre: str
    description: Optional[str] = None
    prix: Optional[float] = None
    prix_label: Optional[str] = None
    categorie: str
    localisation: str
    specs: Optional[Dict[str, str]] = {}


class AnnonceUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[float] = None
    prix_label: Optional[str] = None
    localisation: Optional[str] = None
    statut: Optional[str] = None
    specs: Optional[Dict[str, str]] = None
    boost: Optional[bool] = None


class AnnonceOut(BaseModel):
    id: int
    titre: str
    description: Optional[str] = None
    prix: Optional[float] = None
    prix_label: Optional[str] = None
    categorie: str
    localisation: str
    statut: str
    photos: List[str] = []
    specs: Dict[str, str] = {}
    boost: bool
    views: int
    created_at: datetime
    owner: Optional[UserOut] = None

    model_config = {"from_attributes": True}


# ============================================================
#  MESSAGE
# ============================================================

class MessageCreate(BaseModel):
    content: str
    contact_email: Optional[str] = None
    contact_tel: Optional[str] = None


class MessageOut(BaseModel):
    id: int
    annonce_id: int
    content: str
    contact_email: Optional[str] = None
    contact_tel: Optional[str] = None
    is_read: bool
    created_at: datetime
    from_user_id: Optional[int] = None

    model_config = {"from_attributes": True}


# ============================================================
#  ADMIN STATS
# ============================================================

class AdminStats(BaseModel):
    total_users: int
    total_annonces: int
    active_annonces: int
    pending_annonces: int
    total_messages: int
