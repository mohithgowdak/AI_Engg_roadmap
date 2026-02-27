---
name: Room System Roadmap
overview: Implement room creation/joining first, then room types (food and general shopping), then an order summary flow optimized for chat-first usage.
todos:
  - id: room-creation-core
    content: Add room create/join/switch/member management with active-room context and invite codes.
    status: pending
  - id: room-types
    content: Add room_type (GENERAL_SHOPPING, FOOD) and type-aware command behavior/help text.
    status: pending
  - id: order-summary
    content: Implement chat-first order summary output for one-click copy/share and provider handoff readiness.
    status: pending
  - id: migrations-compat
    content: Add safe runtime migration/backfill and keep backward-compatible aliases.
    status: pending
  - id: tests-docs
    content: Add tests and update README for room flows, room types, and summary flow.
    status: pending
  - id: product-positioning
    content: Add product positioning notes, MVP boundaries, success metrics, risks, and monetization assumptions to docs.
    status: pending
isProject: false
---

# Room Features Plan (Prioritized)

## Goal

Ship room support in 3 phases: (1) room creation/joining, (2) room types (food + general shopping), (3) order summary output for downstream checkout handling.

## Phase 1: Room Creation (Core)

- Commands:
  - `ROOMCREATE <name>`
  - `ROOMJOIN <code>`
  - `ROOMS`
  - `ROOMSWITCH <room_id_or_name>`
  - `ROOMCODE`
  - `ROOMMEMBERS`
  - `ROOMLEAVE`
  - `ROOMREMOVE <member_name_or_id>`
- Active room context:
  - Scope `ADD`, `MY`, `ALL`, `FAMILY`, `REMOVE*` to active room.
- Data model updates in [d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/app/models.py](d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/app/models.py):
  - `User.active_family_id`
  - role field on `FamilyMember` (`owner|admin|member`)
  - preserve multi-room membership behavior.

## Phase 2: Room Types

- Add `room_type` to room entity:
  - `GENERAL_SHOPPING`
  - `FOOD`
- Create room with type:
  - `ROOMCREATE <name> | <type>`
- Type-aware behavior in [d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/app/main.py](d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/app/main.py):
  - different help text
  - command validation per type
  - output formatting defaults (e.g., FOOD uses grouped order style).

## Phase 3: Order Summary

- Add chat command:
  - `ORDERSUMMARY`
  - optional `ORDERSUMMARY TODAY` for food rooms.
- Summary output contains:
  - item name, qty, mapped person, notes (if present), subtotal lines.
  - grouped view for FOOD rooms (person-wise and consolidated).
- Keep integration-ready handoff:
  - generate clean copy/share block for manual checkout on Swiggy/Zomato/any app.
  - future adapter path for API-based cart push if provider APIs exist.

## Migration and Compatibility

- Startup-safe migration in [d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/app/main.py](d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/app/main.py):
  - add missing columns (`active_family_id`, `room_type`, role fields as needed)
  - backfill default active room for existing users.
- Keep existing aliases so current users are not broken during rollout.

## Testing Plan

- Multi-user chat tests:
  - room create/join/switch
  - typed room creation (`FOOD`, `GENERAL_SHOPPING`)
  - order summary generation correctness.
- Permission tests:
  - owner/admin/member actions.
- Regression tests:
  - old commands still work as aliases.

## Documentation Updates

Update [d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/README.md](d:/New folder/AI_Engg_roadmap/Langchain/07_Final_Project/README.md):

- room command reference (core + typed create).
- room type behavior (food vs general shopping).
- order summary command and copy/share flow.

## Product Strategy Notes (to keep in roadmap docs)

### Positioning and Scope Clarity

- Keep one-line positioning consistent: this is a decision-coordination layer on top of commerce apps.
- Explicitly state non-goals: no payments, no delivery orchestration in MVP.
- Clarify integration reality: link capture and summary generation are guaranteed; direct cart push depends on provider APIs.

### MVP Boundaries

- V1: room create/join/switch + shared add + structured summary.
- V1.5: voting workflow and admin override rules.
- V2: richer room types, recurring flows, and provider adapters.

### Success Metrics

- median time-to-finalize group order.
- percentage of active rooms generating at least one summary per week.
- week-4 room retention.
- average items per room and quantity completeness rate.
- summary-to-manual-checkout conversion proxy (self-reported or tracked via feedback command).

### UX/Workflow Rules

- define role model clearly: owner/admin/member.
- define vote resolution rule (e.g., majority or owner override).
- define conflict behavior (duplicate link, quantity merge, person mapping precedence).
- keep command aliases for low-friction onboarding in chat.

### Risk Register

- provider API limitations for cart push.
- link parsing failures and missing metadata.
- noisy rooms/spam and moderation needs.
- policy changes on messaging platforms.

### Monetization Options

- affiliate/referral attribution where allowed.
- premium room features (advanced summary, reminders, analytics).
- B2B/team subscription for office ordering workflows.
- integration partnerships once usage metrics are proven.

