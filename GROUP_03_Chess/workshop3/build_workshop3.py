"""Build the editable SVG figures and the four-page W3 report from local aggregates."""

import json
import os
from collections import defaultdict
from xml.sax.saxutils import escape

from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from prepare_workshop3 import BANDS, DATA, HERE, OUTCOMES, read_csv

INK = HexColor("#172927")
MUTED = HexColor("#485D5A")
RULE = HexColor("#D4DEDA")
GRID = HexColor("#E6ECE9")
PALE = HexColor("#EFF4F1")
ACCENT = HexColor("#734176")
ACCENT_PALE = HexColor("#F4EDF5")
FULL = HexColor("#3B4A66")      # navy slate: primary series (never used for outcomes)
CONTEXT = HexColor("#7C8AA3")   # light slate: comparison series
OUTCOME = {"win": HexColor("#24766E"), "draw": HexColor("#65747D"), "loss": HexColor("#A94F32")}

REGULAR = "Helvetica"
BOLD = "Helvetica-Bold"
DISPLAY = "Times-Roman"
W, H = A4
LEFT = 42
WIDTH = W - LEFT * 2
X0, X1 = 137, 351
TICKS = range(-1, 6)
WINDOW = "Lichess test window  |  1 Sep 2026, 00:00-00:40 UTC"


def pp(value):
    return f"{value:+.2f}"


def plot_x(value):
    return X0 + (value + 1) * (X1 - X0) / 6


def label(fig, x, y, value, size=9.4, color=INK, *, bold=False, align="start"):
    fig.add(String(x, y, str(value), fillColor=color, fontSize=size,
                   fontName=BOLD if bold else REGULAR, textAnchor=align))


def line(fig, x1, y1, x2, y2, color=RULE, width=0.65):
    fig.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width))


def box(fig, x, y, w, h, color, stroke=None):
    fig.add(Rect(x, y, w, h, fillColor=color, strokeColor=stroke))


def marker(fig, x, y, shape="circle", color=FULL):
    """Filled shape = primary series, open shape = comparison series; the shape names the series in a view."""
    filled = shape in ("circle", "triangle")
    fill, stroke = (color, None) if filled else (white, color)
    if shape == "circle":
        fig.add(Circle(x, y, 3.5, fillColor=fill, strokeColor=stroke))
    elif shape == "square":
        fig.add(Rect(x - 3, y - 3, 6, 6, fillColor=fill, strokeColor=stroke, strokeWidth=1.3))
    elif shape == "triangle":
        fig.add(Polygon([x - 4.4, y - 3.4, x + 4.4, y - 3.4, x, y + 4.2], fillColor=fill, strokeColor=stroke))
    else:  # diamond
        fig.add(Polygon([x - 4.4, y, x, y + 4.4, x + 4.4, y, x, y - 4.4], fillColor=fill,
                        strokeColor=stroke, strokeWidth=1.3))


def axis(fig, bottom, top):
    for value in TICKS:
        x = plot_x(value)
        line(fig, x, bottom, x, top, CONTEXT if value == 0 else GRID, 0.9 if value == 0 else 0.65)
        label(fig, x, bottom - 13, f"{value:+d}" if value else "0", color=MUTED, align="middle")
    label(fig, (X0 + X1) / 2, bottom - 28, "White minus Black score (pp)", color=MUTED, align="middle")


