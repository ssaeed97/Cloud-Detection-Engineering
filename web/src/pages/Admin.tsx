import React, { useState } from "react";
import { Guard } from "../components/Guard";
import { api } from "../api/client";
import { getMeta } from "../auth/token";

export default function Admin() {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);
  const meta = getMeta();

  async function fetchStats() {
    setErr(null); setData(null);
    try {
      const res = await api<any>({ method: "GET", path: "/admin/stats", auth: true });
      setData(res);
    } catch (e: any) {
      setErr(e.message || "Failed");
    }
  }

  return (
    <Guard>
      <div className="card">
        <h2>Admin</h2>
        <div className="small" style={{ marginBottom: 8 }}>
          If you are not admin, this should 403 — useful for detection signals.
        </div>
        <div className="small" style={{ marginBottom: 12 }}>
          Current role: <span className="badge">{meta?.role ?? "unknown"}</span>
        </div>

        <button onClick={fetchStats}>Fetch /admin/stats</button>

        {err && <div className="error" style={{ marginTop: 10 }}>{err}</div>}
        {data && (
          <div className="card" style={{ background: "#0f1626", marginTop: 10 }}>
            <pre style={{ overflowX: "auto" }}>{JSON.stringify(data, null, 2)}</pre>
          </div>
        )}
      </div>
    </Guard>
  );
}
