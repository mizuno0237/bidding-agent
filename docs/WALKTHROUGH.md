# Harborlight sample walkthrough

All files are synthetic. No customer bid.

1. Open [`samples/rfp/harborlight-dc-rfp.md`](../samples/rfp/harborlight-dc-rfp.md). Six headings: scope, functional, non-functional, implementation, training, format.
2. Run the offline job:

```bash
PYTHONPATH=src python -m bidding_agent samples/rfp/harborlight-dc-rfp.md --strict
```

3. Read [`samples/output/outline.json`](../samples/output/outline.json). Each bullet has a stable id (`REQ-F1` …). That id is the contract for a later model call.
4. Read [`samples/output/coverage.json`](../samples/output/coverage.json). `complete: true` on this pack. Delete the training heading and `--strict` exits non-zero — the agent must not invent a training chapter.
5. Read [`samples/output/proposal.md`](../samples/output/proposal.md). Every line is a traced `REQ-*`, not a free-text essay.
6. Read [`samples/output/traceability.md`](../samples/output/traceability.md). `REQ-F1` sits on the functional chapter so a reviewer can jump RFP line → response heading.
7. Read [`samples/output/coverage.md`](../samples/output/coverage.md). Chapter counts (`functional` = 5 on this pack) sit next to the JSON report.

`--strict` is what you show in an interview: *coverage first, then draft*.
