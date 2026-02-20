from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id           = Column(Integer, primary_key=True, index=True)
    email        = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role         = Column(String, default="personnel")   # personnel | pro | admin
    nom          = Column(String, nullable=False)
    tel          = Column(String, nullable=True)
    whatsapp     = Column(String, nullable=True)
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    annonces         = relationship("Annonce", back_populates="owner", cascade="all, delete")
    messages_sent    = relationship("Message", foreign_keys="Message.from_user_id", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="Message.to_user_id", back_populates="recipient")


class Annonce(Base):
    __tablename__ = "annonces"

    id           = Column(Integer, primary_key=True, index=True)
    titre        = Column(String, nullable=False)
    description  = Column(Text, nullable=True)
    prix         = Column(Float, nullable=True)          # valeur numérique (XPF)
    prix_label   = Column(String, nullable=True)         # "180 000 XPF/mois", "Sur devis"...
    categorie    = Column(String, nullable=False)        # immobilier | vehicules | emploi | vente-privee | nouveautes | promo
    localisation = Column(String, nullable=False)
    user_id      = Column(Integer, ForeignKey("users.id"))
    statut       = Column(String, default="active")     # active | pending | rejected | sold
    photos       = Column(Text, default="[]")            # JSON array of URL paths
    specs        = Column(Text, default="{}")            # JSON dict of characteristics
    boost        = Column(Boolean, default=False)        # PRO boost — shown first
    views        = Column(Integer, default=0)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner    = relationship("User", back_populates="annonces")
    messages = relationship("Message", back_populates="annonce", cascade="all, delete")


class Message(Base):
    __tablename__ = "messages"

    id            = Column(Integer, primary_key=True, index=True)
    annonce_id    = Column(Integer, ForeignKey("annonces.id"))
    from_user_id  = Column(Integer, ForeignKey("users.id"), nullable=True)  # null = visiteur anonyme
    to_user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    content       = Column(Text, nullable=False)
    contact_email = Column(String, nullable=True)   # pour visiteurs non-connectés
    contact_tel   = Column(String, nullable=True)
    is_read       = Column(Boolean, default=False)
    created_at    = Column(DateTime, default=datetime.utcnow)

    annonce   = relationship("Annonce", back_populates="messages")
    sender    = relationship("User", foreign_keys=[from_user_id], back_populates="messages_sent")
    recipient = relationship("User", foreign_keys=[to_user_id], back_populates="messages_received")
