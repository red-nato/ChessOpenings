# Team review record

The following personal statements must be supplied or confirmed by their respective members. They are not completed by AI on their behalf. The C1 report identifies this tracking-version limitation explicitly.

| Member | Share (%) | Concrete contribution and evidence location | Learning gain | Unresolved uncertainty |
|---|---|---|---|---|
| Javier Alcaíno | 33.3% | Reviewed and validated the main clustering pipeline (`C2_clustering.ipynb`) -- feature design, k-prototypes fitting and cluster profiles. | The main clustering pipeline (`C2_clustering.ipynb`): building the mixed-type Gower-style dissimilarity and fitting k-prototypes on player-game perspectives, and why plain K-means breaks down with ~140 opening categories. | To be supplied by Javier |
| Lucas Riquelme | 33.3% | Led the AI-assisted implementation session: chose the clustering route, directed the feature design and the two sensitivity analyses, and reviewed/validated all results before submission. | The opening-level clustering annex (`C2_clustering_anexo_aperturas.ipynb`): building opening profiles, standardising and reducing them with PCA, and choosing K for a Gaussian Mixture Model via BIC. | To be supplied by Lucas |
| Renato Varela | 33.3% | Reviewed the chess-domain terminology used throughout the project and handled submission logistics (EVA/Canvas). | The chess-specific vocabulary used throughout the project: the difference between the prefix-derived `opening_family_20` and the post-game ECO/final-opening tag, the 20-ply (10-move) checkpoint that freezes the analysis before the outcome is known, Glicko-2 rating bands, the blitz/rapid time-control distinction, and the named opening families that recur throughout the results (Sicilian Defense, Queen's Pawn Game, Caro-Kann Defense, King's Indian Defense, among others) — plus the administrative side of preparing and submitting the deliverable through the course's EVA platform. | To be supplied by Renato |

Share (%): equal three-way split, set by the group for C2 as a fair default when
contribution is not tracked at a finer grain. If any member's actual involvement in C2
differed meaningfully from an equal third, replace these numbers before submission — they
are a default, not a verified measurement.

Confirmed collective decisions from the conversation: chess; openings and results for training; recent Lichess records; several rating bands; separate blitz and rapid; prediction only from a fixed opening checkpoint; C1 report and notebook without slides; W2 continuation; local package only.

Instructor feedback on the original C1 was not available. W2 self-audits must remain labelled as self-audits. Do not replace them with invented instructor comments.

Before presenting the work, each member should be able to explain what one row means, why both color scores must not be pooled to rank openings, how the prefix label is computed, why the source windows are not representative months, and which information was available at the prediction checkpoint.
