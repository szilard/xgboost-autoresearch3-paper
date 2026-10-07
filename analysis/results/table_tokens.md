<!-- analysis/tokens.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 21:21Z -->

## Token usage per run (mean, with min to max), from the session logs

| LLM | token_count events | input tokens, M | cached share of input | output tokens, K | of which reasoning, K | list-price projection per run, USD | USD per M input tokens, effective |
|--------|----------------|-------------------|----------|---------------|---------------|----------------------|--------------|
| Astra | 126 (100 to 157) | 16.0 (12.2 to 21.4) | 98.1% | 89 (69 to 105) | 50 (34 to 63) | 23.17 (18.79 to 29.01) | 1.44 |
| Sol | 304 (250 to 371) | 34.6 (21.9 to 51.8) | 99.1% | 65 (48 to 92) | 25 (18 to 45) | 8.11 (5.37 to 11.69) | 0.23 |
| Luna | 298 (185 to 415) | 37.1 (22.6 to 55.2) | 98.6% | 104 (91 to 121) | 65 (51 to 79) | 0.47 (0.31 to 0.65) | 0.01 |

Totals are the last cumulative `total_token_usage` of each session (checked to equal the sum of the per-event usage). The projection applies OpenAI's list prices per million tokens (input / cached input / output: Astra 10.0 / 1.0 / 50.0; Sol 2.0 / 0.2 / 10.0; Luna 0.1 / 0.01 / 0.5) to those totals. It is a projection, not a bill: the runs ran on a ChatGPT subscription. Reasoning tokens are a subset of output tokens.
