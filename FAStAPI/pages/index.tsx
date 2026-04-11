import Head from "next/head";
import Script from "next/script";

export default function Home() {
  return (
    <>
      <Head>
        <title>70-Day GenAI Interview Prep</title>
        <meta
          name="description"
          content="A day-by-day 70-day plan for GenAI/LLM app + backend interview readiness. Track progress locally and sync to cloud."
        />
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
          <div className="brand__kicker">Interview Prep • 2 hours/day</div>
          <div className="brand__title">70-Day GenAI System Design</div>
          <div className="brand__sub">40m learn • 60m build • 20m journal</div>
        </div>

        <div className="topbar__actions">
          <a className="btn btn--ghost" href="/workout">
            Workout
          </a>
          <button className="btn btn--ghost" id="todayBtn" type="button">
            Jump to today
          </button>
          <button className="btn btn--ghost" id="resetBtn" type="button">
            Reset progress
          </button>
          <button className="btn" id="exportBtn" type="button">
            Export
          </button>
        </div>
      </header>

      <main className="layout">
        <aside className="sidebar">
          <div className="panel">
            <div className="panel__title">Progress</div>
            <div className="progress">
              <div className="progress__meta">
                <span id="progressText">0%</span>
                <span className="muted" id="progressCounts">
                  0/0
                </span>
              </div>
              <div className="progress__bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={0}>
                <div className="progress__fill" id="progressFill" />
              </div>
              <div className="progress__mini muted" id="streakText">
                Streak: 0 days
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel__title">Find a day</div>
            <label className="field">
              <span className="field__label">Search</span>
              <input id="searchInput" className="input" placeholder="e.g., RAG, eval, agents, FastAPI" />
            </label>

            <label className="field">
              <span className="field__label">Phase</span>
              <select id="phaseSelect" className="input">
                <option value="all">All phases</option>
              </select>
            </label>

            <label className="field field--row">
              <input id="hideCompleted" type="checkbox" />
              <span>Hide completed days</span>
            </label>
          </div>

          <div className="panel">
            <div className="panel__title">Days</div>
            <div className="daylist" id="dayList" aria-label="Day list" />
          </div>

          <div className="footer muted">
            Data stays in your browser (localStorage). Journal is external: use your Notes app.
          </div>
        </aside>

        <section className="content">
          <div className="content__header">
            <div className="content__title" id="dayTitle">
              Select a day
            </div>
            <div className="content__meta muted" id="dayMeta" />
          </div>

          <div className="card" id="dayCard" hidden>
            <div className="card__top">
              <div className="pill" id="phasePill">
                Phase
              </div>
              <div className="card__actions">
                <button className="btn btn--ghost" id="prevDayBtn" type="button">
                  Prev
                </button>
                <button className="btn btn--ghost" id="nextDayBtn" type="button">
                  Next
                </button>
              </div>
            </div>

            <div className="grid">
              <div className="block">
                <div className="block__hdr">
                  <div className="block__title">Learn (40 min)</div>
                  <label className="check">
                    <input type="checkbox" data-block="learn" />
                    <span>Done</span>
                  </label>
                </div>
                <ul className="list" id="learnList" />
              </div>

              <div className="block">
                <div className="block__hdr">
                  <div className="block__title">Build (60 min)</div>
                  <label className="check">
                    <input type="checkbox" data-block="build" />
                    <span>Done</span>
                  </label>
                </div>
                <ul className="list" id="buildList" />
              </div>

              <div className="block">
                <div className="block__hdr">
                  <div className="block__title">Journal (20 min)</div>
                  <label className="check">
                    <input type="checkbox" data-block="journal" />
                    <span>Done</span>
                  </label>
                </div>
                <ul className="list" id="journalList" />
              </div>
            </div>

            <div className="split">
              <div className="block">
                <div className="block__hdr">
                  <div className="block__title">Build checklist (60 min)</div>
                </div>
                <ol className="list list--ol" id="buildChecklist" />
              </div>

              <div className="block">
                <div className="block__hdr">
                  <div className="block__title">Practice set</div>
                </div>
                <ul className="list" id="practiceList" />
              </div>
            </div>

            <div className="split">
              <div className="block">
                <div className="block__hdr">
                  <div className="block__title">Self-test (5–10 min)</div>
                </div>
                <ol className="list list--ol" id="testList" />
              </div>
            </div>

            <div className="card__bottom">
              <button className="btn" id="markDayBtn" type="button">
                Mark day complete
              </button>
              <div className="muted">Tip: for interviews, practice saying the answer out loud in 2 minutes.</div>
            </div>
          </div>

          <div className="card card--empty" id="emptyState">
            <div className="empty__title">Build less noise. Build more signal.</div>
            <div className="muted">Pick a day from the left. Track learn/build/journal completion and export progress anytime.</div>
          </div>
        </section>
      </main>

      <dialog className="dialog" id="exportDialog">
        <div className="dialog__hdr">
          <div className="dialog__title">Export progress</div>
          <button className="btn btn--ghost" id="closeExportBtn" type="button">
            Close
          </button>
        </div>
        <div className="dialog__body">
          <div className="muted">Copy this JSON into a file (or paste into Notion/Docs). You can import later (manual).</div>
          <textarea className="textarea" id="exportText" spellCheck={false} />
        </div>
        <div className="dialog__actions">
          <button className="btn" id="copyExportBtn" type="button">
            Copy
          </button>
        </div>
      </dialog>

      <Script src="/plan-data.js" strategy="beforeInteractive" />
      <Script src="/app.js" strategy="afterInteractive" />
    </>
  );
}

