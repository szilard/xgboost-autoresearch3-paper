| LLM | dropped the day-of-month category | numeric day of year | holiday features | dropped the month category | mean holdout, dropped | mean holdout, kept | difference |
|---------|------------|-----------|------------|------------|------------|------------|---------------|
| Astra | 19 | 11 | 15 | 12 | 0.6867 | 0.6836 | +0.0031 |
| Sol | 13 | 16 | 3 | 9 | 0.6852 | 0.6823 | +0.0028 |
| Luna | 4 | 5 | 2 | 5 | 0.6834 | 0.6800 | +0.0034 |

Table: How the 20 final models of each LLM handle the calendar, from an audit of their train.py. Means are holdout AUCs of the runs that dropped or kept the day-of-month category (Astra kept it in one run).