def paired_dot_figure(rows, kind):
    """Use a shared gap scale and exact labels for both final comparison views."""
    fig = Drawing(WIDTH, 192)
    is_cluster = kind == "cluster"
    a_label, b_label = ("All test", "Neither in July") if is_cluster else ("Blitz", "Rapid")
    a_shape, b_shape = ("circle", "square") if is_cluster else ("triangle", "diamond")
    label(fig, 0, 176, "C2 CLUSTER" if is_cluster else "FOCAL RATING", 8.4, MUTED, bold=True)
    label(fig, 397, 176, a_label, 8.6, MUTED, bold=True, align="middle")
    label(fig, 477, 176, b_label, 8.6, MUTED, bold=True, align="middle")
    marker(fig, 366 if is_cluster else 377, 179, a_shape)
    marker(fig, 436 if is_cluster else 454, 179, b_shape, color=CONTEXT)
    if not is_cluster:
        box(fig, 0, 38, WIDTH, 30, ACCENT_PALE)
    axis(fig, 31, 162)
    for index, (name, detail, a, b) in enumerate(rows):
        y = 145 - index * 31
        accent = not is_cluster and name == "2000+"
        if index:
            line(fig, 0, y + 15.5, WIDTH, y + 15.5, GRID)
        label(fig, 0, y - (1 if detail else 3), name, 11, ACCENT if accent else INK, bold=True)
        if detail:
            label(fig, 0, y - 13, detail, 8.4, MUTED)
        ax, bx = plot_x(a), plot_x(b)
        if is_cluster:
            line(fig, ax, y + 4, bx, y - 4, RULE, 1.8)
        marker(fig, ax, y + 4, a_shape, ACCENT if accent else FULL)
        marker(fig, bx, y - 4, b_shape, CONTEXT)
        label(fig, 397, y - 3, pp(a), 10.4, ACCENT if accent else INK, bold=accent, align="middle")
        label(fig, 477, y - 3, pp(b), 10.4, MUTED, align="middle")
    return fig


def paired_bar_figure(rows, kind):
    fig = Drawing(WIDTH, 132)
    is_cluster = kind == "cluster"
    series = ("All test games", "Neither in July") if is_cluster else ("Blitz", "Rapid")
    for x, name, color in ((0, series[0], FULL), (113, series[1], CONTEXT)):
        box(fig, x, 117, 9, 7, color)
        label(fig, x + 14, 116.5, name, 8.7, MUTED)
    axis(fig, 32, 107)
    for index, (name, _, a, b) in enumerate(rows):
        y = 96 - index * 18
        label(fig, 0, y - 3, name)
        for shift, value, color in ((1, a, FULL), (-6, b, CONTEXT)):
            x = plot_x(value)
            zero = plot_x(0)
            box(fig, min(x, zero), y + shift, abs(x - zero), 5, color)
    label(fig, 379, 84, "Positive values favour White.", 8.5, MUTED)
    return fig


def stacked_opening_bars(rows):
    fig = Drawing(WIDTH, 131)
    chart_left, chart_right = 145, 442
    scale = (chart_right - chart_left) / 2000
    for x, result in zip((145, 260, 370), OUTCOMES):
        box(fig, x, 119, 8, 7, OUTCOME[result])
        label(fig, x + 13, 118, f"{result.title()}  {sum(r[result] for r in rows):,}", 8.7, MUTED)
    for tick in range(0, 2001, 500):
        x = chart_left + tick * scale
        line(fig, x, 28, x, 111, CONTEXT if tick == 0 else GRID)
        label(fig, x, 16, f"{tick:,}", 8.5, MUTED, align="middle")
    label(fig, (chart_left + chart_right) / 2, 3, "Games", 8.6, MUTED, align="middle")
    ordered = sorted(rows[:-1], key=lambda row: row["opening_family"]) + rows[-1:]
    for index, row in enumerate(ordered):
        y = 101 - index * 13.3
        label(fig, 0, y - 2.5, row["opening_family"], 9)
        x = chart_left
        for result in OUTCOMES:
            width = row[result] * scale
            box(fig, x, y - 3.5, width, 8, OUTCOME[result])
            x += width
        label(fig, x + 5, y - 2.5, f'{row["games"]:,}', 8.5, MUTED)
    return fig


