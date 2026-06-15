import { useEffect, useState, useCallback } from "react";

export interface AuthUser {
  memberId: number;
  username: string;
  nickname: string;
  role: "USER" | "ADMIN" | string;
}

const KEYS = ["memberId", "username", "nickname", "role"] as const;

export function getAuthUser(): AuthUser | null {
  if (typeof window === "undefined") return null;
  const memberId = localStorage.getItem("memberId");
  const username = localStorage.getItem("username");
  const nickname = localStorage.getItem("nickname");
  const role = localStorage.getItem("role");
  if (!memberId || !username || !nickname || !role) return null;
  return { memberId: Number(memberId), username, nickname, role };
}

export function setAuthUser(u: AuthUser) {
  localStorage.setItem("memberId", String(u.memberId));
  localStorage.setItem("username", u.username);
  localStorage.setItem("nickname", u.nickname);
  localStorage.setItem("role", u.role);
  window.dispatchEvent(new Event("auth-changed"));
}

export function clearAuth() {
  KEYS.forEach((k) => localStorage.removeItem(k));
  window.dispatchEvent(new Event("auth-changed"));
}

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const refresh = useCallback(() => setUser(getAuthUser()), []);
  useEffect(() => {
    refresh();
    const handler = () => refresh();
    window.addEventListener("auth-changed", handler);
    window.addEventListener("storage", handler);
    return () => {
      window.removeEventListener("auth-changed", handler);
      window.removeEventListener("storage", handler);
    };
  }, [refresh]);
  return { user, isAuthenticated: !!user, isAdmin: user?.role === "ADMIN", refresh };
}