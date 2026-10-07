import csv, statistics as st, itertools, random
from pathlib import Path
R = Path("/home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs/run-multi")
groups = {"gpt-6-luna":"luna6_n20","gpt-6-sol":"sol6_n20","gpt-6-astra":"astra6_n20"}
data = {}
for m,g in groups.items():
    rows = list(csv.DictReader(open(R/g/"holdout_auc.tsv"), delimiter="\t"))
    data[m] = [dict(h=float(r["holdout_auc"]), e=float(r["eval_auc"]), gap=float(r["gap"]), x=int(r["experiments"]), run=r["run"], valid=r["valid"], flags=r["flags"]) for r in rows if r["valid"] in ("yes","caveat")]
try:
    from scipy import stats
    tq = lambda n: stats.t.ppf(0.975, n-1)
except Exception:
    tq = lambda n: 2.093 if n==20 else 1.96
import numpy as np
BASE=0.6725
print("model  n  mean  sd  min  p10  median  p90  max  ci95  range  impr  caveats  exp_mean  exp_min  exp_max  eval_mean  gap_mean  gap_sd")
for m,d in data.items():
    h=np.array([r["h"] for r in d]); n=len(h)
    p10,p90=np.percentile(h,[10,90],method="nearest")
    half=tq(n)*h.std(ddof=1)/np.sqrt(n)
    print(f"{m} {n} {h.mean():.4f} {h.std(ddof=1):.4f} {h.min():.4f} {p10:.4f} {np.median(h):.4f} {p90:.4f} {h.max():.4f} [{h.mean()-half:.4f},{h.mean()+half:.4f}] {h.max()-h.min():.4f} {h.mean()-BASE:.4f} {sum(r['valid']=='caveat' for r in d)} {np.mean([r['x'] for r in d]):.1f} {min(r['x'] for r in d)} {max(r['x'] for r in d)} {np.mean([r['e'] for r in d]):.4f} {np.mean([r['gap'] for r in d]):.4f} {np.std([r['gap'] for r in d],ddof=1):.4f}")
print("\nall 60 beat starter on holdout:", all(r["h"]>BASE for d in data.values() for r in d))
# pairwise win prob with ties half + bootstrap
rng=np.random.default_rng(1); NB=10000
models=sorted(data,key=lambda m:-np.mean([r["h"] for r in data[m]]))
print("\npairwise (model1 better on average):")
for a,b in itertools.combinations(models,2):
    A=np.array([r["h"] for r in data[a]]); B=np.array([r["h"] for r in data[b]])
    win=(A[:,None]>B[None,:])+0.5*(A[:,None]==B[None,:]); p=win.mean()
    ia=rng.integers(0,len(A),(NB,len(A))); ib=rng.integers(0,len(B),(NB,len(B)))
    boot=win[ia[:,:,None],ib[:,None,:]].mean(axis=(1,2)); lo,hi=np.percentile(boot,[2.5,97.5])
    # Welch t-test and Mann-Whitney
    try:
        from scipy import stats as ss
        t=ss.ttest_ind(A,B,equal_var=False); u=ss.mannwhitneyu(A,B,alternative="two-sided")
        extra=f" welch_t p={t.pvalue:.2e} MWU p={u.pvalue:.2e}"
    except Exception: extra=""
    print(f"  {a} vs {b}: P(win)={p:.3f} [{lo:.3f},{hi:.3f}] mean diff={A.mean()-B.mean():+.4f}{extra}")
# overlap claims
L=np.array([r["h"] for r in data["gpt-6-luna"]]); S=np.array([r["h"] for r in data["gpt-6-sol"]]); A_=np.array([r["h"] for r in data["gpt-6-astra"]])
print("\nLuna best beats how many Sol runs:", (S<L.max()).sum(), "ties:", (S==L.max()).sum(), "; beats how many Astra runs:", (A_<L.max()).sum())
print("Sol best beats how many Astra runs:", (A_<S.max()).sum(), "ties:", (A_==S.max()).sum())
# pooled sd ratio: range / improvement
for m in models:
    h=np.array([r["h"] for r in data[m]]); print(f"{m}: range/improvement = {(h.max()-h.min())/(h.mean()-BASE):.2f}")
print("best-worst model mean diff:", f"{np.mean(A_)-np.mean(L):.4f}")
# runs needed per arm: 16 sd^2/gap^2 (80% power, 5% two-sided)
sd=np.median([np.std([r['h'] for r in data[m]],ddof=1) for m in models])
for a,b in itertools.combinations(models,2):
    gap=abs(np.mean([r['h'] for r in data[a]])-np.mean([r['h'] for r in data[b]]))
    print(f"runs/arm to detect {a} vs {b} gap {gap:.4f} with sd {sd:.4f}: {16*sd**2/gap**2:.0f}")
