import Head from "next/head";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

type WorkoutItemId =
  | "running"
  | "pushup"
  | "shoulder_weights"
  | "pullup"
  | "plank"
  | "tricep_dip"
  | "tricep_extension"
  | "dumbbell"
  | "squat"
  | "grip";

type WorkoutItemDef = {
  id: WorkoutItemId;
  name: string;
  meta: string;
};

type WorkoutEntry = {
  checked: boolean;
  notes?: string;
};

type WorkoutPayload = {
  updatedAt: number;
  byDate: Record<string, Record<WorkoutItemId, WorkoutEntry>>;
};

const STORAGE_KEY = "workout.daily.v1";
const CLOUD_ENDPOINT = "/api/workout";
const CLOUD_DEBOUNCE_MS = 900;

const ITEMS: WorkoutItemDef[] = [
  { id: "running", name: "Running", meta: "1.6 km at 8/7" },
  { id: "pushup", name: "Push-up", meta: "6 sets → 12 reps" },
  { id: "shoulder_weights", name: "Shoulder weights", meta: "50 reps → 2 sets" },
  { id: "pullup", name: "Pull-up", meta: "3 sets → 5 reps" },
  { id: "plank", name: "Plank", meta: "3 sets → 10 reps" },
  { id: "tricep_dip", name: "Tricep dip", meta: "12 reps → 2 sets" },
  { id: "tricep_extension", name: "Tricep extension", meta: "3 sets → 12 reps" },
  { id: "dumbbell", name: "Dumbbell", meta: "50 reps → 2 sets (1 set each)" },
  { id: "squat", name: "Squat", meta: "3 sets → 12 reps" },
  { id: "grip", name: "Grip", meta: "in free time" },
];

