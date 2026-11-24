# Opening outcomes for training planning

Business Intelligence · IIB423T-1 · C3 final assessment · Group 03

**Javier Alcaíno · Lucas Riquelme · Renato Varela**

**Question.** Which games should a chess club review first when training time is limited, and what does behavioral clustering add to a rule based on speed and rating?

**Decision.** For a proposed club training coordinator, start with White's Sicilian Defense losses in 2000+ Blitz. The September window contains 255 losses in 556 Sicilian games (45.9%), compared with 1,370 in 3,297 games (41.6%) across that White cohort. The priority is exploratory and reflects the volume of reviewable games. K-prototypes summarizes four broad speed and rating profiles. The manual rule keeps the 2000+ Blitz segment visible.

**Assessment version.** Use the commit at the tip of the `c3-final` branch for C3. Earlier course submissions form the development record. All assessed notebook outputs are saved and can be read on GitHub without installing software, downloading data or running code.

## Read in this order

| Stage | File | What to look for |
|---|---|---|
| C1 · EDA | [Opening outcomes](GROUP_03_Chess/notebooks/C1_openings.ipynb) | Source scope, record grain, checkpoint, quality, preparation and opening exposure. |
| W2 · Preparation and validation | [From EDA to validation](GROUP_03_Chess/notebooks/W2_project.ipynb) | Game-level chronological split, 25% stratified sensitivity sample, same-cohort check, leakage audit and July-only transformations. |
| C2 · Model and reference | [Behavioral groups](GROUP_03_Chess/notebooks/C2_clustering.ipynb) | July-trained K-prototypes, K selection, September color-specific scores, speed-by-rating reference and sensitivity checks. |
| W3/C3 · Views and recommendation | [Final views](GROUP_03_Chess/notebooks/C3_final_visualizations.ipynb) | Three saved charts, comparison and support tables, the opening-review decision and its limits. |
| Optional · C2 annex | [Opening family profiles](GROUP_03_Chess/notebooks/C2_clustering_anexo_aperturas.ipynb) | A complementary July PCA/GMM analysis of family-level profiles. |

- [C3 presentation PDF](GROUP_03_Chess/Presentaci%C3%B3n%20de%20ajedrez%20animada.pdf) · [Animated presentation](https://claude.ai/artifact/6sDrUtsrb9mskH5PqT3WdA#1)
- [W3 designs, editable SVGs and chart-generation scripts](GROUP_03_Chess/workshop3/README.md)
- [Decision and traceability record](GROUP_03_Chess/DECISION_LOG.md) · [Team contributions and AI use](GROUP_03_Chess/TEAM_REVIEW.md)
- [Guía de lectura en español](GROUP_03_Chess/GUIA_DE_LECTURA.md)

## Scope and pipeline

The earlier W1 case concerned education spending in La Cisterna. The team subsequently adopted a training-planning question using public chess games. The C1 tracking reconstruction starts the chess evidence chain, and W2, C2 and W3 carry its question and score measure forward.

**Source → EDA → frozen split → model and reference → review material.** The source consists of the first 16 MiB of each compressed July, August and September 2026 standard-rated Lichess archive, downloaded on 21 October 2026. The last uncertified record in each prefix was discarded. C1 retained 86,950 of 153,817 source records (64,824 Blitz and 22,126 Rapid), grouped into 140 opening families. Both the [Lichess archives](https://database.lichess.org/#standard_games) and the [opening taxonomy at a6189a3](https://github.com/lichess-org/chess-openings/tree/a6189a3) are CC0. The [source manifest](GROUP_03_Chess/provenance/source_manifest.json) records exact byte ranges, input hashes and window coverage.

Each game contributes one opening label from its shared sequence through ply 20, immediately after Black's tenth turn. The prefix contains moves by both sides. Each side keeps its own rating and outcome. W2 splits the game IDs before C2 derives linked player-game perspectives. The annex uses one row per opening family. The final White opening view counts each selected game once.

| UTC source window | Game count | Role |
|---|---:|---|
| July | 30,615 | Estimate preprocessing parameters, select K and fit the prototypes. |
| August | 25,782 | Apply the frozen model for a window sensitivity check. |
| September | 30,553 | Compare frozen cluster assignments and manual segments, then explore review priorities. |

**Score rate** is (wins + 0.5 × draws) divided by the count for the stated color and group. The manual rule's largest observed contrast is +4.62 percentage points in 2000+ Blitz (White 55.55%, n = 3,297, and Black 50.93%, n = 3,288). The largest of four cluster contrasts is +2.87 pp. Across all contrasts, the support-weighted absolute gaps are 2.47 pp for the eight manual segments and 2.44 pp for the clusters. Each color can contain a different mix of games.

September was already explored in C1. The roughly 36–43 minute windows cover particular UTC periods and may include the same players. Neither the observed gaps nor the volume of losses measures the effect of color, opening choice or a training intervention.

## Software and files

The work uses Python and Jupyter with pandas and NumPy for preparation, python-chess for prefix matching, scikit-learn and SciPy for transformations and evaluation, kmodes for K-prototypes, Matplotlib and Seaborn for analytical plots, and ReportLab for the W3 visual system. The C3 notebook rasterizes those same drawings with Poppler for saved PNG display. [Python dependencies](GROUP_03_Chess/requirements.txt) and the [execution record](GROUP_03_Chess/provenance/C3_execution_record.json) document the environment.

`notebooks/` contains code and rendered evidence. `outputs/` holds figures and aggregate results. `workshop3/` holds the shared drawing code, SVGs and compact chart summaries. `provenance/` records source identity and preparation settings. `report/` and the C2 slides are historical context.

The C3 revision excludes local dataset inputs and row-level exports, including PGN prefixes, raw and prepared games, taxonomy TSVs, split membership and feature arrays. Earlier commits retain the archives used in prior course submissions. See the assessment version above.

AI assisted research, code, writing and review across the project. See the [team review](GROUP_03_Chess/TEAM_REVIEW.md) for the recorded tools, uses and member contributions.
