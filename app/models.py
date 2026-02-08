from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="tenant")
    notes = relationship("Note", back_populates="tenant")
    files = relationship("FileObject", back_populates="tenant")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # "user" or "admin"
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", back_populates="users")
    notes = relationship("Note", back_populates="owner")
    files = relationship("FileObject", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", back_populates="notes")
    owner = relationship("User", back_populates="notes")


class FileObject(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(120), nullable=False, default="application/octet-stream")
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stored_path: Mapped[str] = mapped_column(String(500), nullable=False)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", back_populates="files")
    owner = relationship("User", back_populates="files")
