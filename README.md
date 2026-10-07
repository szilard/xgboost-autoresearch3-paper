# One Run Is Not Enough: How Much AI Agent Results Vary in Data Science, an XGBoost Optimization Study

#### by Szilard Pafka and Eduardo Ariño de la Rubia

The arXiv paper, with the scripts that produce every number, table and figure in it from the 60 archived runs of [xgboost-autoresearch-minimal3-runs](https://github.com/szilard/xgboost-autoresearch-minimal3-runs). The single-run building block is [xgboost-autoresearch-minimal3](https://github.com/szilard/xgboost-autoresearch-minimal3), and the blog post with the main results is [xgboost-autoresearch3](https://szilard.github.io/xgboost-autoresearch3).

- `paper/`: the paper's Markdown source, the generated tables, the build, and the built PDF (`paper/main.pdf`)
- `analysis/`: the analysis scripts and their outputs in `analysis/results/` (see [analysis/README.md](analysis/README.md))
- `figures/`: the figures, as PDF and PNG
- `plan/`: the plan the paper was written from, the authors' decisions and the bibliography checks

To rebuild everything, with the runs repo and the single-run repo checked out next to this one, run `analysis/run_all.sh` and then `make pdf` in `paper/` (needs pandoc and pdflatex).

License: [MIT](LICENSE)
