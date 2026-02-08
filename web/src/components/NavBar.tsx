import React from "react";
import { clearToken, getMeta } from "../auth/token";

type Props = {
  route: string;
  setRoute: (r: string) => void;
  onLogout: () => void;
};

export default function NavBar({ route, setRoute, onLogout }: Props) {
  const meta = getMeta();

  return (
    <div className="nav">
      <div className="links">
        <span className="badge">Cloud Detection Lab</span>
        <a href="#" onClick={(e) => { e.preventDefault(); setRoute("login"); }} style={{ opacity: route==="login" ? 1 : 0.75 }}>Login</a>
        <a href="#" onClick={(e) => { e.preventDefault(); setRoute("notes"); }} style={{ opacity: route==="notes" ? 1 : 0.75 }}>Notes</a>
        <a href="#" onClick={(e) => { e.preventDefault(); setRoute("upload"); }} style={{ opacity: route==="upload" ? 1 : 0.75 }}>Upload</a>
        <a href="#" onClick={(e) => { e.preventDefault(); setRoute("admin"); }} style={{ opacity: route==="admin" ? 1 : 0.75 }}>Admin</a>
      </div>

      <div className="links">
        {meta ? (
          <>
            <span className="small">{meta.tenant_name} · {meta.email} · {meta.role}</span>
            <button
              style={{ width: "auto" }}
              onClick={() => {
                clearToken();
                onLogout();
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <span className="small">Not logged in</span>
        )}
      </div>
    </div>
  );
}
