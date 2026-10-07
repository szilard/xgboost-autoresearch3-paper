# Author-list verification for plan/references.bib

Date of check: 2026-10-07.

Scope: the `author` field of all 71 entries in `plan/references.bib`, compared with the primary
source for the version each entry cites: number of authors, order, and spelling (diacritics
included; initials vs full given names and "Last, First" vs "First Last" are not errors).
`zhu2025abc` is excluded (being fixed separately). The five `pafka20*` entries are skipped because
the bib already shows exactly `Pafka, Szilard` and/or `Ari{\~n}o de la Rubia, Eduardo`;
`arino2026identicalruns` was checked anyway. `references.bib` was NOT edited.

Method: arXiv entries were compared against the `citation_author` list of
`https://arxiv.org/abs/<id>` (latest version). Published entries were compared against the
proceedings or publisher page. For those, the first page of the paper PDF from the same
proceedings was also read. Where the page and the PDF disagree, the printed paper was taken as the
version of record (see the notes on chan2024mlebench, bouthillier2021variance, cai2025temporal and
dwork2015generalization). Unreachable publisher pages: dl.acm.org, science.org,
journals.sagepub.com, academic.oup.com, pubs.rsna.org, sciencedirect.com (all HTTP 403);
psycnet.apa.org and jstor.org (bot-check pages); openreview.net (challenge page, API too).
dblp was also unreachable (connection reset). In those cases the Crossref record of the DOI
(deposited by the publisher) and the Semantic Scholar API were used, as noted per row.

**Summary: 65 checked, 64 MATCH, 1 MISMATCH, 0 COULD NOT CHECK** (plus 5 skipped own-work entries
and 1 excluded entry, 71 in total).