function todayKey() {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function safeJsonParse(s: string | null): unknown {
  try {
    return JSON.parse(s ?? "null");
  } catch {
    return null;
  }
}

function isObject(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function emptyDay(): Record<WorkoutItemId, WorkoutEntry> {
  const day = {} as Record<WorkoutItemId, WorkoutEntry>;
  for (const it of ITEMS) day[it.id] = { checked: false, notes: "" };
  return day;
}

function normalizePayload(raw: unknown): WorkoutPayload {
  if (!isObject(raw)) return { updatedAt: 0, byDate: {} };
  const updatedAt = typeof raw.updatedAt === "number" ? raw.updatedAt : 0;
  const byDate = isObject(raw.byDate) ? (raw.byDate as WorkoutPayload["byDate"]) : {};
  return { updatedAt, byDate };
}

function computeDoneCount(day: Record<WorkoutItemId, WorkoutEntry>) {
  let done = 0;
  for (const it of ITEMS) if (day[it.id]?.checked) done += 1;
  return { done, total: ITEMS.length };
}

export default function WorkoutPage() {
  const [date, setDate] = useState<string>(todayKey());
  const [payload, setPayload] = useState<WorkoutPayload>({ updatedAt: 0, byDate: {} });
  const [cloudHint, setCloudHint] = useState<"idle" | "synced" | "local-only">("idle");
  const cloudTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const payloadRef = useRef(payload);
  payloadRef.current = payload;

  const pushCloud = useCallback(async (p: WorkoutPayload) => {
    const res = await fetch(CLOUD_ENDPOINT, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(p),
    });
    if (!res.ok) throw new Error(`Cloud POST failed: ${res.status}`);
  }, []);

  const scheduleCloudPush = useCallback(
    (p: WorkoutPayload) => {
      if (cloudTimer.current) clearTimeout(cloudTimer.current);
      cloudTimer.current = setTimeout(() => {
        cloudTimer.current = null;
        pushCloud(p)
          .then(() => setCloudHint("synced"))
          .catch(() => setCloudHint("local-only"));
      }, CLOUD_DEBOUNCE_MS);
    },
    [pushCloud]
  );

  useEffect(() => {
    const loaded = normalizePayload(safeJsonParse(typeof window !== "undefined" ? localStorage.getItem(STORAGE_KEY) : null));
    setPayload(loaded);

    let cancelled = false;
    (async () => {
      try {
        const res = await fetch(CLOUD_ENDPOINT, { method: "GET", cache: "no-store" });
        if (!res.ok) throw new Error(String(res.status));
        const cloud = normalizePayload(await res.json());
        if (cancelled) return;

        const local = loaded;
        if ((cloud.updatedAt ?? 0) > (local.updatedAt ?? 0)) {
          setPayload(cloud);
          try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(cloud, null, 2));
          } catch {
            /* ignore */
          }
          setCloudHint("synced");
        } else if ((local.updatedAt ?? 0) > (cloud.updatedAt ?? 0)) {
          await pushCloud(local);
          if (!cancelled) setCloudHint("synced");
        } else {
          setCloudHint("synced");
        }
      } catch {
        if (!cancelled) setCloudHint("local-only");
      }
    })();

    return () => {
      cancelled = true;
      if (cloudTimer.current) clearTimeout(cloudTimer.current);
    };
  }, [pushCloud]);

  const day = useMemo(() => {
    return payload.byDate[date] ?? emptyDay();
  }, [payload.byDate, date]);

  const { done, total } = useMemo(() => computeDoneCount(day), [day]);

  function persist(next: WorkoutPayload) {
    setPayload(next);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next, null, 2));
    } catch {
      // ignore
    }
    scheduleCloudPush(next);
  }

  function setEntry(id: WorkoutItemId, patch: Partial<WorkoutEntry>) {
    const cur = payloadRef.current;
    const next: WorkoutPayload = {
      updatedAt: Date.now(),
      byDate: { ...cur.byDate },
    };
    const nextDay: Record<WorkoutItemId, WorkoutEntry> = { ...(next.byDate[date] ?? emptyDay()) };
    nextDay[id] = { ...(nextDay[id] ?? { checked: false, notes: "" }), ...patch };
    next.byDate[date] = nextDay;
    persist(next);
  }

  function resetDate(d: string) {
    const next: WorkoutPayload = { updatedAt: Date.now(), byDate: { ...payloadRef.current.byDate } };
    delete next.byDate[d];
    persist(next);
    pushCloud(next)
      .then(() => setCloudHint("synced"))
      .catch(() => setCloudHint("local-only"));
  }

  async function copyExport() {
    const text = JSON.stringify(
      { version: 1, exportedAt: new Date().toISOString(), payload },
      null,
      2
    );
    await navigator.clipboard.writeText(text);
  }

  return (
    <>
      <Head>
        <title>Workout • Daily Tracker</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Inter:wght@300..700&display=swap"
          rel="stylesheet"
        />
      </Head>

      <div className="bg-noise" aria-hidden="true" />
      <header className="topbar">
        <div className="brand">
          <div className="brand__kicker">Daily workout • check it off</div>
          <div className="brand__title">Workout Tracker</div>
          <div className="brand__sub">
            {done}/{total} done •{" "}
            <Link className="link" href="/">
              Back to plan
            </Link>
          </div>
        </div>

        <div className="topbar__actions">
          <label className="field" style={{ marginBottom: 0, minWidth: 170 }}>
            <span className="field__label">Date</span>
            <input className="input" type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </label>
          <button className="btn btn--ghost" type="button" onClick={() => resetDate(date)}>
            Reset this day
          </button>
          <button className="btn" type="button" onClick={copyExport}>
            Copy export
          </button>
        </div>
      </header>

      <main className="content">
        <div className="card">
          <div className="workout-list" role="list" aria-label="Workout checklist">
            {ITEMS.map((it) => {
              const entry = day[it.id] ?? { checked: false, notes: "" };
              return (
                <div key={it.id} className="workout-row" role="listitem">
                  <label className="workout-row__left">
                    <input
                      type="checkbox"
                      checked={!!entry.checked}
                      onChange={(e) => setEntry(it.id, { checked: e.target.checked })}
                    />
                    <div className="workout-row__text">
                      <div className="workout-row__name">{it.name}</div>
                      <div className="muted workout-row__meta">{it.meta}</div>
                    </div>
                  </label>
                  <input
                    className="input workout-row__notes"
                    placeholder="Notes (optional)"
                    value={entry.notes ?? ""}
                    onChange={(e) => setEntry(it.id, { notes: e.target.value })}
                  />
                </div>
              );
            })}
          </div>
          <div className="muted" style={{ marginTop: 12, fontSize: 12 }}>
            Saved in your browser (per day). With Supabase env vars set, changes also sync to the cloud (
            {cloudHint === "synced"
              ? "last write synced"
              : cloudHint === "local-only"
                ? "cloud unavailable — local only"
                : "checking cloud…"}
            ). Export copies JSON for a manual backup.
          </div>
        </div>
      </main>
    </>
  );
}

