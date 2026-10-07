import re, csv, statistics as st
from pathlib import Path
R = Path("/home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs/run-multi")
BASE=0.6725
for g in ["luna6_n20","sol6_n20","astra6_n20"]:
    rows = {r["run"]: r for r in csv.DictReader(open(R/g/"holdout_auc.tsv"), delimiter="\t")}
    out=[]
    for run,r in rows.items():
        src=(R/g/run/"train.py").read_text()
        # cat_cols list definition(s): take the last assignment
        m=re.findall(r"cat_cols\s*=\s*\[([^\]]*)\]", src)
        catlist = m[-1] if m else ""
        dom_cat = '"DayofMonth"' in catlist or "'DayofMonth'" in catlist
        month_cat = '"Month"' in catlist or "'Month'" in catlist
        holiday = bool(re.search(r"holiday|thanksgiving|christmas", src, re.I))
        doy = bool(re.search(r"day_?of_?year|\bdoy\b|dayofyear", src, re.I))
        out.append((run, float(r["holdout_auc"]), dom_cat, month_cat, holiday, doy))
    n=len(out)
    kept=[o for o in out if o[2]]; dropped=[o for o in out if not o[2]]
    print(f"== {g}: n={n}; DayofMonth still a category in cat_cols: {len(kept)}; dropped: {len(dropped)}; Month category: {sum(o[3] for o in out)}; holiday: {sum(o[4] for o in out)}; day-of-year-ish: {sum(o[5] for o in out)}")
    if kept and dropped:
        print(f"   mean holdout kept {st.mean(o[1] for o in kept):.4f} vs dropped {st.mean(o[1] for o in dropped):.4f} (diff {st.mean(o[1] for o in dropped)-st.mean(o[1] for o in kept):+.4f})")
    print("   runs keeping DayofMonth cat:", [o[0].split('-')[1] for o in kept])
    print("   no cat_cols list found in:", [o[0] for o in out if not re.findall(r"cat_cols\s*=\s*\[", (R/g/o[0]/'train.py').read_text())])
