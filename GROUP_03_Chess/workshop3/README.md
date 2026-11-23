# Workshop 3 · From player groups to opening review

[Read the four-page report](W3_Opening_Review.pdf). It uses Group 03's C2 results to help a club training coordinator choose games for an opening-review session. Each comparison uses the same plotted values in both versions. The earlier drafts were created for W3.

| View | Earlier draft | Final chart | Chart data |
| --- | --- | --- | --- |
| Score gap by cluster | [Paired bars](figures/01-clusters-before.svg) | [Paired dots](figures/01-clusters-after.svg) | [Cluster gaps and sample sizes](data/cluster_gaps.csv) |
| Score gap by speed and rating | [Paired bars](figures/02-segments-before.svg) | [Aligned dots](figures/02-segments-after.svg) | [Segment gaps, rates and sample sizes](data/segment_gaps.csv) |
| Opening families and White losses | [Stacked bars](figures/03-openings-before.svg) | [Ranked bars with losses at the baseline](figures/03-openings-after.svg) | [Exact outcomes for all 111 families](data/opening_outcomes.csv) |

## Edit or rebuild

Edit the labels and charts in the SVG files or revise the report text and figure definitions in [build_workshop3.py](build_workshop3.py). From this folder, with Python 3.12+ and ReportLab installed, run:

```sh
python3 build_workshop3.py
```

To add the student name to the cover, run `W3_AUTHOR="Full name" python3 build_workshop3.py`. The build uses the included `data/` folder. To refresh these inputs from the full project, run `python3 prepare_workshop3.py` first. It reads the saved C2 results and checks all 16 colour-specific speed/rating cells against the frozen September split. It counts unique games for White rated 2000+ in blitz and verifies the outcome totals against the corresponding cell.

## Evidence

These references point to files in the full C2 project.

- **View 1.** The gap is White score rate minus Black score rate, in percentage points. The sensitivity subset includes games where neither player appears in the July training window. Every game contributes two colour perspectives. The [C2 notebook](../notebooks/C2_clustering.ipynb) and its [colour profiles](../outputs/tables/C2_cluster_profile_by_color_test.csv), [player sensitivity](../outputs/tables/C2_player_overlap_sensitivity.csv) and [window sensitivity](../outputs/tables/C2_month_sensitivity.csv) are the sources.
- **View 2.** The comparison uses the [C2 club-rule table](../outputs/tables/C2_manual_rule_test.csv). The 2000+ Blitz segment had the largest absolute observed gap. The rating band is assigned separately to each focal colour, so White and Black may have different games and denominators.
- **View 3.** The ranked bars use [September's frozen test split](../data/splits/test.csv) with opening family at 20 plies. Each record contributes once and is classified as a White win, draw or loss. The five families with the most games are drawn individually and ranked by losses; every bar starts with losses at zero. The remaining 106 families are summarised in a note and are available individually in the chart data. The before version draws all six groups with the same counts.
- **Visual system.** Dark slate is the primary series and light slate the comparison series. Plum marks the item to act on next. Teal, grey and rust are reserved for win, draw and loss. Filled shapes are primary and open shapes are comparison series; circle and square are used only in View 1, triangle and diamond only in View 2.