def ranked_loss_bars(ranked, other, overall_loss_rate):
    """Rank named families by losses; every bar starts with losses at the common zero baseline."""
    fig = Drawing(WIDTH, 214)
    left, right = 150, 400
    scale = (right - left) / 600
    label(fig, 0, 202, "OPENING FAMILY", 8.4, MUTED, bold=True)
    for x, name, key in ((150, "Loss (from zero)", "loss"), (243, "Draw", "draw"), (295, "Win", "win")):
        box(fig, x, 201, 8, 7, OUTCOME[key])
        label(fig, x + 13, 201, name, 8.7, MUTED)
    label(fig, 444, 202, "LOSSES", 8.4, MUTED, bold=True, align="end")
    label(fig, WIDTH, 202, "LOSS RATE", 8.4, MUTED, bold=True, align="end")
    for tick in range(0, 601, 100):
        x = left + tick * scale
        line(fig, x, 62, x, 194, CONTEXT if tick == 0 else GRID, 0.9 if tick == 0 else 0.65)
        label(fig, x, 50, f"{tick:,}", 8.5, MUTED, align="middle")
    label(fig, (left + right) / 2, 37, "Games, with losses drawn first", 8.6, MUTED, align="middle")
    for index, row in enumerate(ranked):
        y = 180 - index * 26
        first = index == 0
        if first:
            box(fig, 0, y - 14, WIDTH, 27, ACCENT_PALE)
        elif index:
            line(fig, 0, y + 13, WIDTH, y + 13, GRID)
        label(fig, 0, y + 2, row["opening_family"], 9.6, ACCENT if first else INK, bold=first)
        label(fig, 0, y - 9, f'{row["games"]:,} games  /  {row["win"]}W {row["draw"]}D {row["loss"]}L', 8, MUTED)
        x = left
        for result in ("loss", "draw", "win"):
            width = row[result] * scale
            box(fig, x, y - 5, width, 11, OUTCOME[result])
            x += width
        label(fig, 444, y - 3, f'{row["loss"]:,}', 10.4, ACCENT if first else INK, bold=first, align="end")
        label(fig, WIDTH, y - 3, f'{row["loss"] / row["games"]:.1%}', 10.4,
              ACCENT if first else INK, bold=first, align="end")
    line(fig, 0, 27, WIDTH, 27)
    label(fig, 0, 12, f'Not drawn: Other ({other["families"]} families), {other["games"]:,} games, {other["loss"]:,} losses '
          f'({other["loss"] / other["games"]:.1%}). Cohort loss rate {overall_loss_rate:.1%}.', 8.4, MUTED)
    return fig


def text(pdf, x, top, value, size=10, color=INK, font=REGULAR):
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    pdf.drawString(x, H - top, value)


def paragraph(pdf, x, top, value, width=WIDTH, size=10.7, leading=14.4, color=INK):
    style = ParagraphStyle("Report", fontName=REGULAR, fontSize=size, leading=leading,
                           alignment=TA_LEFT, textColor=color)
    block = Paragraph(value, style)
    _, height = block.wrap(width, H)
    block.drawOn(pdf, x, H - top - height)
    return top + height


def rule(pdf, top, x=LEFT, width=WIDTH, color=RULE):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(0.7)
    pdf.line(x, H - top, x + width, H - top)


def page_frame(pdf, number):
    pdf.setFillColor(ACCENT)
    pdf.rect(LEFT, H - 42, 16, 2.5, fill=1, stroke=0)
    text(pdf, LEFT + 25, 43, "BUSINESS INTELLIGENCE  /  WORKSHOP 3", 8.4, MUTED, BOLD)
    pdf.setFont(BOLD, 8.4)
    pdf.drawRightString(W - LEFT, H - 43, "IIB423T-1")
    rule(pdf, 798)
    text(pdf, LEFT, 817, "OPENING OUTCOMES FOR TRAINING PLANNING  /  C2 GROUP 03 DATA", 7.9, MUTED)
    pdf.setFont(BOLD, 8.4)
    pdf.drawRightString(W - LEFT, H - 817, f"{number} / 4")


