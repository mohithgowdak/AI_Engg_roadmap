import type { NextApiRequest, NextApiResponse } from "next";
import crypto from "crypto";

type Body = { username?: string; password?: string };

/** Must match authTokenHex in middleware.ts */
function authTokenHex(secret: string) {
  return crypto.createHash("sha256").update(`${secret}|prep_auth_v1`, "utf8").digest("hex");
}

function json(res: NextApiResponse, status: number, data: unknown) {
  res.status(status).setHeader("content-type", "application/json").send(JSON.stringify(data));
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const user = process.env.AUTH_USER;
  const pass = process.env.AUTH_PASS;
  const secret = process.env.AUTH_SECRET;
  if (!user || !pass || !secret) {
    json(res, 500, { error: "Missing AUTH_USER/AUTH_PASS/AUTH_SECRET" });
    return;
  }

  if (req.method === "POST") {
    const body = (req.body ?? {}) as Body;
    const ok = body.username === user && body.password === pass;
    if (!ok) {
      json(res, 401, { error: "Invalid credentials" });
      return;
    }

    const token = authTokenHex(secret);
    const isProd = process.env.NODE_ENV === "production";
    const cookie = [
      `prep_auth=${token}`,
      "Path=/",
      "HttpOnly",
      "SameSite=Lax",
      isProd ? "Secure" : "",
      // 180 days
      `Max-Age=${60 * 60 * 24 * 180}`,
    ]
      .filter(Boolean)
      .join("; ");

    res.setHeader("Set-Cookie", cookie);
    json(res, 200, { ok: true });
    return;
  }

  if (req.method === "DELETE") {
    res.setHeader("Set-Cookie", "prep_auth=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0");
    json(res, 200, { ok: true });
    return;
  }

  res.setHeader("Allow", "POST, DELETE");
  res.status(405).end("Method Not Allowed");
}

