import Head from "next/head";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/router";

const QUOTES = [
  "Discipline beats motivation, but today you get both.",
  "Small progress today becomes confidence tomorrow.",
  "You don’t rise to the occasion. You fall to the level of your systems.",
  "Build less noise. Build more signal.",
  "One focused hour a day compounds faster than talent.",
  "You’re not behind. You’re building momentum.",
];

function pickQuote() {
  const seed = new Date().toDateString();
  let h = 0;
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  return QUOTES[h % QUOTES.length];
}

export default function Login() {
  const router = useRouter();
  const [nextPath, setNextPath] = useState("/");

  useEffect(() => {
    if (!router.isReady) return;
    const n = router.query.next;
    const candidate = typeof n === "string" && n.startsWith("/") ? n : "/";
    setNextPath(candidate.startsWith("/login") ? "/" : candidate);
  }, [router.isReady, router.query.next]);

  const quote = useMemo(() => pickQuote(), []);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "content-type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        throw new Error(j?.error || `Login failed (${res.status})`);
      }
      // Full navigation so the new HttpOnly cookie is always sent on the next request
      const dest = nextPath || "/";
      window.location.assign(dest);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Head>
        <title>Login • 70-Day Prep</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Inter:wght@300..700&display=swap"
          rel="stylesheet"
        />
      </Head>

      <div className="bg-noise" aria-hidden="true" />
      <div className="login">
        <div className="login__card">
          <div className="login__kicker">Private • Your training space</div>
          <div className="login__title">70-Day GenAI Prep</div>
          <div className="login__quote">“{quote}”</div>

          <form className="login__form" onSubmit={onSubmit}>
            <label className="field">
              <span className="field__label">Username</span>
              <input
                className="input"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
              />
            </label>

            <label className="field">
              <span className="field__label">Password</span>
              <input
                className="input"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </label>

            {error ? <div className="login__error">{error}</div> : null}

            <button className="btn login__btn" type="submit" disabled={loading}>
              {loading ? "Signing in..." : "Enter"}
            </button>

            <div className="muted login__hint">Tip: keep your journal in Notes; this app tracks progress + sync.</div>
          </form>
        </div>
      </div>
    </>
  );
}

