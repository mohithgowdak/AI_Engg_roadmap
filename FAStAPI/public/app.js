/* global PLAN_DAYS, PLAN_PHASES */

const STORAGE_KEY = "genai70.progress.v2";
const CLOUD_ENDPOINT = "/api/progress";
const CLOUD_DEBOUNCE_MS = 900;

function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

function safeJsonParse(s, fallback) {
  try {
    return JSON.parse(s);
  } catch {
    return fallback;
  }
}

function nowMs() {
  return Date.now();
}

function normalizeLocal(raw) {
  // v1 shape: { [dayNumber]: { learn, build, journal } }
  if (raw && typeof raw === "object" && !Array.isArray(raw) && raw.data && typeof raw.updatedAt === "number") {
    return { updatedAt: raw.updatedAt, data: raw.data };
  }
  if (raw && typeof raw === "object" && !Array.isArray(raw)) {
    return { updatedAt: 0, data: raw };
  }
  return { updatedAt: 0, data: {} };
}

function loadLocalProgress() {
  const raw = localStorage.getItem(STORAGE_KEY);
  return normalizeLocal(safeJsonParse(raw ?? "{}", {}));
}

function saveLocalProgress(payload) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload, null, 2));
}

async function fetchCloudProgress() {
  const res = await fetch(CLOUD_ENDPOINT, { method: "GET", cache: "no-store" });
  if (!res.ok) throw new Error(`Cloud GET failed: ${res.status}`);
  const json = await res.json();
  return normalizeLocal(json);
}

async function pushCloudProgress(payload) {
  const res = await fetch(CLOUD_ENDPOINT, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Cloud POST failed: ${res.status}`);
}

function dayKey(day) {
  return String(day);
}

function getDayProgress(payload, day) {
  const k = dayKey(day);
  const v = payload.data?.[k];
  return {
    learn: !!v?.learn,
    build: !!v?.build,
    journal: !!v?.journal,
  };
}

function setDayBlock(payload, day, block, value) {
  const k = dayKey(day);
  payload.data[k] = payload.data[k] ?? {};
  payload.data[k][block] = !!value;
  payload.updatedAt = nowMs();
}

function isDayComplete(p) {
  return !!(p.learn && p.build && p.journal);
}

function computeProgress(payload) {
  const totalBlocks = PLAN_DAYS.length * 3;
  let doneBlocks = 0;
  let completeDays = 0;
  for (const d of PLAN_DAYS) {
    const p = getDayProgress(payload, d.day);
    doneBlocks += (p.learn ? 1 : 0) + (p.build ? 1 : 0) + (p.journal ? 1 : 0);
    if (isDayComplete(p)) completeDays += 1;
  }
  const pct = totalBlocks === 0 ? 0 : Math.round((doneBlocks / totalBlocks) * 100);
  return { totalBlocks, doneBlocks, pct, completeDays };
}

function computeStreak(payload) {
  let streak = 0;
  for (const d of PLAN_DAYS) {
    const p = getDayProgress(payload, d.day);
    if (!isDayComplete(p)) break;
    streak += 1;
  }
  return streak;
}

function el(id) {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing element: ${id}`);
  return node;
}

function renderList(targetUl, items) {
  targetUl.innerHTML = "";
  for (const t of items) {
    const li = document.createElement("li");
    li.textContent = t;
    targetUl.appendChild(li);
  }
}

function renderOrderedList(targetOl, items) {
  targetOl.innerHTML = "";
  for (const t of items) {
    const li = document.createElement("li");
    li.textContent = t;
    targetOl.appendChild(li);
  }
}

function buildPhaseOptions() {
  const select = el("phaseSelect");
  for (const p of PLAN_PHASES) {
    const opt = document.createElement("option");
    opt.value = p.key;
    opt.textContent = `${p.name} (Days ${p.days[0]}–${p.days[1]})`;
    select.appendChild(opt);
  }
}

function dayMatchesFilters(dayObj, query, phaseKey, hideCompleted, payload) {
  const q = query.trim().toLowerCase();
  const inPhase = phaseKey === "all" ? true : dayObj.phaseKey === phaseKey;
  if (!inPhase) return false;

  const p = getDayProgress(payload, dayObj.day);
  if (hideCompleted && isDayComplete(p)) return false;

  if (!q) return true;

  const hay = [
    `day ${dayObj.day}`,
    dayObj.title,
    dayObj.phaseName,
    ...(dayObj.learn ?? []),
    ...(dayObj.build ?? []),
    ...(dayObj.buildChecklist ?? []),
    ...(dayObj.practice ?? []),
    ...(dayObj.selfTest ?? []),
  ]
    .join(" | ")
    .toLowerCase();

  return hay.includes(q);
}

