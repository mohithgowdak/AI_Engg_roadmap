/* global window */
// 70-day plan data for: 40m learn, 60m build, 20m journal.
// This is generated from phase templates to keep it maintainable, but every day is still explicit in the UI.

(function () {
  const phases = [
    { key: "FND", name: "Foundations", days: [1, 10] },
    { key: "RAG", name: "RAG Build", days: [11, 25] },
    { key: "EVAL", name: "Eval + Guardrails", days: [26, 35] },
    { key: "OPS", name: "Observability + Perf", days: [36, 45] },
    { key: "AGENT", name: "Agents + Orchestration", days: [46, 55] },
    { key: "INT", name: "Interview Sprint", days: [56, 60] },
    { key: "AWS", name: "AWS + Deployment", days: [61, 70] },
  ];

  function phaseForDay(day) {
    const p = phases.find((x) => day >= x.days[0] && day <= x.days[1]);
    return p ? p : phases[0];
  }

  const learnTracks = {
    FND: [
      "Generative AI basics: LLMs vs classic ML; what you can/can’t expect",
      "Tokens & context window; tokenization; truncation failure modes",
      "Transformer basics: self-attention, multi-head attention, positional encoding (high-level)",
      "Embeddings & vector similarity: cosine similarity; nearest-neighbor intuition",
      "LLM decoding: greedy/beam search; temperature, top-k, top-p (why they matter)",
      "Prompting basics: clear instructions, few-shot patterns, structured outputs (JSON/schema)",
      "API design for LLM apps: latency/cost/quality triangle; retries, timeouts, idempotency",
      "FastAPI foundations: routes, Pydantic models, validation, error handling",
      "State & memory: what to store (chat, citations, tool results) vs what not to store",
      "Security primer: prompt injection, data leakage, and safe defaults",
    ],
    RAG: [
      "RAG architecture: ingestion → embed → index → retrieve → synthesize",
      "Chunking strategies: size/overlap, headings, semantic boundaries, metadata",
      "Vector stores: indexing, metadata filters, updates, deletes, versioning",
      "Retrieval strategies: top-k, MMR; hybrid retrieval (BM25 + vectors) (concept)",
      "Rerankers: why/when; cross-encoder intuition (concept)",
      "Query rewriting & multi-query retrieval (concept)",
      "Citations & grounding: trust signals and claim-to-source discipline",
      "Context compression: summarization vs selective quoting; budget control",
      "Multi-tenant + permissions: filtering and leakage risks",
      "RAG failure modes: missing recall, wrong chunk, stale index, hallucination",
      "What NOT to use RAG for; alternative patterns (tools, DB queries, workflows)",
      "LangChain concepts (light): loader → splitter → retriever → chain",
      "Performance basics: caching (embeddings/retrieval/response) and batching",
      "Cost engineering for RAG: context length, calls/request, model choice",
      "Model routing basics: when to use small/cheap vs bigger models (concept)",
    ],
    EVAL: [
      "Evaluation engineering: golden datasets + regression testing mindset",
      "Retrieval metrics: recall@k, MRR; what a “good” retriever looks like",
      "Answer metrics: faithfulness/groundedness, completeness, refusal correctness",
      "LLM-as-judge: where it helps, where it lies; controlling variance",
      "Prompt injection: direct/indirect; defense-in-depth approach",
      "Guardrails: structured outputs + schema validation; “safe completion” patterns",
      "PII & secrets: redaction, logging hygiene, data minimization",
      "Tool calling safety: allowlists, arg validation, SSRF-style risks",
      "A/B testing prompts + retrieval configs; rollout strategy",
      "Model tuning overview: LoRA/finetune vs prompt/RAG (high-level, interview-ready)",
    ],
    OPS: [
      "Observability: logs vs metrics vs traces; why each matters in GenAI",
      "What to log: request IDs, tenant/user, token counts, retrieval stats, sources",
      "Latency breakdown: ingest vs retrieve vs rerank vs LLM; p95 thinking",
      "Caching strategy: what is safe to cache (and what is dangerous)",
      "Rate limiting + quotas: cost control and abuse prevention",
      "Resilience: retries/timeouts/circuit breakers/fallback models",
      "Background processing: ingestion, re-embedding, summarization queues",
      "Deployment basics: Docker fundamentals; env config; health checks",
      "Cloud awareness (high-level): AWS primitives (S3, RDS, ECS/Lambda) and trade-offs",
      "SLOs + incident response: alerts, dashboards, runbooks",
    ],
    AGENT: [
      "Agents vs workflows: when agents help, when they’re unnecessary risk",
      "Tool calling: function signatures, schemas, validation and safe defaults",
      "Planner/executor split + step budgeting; stopping conditions",
      "Memory: chat memory vs retrieval memory vs tool-result memory",
      "Tool reliability: retries, idempotency, partial progress, compensation",
      "Human-in-the-loop: approvals and checkpointing (concept)",
      "LangGraph concepts: nodes, edges, state, cycles, durable execution (interview-ready)",
      "Multi-agent patterns: router + specialists (optional; pros/cons)",
      "Security: prompt injection into tools, tool abuse, data exfiltration",
      "Agent eval: success criteria, traces, and failure taxonomy",
    ],
    INT: [
      "Interview framing: clarify requirements + constraints fast",
      "System design outline for GenAI apps (10-minute version)",
      "Trade-offs: chunking, k, rerank, context budget, caching",
      "Testing: what unit/integration tests look like for LLM apps",
      "Metrics to mention: recall@k, p95 latency, cost/request",
      "Failure modes: injection, drift, stale index, outages",
      "Security: permissions, PII, logging, tool allowlists",
      "Behavioral stories: ownership, incident response, trade-offs",
      "Project pitch: 2-minute overview + deep dive",
      "Mock rounds + refine your “default architecture”",
    ],
    AWS: [
      "AWS fundamentals: IAM users/roles/policies; least privilege; creds hygiene",
      "Networking: VPC, subnets, route tables, security groups (what interviews expect)",
      "Compute choices: EC2 vs ECS/Fargate vs Lambda; when to pick what",
      "Storage: S3 basics, lifecycle, encryption, presigned URLs; common pitfalls",
      "Databases: RDS/Postgres basics, backups, read replicas; DynamoDB (high-level)",
      "Observability: CloudWatch logs/metrics/alarms; tracing basics (X-Ray concept)",
      "Deployment: containers to ECS/Fargate (high-level) + env config + secrets",
      "API layer: API Gateway vs ALB; rate limiting and auth patterns",
      "Cost controls: budgets, tagging, request-based costs; LLM cost tie-in",
      "Security review: KMS, secrets manager (concept), audit mindset",
    ],
  };

  const buildTracks = {
    FND: [
      "Bootstrap a FastAPI app with `/health` + `/version` + OpenAPI title/description.",
      "Add `.env` config loading + structured JSON logs + request IDs.",
      "Add `/chat` endpoint (mock LLM) with message schema (role/content) and max length checks.",
      "Add strict response schema for `/chat` (structured output) and consistent error envelope.",
      "Add client wrapper: timeouts + retries + backoff + budget (max tokens/request) (mocked).",
      "Add streaming `/chat/stream` (SSE) returning partial tokens (even mocked) to learn streaming.",
      "Add simple persistence: store conversations + token counts to a local SQLite DB.",
      "Add a CLI script to hit `/chat` and print latency + response size for 10 runs.",
      "Add API-key auth + rate limit (in-memory) to learn abuse control patterns.",
      "Write README: architecture + failure modes + how you’d deploy (Docker later).",
    ],
    RAG: [
      "Implement `/ingest`: accept docs (text + source_id) → chunk → store chunks + metadata in SQLite.",
      "Implement embeddings interface + cache by chunk hash (use a placeholder embedding if needed).",
      "Implement a dev vector index: normalize vectors + cosine top-k; store chunk_id → vector map.",
      "Implement `/retrieve`: return top-k chunks with scores + metadata filters (tenant_id).",
      "Implement `/query`: retrieve + build context + synthesize answer (mock or real LLM).",
      "Add citations: answer includes `citations[]` with chunk_id, source_id, and snippet.",
      "Add reranking: rerank top candidates (simple heuristic) + compare before/after.",
      "Add query rewrite: if query is short/ambiguous, create 2 reformulations and merge results.",
      "Add updates: re-ingest same source replaces previous version; ensure citations map to version.",
      "Add prompt template: must cite sources; must refuse if not supported by citations.",
      "Add streaming `/query/stream` (send citations at end) and handle partial generation safely.",
      "Add retrieval caching with TTL keyed by (query, filters, index_version).",
      "Add context budgeting: cap chunks by token estimate; add optional compression summary step.",
      "Add model routing stub: cheap model for rewrite; stronger model for final answer (config).",
      "Polish API docs + examples for ingest/query; add a demo script that ingests 3 docs and queries 5 questions.",
    ],
    EVAL: [
      "Create `golden.json`: 15–25 queries with expected source_id (and optional chunk hints).",
      "Write eval runner: run `/retrieve` for each query → compute recall@k and MRR; save results.",
      "Add answer checks: verify citations exist; block answers with zero citations unless refusal.",
      "Add injection tests: include 5 injection queries; ensure system refuses or ignores malicious instructions.",
      "Add tool safety scaffolding: tool allowlist + arg schema validation (even if only internal tools).",
      "Add PII redaction before logs: email/phone/keys patterns; ensure logs never store full prompts by default.",
      "Add strict response schemas for `/query` and validate before returning.",
      "Add A/B configs: compare chunk sizes and k values; auto-generate a small report.",
      "Add calibrated refusal: threshold on retrieval score + “no evidence” rule; measure refusal rate in eval.",
      "Write `EVAL_REPORT.md`: top failures + fixes + next experiments (rerank, rewrite, chunking).",
    ],
    OPS: [
      "Add request IDs everywhere + structured logs (include retrieval stats + model choice).",
      "Add metrics endpoint: requests, errors, p50/p95 latency, tokens, cost/request (approx).",
      "Add simple tracing spans: ingest/retrieve/rerank/LLM; return timings in debug mode.",
      "Add safe caching layer: response cache keyed by (tenant, query, index_version) + TTL.",
      "Add rate limiting + quotas: per API key and per tenant; enforce token budget per day (simple).",
      "Add fallback strategy: if LLM fails/timeouts, return citations + a safe summary/refusal.",
      "Move ingest/re-embed to background queue (in-process) and track job status endpoint.",
      "Optimize retrieval path: precomputed norms + vector normalization; avoid recompute per request.",
      "Add Dockerfile + `docker run` instructions; healthcheck endpoint; env vars documented.",
      "Write `RUNBOOK.md`: alerts → diagnosis steps → mitigations; add a tiny load test script and include results.",
    ],
    AGENT: [
      "Define tool contracts (JSON schema): `searchDocs`, `getDocById`, `summarize` (safe, local).",
      "Implement constrained agent loop: allowlist + max steps + max tool calls + stop conditions.",
      "Add planner/executor: planner outputs steps; executor runs tools only and records trace.",
      "Add agent memory: persist only citations + tool outputs + decisions (no raw user secrets).",
      "Add tool failure handling: retries/backoff; safe abort with a user-facing explanation.",
      "Add human checkpoint mode: if confidence low or tool risk high, stop and ask for approval.",
      "Implement a state-machine workflow (LangGraph-like) for: plan → retrieve → draft → verify → final.",
      "Add router: decide between direct answer, RAG, or tools; log decision + features.",
      "Add security guard: refuse tool calls when injection markers or URL-like payloads appear.",
      "Add agent eval: 10 tasks; capture success/fail + trace; summarize failure categories in a report.",
    ],
    INT: [
      "Polish README: setup, architecture diagram (ASCII), and demo examples.",
      "Create a default system design doc: RAG + eval + ops (one-pager).",
      "Record 2-minute pitch for Project A (script text is fine).",
      "Do 2 mock design questions; write your answer outline and refine.",
      "Add a ‘metrics and SLOs’ section to README (p95, recall@k, cost).",
      "Create 10 behavioral STAR stories (bullets) related to your project work.",
      "Run a full end-to-end eval and attach results to the repo as a report.",
      "Create a “failure modes” page and link it in README.",
      "Do 3 timed mock rounds (45 min each across 3 days) and improve weak points.",
      "Final polish: clean APIs, remove dead code, ensure reproducible demo.",
    ],
    AWS: [
      "Create an AWS ‘one-pager’: your service mapped to AWS components (S3/RDS/ECS/ALB/CloudWatch).",
      "Write IAM policies for your app (concept): S3 read, logs write, secrets read; least privilege checklist.",
      "Design VPC layout for your app: public ALB, private app tasks, private DB; security groups rules.",
      "Create a deploy plan: Docker image → registry (concept) → ECS/Fargate; env vars + secrets handling.",
      "Add a production config checklist: timeouts, retries, rate limits, quotas, health checks.",
      "Create CloudWatch-style metrics/alarms list for your app (p95, 5xx, throttles, cost).",
      "Write a cost model: estimate monthly cost drivers (compute, storage, DB, logs) + LLM spend guardrails.",
      "Practice AWS interview drills: explain ECS vs Lambda vs EC2 for your use case.",
      "Write a security review doc: PII handling, encryption at rest, secret rotation, audit logging (concept).",
      "Final cloud story: 2-minute explanation of how you’d deploy and operate your system on AWS.",
    ],
  };

  function dayTitle(day, phaseKey) {
    const phaseName = phases.find((p) => p.key === phaseKey)?.name ?? "Phase";
    const n =
      phaseKey === "FND"
        ? day
        : phaseKey === "RAG"
          ? day - 10
          : phaseKey === "EVAL"
            ? day - 25
            : phaseKey === "OPS"
              ? day - 35
              : phaseKey === "AGENT"
                ? day - 45
                : phaseKey === "INT"
                  ? day - 55
                  : day - 60;
    return `${phaseName} • Day ${n}`;
  }

  function pick(arr, idx) {
    return arr[idx % arr.length];
  }

  function makeJournalPrompts(day, phaseKey) {
    const common = [
      "Write 5 bullets: what you learned + what confused you.",
      "List 3 trade-offs you can explain in 2 minutes.",
      "Record 1 failure mode you hit today and how you’d detect it.",
      "Write 1 interview answer: “How would you design this?” (short outline).",
    ];

    const phaseSpecific = {
      FND: [
        "Explain tokens/context to a beginner in 5 lines.",
        "Write your default LLM API client checklist (timeouts/retries/budgets).",
      ],
      RAG: [
        "Write: why your chunking strategy is reasonable for your documents.",
        "Write: how you’d handle document updates without breaking citations.",
      ],
      EVAL: [
        "Write: what metric you trust most for retrieval and why.",
        "Write: one prompt-injection example and your mitigation.",
      ],
      OPS: [
        "Write: your top 5 logs/metrics you’d want during an outage.",
        "Write: where caching helps vs where it can cause incorrect answers.",
      ],
      AGENT: [
        "Write: when you would refuse to run a tool and why.",
        "Write: your agent stop conditions and safety gates.",
      ],
      INT: [
        "Write: your 2-minute project pitch (problem → approach → results).",
        "Write: one story showing ownership and one showing trade-off judgment.",
      ],
    };

    return [
      pick(phaseSpecific[phaseKey] ?? common, day),
      pick(common, day + 1),
      pick(common, day + 2),
    ];
  }

  function makePractice(day, phaseKey) {
    const practice = {
      FND: [
        "Explain: tokens vs context window (2 minutes, out loud).",
        "Draw: a minimal LLM app architecture (client → API → model).",
        "List: 5 ways LLM calls fail and how you handle each.",
        "Write: a Pydantic model for a chat request/response (by hand).",
      ],
      RAG: [
        "Sketch: RAG data flow with citations (ingest → query).",
        "Choose: chunk size/overlap for a doc type you know; justify.",
        "Design: retrieval filters for permissions (tenant/team).",
        "Argue: when reranking matters (example).",
      ],
      EVAL: [
        "Create: 5 golden Q/A pairs and label expected sources.",
        "Write: how to compute recall@k in one paragraph.",
        "Threat model: 3 prompt-injection patterns and defenses.",
        "Decide: when to refuse (“don’t know”) vs answer.",
      ],
      OPS: [
        "List: 10 metrics/log fields for a GenAI API.",
        "Estimate: cost/request for your RAG (rough).",
        "Design: rate limit strategy (per user, per tenant, burst).",
        "Explain: p95 latency breakdown and how to reduce it.",
      ],
      AGENT: [
        "Define: 2 tools with strict schemas and validation rules.",
        "Design: agent loop with max steps + stop conditions.",
        "Explain: planner/executor split and why it helps.",
        "Write: 3 ways tool use can be exploited and mitigations.",
      ],
      INT: [
        "Do: 10-minute system design outline for ‘RAG for internal docs’.",
        "Do: 10-minute outline for ‘support copilot with escalation’.",
        "Answer: ‘How do you evaluate and monitor this system?’",
        "Answer: ‘How do you prevent hallucinations and injection?’",
      ],
      AWS: [
        "Draw: VPC diagram for your app (public ALB, private tasks, private DB).",
        "Explain: IAM role vs policy vs user (60 seconds).",
        "Choose: ECS/Fargate vs Lambda vs EC2 for your service; justify in 5 bullets.",
        "List: 5 CloudWatch alarms you would set for your API.",
      ],
    };
    const items = practice[phaseKey] ?? practice.FND;
    return [pick(items, day), pick(items, day + 2)];
  }

  function makeSelfTest(day, phaseKey) {
    const tests = {
      FND: [
        "What is an embedding, and why is cosine similarity used?",
        "Name 3 decoding parameters and what changing them does.",
        "What does idempotency mean for an API call, and why do we care?",
      ],
      RAG: [
        "What is chunking, and what breaks if chunks are too large/small?",
        "What is recall@k measuring in retrieval?",
        "How do citations reduce hallucination risk but not eliminate it?",
      ],
      EVAL: [
        "What makes an eval dataset ‘good’ for regression testing?",
        "Give 2 ways LLM-as-judge can mislead you.",
        "What is prompt injection, and what is the safest default behavior?",
      ],
      OPS: [
        "What’s the difference between logs, metrics, and traces?",
        "Name 4 fields you would log for every LLM request.",
        "Where can caching create correctness bugs in multi-tenant systems?",
      ],
      AGENT: [
        "Why do agents need step budgets and stop conditions?",
        "What’s a tool allowlist and how does it reduce risk?",
        "What should you persist in agent memory vs avoid persisting?",
      ],
      INT: [
        "Give your 2-minute pitch for your project.",
        "List 5 failure modes and the metric/alert for each.",
        "State your default GenAI system design template (bullets).",
      ],
      AWS: [
        "What’s the difference between IAM role and IAM user? When do you use each?",
        "Explain security groups vs subnets in one minute.",
        "Pick ECS/Fargate vs Lambda vs EC2 for your app and justify.",
      ],
    };
    return [
      pick(tests[phaseKey], day),
      pick(tests[phaseKey], day + 1),
      pick(tests[phaseKey], day + 2),
    ];
  }

  function makeBuildChecklist(dayObj) {
    const phaseKey = dayObj.phaseKey;
    const primary = (dayObj.build ?? [])[0] ?? "Implement today’s build task.";
    const secondary = (dayObj.build ?? [])[1] ?? "Polish and verify.";

    const common = [
      "Set a 60-minute timer and define the smallest deliverable for today.",
      `Implement the core change: ${primary}`,
      `Add one improvement or edge-case handling: ${secondary}`,
      "Run a quick manual test (1–3 example requests) and note the result.",
      "Write 3 bullets in your journal: what changed, what broke, what you’d do next.",
    ];

    const byPhase = {
      FND: [
        "Set a 60-minute timer and define the smallest deliverable for today.",
        `Implement the core change: ${primary}`,
        "Add strict validation: input limits + consistent error envelope.",
        "Add one log line that would help debug failures (include request ID).",
        "Do 3 manual calls (happy path, invalid input, timeout simulation) and record results.",
      ],
      RAG: [
        "Set a 60-minute timer and define the smallest RAG improvement for today.",
        `Build the pipeline piece: ${primary}`,
        "Add/confirm metadata fields (source_id, chunk_id, tenant_id, version).",
        "Run 5 queries and inspect retrieved chunks + citations for correctness.",
        `Add one correctness guard: ${secondary}`,
      ],
      EVAL: [
        "Pick 10 golden queries to focus on today (or extend the dataset by 3).",
        `Implement the eval/guardrail: ${primary}`,
        "Add a failing test case first, then make it pass.",
        "Record before/after metrics (recall@k, refusal rate, citation coverage).",
        `Write a 5-line eval note: what improved + what still fails (${secondary}).`,
      ],
      OPS: [
        "Define the SLO you’re improving (p95 latency, cost/request, error rate).",
        `Implement the ops feature: ${primary}`,
        "Add one metric and one alert condition you’d use in production.",
        "Run a mini load check (10–20 calls) and record timing distribution.",
        `Harden one risk area: ${secondary}`,
      ],
      AGENT: [
        "Define the agent boundary: allowed tools + max steps + stop condition.",
        `Implement the agent feature: ${primary}`,
        "Add strict tool argument validation + allowlist check.",
        "Run 5 tasks and capture the trace (decisions + tool calls).",
        `Add one safety gate or eval: ${secondary}`,
      ],
      INT: [
        "Pick today’s interview question (RAG design / eval / ops).",
        `Produce one artifact: ${primary}`,
        "Do one 10-minute whiteboard outline (requirements → design → metrics → failures).",
        "Record a 2-minute answer out loud; tighten to fewer bullets.",
        `Fix one weak point in your materials: ${secondary}`,
      ],
      AWS: [
        "Pick today’s AWS topic and map it to your app (1 diagram or 10 bullets).",
        `Write/build the artifact: ${primary}`,
        "Add one ‘interview answer’: trade-offs + failure modes + security considerations.",
        "Do 3 flash answers (60 seconds each): IAM, VPC, compute choice.",
        `Update your cloud one-pager with what you learned: ${secondary}`,
      ],
    };

    return byPhase[phaseKey] ?? common;
  }

  const PLAN_DAYS = Array.from({ length: 70 }, (_, i) => {
    const day = i + 1;
    const phase = phaseForDay(day);
    const phaseKey = phase.key;

    const learnIdx =
      phaseKey === "FND"
        ? day - 1
        : phaseKey === "RAG"
          ? day - 11
          : phaseKey === "EVAL"
            ? day - 26
            : phaseKey === "OPS"
              ? day - 36
              : phaseKey === "AGENT"
                ? day - 46
                : day - 56;

    return {
      day,
      phaseKey,
      phaseName: phase.name,
      title: dayTitle(day, phaseKey),
      learn: [pick(learnTracks[phaseKey], learnIdx), pick(learnTracks[phaseKey], learnIdx + 3)],
      build: [pick(buildTracks[phaseKey], learnIdx), pick(buildTracks[phaseKey], learnIdx + 4)],
      journal: makeJournalPrompts(day, phaseKey),
      practice: makePractice(day, phaseKey),
      selfTest: makeSelfTest(day, phaseKey),
    };
  });

  for (const d of PLAN_DAYS) d.buildChecklist = makeBuildChecklist(d);

  const override = new Map(
    [
      [
        1,
        {
          title: "Foundations • Day 1 (Kickoff)",
          learn: ["What is an LLM app? Core components and constraints.", "Tokens vs context window; what truncation looks like."],
          build: ["Create repo structure + FastAPI health endpoint.", "Write a 1-page “LLM app anatomy” note in your journal."],
          selfTest: ["Define context window in 1 sentence.", "What breaks when prompts exceed context?", "What would you log for a request?"],
        },
      ],
      [
        11,
        {
          title: "RAG Build • Day 1 (First ingestion)",
          learn: ["RAG architecture: ingest → index → retrieve → answer.", "Chunking strategies: headings + overlap + metadata."],
          build: ["Implement `/ingest` to chunk + store chunks with source metadata.", "Add a tiny sample docs folder (3 docs) and ingest them."],
        },
      ],
      [
        16,
        {
          title: "RAG Build • Day 6 (First real query)",
          learn: ["Retrieval: top-k and why similarity scores can lie.", "Citations: mapping chunks to sources and building trust."],
          build: ["Implement `/query` retrieval + return top-k chunks with scores.", "Add basic citations fields in the response schema."],
        },
      ],
      [
        26,
        {
          title: "Eval + Guardrails • Day 1 (Golden set)",
          learn: ["Offline eval: what to freeze and why regressions happen.", "Retrieval metrics: recall@k and what it actually means."],
          build: ["Create `golden.json` with 10 questions + expected source doc IDs.", "Write a script to run those queries and record retrieved IDs."],
        },
      ],
      [
        36,
        {
          title: "Observability + Perf • Day 1 (Visibility)",
          learn: ["Logs vs metrics vs traces (and what each answers).", "Latency breakdown: where time goes in RAG."],
          build: ["Add request IDs and stage timing (retrieve/LLM) to logs.", "Add token/cost fields to responses (even if mocked)."],
        },
      ],
      [
        46,
        {
          title: "Agents + Orchestration • Day 1 (Constrained loop)",
          learn: ["Agents: when to use them and when not to.", "Tool contracts: schemas, allowlists, validation."],
          build: ["Define 1 tool schema (e.g., `searchDocs`) and validate args.", "Implement a max-steps agent loop (even with a stub model)."],
        },
      ],
      [
        56,
        {
          title: "Interview Sprint • Day 1 (Default design)",
          learn: ["Interview outline: requirements → architecture → metrics → failures → trade-offs.", "Your default GenAI architecture template."],
          build: ["Write a 1-page default design doc for ‘RAG for internal docs’.", "Practice a 10-minute explanation out loud; refine bullets."],
        },
      ],
      [
        70,
        {
          title: "AWS + Deployment • Day 10 (Final cloud story)",
          learn: ["Security review: KMS, secrets manager (concept), audit mindset", "Interview framing: clarify requirements + constraints fast"],
          build: ["Final cloud story: 2-minute explanation of how you’d deploy and operate your system on AWS.", "Polish README + deployment section + runbook links."],
          practice: ["Deliver your 2-minute pitch twice (record if possible).", "Answer: ‘How do you evaluate, monitor, and secure this system?’"],
          selfTest: ["Pick ECS/Fargate vs Lambda vs EC2 for your app and justify.", "List 5 CloudWatch alarms you’d set.", "State your biggest trade-off and why."],
        },
      ],
    ].map(([day, patch]) => [String(day), patch])
  );

  for (const d of PLAN_DAYS) {
    const p = override.get(String(d.day));
    if (p) Object.assign(d, p);
  }

  for (const d of PLAN_DAYS) d.buildChecklist = makeBuildChecklist(d);

  window.PLAN_DAYS = PLAN_DAYS;
  window.PLAN_PHASES = phases;
})();

