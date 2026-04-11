const STORAGE_KEY = "genai70.progress.v1";

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

function loadProgress() {
  const raw = localStorage.getItem(STORAGE_KEY);
  const data = safeJsonParse(raw ?? "{}", {});
  // shape: { [dayNumber]: { learn: bool, build: bool, journal: bool } }
  return typeof data === "object" && data ? data : {};
}

function saveProgress(progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress, null, 2));
}

function dayKey(day) {
  return String(day);
}

function getDayProgress(progress, day) {
  const k = dayKey(day);
  const v = progress[k];
  return {
    learn: !!v?.learn,
    build: !!v?.build,
    journal: !!v?.journal,
  };
}

function setDayBlock(progress, day, block, value) {
  const k = dayKey(day);
  progress[k] = progress[k] ?? {};
  progress[k][block] = !!value;
}

function isDayComplete(p) {
  return !!(p.learn && p.build && p.journal);
}

function computeProgress(progress) {
  const PLAN_DAYS = window.PLAN_DAYS;
  if (!Array.isArray(PLAN_DAYS)) return { totalBlocks: 0, doneBlocks: 0, pct: 0, completeDays: 0 };
  const totalBlocks = PLAN_DAYS.length * 3;
  let doneBlocks = 0;
  let completeDays = 0;
  for (const d of PLAN_DAYS) {
    const p = getDayProgress(progress, d.day);
    doneBlocks += (p.learn ? 1 : 0) + (p.build ? 1 : 0) + (p.journal ? 1 : 0);
    if (isDayComplete(p)) completeDays += 1;
  }
  const pct = totalBlocks === 0 ? 0 : Math.round((doneBlocks / totalBlocks) * 100);
  return { totalBlocks, doneBlocks, pct, completeDays };
}

function computeStreak(progress) {
  const PLAN_DAYS = window.PLAN_DAYS;
  if (!Array.isArray(PLAN_DAYS)) return 0;
  // streak from day 1 onwards, counting consecutive fully complete days
  let streak = 0;
  for (const d of PLAN_DAYS) {
    const p = getDayProgress(progress, d.day);
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
  const PLAN_PHASES = window.PLAN_PHASES;
  if (!Array.isArray(PLAN_PHASES)) return;
  const select = el("phaseSelect");
  for (const p of PLAN_PHASES) {
    const opt = document.createElement("option");
    opt.value = p.key;
    opt.textContent = `${p.name} (Days ${p.days[0]}–${p.days[1]})`;
    select.appendChild(opt);
  }
}

function dayMatchesFilters(dayObj, query, phaseKey, hideCompleted, progress) {
  const q = query.trim().toLowerCase();
  const inPhase = phaseKey === "all" ? true : dayObj.phaseKey === phaseKey;
  if (!inPhase) return false;

  const p = getDayProgress(progress, dayObj.day);
  if (hideCompleted && isDayComplete(p)) return false;

  if (!q) return true;

  const hay = [
    `day ${dayObj.day}`,
    dayObj.title,
    dayObj.phaseName,
    ...(dayObj.learn ?? []),
    ...(dayObj.build ?? []),
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
  const { progress, filters, selectedDay } = state;
  const PLAN_DAYS = window.PLAN_DAYS;
  if (!Array.isArray(PLAN_DAYS)) return;
  const visibleDays = PLAN_DAYS.filter((d) =>
    dayMatchesFilters(d, filters.query, filters.phaseKey, filters.hideCompleted, progress)
  );

  if (visibleDays.length === 0) {
    const div = document.createElement("div");
    div.className = "muted";
    div.style.padding = "8px 2px";
    div.textContent = "No days match your filters.";
    container.appendChild(div);
    return;
  }

  for (const d of visibleDays) {
    const p = getDayProgress(progress, d.day);
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
  const { selectedDay, progress } = state;
  const PLAN_DAYS = window.PLAN_DAYS;
  if (!Array.isArray(PLAN_DAYS)) return;
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

  const p = getDayProgress(progress, dayObj.day);
  const checkboxes = card.querySelectorAll("input[type='checkbox'][data-block]");
  checkboxes.forEach((cb) => {
    const block = cb.getAttribute("data-block");
    cb.checked = block === "learn" ? p.learn : block === "build" ? p.build : p.journal;
    cb.onchange = () => {
      setDayBlock(state.progress, dayObj.day, block, cb.checked);
      saveProgress(state.progress);
      renderAll(state);
    };
  });

  el("markDayBtn").onclick = () => {
    setDayBlock(state.progress, dayObj.day, "learn", true);
    setDayBlock(state.progress, dayObj.day, "build", true);
    setDayBlock(state.progress, dayObj.day, "journal", true);
    saveProgress(state.progress);
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
  const PLAN_DAYS = window.PLAN_DAYS;
  const dayCount = Array.isArray(PLAN_DAYS) ? PLAN_DAYS.length : 0;
  const { pct, doneBlocks, totalBlocks, completeDays } = computeProgress(state.progress);
  el("progressText").textContent = `${pct}%`;
  el("progressCounts").textContent = `${doneBlocks}/${totalBlocks} blocks • ${completeDays}/${dayCount} days`;

  const fill = el("progressFill");
  fill.style.width = `${pct}%`;

  const bar = document.querySelector(".progress__bar");
  if (bar) bar.setAttribute("aria-valuenow", String(pct));

  const streak = computeStreak(state.progress);
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
      version: 1,
      exportedAt: new Date().toISOString(),
      progress: state.progress,
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
    state.progress = loadProgress();
    renderAll(state);
  };

  el("todayBtn").onclick = () => {
    const PLAN_DAYS = window.PLAN_DAYS;
    if (!Array.isArray(PLAN_DAYS) || PLAN_DAYS.length === 0) return;
    // “Today” heuristic: next incomplete day, else day 70
    let pickDay = 70;
    for (const d of PLAN_DAYS) {
      const p = getDayProgress(state.progress, d.day);
      if (!isDayComplete(p)) {
        pickDay = d.day;
        break;
      }
    }
    state.selectedDay = pickDay;
    renderAll(state);
    // scroll list a bit
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

function init() {
  if (!Array.isArray(window.PLAN_DAYS) || !Array.isArray(window.PLAN_PHASES)) return;
  if (!document.getElementById("phaseSelect")) return;

  buildPhaseOptions();

  const state = {
    progress: loadProgress(),
    selectedDay: null,
    filters: { query: "", phaseKey: "all", hideCompleted: false },
  };

  setupFilters(state);
  setupTopActions(state);
  setupExport(state);

  renderAll(state);
}

init();