def render_figure(pdf, figure, name, top, title, description):
    renderPDF.draw(figure, pdf, LEFT, H - top - figure.height)
    # Give standalone vectors a self-contained heading and data window.
    export = Drawing(WIDTH + 32, figure.height + 70)
    box(export, 0, 0, export.width, export.height, white)
    label(export, 16, export.height - 23, title, 13, bold=True)
    label(export, 16, export.height - 41, description, 9.3, MUTED)
    figure.translate(16, 12)
    export.add(figure)
    svg = renderSVG.drawToString(export, svgAttrs={"role": "img"})
    svg = svg.replace("<title>...</title>", f"<title>{escape(title)}</title>", 1)
    svg = svg.replace("<desc>...</desc>", f"<desc>{escape(description)}</desc>", 1)
    svg = svg.replace("font-family: Helvetica-Bold;", "font-family: Helvetica, Arial, sans-serif; font-weight: bold;")
    svg = svg.replace("font-family: Helvetica;", "font-family: Helvetica, Arial, sans-serif;")
    (HERE / "figures" / f"{name}.svg").write_text(svg, encoding="utf-8")


def cover(pdf, context, largest_cluster, largest_segment, sicilian):
    page_frame(pdf, 1)
    text(pdf, LEFT, 76, "VISUAL SYSTEM FOR AN OPENING REVIEW", 9.3, ACCENT, BOLD)
    author = os.environ.get("W3_AUTHOR", "").strip()
    if author:
        pdf.setFillColor(MUTED)
        pdf.setFont(BOLD, 9.3)
        pdf.drawRightString(W - LEFT, H - 76, f"Student: {author}")
    text(pdf, LEFT, 124, "From player groups", 47, font=DISPLAY)
    text(pdf, LEFT, 170, "to opening review", 47, font=DISPLAY)
    paragraph(pdf, LEFT, 190,
              "A club training coordinator needs to choose which opening games to bring to a review session. "
              "The three views move from C2's player groups to a training segment, then to the opening that offers "
              "the largest set of losses to review among the named families.", size=12, leading=16)

    rule(pdf, 255, color=FULL)
    steps = (
        ("01", "Summarize the groups", f"The largest cluster gap is {pp(largest_cluster)} pp."),
        ("02", "Compare training segments", f"Blitz 2000+ has the largest gap, {pp(largest_segment)} pp."),
        ("03", "Identify a review candidate", f"The Sicilian Defense accounts for {sicilian['loss']:,} White losses."),
    )
    for index, (number, heading, detail) in enumerate(steps):
        x = LEFT + index * (WIDTH / 3 + 1)
        text(pdf, x, 278, number, 9, ACCENT, BOLD)
        text(pdf, x, 297, heading, 10.4, font=BOLD)
        paragraph(pdf, x, 307, detail, 153, size=10.2, leading=13)
    rule(pdf, 347)

    text(pdf, LEFT, 376, "Shared visual rules", 23, font=DISPLAY)
    gutter = 23
    col = (WIDTH - gutter) / 2
    right = LEFT + col + gutter
    for x, heading, body in (
        (LEFT, "Typography and layout", "Use a serif headline, sans-serif labels and sentence case. "
         "Read down from the question and cohort to the final chart, takeaway, earlier draft and design notes."),
        (right, "Colour and emphasis", "Dark slate marks the primary series and light slate the comparison series in every view. "
         "Plum marks the item to act on next: blitz 2000+, then the Sicilian Defense. Teal, grey and rust are reserved "
         "for win, draw and loss, and nothing else uses them."),
    ):
        text(pdf, x, 403, heading, 10.7, font=BOLD)
        paragraph(pdf, x, 412, body, col, size=10.2, leading=13.6)
    rule(pdf, 481)
    for x, heading, body in (
        (LEFT, "Marks and shapes", "Filled = primary series, open = comparison series. Circle and square in View 1 (all test games, neither "
         "player in July); triangle and diamond in View 2 (blitz, rapid). No shape changes meaning between views. "
         "Outcomes are also named in text."),
        (right, "Scales, units and labels", "Views 1-2 share one -1 to +5 pp axis with a visible zero. View 3 counts whole games "
         "on a zero-based axis, so lengths compare directly. Each view states window, cohort and denominator. Rating bands keep "
         "their order and gaps use two decimals."),
    ):
        text(pdf, x, 503, heading, 10.7, font=BOLD)
        paragraph(pdf, x, 512, body, col, size=10.2, leading=13.6)

    pdf.setFillColor(PALE)
    pdf.rect(LEFT, H - 704, WIDTH, 96, stroke=0, fill=1)
    text(pdf, LEFT + 13, 624, "How to read the scores", 10.5, font=BOLD)
    paragraph(pdf, LEFT + 13, 633,
              "Score rate = (wins + 0.5 × draws) / games for the stated colour and cohort. "
              "A 1 pp gap is a difference of 0.01 points per game. The September test window contains "
              f"{context['n_test_games']:,} unique standard-rated Lichess games in blitz and rapid. "
              "The snapshot covers roughly 40 minutes. The observed outcomes can guide game selection for review. "
              "Estimating improvement from training would require a separate evaluation.",
              WIDTH - 26, size=10.4, leading=14)
    paragraph(pdf, LEFT, 716,
              "<b>Sources.</b> C2 clustering notebook (sections 4 and 6-7), its exported tables, "
              "and the frozen September split. The chart source includes the underlying values and the refresh procedure.",
              size=9.7, leading=13, color=MUTED)
    paragraph(pdf, LEFT, 751,
              "<b>AI disclosure.</b> Codex helped aggregate and cross-check outcomes, implement the first graphics "
              "and draft the first design rationale. Claude helped revise the marker shapes, colours, View 3 and the "
              "design text.",
              size=9.7, leading=13, color=MUTED)
    pdf.showPage()