| # | key | source opened | result | details |
|---|-----|---------------|--------|---------|
| 1 | pafka2026autoresearch | none | SKIPPED | Own work; bib shows exactly `Pafka, Szilard and Ari{\~n}o de la Rubia, Eduardo`. |
| 2 | pafka2026onerun | none | SKIPPED | Own work; same author field as above. |
| 3 | pafka2026minimal3 | none | SKIPPED | Own work; `Pafka, Szilard`. |
| 4 | pafka2026minimal3runs | none | SKIPPED | Own work; `Pafka, Szilard`. |
| 5 | arino2026identicalruns | arxiv.org/abs/2609.33812 | MATCH | 2 authors: Eduardo Ariño de la Rubia, Szilard Pafka. |
| 6 | dataexpo2009 | api.datacite.org/dois/10.7910/DVN/HG7NV7; Harvard Dataverse API | MATCH | No `author` field in bib; the record has no author (DataCite creator `:unav`, Dataverse author "N/A"). Corporate `key` is fine. |
| 7 | pafka2015benchmml | none | SKIPPED | Own work; `Pafka, Szilard`. |
| 8 | karpathy2026autoresearch | github.com/karpathy/autoresearch; GitHub API | MATCH | Repo owned by user `karpathy` (Andrej Karpathy); README signed "-@karpathy". |
| 9 | openai2026codex | github.com/openai/codex/releases/tag/rust-v0.160.0; GitHub API | MATCH | Organisation `openai` ("OpenAI"); release 0.160.0, published 2026-10-01. |
| 10 | openai2026codexconfig | developers.openai.com/codex/config-reference | MATCH | OpenAI documentation (served as "ChatGPT Learn"). |
| 11 | openai2026gpt6 | developers.openai.com/api/docs/models/gpt-6-astra | MATCH | OpenAI documentation ("OpenAI Developers"). |
| 12 | ferreira2026autoresearch | arxiv.org/abs/2603.24647 | MATCH | 5 authors, identical. |
| 13 | rodrigues2026llmhpo | arxiv.org/abs/2606.21641 | MATCH | 4 authors, identical. |
| 14 | zhang2023llmhpo | neurips.cc/virtual/2023/82901 (workshop page; OpenReview blocked); arxiv.org/abs/2312.04528 | MATCH | 5 authors, same order (page: "Michael Zhang"; arXiv: "Michael R. Zhang"). |
| 15 | liu2024llambo | proceedings.iclr.cc 2024 (hash 84b8d9fc...) + PDF | MATCH | 4 authors incl. Nicolás Astorga, Mihaela van der Schaar. |
| 16 | liu2024agenthpo | arxiv.org/abs/2402.01881 | MATCH | 3 authors, identical. |
| 17 | huang2024mlagentbench | proceedings.mlr.press/v235/huang24y.html + PDF | MATCH | 4 authors, identical. |
| 18 | guo2024dsagent | proceedings.mlr.press/v235/guo24b.html + PDF | MATCH | 6 authors, identical. (The bib has no pages and points to arXiv; PMLR v235 pp. 16813-16848 if wanted.) |
| 19 | jiang2025aide | arxiv.org/abs/2502.13138 | MATCH | 7 authors, identical. |
| 20 | chan2024mlebench | proceedings.iclr.cc 2025 (hash 7e3767db...) page, its BibTeX, the PDF; arxiv.org/abs/2410.07095 | **MISMATCH** | Last two authors are in the wrong order, and the diacritic is missing. The printed ICLR 2025 paper and arXiv both end "..., Tejal Patwardhan, Lilian Weng, Aleksander Mądry". The bib ends "Madry, Aleksander and Weng, Lilian". Caveat: the bib copies the ICLR proceedings web page and the proceedings' own BibTeX, which list "Madry, Aleksander and Weng, Lilian". So this is a page-versus-paper conflict. The correction below follows the paper. |
| 21 | wijk2025rebench | proceedings.mlr.press/v267/wijk25a.html, its BibTeX, the PDF; arxiv.org/abs/2411.15114 | MATCH | 22 authors; the bib matches the PMLR BibTeX character for character. The PDF prints the same 22 in the same order (as Tao Lin, Joshua Clymer, Lucas Sato). Note: the latest arXiv version has 23 authors, adding Holden Karnofsky between Jurkovic and Kinniment. That is not in the cited ICML version. |
| 22 | jing2025dsbench | proceedings.iclr.cc 2025 (hash 50e9ad96...) + PDF | MATCH | 9 authors, identical. |
| 23 | li2024autokaggle | arxiv.org/abs/2410.20424 | MATCH | 14 authors, identical. |
| 24 | grosnit2024agentk | arxiv.org/abs/2411.03562 | MATCH | 19 authors, identical (incl. Balázs Kégl). The bib's family-name split "Attia El-Hili, Youssef" and "S N, Refinath" differs from arXiv's automatic meta split. Spelling and order are the same. |
| 25 | nam2025mlestar | arxiv.org/abs/2506.15692 | MATCH | 6 authors, identical (Sercan Ö. Arık). |
| 26 | rahman2026dsagentbench | arxiv.org/abs/2608.10366 | MATCH | 6 authors, identical. The bib splits the last author as "Hoque Prince, Enamul"; arXiv's automatic meta has "Prince, Enamul Hoque". Spelling is the same. |
| 27 | moukpe2026deltaml | arxiv.org/abs/2608.19653 | MATCH | 3 authors, identical. |
| 28 | ouyang2024nondeterminism | dl.acm.org 403; Crossref record of 10.1145/3697010; Semantic Scholar; arxiv.org/abs/2308.02828 | MATCH | 4 authors, identical (Jie M. Zhang). |
| 29 | atil2025nondeterminism | arxiv.org/abs/2408.04667 | MATCH | 13 authors, identical. |
| 30 | he2025defeating | thinkingmachines.ai blog page (byline and its own "Citation" block) | MATCH | Byline "Horace He, in collaboration with others at Thinking Machines"; the page's own BibTeX has `author = {Horace He and Thinking Machines Lab}`. |
| 31 | yao2024taubench | proceedings.iclr.cc 2025 (hash 1b126cc3...) + PDF | MATCH | 4 authors, identical. |
| 32 | rabanser2026reliability | proceedings.mlr.press/v306/rabanser26a.html + PDF (ICML 2026, PMLR v306, published 29 Sep 2026) | MATCH | 6 authors, identical. Side note: the proceedings are now out, PMLR v306 pp. 102769-102820. The bib still points to arXiv. |
| 33 | bjarnason2026randomness | arxiv.org/abs/2602.07150 | MATCH | 3 authors, identical (André Silva). |
| 34 | mehta2026disagree | arxiv.org/abs/2602.11619 | MATCH | 1 author. |
| 35 | madaan2024variance | arxiv.org/abs/2406.10229 | MATCH | 8 authors, identical. |
| 36 | wang2025noises | arxiv.org/abs/2512.21326 | MATCH | 1 author (Sida Wang). |
| 37 | bowyer2025clt | proceedings.mlr.press/v267/bowyer25a.html + PDF | MATCH | 3 authors, identical. |
| 38 | hariri2026dontpassk | proceedings.iclr.cc 2026 (hash f04edfc6...) + PDF | MATCH | 4 authors, identical. (ICLR 2026 pp. 148539-148579 if wanted.) |
| 39 | miller2024errorbars | arxiv.org/abs/2411.00640 | MATCH | 1 author. |
| 40 | kapoor2024agents | TMLR paper list at jmlr.org/tmlr/papers/ (OpenReview blocked); arxiv.org/abs/2407.01502 | MATCH | 5 authors, identical; TMLR, June 2025. |
| 41 | henderson2018deep | ojs.aaai.org/index.php/AAAI/article/view/11694 + PDF | MATCH | 6 authors, identical. |
| 42 | colas2018seeds | arxiv.org/abs/1806.08295 | MATCH | 3 authors, identical (Cédric Colas). |
| 43 | agarwal2021precipice | proceedings.neurips.cc 2021 (hash f514cec8...) + PDF | MATCH | 5 authors, same order. The page has "Marc Bellemare"; the PDF and bib have "Marc G. Bellemare". |
| 44 | bouthillier2021variance | proceedings.mlsys.org 2021 (hash 0184b0cd...) page + PDF; arxiv.org/abs/2103.03098 | MATCH | The bib's 17 authors match the printed MLSys paper and arXiv exactly (incl. Naz Sepah, Dmitriy Serdyuk, Gaël Varoquaux). Note: the MLSys web page metadata differs. It lists 16 authors, gives "Nazanin Mohammadi Sepahvand" in place of "Naz Sepah", omits Dmitriy Serdyuk, and has "Gael". The paper itself is taken as authoritative, so no change. |
| 45 | dodge2020finetuning | arxiv.org/abs/2002.06305 | MATCH | 6 authors, identical. |
| 46 | mann1947test | projecteuclid.org page for 10.1214/aoms/1177730491 | MATCH | H. B. Mann, D. R. Whitney. |
| 47 | mcgraw1992cl | psycnet/doi.org bot check; Crossref record of 10.1037/0033-2909.111.2.361; Semantic Scholar | MATCH | Kenneth O. McGraw, S. P. Wong. |
| 48 | vargha2000a | journals.sagepub.com 403; Crossref record of 10.3102/10769986025002101; Semantic Scholar | MATCH | András Vargha, Harold D. Delaney. |
| 49 | efron1979bootstrap | projecteuclid.org page for 10.1214/aos/1176344552 | MATCH | B. Efron. |
| 50 | welch1947 | academic.oup.com 403; Crossref record of 10.1093/biomet/34.1-2.28; Semantic Scholar | MATCH | B. L. Welch. |
| 51 | hanley1982meaning | pubs.rsna.org 403; Crossref record of 10.1148/radiology.143.1.7063747; Semantic Scholar | MATCH | James A. Hanley, Barbara J. McNeil. |
| 52 | delong1988comparing | jstor.org bot check; Crossref record of 10.2307/2531595; Semantic Scholar | MATCH | Elizabeth R. DeLong, David M. DeLong, Daniel L. Clarke-Pearson. |
| 53 | chen2021codex | arxiv.org/abs/2107.03374 | MATCH | The bib lists the first 6 of 58 authors, correct and in order, then `and others`. This is a deliberate truncation (renders as "et al."), not a wrong list. The full 58-name field is in the appendix if wanted. |
| 54 | brown2024monkeys | arxiv.org/abs/2407.21787 | MATCH | 7 authors, identical (Christopher Ré). |
| 55 | cawley2010overfitting | jmlr.org/papers/v11/cawley10a.html + PDF | MATCH | Gavin C. Cawley, Nicola L. C. Talbot. |
| 56 | dwork2015reusable | science.org 403; Crossref record of 10.1126/science.aaa9375; Semantic Scholar | MATCH | 6 authors, identical (Toniann Pitassi). |
| 57 | dwork2015generalization | papers.nips.cc / proceedings.neurips.cc 2015 (hash bad5f337...) + PDF | MATCH | 6 authors, same order. The page has "Toni Pitassi"; the PDF, arXiv and bib have "Toniann Pitassi". |
| 58 | roelofs2019meta | proceedings.neurips.cc 2019 (hash ee39e503...) + PDF | MATCH | 7 authors, identical to the proceedings metadata. The PDF uses a grid layout, so it gives no order of its own. |
| 59 | lewis2026same | arxiv.org/abs/2608.26218 | MATCH | 1 author. |
| 60 | fan2026harness | arxiv.org/abs/2609.20804 | MATCH | 9 authors, identical. |
| 61 | pan2026harnesstax | harnesstax.github.io (byline in the post content the page loads: harnesstax.github.io/blog.json -> data/blog/harness-x-model.*.json) | MATCH | 6 authors, identical (Melissa Z. Pan ... Matei Zaharia). Side note on the title: the page reads "HarnessTax: How Much Does **the** Harness Matter for Coding Agents?". The bib omits "the". |
| 62 | metr2025o3 | metr.org/evaluations/openai-o3-report/ (incl. its BibTeX) | MATCH | Page BibTeX `author = {METR}`; JSON-LD author "METR". |
| 63 | zhao2026specbench | arxiv.org/abs/2605.21384 | MATCH | 4 authors, identical. |
| 64 | chen2026publicscore | arxiv.org/abs/2604.20200 | MATCH | 11 authors, identical. |
| 65 | zhu2025abc | none | EXCLUDED | Being fixed separately by the user. Side note: the arXiv title is "Establishing Best Practices **for** Building Rigorous Agentic Benchmarks". The bib says "in Building". Check this against the proceedings title when editing. |
| 66 | chen2016xgboost | dl.acm.org 403; Crossref record of 10.1145/2939672.2939785; Semantic Scholar | MATCH | Tianqi Chen, Carlos Guestrin. |
| 67 | grinsztajn2022tabular | proceedings.neurips.cc 2022 D&B (hash 0378c769...) + PDF | MATCH | 3 authors, same order. The page drops the accents ("Leo", "Gael"); the PDF and arXiv print "Léo" and "Gaël", as in the bib. |
| 68 | shwartzziv2022tabular | sciencedirect.com 403; Crossref record of 10.1016/j.inffus.2021.11.011; Semantic Scholar | MATCH | Ravid Shwartz-Ziv, Amitai Armon. |
| 69 | rubachev2024tabred | proceedings.iclr.cc 2025 (hash 57179948...) + PDF | MATCH | 4 authors, identical. |
| 70 | gardner2023tableshift | proceedings.neurips.cc 2023 D&B (hash a76a757e...) + PDF | MATCH | 3 authors, same order. The page and arXiv print "Popovic"; the PDF prints "Zoran Popović", as in the bib. |
| 71 | cai2025temporal | proceedings.mlr.press/v267/cai25j.html + PDF | MATCH | 2 authors, same order. The PMLR page metadata has "Haorun Cai"; the PDF and arXiv print "Hao-Run Cai", as in the bib. (PMLR v267 pp. 6366-6386 if wanted.) |

