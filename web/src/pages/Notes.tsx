import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { Guard } from "../components/Guard";

type Note = { id: number; title: string; body: string; tenant_id: number; owner_user_id: number };

export default function Notes() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState("hello");
  const [body, setBody] = useState("world");
  const [err, setErr] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [useLegacy, setUseLegacy] = useState(false);


  async function refresh() {
    setErr(null);
    const data = await api<Note[]>({ method: "GET", path: "/notes", auth: true });
    setNotes(data);
  }

  async function create() {
    setErr(null); setMsg(null);
    const n = await api<Note>({ method: "POST", path: "/notes", body: { title, body }, auth: true }); 
    setMsg(`Created note id=${n.id}`);
    await refresh();
  }

  useEffect(() => { refresh().catch(e => setErr(e.message)); }, []);

  return (
    <Guard>
      <div className="card">
        <h2>Notes</h2>

        <div className="row">
          <div className="col">
            <label className="small">Title</label>
            <input value={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div className="col">
            <label className="small">Body</label>
            <textarea value={body} onChange={(e) => setBody(e.target.value)} />
          </div>
        </div>

        <div className="row">
          <div className="col"><button onClick={create}>Create note</button></div>
          <div className="col"><button onClick={refresh}>Refresh</button></div>
        </div>

        {msg && <div className="success">{msg}</div>}
        {err && <div className="error">{err}</div>}
      </div>

      <div className="card">
        <h3>Recent notes</h3>
        {showDetails && selectedId !== null && (
          <div className="card">
            <div className="row">
              <div className="col">
                {/* <div className="small">Selected note id: {selectedId}</div> */}
                <div className="small">Selected note ID: {selectedId} </div>
                <div className="small"> Tenant ID: {notes.find(n => n.id === selectedId)?.tenant_id} </div>
                <div className="small"> Owner ID:{notes.find(n => n.id === selectedId)?.owner_user_id}</div>
              </div>
              <div className="col">
                <button onClick={() => setShowDetails(false)}>Close details</button>
              </div>
            </div>

            <label className="small">
              <input
                type="checkbox"
                checked={useLegacy}
                onChange={(e) => setUseLegacy(e.target.checked)}
              />
              Use legacy mode
            </label>
          </div>
        )}
        {notes.length === 0 ? (
          <div className="small">No notes yet.</div>
        ) : (
          notes.map((n) => (
            <div key={n.id} className="card" style={{ background: "#0f1626" }}>
              {/* <div className="small">id={n.id} tenant={n.tenant_id} owner={n.owner_user_id}</div> */}
              <div style={{ fontWeight: 600 }}>{n.title}</div>
              <div style={{ opacity: 0.9 }}>{n.body}</div>
              <button
                onClick={() => {
                  setSelectedId(n.id);
                  setShowDetails(true);
                }}
              >
                View details
              </button>

            </div>
          ))
        )}
      </div>
    </Guard>
  );
}
