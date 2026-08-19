# Harborlight Regional DC — request for proposal (synthetic)

> Synthetic bid pack for the public sample. No live plant, no customer brand, no real prices.

Issuer: **Harborlight Distribution Co.** (fictional)
Site: Regional distribution center, 48,000 pallet locations
Due: 2026-09-30
Envelope: technical proposal only (commercial envelope is out of scope for this sample)

## 1. Scope of work

Supply and configure a **warehouse planning and execution** layer for inbound ASN, slotting, wave picking, and a finite-capacity labor plan. The issuer already has WMS transactions; this bid is for the planning copilot that sits on top.

The vendor must:

- Ingest daily demand and dock calendars
- Produce a 7-day labor and wave plan
- Flag capacity breaches before the shift starts
- Export the plan as a board the floor supervisor can read

## 2. Functional requirements

1. ASN-to-slot recommendation within 15 minutes of inbound EDI.
2. Wave building that respects pick-face constraints and carrier cut-off times.
3. A finite-capacity view of picking, packing, and staging labor by hour.
4. Exception queue for late ASN, short pick, and dock conflict.
5. Read-only glossary of planning terms used on the floor (wave, cut-off, slotting).

## 3. Non-functional requirements

- Plan refresh ≤ 60 seconds for the sample volume (8,000 lines / day).
- Role-based access: planner, supervisor, read-only auditor.
- Audit log of every plan publish (who / when / which wave set).
- On-prem or private VPC; no training on issuer data.

## 4. Implementation and cut-over

- Parallel run against the current spreadsheet plan for two peak weeks.
- Data mapping for SKU, location, and carrier calendars.
- Hypercare window of ten business days after go-live.

## 5. Training and support

- Supervisor workshop (one day) and planner workshop (two days).
- Runbook for cut-off misses and labor breach alerts.
- Named vendor contact during hypercare.

## 6. Proposal format

Respond with:

1. Understanding of scope
2. Functional response (trace each numbered requirement)
3. Non-functional response
4. Implementation plan
5. Training and support
6. Assumptions and exclusions
