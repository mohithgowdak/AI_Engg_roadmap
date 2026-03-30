# 70-Day GenAI Interview Prep (Private Website)

This folder contains a **simple static website** that renders a **day-by-day 70-day plan**:
- **40 min** learn topics
- **60 min** project/practical implementation
- **20 min** journaling prompts (you keep the journal in your Notes app)

It includes:
- **Private login page** (username/password) so only you can access it
- **Cloud sync** of progress via Supabase (still keeps local fallback)
- **Export** button that outputs progress JSON

## Run it

```bash
npm install
npm run dev
```

Then open `http://localhost:3000/` (you’ll see the login page).

## What to edit
- `plan-data.js` (root copy): plan content
- `public/plan-data.js`: plan content actually served to the browser
- `public/app.js`: UI + localStorage + Supabase sync
- `styles/globals.css`: theme

## Deploy to Vercel
1. Import this folder as a Vercel project.
2. Add **Environment Variables**:
   - `AUTH_USER`: your username
   - `AUTH_PASS`: your password
   - `AUTH_SECRET`: random long string used to sign auth cookie
   - `SUPABASE_URL`: from Supabase project settings
   - `SUPABASE_SERVICE_ROLE_KEY`: from Supabase project settings (**server-side only**)
3. Deploy.

## Supabase setup
Create a table named `progress`:

```sql
create table if not exists public.progress (
  id text primary key,
  data jsonb not null default '{}'::jsonb,
  updated_at_ms bigint not null default 0
);
```

Notes:
- This app uses the fixed row id `default` (single-user).
- Keep the service role key **only** in Vercel env vars (never in the browser).

