import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session

from settings import settings
from db import Base, engine, get_db
from models import Tenant, User, Note, FileObject
from schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserMeResponse,
    NoteCreateRequest,
    NoteResponse,
    FileMetaResponse,
)
from auth import hash_password, verify_password, create_access_token, get_auth_context, require_admin, AuthContext
from logging_utils import get_logger, json_log, RequestContextMiddleware

logger = get_logger("cloud_detection_app")

app = FastAPI(title="Cloud Detection Lab App", version="1.0.0")

# Middleware for request_id + structured request logs
app.add_middleware(RequestContextMiddleware, logger=logger)


@app.on_event("startup")
def on_startup():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Ensure upload dir exists
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)

    # Optional bootstrap admin (only if env vars set)
    if settings.bootstrap_admin_email and settings.bootstrap_admin_password:
        with next(get_db()) as db:
            tenant = db.query(Tenant).filter(Tenant.name == "bootstrap").first()
            if not tenant:
                tenant = Tenant(name="bootstrap")
                db.add(tenant)
                db.commit()
                db.refresh(tenant)

            existing = db.query(User).filter(User.tenant_id == tenant.id, User.email == settings.bootstrap_admin_email).first()
            if not existing:
                admin = User(
                    tenant_id=tenant.id,
                    email=settings.bootstrap_admin_email,
                    password_hash=hash_password(settings.bootstrap_admin_password),
                    role="admin",
                )
                db.add(admin)
                db.commit()
                json_log(logger, "bootstrap_admin_created", tenant_id=tenant.id, email=admin.email)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/register", response_model=UserMeResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db), request: Request = None):
    # Tenant create/get
    tenant = db.query(Tenant).filter(Tenant.name == req.tenant_name).first()
    if not tenant:
        tenant = Tenant(name=req.tenant_name)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    # Prevent duplicate email within same tenant
    existing = db.query(User).filter(User.tenant_id == tenant.id, User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(
        tenant_id=tenant.id,
        email=req.email,
        password_hash=hash_password(req.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    json_log(
        logger,
        "user_registered",
        request_id=getattr(request.state, "request_id", None),
        tenant_id=tenant.id,
        tenant_name=tenant.name,
        user_id=user.id,
        email=user.email,
    )

    return UserMeResponse(
        user_id=user.id,
        tenant_id=tenant.id,
        tenant_name=tenant.name,
        email=user.email,
        role=user.role,
    )


@app.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db), request: Request = None):
    tenant = db.query(Tenant).filter(Tenant.name == req.tenant_name).first()
    if not tenant:
        # detection-friendly (optional) verbose errors
        reason = "tenant_not_found"
        json_log(logger, "auth_login_failed", request_id=getattr(request.state, "request_id", None), tenant_name=req.tenant_name, email=req.email, reason=reason)
        if settings.verbose_auth_errors:
            raise HTTPException(status_code=401, detail="Tenant not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.query(User).filter(User.tenant_id == tenant.id, User.email == req.email).first()
    if not user:
        reason = "user_not_found"
        json_log(logger, "auth_login_failed", request_id=getattr(request.state, "request_id", None), tenant_id=tenant.id, tenant_name=tenant.name, email=req.email, reason=reason)
        if settings.verbose_auth_errors:
            raise HTTPException(status_code=401, detail="User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(req.password, user.password_hash):
        reason = "wrong_password"
        json_log(logger, "auth_login_failed", request_id=getattr(request.state, "request_id", None), tenant_id=tenant.id, tenant_name=tenant.name, user_id=user.id, email=user.email, reason=reason)
        if settings.verbose_auth_errors:
            raise HTTPException(status_code=401, detail="Wrong password")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id=user.id, tenant_id=tenant.id, role=user.role)

    json_log(
        logger,
        "auth_login_success",
        request_id=getattr(request.state, "request_id", None),
        tenant_id=tenant.id,
        tenant_name=tenant.name,
        user_id=user.id,
        email=user.email,
        role=user.role,
    )

    return TokenResponse(access_token=token, expires_in_minutes=settings.jwt_exp_minutes)


@app.get("/auth/me", response_model=UserMeResponse)
def me(ctx: AuthContext = Depends(get_auth_context)):
    return UserMeResponse(
        user_id=ctx.user.id,
        tenant_id=ctx.tenant.id,
        tenant_name=ctx.tenant.name,
        email=ctx.user.email,
        role=ctx.user.role,
    )


@app.post("/notes", response_model=NoteResponse)
def create_note(req: NoteCreateRequest, ctx: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db), request: Request = None):
    note = Note(tenant_id=ctx.tenant.id, owner_user_id=ctx.user.id, title=req.title, body=req.body)
    db.add(note)
    db.commit()
    db.refresh(note)

    json_log(logger, "note_created", request_id=getattr(request.state, "request_id", None), tenant_id=ctx.tenant.id, user_id=ctx.user.id, note_id=note.id)
    return NoteResponse(id=note.id, tenant_id=note.tenant_id, owner_user_id=note.owner_user_id, title=note.title, body=note.body)


@app.get("/notes", response_model=list[NoteResponse])
def list_notes(ctx: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.tenant_id == ctx.tenant.id).order_by(Note.id.desc()).all()
    return [NoteResponse(id=n.id, tenant_id=n.tenant_id, owner_user_id=n.owner_user_id, title=n.title, body=n.body) for n in notes]


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    legacy: Optional[bool] = None,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
    request: Request = None,
):
    """
    Vulnerable-by-design toggle:
      - If legacy_insecure_tenant_mode is enabled AND client passes ?legacy=true,
        tenant scoping is NOT enforced (simulates an IDOR/multi-tenant scoping bug).
    """
    use_legacy = bool(legacy) and settings.legacy_insecure_tenant_mode

    if use_legacy:
        note = db.query(Note).filter(Note.id == note_id).first()
        json_log(
            logger,
            "legacy_tenant_bypass_used",
            request_id=getattr(request.state, "request_id", None),
            note_id=note_id,
            caller_tenant_id=ctx.tenant.id,
            caller_user_id=ctx.user.id,
        )
    else:
        note = db.query(Note).filter(Note.id == note_id, Note.tenant_id == ctx.tenant.id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Detection hook: log tenant mismatch if legacy bypass returns a cross-tenant object
    if use_legacy and note.tenant_id != ctx.tenant.id:
        json_log(
            logger,
            "cross_tenant_access_detected",
            request_id=getattr(request.state, "request_id", None),
            note_id=note.id,
            note_tenant_id=note.tenant_id,
            caller_tenant_id=ctx.tenant.id,
            caller_user_id=ctx.user.id,
        )

    return NoteResponse(id=note.id, tenant_id=note.tenant_id, owner_user_id=note.owner_user_id, title=note.title, body=note.body)


@app.post("/files/upload", response_model=FileMetaResponse)
def upload_file(
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
    request: Request = None,
    up: UploadFile = File(...),
):
    # size control (best-effort: relies on reading the file)
    max_bytes = settings.max_upload_mb * 1024 * 1024

    data = up.file.read()
    size = len(data)
    if size > max_bytes:
        json_log(logger, "file_upload_rejected", request_id=getattr(request.state, "request_id", None), tenant_id=ctx.tenant.id, user_id=ctx.user.id, filename=up.filename, size_bytes=size, reason="too_large")
        raise HTTPException(status_code=413, detail="File too large")

    safe_name = os.path.basename(up.filename or "upload.bin")
    stored_path = str(Path(settings.upload_dir) / f"t{ctx.tenant.id}_u{ctx.user.id}_{safe_name}")

    with open(stored_path, "wb") as f:
        f.write(data)

    obj = FileObject(
        tenant_id=ctx.tenant.id,
        owner_user_id=ctx.user.id,
        filename=safe_name,
        content_type=up.content_type or "application/octet-stream",
        size_bytes=size,
        stored_path=stored_path,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    json_log(
        logger,
        "file_uploaded",
        request_id=getattr(request.state, "request_id", None),
        tenant_id=ctx.tenant.id,
        user_id=ctx.user.id,
        file_id=obj.id,
        filename=obj.filename,
        content_type=obj.content_type,
        size_bytes=obj.size_bytes,
    )

    return FileMetaResponse(
        id=obj.id,
        tenant_id=obj.tenant_id,
        owner_user_id=obj.owner_user_id,
        filename=obj.filename,
        content_type=obj.content_type,
        size_bytes=obj.size_bytes,
    )


@app.get("/files/{file_id}/meta", response_model=FileMetaResponse)
def file_meta(file_id: int, ctx: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db), request: Request = None):
    obj = db.query(FileObject).filter(FileObject.id == file_id, FileObject.tenant_id == ctx.tenant.id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="File not found")

    return FileMetaResponse(
        id=obj.id,
        tenant_id=obj.tenant_id,
        owner_user_id=obj.owner_user_id,
        filename=obj.filename,
        content_type=obj.content_type,
        size_bytes=obj.size_bytes,
    )


@app.get("/admin/stats")
def admin_stats(ctx: AuthContext = Depends(require_admin), db: Session = Depends(get_db), request: Request = None):
    # minimal stats (good for "rare endpoint" and authz detection)
    tenant_count = db.query(Tenant).count()
    user_count = db.query(User).count()
    note_count = db.query(Note).count()
    file_count = db.query(FileObject).count()

    json_log(
        logger,
        "admin_stats_accessed",
        request_id=getattr(request.state, "request_id", None),
        admin_user_id=ctx.user.id,
        admin_tenant_id=ctx.tenant.id,
    )

    return {
        "tenants": tenant_count,
        "users": user_count,
        "notes": note_count,
        "files": file_count,
    }