# best-of-k by eval AUC, simulated with replacement
print("\nbest-of-k (choose by eval AUC, report holdout): k -> median, mean, p5, p95")
for m in models:
    d=data[m]; e=np.array([r["e"] for r in d]); h=np.array([r["h"] for r in d])
    for k in (1,2,3,5,10):
        idx=rng.integers(0,len(d),(20000,k)); pick=idx[np.arange(20000), e[idx].argmax(axis=1)]; hk=h[pick]
        print(f"  {m} k={k}: median {np.median(hk):.4f} mean {hk.mean():.4f} p5 {np.percentile(hk,5):.4f} p95 {np.percentile(hk,95):.4f}")
# rank correlation eval vs holdout within model
try:
    from scipy import stats as ss
    for m in models:
        e=[r["e"] for r in data[m]]; h=[r["h"] for r in data[m]]
        print(f"{m}: spearman(eval,holdout) = {ss.spearmanr(e,h).correlation:.2f}; spearman(experiments,holdout) = {ss.spearmanr([r['x'] for r in data[m]],h).correlation:.2f}")
    allh=[r["h"] for m in models for r in data[m]]; allx=[r["x"] for m in models for r in data[m]]
    f=ss.f_oneway(*[[r["h"] for r in data[m]] for m in models]); kw=ss.kruskal(*[[r["h"] for r in data[m]] for m in models])
    print(f"one-way ANOVA p={f.pvalue:.2e}; Kruskal p={kw.pvalue:.2e}")
except Exception as ex: print("scipy missing:",ex)

# ---- time course per run ----
import json
print("\n=== time course (per model medians) ===")
def run_course(rd):
    clock=json.loads((rd/"timing"/"clock.json").read_text()); start=clock["start"]; stop=clock["stop"]
    runs=list(csv.DictReader(open(rd/"timing"/"runs.tsv"),delimiter="\t"))
    end={}
    for r in runs:
        if r["status"]=="ok": end.setdefault(r["commit"],(float(r["end"])-start)/60)
    hs=list(csv.DictReader(open(rd/"holdout_scores.tsv"),delimiter="\t"))
    path=[(end[r["commit"]],float(r["holdout_auc"])) for r in hs if r["status"]=="keep" and r["holdout_auc"] not in ("","N/A","CRASH") and r["commit"] in end]
    nkeep=sum(r["status"]=="keep" for r in hs); ndis=sum(r["status"]=="discard" for r in hs); ncr=sum(r["status"]=="crash" for r in hs)
    def at(t):
        v=[a for m,a in path if m<=t]; return v[-1] if v else BASE
    first_gain=next((m for m,a in path if a>BASE+0.0005),None)
    # time to reach within 0.002 of final
    final=path[-1][1] if path else BASE
    t_near=next((m for m,a in path if a>=final-0.002),None)
    # longest plateau (gap between consecutive keeps or until end)
    times=[m for m,_ in path]+[(stop-start)/60]
    plateau=max(b-a for a,b in zip(times,times[1:])) if len(times)>1 else 0
    # downward steps (holdout decreases on a keep)
    downs=sum(1 for (m1,a1),(m2,a2) in zip(path,path[1:]) if a2<a1)
    rep=(rd/"report.txt").read_text(); import re
    ai=float(re.search(r"AI:\s+\S+\s+([\d.]+)%",rep).group(1)); nruns=int(re.search(r"\((\d+) runs:",rep).group(1))
    xg=float(re.search(r"XGBoost runs:\s+\S+\s+([\d.]+)%",rep).group(1))
    return dict(nkeep=nkeep,ndis=ndis,ncr=ncr,first_gain=first_gain,t_near=t_near,plateau=plateau,downs=downs,ai=ai,xg=xg,nruns=nruns,
                h15=at(15),h30=at(30),h45=at(45),final=final,best_final=(max(a for _,a in path)==final) if path else None, keeps_down_final=final<max(a for _,a in path) if path else None)
import statistics
for m,g in groups.items():
    cs=[run_course(R/g/r["run"]) for r in data[m]]
    med=lambda k: statistics.median([c[k] for c in cs if c[k] is not None])
    mean=lambda k: statistics.mean([c[k] for c in cs if c[k] is not None])
    print(f"{m}: keeps mean {mean('nkeep'):.1f} discards {mean('ndis'):.1f} crashes {mean('ncr'):.1f}; harness runs mean {mean('nruns'):.1f}; AI share mean {mean('ai'):.1f}% (xgb {mean('xg'):.1f}%)")
    print(f"   first gain (>+0.0005 holdout) median {med('first_gain'):.1f} min; holdout median at 15/30/45/60 min: {med('h15'):.4f}/{med('h30'):.4f}/{med('h45'):.4f}/{med('final'):.4f}")
    print(f"   median longest plateau {med('plateau'):.1f} min (max {max(c['plateau'] for c in cs):.1f}); runs with >=20 min plateau: {sum(c['plateau']>=20 for c in cs)}; mean downward holdout steps per run {mean('downs'):.2f}; runs whose final kept model is below their best kept model on holdout: {sum(bool(c['keeps_down_final']) for c in cs)}")
    print(f"   time to within 0.002 of final: median {med('t_near'):.1f} min")