def view_header(pdf, number, title, question, task, cohort):
    page_frame(pdf, number + 1)
    text(pdf, LEFT, 75, f"VIEW {number:02d} / {('PLAYER GROUPS', 'TRAINING SEGMENTS', 'OPENING FAMILIES')[number - 1]}",
         9.3, ACCENT, BOLD)
    text(pdf, LEFT, 116, title, 33, font=DISPLAY)
    text(pdf, LEFT, 141, question, 11.1, font=BOLD)
    paragraph(pdf, LEFT, 150, f"<b>Task.</b> {task}", size=10.1, leading=13)
    text(pdf, LEFT, 180, cohort, 9.2, ACCENT if number == 3 else MUTED)
    rule(pdf, 190)


def stage(pdf, top, lead, qualifier):
    text(pdf, LEFT, top, lead, 9.3, ACCENT if lead == "AFTER" else MUTED, BOLD)
    text(pdf, LEFT + 54, top, qualifier, 9.5, MUTED)


def takeaway(pdf, top, prose):
    pdf.setFillColor(ACCENT)
    pdf.rect(LEFT, H - top - 31, 2, 31, fill=1, stroke=0)
    paragraph(pdf, LEFT + 12, top, prose, WIDTH - 15, size=10.5, leading=14.3)


def design_notes(pdf, top, design, review, left_width=270):
    """Left: encoding, reading problem, change and class concept. Right: limit, risk, keep, next."""
    col_gap = 22
    widths = (left_width, WIDTH - left_width - col_gap)
    right = LEFT + widths[0] + col_gap
    left_items = list(design)
    right_items = [f"<b>{tag}.</b> {detail}" for tag, detail in zip(("Limit", "Risk", "Keep", "Next"), review)]
    for size in (9.6, 9.3, 9.0, 8.7, 8.4):
        leading = size * 1.28
        heights = []
        for items, width in zip((left_items, right_items), widths):
            total = top + 24
            for item in items:
                block = Paragraph(item, ParagraphStyle("Fit", fontName=REGULAR, fontSize=size, leading=leading))
                total += block.wrap(width, H)[1] + 4
            heights.append(total)
        if max(heights) < 797:
            break
    assert max(heights) < 797, heights
    rule(pdf, top)
    text(pdf, LEFT, top + 17, "Design and redesign", 10.7, font=BOLD)
    text(pdf, right, top + 17, "Trade-off and next improvement", 10.7, font=BOLD)
    for x, items, width in ((LEFT, left_items, widths[0]), (right, right_items, widths[1])):
        y = top + 24
        for item in items:
            y = paragraph(pdf, x, y, item, width, size=size, leading=leading) + 4
    pdf.showPage()


