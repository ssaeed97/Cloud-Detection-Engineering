import React, { useMemo } from "react";
import { getMeta, getToken } from "../auth/token";

type Props = {
  onLogout: () => void;
};

function base64UrlDecode(input: string): string {
  // Convert base64url -> base64
  const base64 = input.replace(/-/g, "+").replace(/_/g, "/");
  // Pad with '='
  const padded = base64 + "===".slice((base64.length + 3) % 4);
  return atob(padded);
}

function decodeJwtPayload(token: string): any | null {
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const json = base64UrlDecode(parts[1]);
    return JSON.parse(json);
  } catch {
    return null;
  }
}


export default function SessionInspector({ onLogout }: Props) {
  const meta = getMeta();
  const token = getToken();

  const payload = token ? decodeJwtPayload(token) : null;

  const expText = useMemo(() => {
    const exp = payload?.exp;
    if (!exp) return "(no exp claim)";
    const expMs = exp * 1000;
    const expDate = new Date(expMs);
    const minsLeft = Math.floor((expMs - Date.now()) / 60000);
    return `${expDate.toLocaleString()} (${minsLeft} min left)`;
  }, [payload]);

  const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const headerPreview = useMemo(() => {
    return {
      "X-Client": "react-v1",
      "Authorization": token ? `Bearer ${token.slice(0, 16)}...` : "(none)"
    };
  }, [token]);

  return (
    <div className="card">
      <h3>Session Inspector</h3>

      <div className="small">API Base: {apiBase}</div>

      <div style={{ marginTop: 10 }}>
        <div className="small">Token: {token ? "present" : "missing"}</div>
        <div className="small">
          User: {meta ? `${meta.tenant_name} · ${meta.email} · ${meta.role}` : "(none)"}
        </div>
      </div>
      <div className="small">JWT exp: {payload ? expText : "(no token)"}</div>
      <div className="small">JWT iat: {payload?.iat ? new Date(payload.iat * 1000).toLocaleString() : "(no iat)"}</div>


      <div style={{ marginTop: 10 }}>
        <div className="small">Header preview:</div>
        <pre style={{ overflowX: "auto" }}>{JSON.stringify(headerPreview, null, 2)}</pre>
      </div>

      <button
        style={{ marginTop: 10 }}
        onClick={onLogout}
        disabled={!token}
      >
        Clear session (logout)
      </button>
    </div>
  );
}