function renderDayList(state) {
  const container = el("dayList");
  container.innerHTML = "";
  const { payload, filters, selectedDay } = state;
  const visibleDays = PLAN_DAYS.filter((d) => dayMatchesFilters(d, filters.query, filters.phaseKey, filters.hideCompleted, payload));

  if (visibleDays.length === 0) {
    const div = document.createElement("div");
    div.className = "muted";
    div.style.padding = "8px 2px";
    div.textContent = "No days match your filters.";
    container.appendChild(div);
    return;
  }

  for (const d of visibleDays) {
    const p = getDayProgress(payload, d.day);
    const row = document.createElement("div");
    row.className = "dayitem" + (selectedDay === d.day ? " dayitem--active" : "");
    row.tabIndex = 0;
    row.setAttribute("role", "button");
    row.setAttribute("aria-label", `Open day ${d.day}`);

    const left = document.createElement("div");
    left.className = "dayitem__left";

    const dayText = document.createElement("div");
    dayText.className = "dayitem__day";
    dayText.textContent = `Day ${String(d.day).padStart(2, "0")} • ${d.phaseKey}`;

    const title = document.createElement("div");
    title.className = "dayitem__title";
    title.textContent = d.title;

    left.appendChild(dayText);
    left.appendChild(title);

    const tag = document.createElement("div");
    tag.className = "tag" + (isDayComplete(p) ? " tag--done" : "");
    tag.textContent = isDayComplete(p) ? "Done" : `${(p.learn ? 1 : 0) + (p.build ? 1 : 0) + (p.journal ? 1 : 0)}/3`;

    row.appendChild(left);
    row.appendChild(tag);

    const open = () => {
      state.selectedDay = d.day;
      renderAll(state);
    };

    row.addEventListener("click", open);
    row.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") open();
    });

    container.appendChild(row);
  }
}

function renderSelectedDay(state) {
  const { selectedDay, payload } = state;
  const dayObj = PLAN_DAYS.find((d) => d.day === selectedDay);

  const title = el("dayTitle");
  const meta = el("dayMeta");
  const card = el("dayCard");
  const empty = el("emptyState");

  if (!dayObj) {
    title.textContent = "Select a day";
    meta.textContent = "";
    card.hidden = true;
    empty.hidden = false;
    return;
  }

  empty.hidden = true;
  card.hidden = false;

  title.textContent = `Day ${dayObj.day}: ${dayObj.title}`;
  meta.textContent = `${dayObj.phaseName} • ${dayObj.phaseKey} • 2 hours total`;
  el("phasePill").textContent = `${dayObj.phaseName}`;

  renderList(el("learnList"), dayObj.learn ?? []);
  renderList(el("buildList"), dayObj.build ?? []);
  renderList(el("journalList"), dayObj.journal ?? []);
  renderOrderedList(el("buildChecklist"), dayObj.buildChecklist ?? []);
  renderList(el("practiceList"), dayObj.practice ?? []);
  renderOrderedList(el("testList"), dayObj.selfTest ?? []);

  const p = getDayProgress(payload, dayObj.day);
  const checkboxes = card.querySelectorAll("input[type='checkbox'][data-block]");
  checkboxes.forEach((cb) => {
    const block = cb.getAttribute("data-block");
    cb.checked = block === "learn" ? p.learn : block === "build" ? p.build : p.journal;
    cb.onchange = () => {
      setDayBlock(state.payload, dayObj.day, block, cb.checked);
      state.persist();
      renderAll(state);
    };
  });

  el("markDayBtn").onclick = () => {
    setDayBlock(state.payload, dayObj.day, "learn", true);
    setDayBlock(state.payload, dayObj.day, "build", true);
    setDayBlock(state.payload, dayObj.day, "journal", true);
    state.persist();
    renderAll(state);
  };

  el("prevDayBtn").onclick = () => {
    state.selectedDay = clamp(selectedDay - 1, 1, PLAN_DAYS.length);
    renderAll(state);
  };
  el("nextDayBtn").onclick = () => {
    state.selectedDay = clamp(selectedDay + 1, 1, PLAN_DAYS.length);
    renderAll(state);
  };
}

