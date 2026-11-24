# Team review record

| Member | Contribution recorded for C2 | Evidence |
|---|---|---|
| Javier Alcaíno | Reviewed feature design, K-prototypes fitting and cluster profiles. | [C2 §§2–4](notebooks/C2_clustering.ipynb) |
| Lucas Riquelme | Directed the AI-assisted clustering implementation, including feature design and both sensitivity checks, and reviewed results. | [C2 §§2–3 and 6–7](notebooks/C2_clustering.ipynb) |
| Renato Varela | Reviewed chess terminology and handled course submission logistics. | [C1 measurement and prefix lookup](notebooks/C1_openings.ipynb) and the team's submission record. |

The C2 record identifies topics learned by each member: mixed-input clustering for Javier,
opening-family PCA and GMM for Lucas, and checkpoint terminology, ratings and speed for
Renato. Each member can confirm their own account and supply their own unresolved question
in the defense. The earlier equal split was the team's default allocation.

**AI use.** Codex and Claude assisted research, analysis code and drafting. The C2 record
identifies Claude Code support for clustering and the annex. For C3, Codex audited consistency,
clarified the method, embedded the W3 figures and prepared the assessment snapshot. Claims are
tied to saved project results. The defense is conducted by the students without live AI assistance.

## Using the presentation in the defense

Open with the illustrated club coordinator and the decision. The short answer on slide 4
gives her a review priority. Slides 15 and 17 explain the segment and available loss
examples; slides 19–20 give the limits and next step. This decision-first structure gives
the coordinator a concrete choice and the evidence needed to judge it.

Make the change of audience explicit when turning to the process. Use slides 6–9 for the
data and chronology, slides 11–14 for the model and sensitivity, and the two V3 views
on slides 16–17 for the difference between showing all game flow and ranking named
families. Use the [decision record](DECISION_LOG.md) to connect design feedback with the
chart evidence. The title cards and appendix can serve as transition and question material
within the ten-minute session.

| Slide | Precision for the oral explanation |
|---|---|
| 1 | The recommendation applies to the Sicilian Defense family. The Najdorf sequence illustrates one line within it. |
| 11 | C1 observed a modest rating-gap association. K = 4 leads the tested July grid; a supervised classifier was outside the study. |
| 13 | Cluster 3 accounts for about 5% of September player-game perspectives. |
| 14 | The largest connected component contains 84.5% of games, so keeping every game and every component intact precludes a roughly balanced player-disjoint split. The 77.8% figure refers to September games where neither player appears in July. |
| 15–17 | The rating bands are assigned by focal color. C3's opening table restores the full numerical comparison for `Other` (1,892 games, 795 losses). The Sicilian's loss count is an exploratory measure of how many examples are available to review. |