def read_chart_inputs():
    clusters = read_csv(DATA / "cluster_gaps.csv")
    segments = read_csv(DATA / "segment_gaps.csv")
    raw_openings = read_csv(DATA / "opening_chart_summary.csv")
    context = json.loads((DATA / "context.json").read_text(encoding="utf-8"))
    breakdown = [{"opening_family": row["opening_family"],
                  **{key: int(row[key]) for key in (*OUTCOMES, "games", "families")}}
                 for row in raw_openings]
    assert len(breakdown) == 6 and breakdown[-1]["opening_family"] == "Other"
    assert all(row["games"] == sum(row[o] for o in OUTCOMES) for row in breakdown)
    breakdown[-1]["opening_family"] = f"Other ({breakdown[-1]['families']} families)"
    return clusters, segments, breakdown, context


def comparison_rows(clusters, segments):
    cluster_rows = [
        (f"Cluster {row['cluster']}", f"{float(row['blitz_share']):.0%} blitz  /  mean rating {float(row['mean_rating']):,.0f}",
         float(row["full_gap_pp"]), float(row["unseen_gap_pp"]))
        for row in sorted(clusters, key=lambda row: -int(row["n_full"]))
    ]
    by_band = defaultdict(dict)
    for row in segments:
        by_band[row["rating_band"]][row["speed"]] = float(row["white_minus_black_pp"])
    segment_rows = [(rating, "", by_band[rating]["blitz"], by_band[rating]["rapid"]) for rating in BANDS]
    return cluster_rows, segment_rows


