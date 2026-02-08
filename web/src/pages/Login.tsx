import React, { useState } from "react";
import { api } from "../api/client";
import { setMeta, setToken } from "../auth/token";

type Props = {
  onAuthed: () => void;
};

export default function Login({ onAuthed }: Props) {
  const [tenant, setTenant] = useState("acme");
  const [email, setEmail] = useState("user1@acme.com");
  const [password, setPassword] = useState("secret12");

  const [mode, setMode] = useState<"login" | "register">("login");
  const [msg, setMsg] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function doRegister() {
    setErr(null); setMsg(null);
    const me = await api<any>({
      method: "POST",
      path: "/auth/register",
      body: { tenant_name: tenant, email, password },
      auth: false
    });
    setMsg(`Registered: ${me.email} (tenant=${me.tenant_name})`);
  }

  async function doLogin() {
    setErr(null); setMsg(null);
    const tok = await api<any>({
      method: "POST",
      path: "/auth/login",
      body: { tenant_name: tenant, email, password },
      auth: false
    });
    setToken(tok.access_token);

    const me = await api<any>({ method: "GET", path: "/auth/me", auth: true });
    setMeta({ tenant_name: me.tenant_name, email: me.email, role: me.role });

    setMsg("Logged in.");
    onAuthed();
  }

  return (
    <div className="card">
      <h2>{mode === "login" ? "Login" : "Register"}</h2>

      <div className="row">
        <div className="col">
          <label className="small">Tenant</label>
          <input value={tenant} onChange={(e) => setTenant(e.target.value)} />
        </div>
        <div className="col">
          <label className="small">Email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
      </div>

      <div className="row">
        <div className="col">
          <label className="small">Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
      </div>

      <div className="row">
        <div className="col">
          <button onClick={() => setMode(mode === "login" ? "register" : "login")}>
            Switch to {mode === "login" ? "Register" : "Login"}
          </button>
        </div>
        <div className="col">
          {mode === "login" ? (
            <button onClick={doLogin}>Login</button>
          ) : (
            <button onClick={doRegister}>Register</button>
          )}
        </div>
      </div>

      {msg && <div className="success">{msg}</div>}
      {err && <div className="error">{err}</div>}
      <div className="small" style={{ marginTop: 10, opacity: 0.8 }}>
        Note: v1 stores JWT in <code>localStorage</code> for simplicity. In production, consider HttpOnly cookies or in-memory tokens.
      </div>
    </div>
  );
}
