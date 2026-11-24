# Workshop 3 · From player groups to opening review

The [W3 report](W3_Opening_Review.pdf) preserves the submitted design comparisons.
The [C3 closing notebook](../notebooks/C3_final_visualizations.ipynb) embeds the
three final views with their denominators, supporting tables and interpretation.

| View | Earlier draft | Final chart | Compact chart summary |
|---|---|---|---|
| Score gap by cluster | [Paired bars](figures/01-clusters-before.svg) | [Paired dots](figures/01-clusters-after.svg) | [Four cluster contrasts](data/cluster_gaps.csv) |
| Score gap by speed and focal rating | [Paired bars](figures/02-segments-before.svg) | [Aligned dots](figures/02-segments-after.svg) | [Eight segment contrasts](data/segment_gaps.csv) |
| Opening families and White losses | [Alphabetical stacked bars](figures/03-openings-before.svg) | [Ranked bars with losses at zero](figures/03-openings-after.svg) | [Five named families and Other](data/opening_chart_summary.csv) |

## Sources and choices

- **View 1** compares the full September window and the subset where neither player appears in July. The [C2 notebook](../notebooks/C2_clustering.ipynb), §4.1 and §§6–7, shows the score complement, sensitivity and cluster composition.
- **View 2** draws the score differences for the C2 reference rule (§4.2). The rating band belongs to each focal player, so each color can have different game IDs and denominators.
- **View 3** counts unique White 2000+ Blitz games in the September window with families identified at ply 20. It selects five families by exposure and orders them by loss count. The final chart moves the aggregate of 106 remaining families to its note. The C3 table gives the full outcome breakdown for the six chart groups. The [decision record](../DECISION_LOG.md) explains the W3 feedback and why the team retained the ranking.
- **Shared design** uses a signed pp scale with a marked zero on both gap charts. Shape and direct labels distinguish series. The game-count chart uses a zero baseline, fixed outcome order and printed counts. Plum identifies the review focus.

## Editable sources

[build_workshop3.py](build_workshop3.py) defines the visual system and regenerates the
SVGs and PDF with Python and ReportLab. Run `python3 build_workshop3.py` from this folder
to render from the included chart summaries. The [preparation script](prepare_workshop3.py)
uses locally held game inputs and saved C2 profiles to verify the September totals and
refresh those summaries. It checks all 16 color-specific manual cells and verifies that
Sicilian Defense leads all individual families by loss count. The assessed revision
includes compact chart summaries and requires no data or software to read.