def build():
    clusters, segments, breakdown, context = read_chart_inputs()
    openings = breakdown[:-1]
    sicilian = openings[0]
    assert sicilian["opening_family"] == "Sicilian Defense" and sicilian["loss"] == max(row["loss"] for row in openings)
    selected = max(segments, key=lambda row: abs(float(row["white_minus_black_pp"])))
    assert (selected["speed"], selected["rating_band"]) == ("blitz", "2000+")
    total = sum(row["games"] for row in breakdown)
    assert total == int(selected["n_white"])
    losses = sum(row["loss"] for row in breakdown)
    win_points = sum(row["win"] + 0.5 * row["draw"] for row in breakdown)
    assert abs(win_points / total - float(selected["white_score_rate"])) < 1e-12

    cluster_rows, segment_rows = comparison_rows(clusters, segments)
    largest_cluster = max(cluster_rows, key=lambda row: abs(row[2]))[2]
    gap = float(selected["white_minus_black_pp"])
    (HERE / "figures").mkdir(exist_ok=True)
    pdf = canvas.Canvas(str(HERE / "W3_Opening_Review.pdf"), pagesize=A4, invariant=True)
    pdf.setTitle("From player groups to opening review | Workshop 3")
    pdf.setSubject("An opening-review visual system based on the C2 chess project")
    cover(pdf, context, largest_cluster, gap, sicilian)

    view_header(pdf, 1, "Three groups favour White", "How large is the score gap within each C2 group?",
                "Summarize White-minus-Black score across the four clusters.",
                f"{WINDOW}  |  {context['n_test_games'] * 2:,} player-game perspectives")
    stage(pdf, 207, "AFTER", "Paired positions expose agreement and reversals")
    cluster_meta = "Lichess · 1 Sep 2026, 00:00–00:40 UTC · C2 clusters · White minus Black score"
    render_figure(pdf, paired_dot_figure(cluster_rows, "cluster"), "01-clusters-after", 212,
                  "Colour gap by C2 cluster | Final", cluster_meta)
    smallest = cluster_rows[-1]
    takeaway(pdf, 409,
             f"<b>Three large groups retain a White edge</b> in the {context['n_unseen_games']:,} games where "
             f"neither player occurs in July. Cluster 3 crosses zero ({pp(smallest[2])} to {pp(smallest[3])} pp).")
    stage(pdf, 458, "BEFORE", "First draft with paired bars, in cluster ID order")
    render_figure(pdf, paired_bar_figure(sorted(cluster_rows), "cluster"), "01-clusters-before", 463,
                  "Colour gap by C2 cluster | First draft", cluster_meta)
    paragraph(pdf, LEFT, 601,
              f"C2 checks. Both colours share a cluster in 95.33% of test games, which pulls the pooled score "
              f"towards 50%. The largest cluster-share range across the three archive windows is "
              f"{context['largest_window_share_range_pp']:.1f} pp.", size=9.1, leading=11.5, color=MUTED)
    design_notes(pdf, 633,
                 ("<b>Encoding.</b> Cluster (nominal) sets the row. Gap in pp (quantitative, signed) sets horizontal position "
                  "on a common axis. Subset (nominal) sets shape: filled circle = all test games, open square = neither "
                  "player in July.",
                  "<b>Reading problem.</b> Paired bars in ID order hid which groups matter most and masked the sign change "
                  "in Cluster 3.",
                  "<b>Change.</b> Dots on one axis, rows sorted by size, linked pairs, exact labels.",
                  "<b>Classes 09-11.</b> Position beats length for small differences; order follows the task; direct "
                  "labels replace a key."),
                 ("The compact gaps compress the two colour rates and hide uncertainty.",
                  "Readers could overread the small reversal for Cluster 3.",
                  "A signed axis makes the broad pattern easy to scan.",
                  "Add player-aware uncertainty intervals for the gaps."))

    view_header(pdf, 2, "Blitz 2000+ has the widest gap",
                "Where does the score gap grow when rating bands are kept separate?",
                "Compare White-minus-Black score across the eight speed and rating combinations.",
                f"{WINDOW}  |  {context['n_test_games'] * 2:,} player-game perspectives")
    stage(pdf, 207, "AFTER", "Aligned dots show how the two speeds differ by rating")
    segment_meta = "Lichess · 1 Sep 2026, 00:00–00:40 UTC · Club segments · Focal-player rating"
    render_figure(pdf, paired_dot_figure(segment_rows, "segment"), "02-segments-after", 212,
                  "Colour gap by speed and rating | Final", segment_meta)
    takeaway(pdf, 409,
             f"<b>The {pp(gap)} pp gap sets up the opening review.</b> Blitz 2000+ scores "
             f"{float(selected['white_score_rate']):.2%} for White (n = {int(selected['n_white']):,}) "
             f"and {float(selected['black_score_rate']):.2%} for Black (n = {int(selected['n_black']):,}).")
    stage(pdf, 458, "BEFORE", "First draft with paired bars and a key")
    render_figure(pdf, paired_bar_figure(segment_rows, "segment"), "02-segments-before", 463,
                  "Colour gap by speed and rating | First draft", segment_meta)
    paragraph(pdf, LEFT, 601,
              "The band uses the rating of the player whose colour is being scored. For the opening review, "
              "the coordinator follows the White side of the highlighted segment.", size=9.1, leading=11.5, color=MUTED)
    design_notes(pdf, 633,
                 ("<b>Encoding.</b> Rating band (ordinal) sets the row, in order. Gap in pp (quantitative, signed) sets "
                  "horizontal position on View 1's axis. Speed (nominal) sets shape: filled triangle = blitz, open "
                  "diamond = rapid. Plum marks the selected segment.",
                  "<b>Reading problem.</b> Readers matched bars to a key to tell speeds apart, and the largest gap was "
                  "not easy to find.",
                  "<b>Change.</b> Aligned dots, exact labels, shapes instead of a key, one plum highlight.",
                  "<b>Classes 09-11.</b> Position on a common scale; colour is not the only carrier of a difference; "
                  "one emphasis only."),
                 ("Colour rates can include different games in the same rating band.",
                  "Readers could mistake the gap for a comparison of identical matchups.",
                  "The grouping matches how the coordinator plans sessions.",
                  "Add a companion cut where both players fall in the same band."))

    ranked = sorted(openings[:5], key=lambda row: (-row["loss"], -row["games"]))
    other = breakdown[-1]
    assert ranked[0] is sicilian and other["loss"] == losses - sum(row["loss"] for row in ranked)
    assert sicilian["loss"] / sicilian["games"] > losses / total
    view_header(pdf, 3, "Start with Sicilian Defense losses",
                "How did the most-played openings finish for White in blitz 2000+?",
                "Identify a named family with a large set of losses to review.",
                f"{WINDOW}  |  White rated 2000+  |  Blitz  |  {total:,} unique games")
    stage(pdf, 207, "AFTER", "Ranked by losses, all bars share a zero baseline")
    opening_meta = f"Lichess · 1 Sep 2026, 00:00–00:40 UTC · White 2000+ · Blitz · {total:,} games"
    render_figure(pdf, ranked_loss_bars(ranked, other, losses / total), "03-openings-after", 212,
                  "Opening families and White results | Final", opening_meta)
    takeaway(pdf, 431, f"<b>Sicilian Defense had {sicilian['loss']} losses in {sicilian['games']} games "
             f"({sicilian['loss'] / sicilian['games']:.1%}).</b> That is the most losses of any family, "
             f"{sicilian['loss'] - ranked[1]['loss']} more than {ranked[1]['opening_family']}, and a loss rate above the "
             f"cohort's {losses / total:.1%}.")
    stage(pdf, 474, "BEFORE", "First draft with stacked counts in alphabetical order")
    render_figure(pdf, stacked_opening_bars(breakdown), "03-openings-before", 479,
                  "Opening families and White results | First draft", opening_meta)
    paragraph(pdf, LEFT, 616,
              "Family is identified after 20 plies (10 moves per side). Both versions use the same counts.",
              size=9.1, leading=11.5, color=MUTED)
    design_notes(pdf, 636,
                 ("<b>Encoding.</b> Family (nominal) sets the row, ranked by losses. Games (quantitative, zero-based) set bar "
                  "length from a baseline where losses start. Outcome (nominal) sets colour and text. Plum marks the "
                  "family to review first.",
                  "<b>Reading problem.</b> Win segments came first, so loss segments started at different points and "
                  "could not be compared across alphabetical rows.",
                  "<b>Change.</b> Rank by losses, anchor them at zero, print counts and loss rates, note what is not drawn.",
                  "<b>Classes 09-11.</b> Length from a common baseline is read more precisely than area or angle; the "
                  "chart follows the task (identify)."),
                 (f"Counts follow exposure, so the most played family can have the most losses. Other combines "
                  f"{other['families']} families and is not drawn.",
                  "Readers could read the longest loss bar as the weakest opening, or trust small-sample rates as much as "
                  "Sicilian's.",
                  "Loss counts show where the most review material is; the rate beside each bar adds context.",
                  "Add intervals to the loss rates and rank every family above a minimum sample size."), left_width=262)

    pdf.save()


if __name__ == "__main__":
    build()
