| LLM | dates (UTC) | failed turns | runs with retry waits | runs stopped after the budget | clock, min to max | runs with a context compaction | peak memory, GiB |
|--------|------------------------|----------|--------|-----------|----------|---------------|------------|
| Astra | 2026-10-06 to 2026-10-07 | 1 | 1 | 4 | 58–61 min | 11 | 3.4–16.5 |
| Sol | 2026-10-05 to 2026-10-06 | 13 | 4 | 2 | 58–60 min | 2 | 3.6–11.7 |
| Luna | 2026-10-05 to 2026-10-06 | 0 | 0 | 0 | 58–59 min | 12 | 3.6–12.0 |

Table: Operational summary. Failed turns ended with the service error 'model at capacity' and were retried; the clock kept running. Every run's agent stopped the clock itself; the clock could exceed the hour when the agent's wrap-up came after its last status check. Nothing was killed at the 24 GiB memory cap.
