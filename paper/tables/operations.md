| LLM | dates (UTC) | failed turns | runs with retry waits | runs stopped after the budget | clock, min:s, shortest to longest | runs with a context compaction | peak memory, GiB |
|--------|------------------------|----------|--------|-----------|-------------------|---------------|---------------|
| Astra | 2026-10-06 to 2026-10-07 | 1 | 1 | 4 | 58:42–61:18 | 11 | 3.4–16.5 |
| Sol | 2026-10-05 to 2026-10-06 | 13 | 4 | 2 | 58:26–60:59 | 2 | 3.6–11.7 |
| Luna | 2026-10-05 to 2026-10-06 | 0 | 0 | 0 | 58:31–59:42 | 12 | 3.6–12.0 |

Table: Operational summary. Failed turns ended with the service error 'model at capacity' and were retried; the clock kept running. Every run's agent stopped the clock itself; the clock could exceed the hour when the agent's wrap-up came after its last status check. Nothing was killed at the 24 GiB memory cap.
