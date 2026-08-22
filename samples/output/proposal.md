# Harborlight Regional DC — technical proposal (synthetic)

> Generated offline from `samples/rfp/harborlight-dc-rfp.md`. Replace this stub with a model call later; the outline is the contract.

## Understanding of scope

*RFP source:* 1. Scope of work

Response traces the RFP as follows:

- **REQ-S1:** Ingest daily demand and dock calendars
- **REQ-S2:** Produce a 7-day labor and wave plan
- **REQ-S3:** Flag capacity breaches before the shift starts
- **REQ-S4:** Export the plan as a board the floor supervisor can read

## Functional response

*RFP source:* 2. Functional requirements

Response traces the RFP as follows:

- **REQ-F1:** ASN-to-slot recommendation within 15 minutes of inbound EDI.
- **REQ-F2:** Wave building that respects pick-face constraints and carrier cut-off times.
- **REQ-F3:** A finite-capacity view of picking, packing, and staging labor by hour.
- **REQ-F4:** Exception queue for late ASN, short pick, and dock conflict.
- **REQ-F5:** Read-only glossary of planning terms used on the floor (wave, cut-off, slotting).

## Non-functional response

*RFP source:* 3. Non-functional requirements

Response traces the RFP as follows:

- **REQ-N1:** Plan refresh ≤ 60 seconds for the sample volume (8,000 lines / day).
- **REQ-N2:** Role-based access: planner, supervisor, read-only auditor.
- **REQ-N3:** Audit log of every plan publish (who / when / which wave set).
- **REQ-N4:** On-prem or private VPC; no training on issuer data.

## Implementation plan

*RFP source:* 4. Implementation and cut-over

Response traces the RFP as follows:

- **REQ-I1:** Parallel run against the current spreadsheet plan for two peak weeks.
- **REQ-I2:** Data mapping for SKU, location, and carrier calendars.
- **REQ-I3:** Hypercare window of ten business days after go-live.

## Training and support

*RFP source:* 5. Training and support

Response traces the RFP as follows:

- **REQ-T1:** Supervisor workshop (one day) and planner workshop (two days).
- **REQ-T2:** Runbook for cut-off misses and labor breach alerts.
- **REQ-T3:** Named vendor contact during hypercare.

## Assumptions and exclusions

*RFP source:* Proposal format

Response traces the RFP as follows:

- **REQ-A1:** Sample is synthetic. No live inventory, no customer brand.
- **REQ-A2:** Commercial envelope (price, bonds) is out of scope for this public slice.
