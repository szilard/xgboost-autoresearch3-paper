| pair | P(first LLM's run wins) | 95% bootstrap interval | difference of means |
|-------------|-----------|---------------|---------------|
| Astra vs Luna | 98% | 93%–100% | +0.0059 |
| Sol vs Luna | 91% | 81%–98% | +0.0035 |
| Astra vs Sol | 80% | 66%–93% | +0.0024 |

Table: Head to head: the probability that a randomly chosen run of the first LLM has a higher holdout AUC than a randomly chosen run of the second, over all 400 pairs of runs, ties counted half. Bootstrap: runs resampled within each LLM, 10,000 resamples. The difference of means is computed before rounding, so it can differ by 0.0001 from the difference of the means in Table 2.
