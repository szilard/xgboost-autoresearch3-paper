| minute | the agent's description of the kept commit | eval AUC | holdout AUC |
|------|--------------------------------------------------|---------|---------|
| 1 | baseline | 0.6743 | 0.6725 |
| 2 | simplify prepare; same features and faster evaluation | 0.6743 | 0.6725 |
| 3 | depth 4; 400 trees; stronger leaf and L2 regularization | 0.6800 | 0.6784 |
| 4 | remove day-of-month calendar feature | 0.6812 | 0.6797 |
| 6 | remove month; retain weekday and schedule inputs | 0.6837 | 0.6810 |
| 7 | fixed category codes; identical AUC and faster evaluation | 0.6837 | 0.6810 |
| 8 | 200 rounds; equal AUC with a smaller faster model | 0.6837 | 0.6814 |
| 12 | departure offsets from train-fitted origin/route/carrier-origin medians | 0.6841 | 0.6824 |
| 19 | balance class weights within each training month | 0.6842 | 0.6822 |
| 28 | equal blend of schedule and geography classifiers | 0.6843 | 0.6823 |
| 29 | three fixed seeds for each schedule/geography representation | 0.6845 | 0.6823 |
| 30 | remove geography; equal AUC with half the ensemble | 0.6845 | 0.6823 |
| 37 | 400 rounds at learning rate 0.025 | 0.6846 | 0.6825 |
| 41 | lossguide growth with 16 leaves | 0.6848 | 0.6828 |
| 48 | narrow Thanksgiving/winter/July-4 relative-date features | 0.6871 | 0.6855 |
| 51 | add Memorial Day and Labor Day offsets | 0.6876 | 0.6857 |
| 52 | shared MLK/Presidents Day relative-date feature | 0.6880 | 0.6857 |
| 54 | remove route-time offset from holiday ensemble | 0.6881 | 0.6857 |
| 55 | remove monthly weighting after adding holiday features | 0.6900 | 0.6880 |

Table: The 19 kept commits of run astra6_n20-1, in order, with the minute of the clock at which each was kept.
