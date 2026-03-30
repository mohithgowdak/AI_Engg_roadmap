import type { NextApiRequest, NextApiResponse } from "next";
import { createClient } from "@supabase/supabase-js";

type ProgressPayload = {
  updatedAt: number;
  data: Record<string, { learn?: boolean; build?: boolean; journal?: boolean }>;
};

function getSupabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    throw new Error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY");
  }
  return createClient(url, key, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}

function isObject(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function normalizePayload(v: unknown): ProgressPayload | null {
  if (!isObject(v)) return null;
  const updatedAt = typeof v.updatedAt === "number" ? v.updatedAt : null;
  const data = v.data;
  if (updatedAt === null || updatedAt < 0) return null;
  if (!isObject(data)) return null;
  return { updatedAt, data: data as ProgressPayload["data"] };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const supabase = getSupabase();
    const id = "default";

    if (req.method === "GET") {
      const { data, error } = await supabase
        .from("progress")
        .select("data, updated_at_ms")
        .eq("id", id)
        .maybeSingle();
      if (error) throw error;

      const payload: ProgressPayload = {
        updatedAt: typeof data?.updated_at_ms === "number" ? data.updated_at_ms : 0,
        data: (data?.data as ProgressPayload["data"]) ?? {},
      };

      res.status(200).json(payload);
      return;
    }

    if (req.method === "POST") {
      const payload = normalizePayload(req.body);
      if (!payload) {
        res.status(400).json({ error: "Invalid payload. Expected { updatedAt:number, data:object }" });
        return;
      }

      const { error } = await supabase.from("progress").upsert(
        {
          id,
          data: payload.data,
          updated_at_ms: payload.updatedAt,
        },
        { onConflict: "id" }
      );
      if (error) throw error;

      res.status(200).json({ ok: true });
      return;
    }

    res.setHeader("Allow", "GET, POST");
    res.status(405).end("Method Not Allowed");
  } catch (e) {
    res.status(500).json({ error: e instanceof Error ? e.message : "Server error" });
  }
}