function renderProgressHeader(state) {
  const { pct, doneBlocks, totalBlocks, completeDays } = computeProgress(state.payload);
  el("progressText").textContent = `${pct}%`;
  el("progressCounts").textContent = `${doneBlocks}/${totalBlocks} blocks • ${completeDays}/${PLAN_DAYS.length} days`;

  const fill = el("progressFill");
  fill.style.width = `${pct}%`;

  const bar = document.querySelector(".progress__bar");
  if (bar) bar.setAttribute("aria-valuenow", String(pct));

  const streak = computeStreak(state.payload);
  el("streakText").textContent = `Streak: ${streak} day${streak === 1 ? "" : "s"}`;
}

function renderAll(state) {
  renderProgressHeader(state);
  renderDayList(state);
  renderSelectedDay(state);
}

function setupExport(state) {
  const dialog = el("exportDialog");
  const text = el("exportText");

  el("exportBtn").onclick = () => {
    const payload = {
      version: 2,
      exportedAt: new Date().toISOString(),
      progress: state.payload,
    };
    text.value = JSON.stringify(payload, null, 2);
    dialog.showModal();
    text.focus();
    text.setSelectionRange(0, 0);
  };

  el("closeExportBtn").onclick = () => dialog.close();
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) dialog.close();
  });

  el("copyExportBtn").onclick = async () => {
    await navigator.clipboard.writeText(text.value);
  };
}

function setupTopActions(state) {
  el("resetBtn").onclick = () => {
    localStorage.removeItem(STORAGE_KEY);
    state.payload = { updatedAt: 0, data: {} };
    state.persist(true);
    renderAll(state);
  };

  el("todayBtn").onclick = () => {
    let pickDay = 70;
    for (const d of PLAN_DAYS) {
      const p = getDayProgress(state.payload, d.day);
      if (!isDayComplete(p)) {
        pickDay = d.day;
        break;
      }
    }
    state.selectedDay = pickDay;
    renderAll(state);
    const list = el("dayList");
    const active = list.querySelector(".dayitem--active");
    if (active) active.scrollIntoView({ block: "center" });
  };
}

function setupFilters(state) {
  const search = el("searchInput");
  const phase = el("phaseSelect");
  const hideCompleted = el("hideCompleted");

  search.oninput = () => {
    state.filters.query = search.value;
    renderAll(state);
  };
  phase.onchange = () => {
    state.filters.phaseKey = phase.value;
    renderAll(state);
  };
  hideCompleted.onchange = () => {
    state.filters.hideCompleted = hideCompleted.checked;
    renderAll(state);
  };
}

function createCloudPersister(state) {
  let t = null;
  let inFlight = false;
  let pending = false;

  async function flush(force) {
    if (inFlight) {
      pending = true;
      return;
    }
    inFlight = true;
    try {
      saveLocalProgress(state.payload);
      if (force) {
        await pushCloudProgress(state.payload);
      } else {
        await pushCloudProgress(state.payload);
      }
    } catch {
      // best-effort: local still saved
    } finally {
      inFlight = false;
      if (pending) {
        pending = false;
        await flush(true);
      }
    }
  }

  return function persist(force = false) {
    saveLocalProgress(state.payload);
    if (t) clearTimeout(t);
    if (force) {
      flush(true);
      return;
    }
    t = setTimeout(() => flush(false), CLOUD_DEBOUNCE_MS);
  };
}

async function init() {
  buildPhaseOptions();

  const local = loadLocalProgress();
  const state = {
    payload: local,
    selectedDay: null,
    filters: { query: "", phaseKey: "all", hideCompleted: false },
    persist: () => {},
  };

  state.persist = createCloudPersister(state);

  // Try to merge with cloud: newer wins; if local is newer, push it.
  try {
    const cloud = await fetchCloudProgress();
    if ((cloud.updatedAt ?? 0) > (state.payload.updatedAt ?? 0)) {
      state.payload = cloud;
      saveLocalProgress(state.payload);
    } else if ((state.payload.updatedAt ?? 0) > (cloud.updatedAt ?? 0)) {
      await pushCloudProgress(state.payload);
    }
  } catch {
    // offline or supabase not configured: keep local-only
  }

  setupFilters(state);
  setupTopActions(state);
  setupExport(state);

  renderAll(state);
}

init();

