import { v4 as uuidv4 } from "uuid";
import { getToken } from "../auth/token";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type RequestOptions = {
  method?: "GET" | "POST";
  path: string;
  body?: any;
  auth?: boolean;
};

export async function api<T>({ method = "GET", path, body, auth = false }: RequestOptions): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-Request-ID": uuidv4(),
    "X-Client": "react-v1"
  };

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const resp = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  });

  const text = await resp.text();
  const data = text ? JSON.parse(text) : null;

  if (!resp.ok) {
    const msg = data?.detail ? String(data.detail) : `HTTP ${resp.status}`;
    throw new Error(msg);
  }

  return data as T;
}

export async function uploadFile(file: File): Promise<any> {
  const headers: Record<string, string> = {
    "X-Request-ID": uuidv4(),
    "X-Client": "react-v1"
  };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const form = new FormData();
  form.append("up", file);

  const resp = await fetch(`${API_BASE}/files/upload`, {
    method: "POST",
    headers, // note: no Content-Type for multipart; browser sets it
    body: form
  });

  const text = await resp.text();
  const data = text ? JSON.parse(text) : null;

  if (!resp.ok) {
    const msg = data?.detail ? String(data.detail) : `HTTP ${resp.status}`;
    throw new Error(msg);
  }
  return data;
}
