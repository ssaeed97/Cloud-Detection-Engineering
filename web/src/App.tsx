import React, { useState } from "react";
import NavBar from "./components/NavBar";
import Login from "./pages/Login";
import Notes from "./pages/Notes";
import Upload from "./pages/Upload";
import Admin from "./pages/Admin";
import { getToken } from "./auth/token";

export default function App() {
  const [route, setRoute] = useState<string>(getToken() ? "notes" : "login");

  return (
    <div className="container">
      <NavBar
        route={route}
        setRoute={setRoute}
        onLogout={() => setRoute("login")}
      />

      {route === "login" && <Login onAuthed={() => setRoute("notes")} />}
      {route === "notes" && <Notes />}
      {route === "upload" && <Upload />}
      {route === "admin" && <Admin />}

      <div className="small" style={{ marginTop: 18, opacity: 0.7 }}>
        Tip: Keep FastAPI running on <code>http://localhost:8000</code> and set <code>VITE_API_BASE_URL</code> if different.
      </div>
    </div>
  );
}