## Corrected author fields (MISMATCH entries)

### chan2024mlebench

Order and spelling as printed in the ICLR 2025 paper
(proceedings.iclr.cc/paper_files/paper/2025/file/7e3767db483c942b883eb4f8cfb74e31-Paper-Conference.pdf)
and on arXiv 2410.07095. The last two authors are swapped relative to the bib, and the paper spells
the name "Mądry":

```bibtex
  author        = {Chan, Jun Shern and Chowdhury, Neil and Jaffe, Oliver and Aung, James and Sherburn, Dane and Mays, Evan and Starace, Giulio and Liu, Kevin and Maksin, Leon and Patwardhan, Tejal and Weng, Lilian and M{\k{a}}dry, Aleksander},
```

(`\k` needs `\usepackage[T1]{fontenc}`, which most ML templates load. The current bib field matches
the ICLR proceedings web page and the BibTeX that page offers, which give "Madry, Aleksander and
Weng, Lilian". Keep the current field only if you prefer the proceedings metadata over the printed
paper.)

## Appendix: full author list for chen2021codex (optional)

The bib's `and others` truncation is legitimate. If the full list is wanted, here are the 58 authors
from arXiv 2107.03374 in order:

```bibtex
  author        = {Chen, Mark and Tworek, Jerry and Jun, Heewoo and Yuan, Qiming and Pinto, Henrique Ponde de Oliveira and Kaplan, Jared and Edwards, Harri and Burda, Yuri and Joseph, Nicholas and Brockman, Greg and Ray, Alex and Puri, Raul and Krueger, Gretchen and Petrov, Michael and Khlaaf, Heidy and Sastry, Girish and Mishkin, Pamela and Chan, Brooke and Gray, Scott and Ryder, Nick and Pavlov, Mikhail and Power, Alethea and Kaiser, Lukasz and Bavarian, Mohammad and Winter, Clemens and Tillet, Philippe and Such, Felipe Petroski and Cummings, Dave and Plappert, Matthias and Chantzis, Fotios and Barnes, Elizabeth and Herbert-Voss, Ariel and Guss, William Hebgen and Nichol, Alex and Paino, Alex and Tezak, Nikolas and Tang, Jie and Babuschkin, Igor and Balaji, Suchir and Jain, Shantanu and Saunders, William and Hesse, Christopher and Carr, Andrew N. and Leike, Jan and Achiam, Josh and Misra, Vedant and Morikawa, Evan and Radford, Alec and Knight, Matthew and Brundage, Miles and Murati, Mira and Mayer, Katie and Welinder, Peter and McGrew, Bob and Amodei, Dario and McCandlish, Sam and Sutskever, Ilya and Zaremba, Wojciech},
```

