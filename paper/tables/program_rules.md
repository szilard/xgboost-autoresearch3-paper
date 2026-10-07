> **The task:** predict whether a flight departs 15 or more minutes late (`dep_delayed_15min`, Y/N) from what is known in advance: month, day of month, day of week, scheduled departure time, carrier, origin, destination and distance. The metric is AUC. `data/train.csv` has 200K rows sampled from 2005 flights and `data/eval.csv` has 50K rows from 2006; both are balanced (half delayed, half not). You optimize the AUC on `eval.csv`; after the run the human checks your models on a holdout set that you never see.
>
>
> **Experimentation**
>
> You launch an experiment as: `python3 harness.py run`. It runs `train.py`, times it, kills it if it exceeds the time limits (1 minute for training, 5 minutes for evaluation, see **Timeout**), and refuses to start once the time budget is used up. Do not run `python3 train.py` directly while the clock is running (it will refuse once training is done, before evaluating).
>
> **What you CAN do:**
>
> - Modify `train.py` - this is the only code file you edit (besides your own `output/results.tsv` and `output/research-log.md`). Everything is fair game that will lead to a model that generalizes on unseen data: data preparation, feature engineering, choosing hyperparameters, and model training. You can also implement new features such as early stopping etc.
> - Inspect `data/train.csv` with read-only scratch commands (e.g. `python3 -c ...`) to understand the data. Do not create other code files; everything that affects the model stays in `train.py`.
> - Search the web and read external resources. This is not optional — you MUST do research before relying solely on your own intuition. See the **Research** section below.
>
> **What you CANNOT do:**
>
> - Do not read, run, or modify anything in the `human/` folder: it holds the human-only tools. `human/make_data.py` builds the data splits, including the holdout set.
> - Do not install new packages or add dependencies. You can only use what's already installed.
> - Do not change the evaluation. The final model is trained on `train.csv` and evaluated by the call `save_and_evaluate(model, prepare)` at the end of `train.py`, which must stay the last line. Do not add cross-validation, a retrain on more data, or any other evaluation of your own as the metric.
> - Do not modify the evaluation harness. Do not modify `harness.py`, and do not modify or delete anything in `artifacts/` or `output/timing/`.
> - Do not use any of the data files other than `train.csv`. Only `data/train.csv` may be read in `train.py`; `data/eval.csv` is read by `harness.py` for evaluation only. Never read, open, or inspect `data/holdout.csv` or the source data `2005.csv` and `2006.csv` (the latter contains the holdout rows) in any way, wherever they are stored. If you need a validation set (e.g. for early stopping), split it off `train.csv`. Note that `train.csv` is sampled from 2005 flights while `eval.csv` (and the holdout set) is from 2006, so a validation split off `train.csv` overstates the AUC and can favour more complex models than the eval set does.
> - Do not read, run, or reference `human/score_holdout.py`, `human/score_holdout_all.sh` or `human/plot_auc_history.py`, and do not read their outputs `output/holdout_scores.tsv` and `output/auc_history.png`. These are human-only tools for post-hoc evaluation of experiments against the holdout set. They are never part of the experiment loop. If you find yourself wanting to use them, stop and tell the human immediately — it means something has gone wrong with your understanding of the task.
> - Do not use git to peek at the results of earlier runs: do not look in the git history for `results.tsv`, `holdout_scores.tsv` or any other .tsv, .txt or .png file with results.
> - Do not peek into results in the `results` folder and its sub-folders (archived earlier runs, including their holdout scores).
>
>
>
> **Keep rule**: Keep an experiment only if its Eval AUC, as printed by the harness (4 decimals), is higher than that of the last kept commit. If it is exactly equal, keep it only if the code is simpler or faster (a simplification or clean-up at no cost in AUC). If it is lower, discard it, however small the drop and however much simpler the code. All else being equal, simpler is better: removing something and getting an equal or better result is a great outcome.
>
>
> **The experiment loop**
>
> The experiment runs on a dedicated branch (e.g. `mar5`).
>
> LOOP until the time budget is used up:
>
> 1. Check the clock: `python3 harness.py status`. If it prints `TIME IS UP`, or less than 2 minutes remain, stop the loop and wrap up (see **Time budget**). Otherwise look at the git state: the current branch/commit we're on
> 2. **Choose your next experiment deliberately.** Before touching any code:
>    - Review `output/results.tsv` and recent commits.
>    - State a short **hypothesis**: what you are changing, why you think it will help, and (if applicable) which prior result motivates this step.
>    - Classify the experiment as one of: *follow-up* to a promising result, *ablation/simplification* of a promising result, or *exploration* of a meaningfully different direction.
>    - **Do not** run near-duplicate experiments unless you can state exactly what is different and why it matters. Avoid random-walk behavior and cosmetic variations of the same idea.
>    - If you haven't done web research in the last 10 experiments, or if you hit a plateau (3+ consecutive discards with <0.001 movement), do research now before proposing your next change. See the **Research** section.
> 3. Tune `train.py` with that experimental idea by directly hacking the code.
> 4. git commit `train.py` only (everything in `output/` stays uncommitted; the human archives or deletes it after the run)
> 5. Run the experiment: `python3 harness.py run > output/run.log 2>&1` (redirect everything - do NOT use tee or let output flood your context). Run one experiment at a time.
> 6. Read out the results: `grep "^Eval AUC:" output/run.log`
> 7. If the grep output is empty, the run crashed or timed out (or the time budget is used up). Run `tail -n 50 output/run.log` to read the Python stack trace and attempt a fix. If you can't get things to work after more than a few attempts, give up on that idea and move on.
> 8. Record the results in the tsv (NOTE: do not commit the results.tsv file, leave it untracked by git)
> 9. If Eval AUC improved (higher), or is exactly equal with simpler or faster code (see the **Keep rule**), you "advance" the branch, keeping the git commit
> 10. Otherwise (Eval AUC lower, or equal without a simplification), you discard it: `git reset --hard <hash of the last kept commit>` (the untracked `output/` folder is not affected), then check with `git log --oneline -1` that HEAD is that last kept commit
> 11. **Every 10 experiments** (not counting the baseline), pause and briefly synthesize what you have learned so far: what kinds of changes help, what kinds do not, what your current best theory is about what matters on this dataset, and what direction to try next. Write this synthesis as a short section in `output/research-log.md` to inform subsequent experiments.
>
> The idea is that you are a completely autonomous researcher trying things out. If they work, keep. If they don't, discard. And you're advancing the branch so that you can iterate. If you feel like you're getting stuck in some way, you can rewind but you should probably do this very very sparingly (if ever).
>
>
> **Time budget**: You have 1 hour of wall-clock time from `python3 harness.py start`, counting everything: thinking, research, editing and runs. Within the budget, do NOT pause to ask the human if you should continue. Do NOT ask "should I keep going?" or "is this a good stopping point?". The human might be asleep, or gone from a computer and expects you to keep working until the budget is used up. You are autonomous. If you run out of ideas, think harder - read papers and documentation, re-read the in-scope files for new angles, try combining previous near-misses, try more radical changes to the features or the model setup. Do not wrap up or stop the clock while 2 minutes or more remain.
>
