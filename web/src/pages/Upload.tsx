import React, { useState } from "react";
import { Guard } from "../components/Guard";
import { uploadFile } from "../api/client";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  async function doUpload() {
    setErr(null); setResult(null);
    if (!file) {
      setErr("Pick a file first.");
      return;
    }
    try {
      const res = await uploadFile(file);
      setResult(res);
    } catch (e: any) {
      setErr(e.message || "Upload failed");
    }
  }

  return (
    <Guard>
      <div className="card">
        <h2>Upload</h2>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <div className="row" style={{ marginTop: 12 }}>
          <div className="col">
            <button onClick={doUpload}>Upload</button>
          </div>
        </div>

        {err && <div className="error">{err}</div>}

        {result && (
          <div className="card" style={{ background: "#0f1626" }}>
            <div className="small">Upload result</div>
            <pre style={{ overflowX: "auto" }}>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>
    </Guard>
  );
}
