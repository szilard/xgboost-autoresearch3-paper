# arXiv submission

Everything the arXiv form asks for, ready to paste. Build the upload with `make arxiv` in `paper/`;
it writes `paper/arxiv.tar.gz` (main.tex, main.bbl, header.tex, the figure PDFs), which compiles on its
own. Check arXiv's compiled preview before submitting.

**Title**

One Run Is Not Enough: How Much AI Agent Results Vary in Data Science, an XGBoost Optimization Study

**Authors**

Szilard Pafka, Eduardo Ariño de la Rubia

**Abstract** (plain text, 1312 characters; arXiv's limit is 1,920)

AI coding agents can automate much of a data scientist's trial-and-error work, but their runs are not deterministic: given the same task twice, the same agent tries different ideas, in a different order, and delivers a different model. We measure how much that matters. OpenAI's Codex agent was given one hour and identical instructions to improve a starter XGBoost model that predicts flight delays, training on one year of flights and evaluating on the next, and every model it kept was scored afterwards on a holdout set it never saw. We ran it 20 times with each of three large language models (LLMs), gpt-6-luna, gpt-6-sol and gpt-6-astra, 60 fully automated runs in all. Every run improved the starter model, and the three LLMs rank clearly on average. But the runs of each LLM vary about as much as the LLMs differ: the spread from an LLM's worst run to its best exceeds the gap between the best and the worst LLM's averages, and one run of each ranks the two closest LLMs wrongly one time in five. Comparisons of agents, LLMs or prompts therefore need repeated runs and distributions, not single numbers, while a better model can be obtained by running the agent several times and choosing the best run on the evaluation data. The single-run building block and the multi-run orchestrator are open source.

**Comments**

40 pages, 9 figures, 16 tables. Code and data: github.com/szilard/xgboost-autoresearch-minimal3-runs

**Primary category:** cs.SE (Software Engineering)

**Cross-list:** cs.LG (Machine Learning)

**License:** CC BY 4.0

**Before submitting:** tag this repository at the submitted commit (e.g. v1.0), as the three source repositories are.

**After announcement:** add the arXiv link and a "How to cite" block to the blog post and to the README of
the four repositories (plan 07).
