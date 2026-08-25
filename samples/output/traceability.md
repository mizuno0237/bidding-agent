# Harborlight Regional DC — requirement traceability (synthetic)

Each `REQ-*` maps to one proposal chapter. The agent does not invent ids.

| Id | Chapter | RFP source | Requirement |
| --- | --- | --- | --- |
| REQ-S1 | Understanding of scope | 1. Scope of work | Ingest daily demand and dock calendars |
| REQ-S2 | Understanding of scope | 1. Scope of work | Produce a 7-day labor and wave plan |
| REQ-S3 | Understanding of scope | 1. Scope of work | Flag capacity breaches before the shift starts |
| REQ-S4 | Understanding of scope | 1. Scope of work | Export the plan as a board the floor supervisor can read |
| REQ-F1 | Functional response | 2. Functional requirements | ASN-to-slot recommendation within 15 minutes of inbound EDI. |
| REQ-F2 | Functional response | 2. Functional requirements | Wave building that respects pick-face constraints and carrier cut-off times. |
| REQ-F3 | Functional response | 2. Functional requirements | A finite-capacity view of picking, packing, and staging labor by hour. |
| REQ-F4 | Functional response | 2. Functional requirements | Exception queue for late ASN, short pick, and dock conflict. |
| REQ-F5 | Functional response | 2. Functional requirements | Read-only glossary of planning terms used on the floor (wave, cut-off, slotting). |
| REQ-N1 | Non-functional response | 3. Non-functional requirements | Plan refresh ≤ 60 seconds for the sample volume (8,000 lines / day). |
| REQ-N2 | Non-functional response | 3. Non-functional requirements | Role-based access: planner, supervisor, read-only auditor. |
| REQ-N3 | Non-functional response | 3. Non-functional requirements | Audit log of every plan publish (who / when / which wave set). |
| REQ-N4 | Non-functional response | 3. Non-functional requirements | On-prem or private VPC; no training on issuer data. |
| REQ-I1 | Implementation plan | 4. Implementation and cut-over | Parallel run against the current spreadsheet plan for two peak weeks. |
| REQ-I2 | Implementation plan | 4. Implementation and cut-over | Data mapping for SKU, location, and carrier calendars. |
| REQ-I3 | Implementation plan | 4. Implementation and cut-over | Hypercare window of ten business days after go-live. |
| REQ-T1 | Training and support | 5. Training and support | Supervisor workshop (one day) and planner workshop (two days). |
| REQ-T2 | Training and support | 5. Training and support | Runbook for cut-off misses and labor breach alerts. |
| REQ-T3 | Training and support | 5. Training and support | Named vendor contact during hypercare. |
| REQ-A1 | Assumptions and exclusions | Proposal format | Sample is synthetic. No live inventory, no customer brand. |
| REQ-A2 | Assumptions and exclusions | Proposal format | Commercial envelope (price, bonds) is out of scope for this public slice. |