## Note relevant to the zhu2025abc fix

Proceedings web metadata did not always agree with the printed paper in the same proceedings. This
happened four times: MLE-bench on the ICLR page, Bouthillier et al. on the MLSys page (16 vs 17
authors), Cai and Ye on the PMLR page, and Dwork et al. on the NeurIPS 2015 page. Before settling
on the 26-author list for zhu2025abc, check the first page of its NeurIPS 2025 PDF as well.

## Resolution (2026-10-07, applied to `plan/references.bib` and `paper/refs.bib`)

Rule: where a proceedings web page and the printed paper disagree, the bib follows the printed paper.

- `chan2024mlebench`: authors end "Patwardhan, Weng, Mądry" as in the printed ICLR paper and on arXiv (checked on arXiv 2410.07095).
- `zhu2025abc`: the NeurIPS proceedings web page lists 26 authors and "in Building"; the first page of the proceedings PDF lists 25 (no Narayanan; Kellermann after Steinhardt) and "for Building", as arXiv does. The bib now has the 25 printed authors and "for".
- `pan2026harnesstax`: title corrected to "How Much Does the Harness Matter for Coding Agents?" (checked on harnesstax.github.io).
- `rabanser2026reliability`: now cites Proceedings of the 43rd ICML, PMLR 306, pp. 102769–102820 (checked on proceedings.mlr.press/v306/rabanser26a.html).
- Kept as they are: `wijk2025rebench` (22 authors, the cited ICML/PMLR version), `chen2021codex` (first six authors and "others", a deliberate et al.).
