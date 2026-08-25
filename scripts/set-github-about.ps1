# Set GitHub repo About (description + topics). Requires: gh auth login
$ErrorActionPreference = "Stop"
$desc = "RFP-to-proposal document agent: ingest a bid pack, stamp requirement ids, draft only against the outline, fail if coverage is incomplete. Synthetic DC sample. Not a customer bid dump."
$topics = @(
  "ai-agents", "rfp", "proposal", "document-generation", "supply-chain", "python"
)
$topicArgs = $topics | ForEach-Object { "--add-topic"; $_ }
gh repo edit --description $desc @topicArgs
Write-Host "Done. Check: https://github.com/mizuno0237/bidding-agent"
