import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

function redirectToLogin(req: NextRequest) {
  const url = req.nextUrl.clone();
  url.pathname = "/login";
  const next = req.nextUrl.pathname + req.nextUrl.search;
  // Prevent recursive "next=/login?next=..." loops.
  const safeNext = next.startsWith("/login") ? "/" : next;
  url.searchParams.set("next", safeNext);
  return NextResponse.redirect(url);
}

/** Must match token generation in pages/api/login.ts (SHA-256 hex, no HMAC key-length edge cases). */
async function authTokenHex(secret: string) {
  const enc = new TextEncoder();
  const msg = `${secret}|prep_auth_v1`;
  const buf = await crypto.subtle.digest("SHA-256", enc.encode(msg));
  const bytes = new Uint8Array(buf);
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export async function middleware(req: NextRequest) {
  const user = process.env.AUTH_USER;
  const pass = process.env.AUTH_PASS;
  const secret = process.env.AUTH_SECRET;

  // If not configured, default-deny (safer).
  if (!user || !pass || !secret) return redirectToLogin(req);

  const path = req.nextUrl.pathname;
  // Allow unauthenticated access to login + Next internal assets
  if (
    path === "/login" ||
    path.startsWith("/api/login") ||
    path.startsWith("/_next/") ||
    path === "/favicon.ico"
  ) {
    return NextResponse.next();
  }

  const cookie = req.cookies.get("prep_auth")?.value ?? "";

  const expected = await authTokenHex(secret);
  if (!cookie || cookie !== expected) return redirectToLogin(req);

  return NextResponse.next();
}

export const config = {
  // Protect everything (pages, API, and static assets).
  matcher: ["/:path*"],
};

