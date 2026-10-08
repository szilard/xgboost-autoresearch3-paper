| LLM | dates (UTC) | failed turns | runs with retry waits | runs stopped after the budget | clock, shortest to longest | runs with a context compaction | peak memory, GiB |
|--------|------------------------|----------|--------|-----------|----------------------|---------------|---------------|
| Astra | 2026-10-06 to 2026-10-07 | 1 | 1 | 4 | 58m42s–61m18s | 11 | 3.4–16.5 |
| Sol | 2026-10-05 to 2026-10-06 | 13 | 4 | 2 | 58m26s–60m59s | 2 | 3.6–11.7 |
| Luna | 2026-10-05 to 2026-10-06 | 0 | 0 | 0 | 58m31s–59m42s | 12 | 3.6–12.0 |

Table: Operational summary. Failed turns ended with the service error "model at capacity" and were retried; the clock kept running. Every run's agent stopped the clock itself; the clock could exceed the hour when the agent's wrap-up came after its last status check. Nothing was killed at the 24 GiB memory cap.
