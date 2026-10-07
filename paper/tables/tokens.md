| LLM | input tokens, millions (min–max) | cached share | output tokens, thousands | of which reasoning | API responses | list-price projection, USD (min–max) |
|--------|----------------|--------|---------|---------|---------|-------------------|
| Astra | 16.0 (12.2–21.4) | 98.1% | 89 | 50 | 126 | 23.17 (18.79–29.01) |
| Sol | 34.6 (21.9–51.8) | 99.1% | 65 | 25 | 304 | 8.11 (5.37–11.69) |
| Luna | 37.1 (22.6–55.2) | 98.6% | 104 | 65 | 298 | 0.47 (0.31–0.65) |

Table: Token usage per run, means over the 20 runs, from the cumulative usage records in the session logs. The projection applies OpenAI's list prices per million tokens (input / cached input / output: Astra 10 / 1 / 50, Sol 2 / 0.20 / 10, Luna 0.10 / 0.01 / 0.50) and is not a bill: the runs ran on a ChatGPT subscription.
