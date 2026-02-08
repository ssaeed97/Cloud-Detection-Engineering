from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    tenant_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    tenant_name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class UserMeResponse(BaseModel):
    user_id: int
    tenant_id: int
    tenant_name: str
    email: EmailStr
    role: str


class NoteCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=20000)


class NoteResponse(BaseModel):
    id: int
    tenant_id: int
    owner_user_id: int
    title: str
    body: str


class FileMetaResponse(BaseModel):
    id: int
    tenant_id: int
    owner_user_id: int
    filename: str
    content_type: str
    size_bytes: int
