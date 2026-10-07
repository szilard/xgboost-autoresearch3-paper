# 08. Decisions only the authors can make

Each item has a recommendation; the default is applied if nothing is decided.

1. **Title.** Keep the blog title (recommended) or one of the alternatives in `01`.
2. **Author order and affiliations.** Blog order (Pafka, Ariño de la Rubia); affiliations as on
   the companion paper (Epoch; Central European University). Confirm.
3. **Short names in prose.** Luna, Sol, Astra after the first mention (recommended); figure
   labels keep the slugs `gpt-6-luna` etc. as the plots already do.
4. **Vendor documentation.** Which official OpenAI pages to cite for the GPT-6 family and for
   Codex CLI's effort levels (the plan found only press coverage). Also whether to mention list
   prices (press: Astra $10/$50, Sol $2/$10, Luna $0.10/$0.50 per million input/output tokens;
   unverified) given that no token counts are reported.
5. **Statistics shown.** Intervals and the head-to-head probabilities only (recommended, as in the
   blog), or also Welch/Mann–Whitney p-values and ANOVA (appendix at most).
6. **Post hoc analyses in the main text or the appendix.** Runs-per-arm approximation (T7),
   best-of-k (T6/F6), experiments-vs-holdout correlation (F9). Recommendation: best-of-k in the
   main text as a short subsection (it supports the second practical consequence); T7 and F9 in
   the appendix.
7. **New computations.** (a) Score the 60 final models on 2007 flights (requires retraining each
   final `train.py`; new S3 slice; a day of work): recommended as future work unless time allows,
   and then as a clearly separate section. (b) Token usage from the session logs: only if the
   slimmed logs carry usage events (check first).
8. **Feature audit depth.** Heuristic script plus a manual check of all 60 files (recommended;
   about an hour) versus the heuristic alone with a caveat.
9. **Wording for the BTS/TranStats items** (astra 7 and 12 HP→US mapping; holiday-season tables):
   "documentation and calendar information, no flight records" and kept (recommended), or a
   sensitivity run without those runs in the appendix.
10. **Companion paper.** Cite in the introduction and related work by design only (the rule in
    `05`). If the authors later want a one-paragraph comparison of magnitudes, that is their
    call; the plan excludes it.
11. **Test runs.** Mention `results/test1`, `test2` and `archive/test1` as development history in
    the appendix (recommended) or omit.
12. **Citation style.** Author-year with natbib (recommended for a 40-reference preprint) or
    numeric.
13. **Toolchain.** Pandoc Markdown (option A, recommended) or plain LaTeX.
14. **arXiv categories.** `cs.LG` primary, cross-list `cs.AI`, `stat.ML`; add `cs.SE`?
15. **Publication of the paper repo.** Public from the start (recommended; the blog and runs are
    already public) or at submission.
16. **Machine wording.** "AWS m8i.2xlarge (8 vCPUs, 32 GB)"; confirm the exact instance type and
    that all 60 runs used the same host.
17. **Example run in the appendix (F8/G).** Which run: astra6_n20-1 (19 keeps, clean, documented in
    `run.md`) or astra6_n20-13 (the best run).
18. **Length.** 10 to 14 pages main text; agree before drafting.
