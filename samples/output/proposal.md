# Harborlight Regional DC — technical proposal (synthetic)

> Generated offline from `samples/rfp/harborlight-dc-rfp.md`. Replace this stub with a model call later; the outline is the contract.

## Understanding of scope

*RFP source:* 1. Scope of work

Response traces the RFP as follows:

- **Trace:** Ingest daily demand and dock calendars
- **Trace:** Produce a 7-day labor and wave plan
- **Trace:** Flag capacity breaches before the shift starts
- **Trace:** Export the plan as a board the floor supervisor can read

## Functional response

*RFP source:* 2. Functional requirements

Response traces the RFP as follows:

- **Trace:** ASN-to-slot recommendation within 15 minutes of inbound EDI.
- **Trace:** Wave building that respects pick-face constraints and carrier cut-off times.
- **Trace:** A finite-capacity view of picking, packing, and staging labor by hour.
- **Trace:** Exception queue for late ASN, short pick, and dock conflict.
- **Trace:** Read-only glossary of planning terms used on the floor (wave, cut-off, slotting).

## Non-functional response

*RFP source:* 3. Non-functional requirements

Response traces the RFP as follows:

- **Trace:** Plan refresh ≤ 60 seconds for the sample volume (8,000 lines / day).
- **Trace:** Role-based access: planner, supervisor, read-only auditor.
- **Trace:** Audit log of every plan publish (who / when / which wave set).
- **Trace:** On-prem or private VPC; no training on issuer data.

## Implementation plan

*RFP source:* 4. Implementation and cut-over

Response traces the RFP as follows:

- **Trace:** Parallel run against the current spreadsheet plan for two peak weeks.
- **Trace:** Data mapping for SKU, location, and carrier calendars.
- **Trace:** Hypercare window of ten business days after go-live.

## Training and support

*RFP source:* 5. Training and support

Response traces the RFP as follows:

- **Trace:** Supervisor workshop (one day) and planner workshop (two days).
- **Trace:** Runbook for cut-off misses and labor breach alerts.
- **Trace:** Named vendor contact during hypercare.

## Assumptions and exclusions

*RFP source:* Proposal format

Response traces the RFP as follows:

- **Trace:** Sample is synthetic. No live inventory, no customer brand.
- **Trace:** Commercial envelope (price, bonds) is out of scope for this public slice.
