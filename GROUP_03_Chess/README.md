# Opening outcomes for training planning

Group 03: Javier Alcaíno, Lucas Riquelme and Renato Varela.

Prepared on 21 October 2026. This is a **local package** containing a reconstructed C1 tracking baseline and its W2 continuation. The team selected opening families and results, several rating bands, and separate blitz/rapid analyses. No GitHub upload, commit, tag or assessment submission is claimed. C1 has no slide deck by explicit request.

## Open these files

1. `report/GROUP_03_C1_Report.pdf`: self-contained English C1 tracking report, with methods, tables, figures, limitations and process record.
2. `notebooks/C1_openings.ipynb`: executed C1 analysis, with all preparation code, tables and figures saved.
3. `notebooks/W2_project.ipynb`: executed English W2 notebook, continuing the same decision, game-level observation unit, 20-ply opening definition and points KPI.
4. `GUIA_DE_LECTURA.md`: a short Spanish guide to the analytical choices and principal limitations.
5. `TEAM_REVIEW.md`: individual contributions/reflections to confirm after review. The project does not fabricate personal statements.

## Question and measurement

A proposed club training coordinator prioritises opening-review material by exposure and observed results, within color, speed and focal-player rating band. The KPI is `(wins + 0.5 × draws) / eligible games` in the specified cell. It is not a causal effect, predictive accuracy, an optimisation of opening choice, or measured training effectiveness.

One primary row is one unique game. A descriptive long table has two complementary color perspectives per game. A game is never split across training and evaluation sets. Opening families are reconstructed from positions reached within the first 20 plies, immediately after Black's 10th move; full-game opening tags are excluded from predictive features. Games not reaching that nonterminal checkpoint are outside the analytical cohort.

## Data and scope

The case comes from official Lichess standard-rated monthly archives for July, August and September 2026. Exactly the first 16 MiB of each compressed archive were retrieved with verified HTTP byte-range responses. Fully bounded PGN records were extracted; the uncertified final record in each prefix was discarded.

**These are three short UTC windows at the start of the months, not random samples or full-month datasets.** Their exact observed start-time ranges are recorded in `provenance/source_manifest.json`. Within-window resampling does not remove coverage bias. All claims are limited accordingly.

- `data/source_prefixes/`: unchanged compressed byte prefixes. A `.part` file is an intentionally incomplete compressed archive, not a complete monthly dump.
- `data/raw/lichess_2026_source_extract.csv`: unchanged reduced source, including other speeds and post-game fields for transparent exclusions and leakage checks. Player names are deterministically pseudonymised. Public game IDs remain.
- `data/reference/a.tsv` through `e.tsv`: CC0 Lichess opening taxonomy frozen to a recorded commit.
- `data/processed/games.csv`: prepared unique-game cohort.
- `data/splits/train.csv`, `validation.csv`, `test.csv`: actual future-prediction datasets; July fitting, August validation, September test. Predictive fields and labels are explicit.
- `data/splits/membership.csv`: unique game-to-subset mapping.
- `data/splits/sample_25pct_ids.csv`: fixed-seed stratified within-frame sampling exercise.
- `data/splits/transformed_features.npz`: features transformed by parameters learned from July only; this is not a trained predictive model.
- `outputs/tables/`, `outputs/figures/`: inspectable exported results.
- `provenance/`: exact sources, response headers, hashes, fixed analytical contract and execution records.

The source and opening reference declare CC0. Source links and versions are in the manifest. All source copies remain unchanged. The reduction script retains only the observed 20-ply prefix, alongside labels and audit fields; it does not retain full move histories as predictive inputs.

## Run the project

Use Python 3.12 or newer in a fresh virtual environment. The delivered outputs were produced under Python 3.12, with exact package versions in `provenance/environment_versions.json`. Core direct dependencies are pinned in `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Open the notebooks in Jupyter or VS Code, choose that environment, restart the kernel, run every cell top to bottom and save. Run C1 first and W2 second if rebuilding all outputs. The shipped C1 summary makes the continuity check independently inspectable.

For automated fresh-kernel execution:

```bash
python scripts/execute_notebooks.py
```

The standard `python3` Jupyter kernel must use the environment containing these dependencies. If necessary, register and select it:

```bash
python -m ipykernel install --user --name chess-bi
python scripts/execute_notebooks.py --kernel chess-bi
```

No network access is needed to execute the supplied notebooks. They use project-relative paths and fixed seed 423 for random sampling. The deterministic preparation rules are embedded in each notebook, not hidden behind an opaque external analysis call.

### Reconstruct the reduced source

```bash
python scripts/acquire_data.py --local-only
```

This recreates the reduced source from the supplied compressed prefixes. Without `--local-only`, the script downloads missing byte prefixes from the exact public URLs and checks range responses; it never requests a full monthly archive. Reference files and their frozen commit are supplied and hashed. If an upstream source changes, compare retained checksums rather than silently replacing the case.

### Rebuild the C1 report and validate the package

```bash
python scripts/make_report_figures.py
python scripts/build_report.py
python scripts/verify_package.py
```

`build_report.py` consumes the executed C1 result tables and prepared cohort. The authoring tool used PDF rendering and visual inspection; generated verification page images are not part of the deliverable. `build_notebooks.py` is optional authoring source and regenerates unexecuted notebook files, so do not run it merely to inspect the finished notebooks.

## W2 interpretation

W2 implements programmatic quality checks, row accounting, three informative EDA figures, a reproducible approximately 25% game sample, KPI/segment comparisons, a contextual leakage audit, actual chronological subsets and train-only scaler/category fitting. No model is fitted and no performance metric is claimed, as neither is required by this W2 brief.

September outcomes were already explored in the reconstructed C1, so the test subset is **not pristine**. No test-based tuning is performed here. A later confirmatory prediction study requires genuinely new data and wider temporal coverage. Repeated players are present; this design does not establish unseen-player generalisation.

The rating bands, 100-point close-opponent restriction and 50-game display threshold are transparent operational choices. The restriction changes the descriptive population and does not identify a causal effect. Scores are always interpreted with denominators and context.

## Continuity and human review

The earlier school-audit W1/C1 work remains in its original folder and repository. This local chess case does not overwrite it or retroactively relabel it. The user stated that C1 feedback was not yet available; W2's feedback-to-action table therefore uses explicitly labelled self-audits. No instructor approval is invented.

The exact C1 brief also requests slides and personal process evidence. Slides were deliberately omitted for this tracking package. Individual contributions and reflections await the members' own confirmation in `TEAM_REVIEW.md`. This is not represented as a fully compliant historic resubmission.

If the team later submits W2 through GitHub, preserve the prior project/history, add this case in an appropriate folder, and record the actual repository URL and W2 commit/tag. Those steps are outside this requested local delivery.

AI assisted research, implementation and writing. Verification records describe executable checks rather than claiming that the three members have already personally reviewed all outputs.
