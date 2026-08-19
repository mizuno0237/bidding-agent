# Public vs internal

This GitHub repo is a **sanitized public slice**.

**Never publish**

- Customer RFP / bid packs (named plants, live prices, client brands)
- Filled `.env` files or API keys
- Internal GitLab, Lark approval, or private-registry hostnames
- A git `--mirror` of the internal bidding workbench

**OK to publish**

- Architecture and the RFP → outline → chapter → export flow
- Synthetic bid samples
- An offline pipeline that runs on those samples

**Scan before every push**

```bash
python scripts/scan-secrets.py
```
