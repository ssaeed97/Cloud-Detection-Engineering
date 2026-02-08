import React from "react";
import { getToken } from "../auth/token";

export function Guard({ children }: { children: React.ReactNode }) {
  const token = getToken();
  if (!token) {
    return (
      <div className="card">
        <div className="error">You must be logged in to view this page.</div>
      </div>
    );
  }
  return <>{children}</>;
}
