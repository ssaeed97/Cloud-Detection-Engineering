const TOKEN_KEY = "cdl_token";
const META_KEY = "cdl_meta"; // stores tenant/email/role for UI convenience

export type SessionMeta = {
  tenant_name: string;
  email: string;
  role: string;
};

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(META_KEY);
}

export function setMeta(meta: SessionMeta) {
  localStorage.setItem(META_KEY, JSON.stringify(meta));
}

export function getMeta(): SessionMeta | null {
  const raw = localStorage.getItem(META_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as SessionMeta;
  } catch {
    return null;
  }
}
