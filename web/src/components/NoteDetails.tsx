import React, { useEffect, useState } from "react";
import { api } from "../api/client";

type Note = {
  id: number;
  title: string;
  body: string;
  tenant_id: number;
  owner_user_id: number;
};

type Props = {
  noteId: number;
  useLegacy: boolean;
  onClose: () => void;
};

export default function NoteDetails({ noteId, useLegacy, onClose }: Props) {
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [note, setNote] = useState<Note | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setErr(null);
      try {
        const path = useLegacy ? `/notes/${noteId}?legacy=true` : `/notes/${noteId}`;
        const res = await api<Note>({ method: "GET", path, auth: true });
        if (!cancelled) setNote(res);
      } catch (e: any) {
        if (!cancelled) setErr(e.message ?? "Failed to load note");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [noteId, useLegacy]);

  return (
    <div className="card" style={{ background: "#0f1626", marginTop: 12 }}>
      <div className="row">
        <div className="col">
          <div className="small">Note details</div>
          <div className="small">ID :{noteId}</div>
          <div className="small">Legacy mode: {useLegacy ? "on" : "off"}</div>
        </div>
        <div className="col">
          <button onClick={onClose}>Close</button>
        </div>
      </div>

      {loading && <div className="small">Loading...</div>}
      {err && <div className="error">{err}</div>}

      {note && !loading && !err && (
        <div style={{ marginTop: 10 }}>
          <div className="small">Tenant ID: {note.tenant_id} </div>
          <div className="small">Owner ID:{note.owner_user_id}</div>
          <div style={{ fontWeight: 700, marginTop: 6 }}>{note.title}</div>
          <div style={{ opacity: 0.9, marginTop: 6 }}>{note.body}</div>
        </div>
      )}
    </div>
  );
}
