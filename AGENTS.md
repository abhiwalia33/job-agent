# Project guidance

Build this job-search agent incrementally, one capability per week.

- The model may READ freely (search, fetch, match) but may only PROPOSE consequential actions.
- Nothing consequential runs until the user explicitly approves it. Approval is code, not a prompt.
- Use the canonical `JobPosting` schema; never pass source-specific payloads through the app.
- Add folders only when working code needs them.
- Never commit credentials, CVs or personal email content.
- Do not scrape LinkedIn or XING. Use official APIs and the user's own alert emails.
- The agent loop (week 1) is written by hand by the owner. Claude Code may do CI, tests, Docker, README polish.
