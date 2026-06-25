"""
Generate etru-facility-guide.pdf for SafeConnect.
Uses only standard ReportLab platypus flowables — no custom Flowable subclasses
that embed nested Paragraphs, which require pre-wrapping in newer ReportLab.
"""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle,
)
import os

# ── Paths ───────────────────────────────────────────────────────────────────
BASE      = r"C:\Users\RyanFoss\Documents\Claude\Projects\safeconnect-landing"
LOGO_PATH = os.path.join(BASE, "assets", "logo.png")
OUT_PATH  = os.path.join(BASE, "assets", "etru-facility-guide.pdf")

# ── Brand colors ────────────────────────────────────────────────────────────
NAVY         = colors.HexColor("#0b1f3a")
NAVY_DARK    = colors.HexColor("#071528")
BLUE         = colors.HexColor("#1565c0")
BLUE_LIGHT_BG = colors.HexColor("#eaf1fb")
GRAY_BODY    = colors.HexColor("#333333")
GRAY_LIGHT   = colors.HexColor("#666666")
WHITE        = colors.white

MARGIN = inch


# ── Header / footer drawn on every page ────────────────────────────────────
def draw_header_footer(canvas, doc):
    canvas.saveState()
    pw, ph = LETTER

    # Logo top-left
    if os.path.exists(LOGO_PATH):
        canvas.drawImage(
            LOGO_PATH,
            MARGIN,
            ph - MARGIN * 0.82,
            width=110, height=36,
            preserveAspectRatio=True,
            mask="auto",
        )

    # Thin rule under header zone
    canvas.setStrokeColor(colors.HexColor("#dce4ef"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, ph - MARGIN, pw - MARGIN, ph - MARGIN)

    # Thin rule above footer zone
    canvas.line(MARGIN, MARGIN * 0.72, pw - MARGIN, MARGIN * 0.72)

    # Footer contact string (centered)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY_LIGHT)
    canvas.drawCentredString(
        pw / 2,
        MARGIN * 0.46,
        "info@safeconnectsystems.com  |  (844) 787-2332  |  www.safeconnectsystems.com",
    )

    # Page number (right)
    canvas.drawRightString(pw - MARGIN, MARGIN * 0.46, f"Page {doc.page}")

    canvas.restoreState()


# ── Styles ──────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)


STYLES = {
    "eyebrow": S("eyebrow", fontName="Helvetica-Bold", fontSize=7.5,
                 textColor=BLUE, leading=11, spaceBefore=0, spaceAfter=4),
    "h1": S("h1", fontName="Helvetica-Bold", fontSize=22,
            textColor=NAVY, leading=28, spaceBefore=16, spaceAfter=8),
    "h2": S("h2", fontName="Helvetica-Bold", fontSize=14,
            textColor=NAVY, leading=19, spaceBefore=22, spaceAfter=7),
    "step_label": S("step_label", fontName="Helvetica-Bold", fontSize=7.5,
                    textColor=BLUE, leading=11, spaceBefore=18, spaceAfter=3),
    "step_head": S("step_head", fontName="Helvetica-Bold", fontSize=12,
                   textColor=NAVY, leading=17, spaceBefore=2, spaceAfter=5),
    "body": S("body", fontName="Helvetica", fontSize=10,
              textColor=GRAY_BODY, leading=16, spaceBefore=0, spaceAfter=9),
    "body_bullet": S("body_bullet", fontName="Helvetica", fontSize=10,
                     textColor=GRAY_BODY, leading=16, leftIndent=14,
                     spaceBefore=0, spaceAfter=5),
    "intro_label": S("intro_label", fontName="Helvetica-Bold", fontSize=7.5,
                     textColor=BLUE, leading=11, spaceBefore=0, spaceAfter=5),
    "intro_body": S("intro_body", fontName="Helvetica", fontSize=10,
                    textColor=colors.HexColor("#1a2a3a"), leading=16,
                    spaceBefore=0, spaceAfter=0),
    "cta_body": S("cta_body", fontName="Helvetica", fontSize=10,
                  textColor=colors.HexColor("#c8d8ee"), leading=16,
                  alignment=TA_CENTER, spaceBefore=0, spaceAfter=0),
    "faq_q": S("faq_q", fontName="Helvetica-Bold", fontSize=10,
               textColor=NAVY, leading=15, spaceBefore=0, spaceAfter=4),
    "faq_a": S("faq_a", fontName="Helvetica", fontSize=10,
               textColor=GRAY_BODY, leading=15, leftIndent=10,
               spaceBefore=0, spaceAfter=0),
}


def sp(n=8):
    return Spacer(1, n)


def rule():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#dce4ef"), spaceAfter=4)


def intro_block(avail_w, label_text, body_text):
    """Light-blue left-bordered intro block using a single-cell Table."""
    pad = 14
    inner = [[
        Paragraph(label_text, STYLES["intro_label"]),
        Paragraph(body_text,  STYLES["intro_body"]),
    ]]
    # Stack label + body vertically inside the table cell — use nested table
    cell_content = [
        [Paragraph(label_text, STYLES["intro_label"])],
        [Paragraph(body_text,  STYLES["intro_body"])],
    ]
    inner_tbl = Table(cell_content, colWidths=[avail_w - pad * 2 - 5])
    inner_tbl.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))

    outer = Table([[inner_tbl]], colWidths=[avail_w])
    outer.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), BLUE_LIGHT_BG),
        ("LINEBEFORE",    (0, 0), (0, -1),  5, BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING",   (0, 0), (-1, -1), pad),
        ("RIGHTPADDING",  (0, 0), (-1, -1), pad),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BLUE_LIGHT_BG]),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return outer


def cta_block(avail_w, body_text):
    """Dark navy centered CTA block."""
    t = Table([[Paragraph(body_text, STYLES["cta_body"])]], colWidths=[avail_w])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
        ("LEFTPADDING",   (0, 0), (-1, -1), 28),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 28),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [NAVY]),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return t


def faq_block(avail_w, q_text, a_text):
    """Single FAQ item: bordered card with Q+A."""
    inner = [
        [Paragraph(q_text, STYLES["faq_q"])],
        [Paragraph(a_text, STYLES["faq_a"])],
    ]
    t = Table(inner, colWidths=[avail_w - 28])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    outer = Table([[t]], colWidths=[avail_w])
    outer.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dce4ef")),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE]),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return outer


# ── Build ───────────────────────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUT_PATH,
        pagesize=LETTER,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN * 1.25,
        bottomMargin=MARGIN,
    )
    avail_w = LETTER[0] - 2 * MARGIN
    frame = Frame(
        MARGIN, MARGIN,
        avail_w,
        LETTER[1] - MARGIN * 1.25 - MARGIN,
        id="normal",
    )
    doc.addPageTemplates([
        PageTemplate(id="main", frames=[frame], onPage=draw_header_footer)
    ])

    story = []

    # ── Title area ────────────────────────────────────────────────────────
    story.append(sp(16))
    story.append(Paragraph("FREE GUIDE", STYLES["eyebrow"]))
    story.append(Paragraph(
        "The Real Cost of Electrifying Yard Operations", STYLES["h1"]))
    story.append(Paragraph(
        "Infrastructure, ROI, and what fleets need to know before switching to eTRU",
        STYLES["body"]))
    story.append(sp(6))
    story.append(rule())
    story.append(sp(14))

    # ── Intro block ───────────────────────────────────────────────────────
    story.append(intro_block(
        avail_w,
        "SHORT ANSWER",
        "To prepare your facility for electric TRU (eTRU) standby, you need to evaluate your available "
        "power, electrical capacity, where power will be delivered across the yard, and how the system "
        "will be installed safely. Most facilities can support eTRU with the right planning, but the "
        "details matter — and that's where projects tend to succeed or stall.",
    ))
    story.append(sp(18))

    # ── Section 1 ─────────────────────────────────────────────────────────
    story.append(Paragraph(
        "What does it mean to prepare a facility for eTRU?", STYLES["h2"]))
    story.append(Paragraph(
        "Preparing your facility for eTRU means making sure you can reliably supply electrical power "
        "to refrigerated trailers while they're stationary — whether they're at the dock or staged in "
        "the yard. On the surface, that sounds straightforward. In practice, it touches several parts "
        "of your operation at once: your electrical infrastructure, your yard layout, and how trailers "
        "actually move through your facility during the day. Facilities that take the time to think "
        "through those pieces upfront tend to have a much smoother transition.",
        STYLES["body"]))

    # ── Steps ─────────────────────────────────────────────────────────────
    steps = [
        (
            "STEP 1",
            "Start with your power source",
            "The first question is whether your facility has access to the right type of power. Most "
            "eTRU systems run on three-phase power, typically 480V (preferred) or 230V. If that's "
            "already in place, you're ahead of the game. If not, it doesn't mean electrification is "
            "off the table — but it does mean you'll need to involve your utility provider early. In "
            "many cases, utilities can upgrade or extend service, but those timelines can impact your "
            "rollout if they're not accounted for upfront.",
        ),
        (
            "STEP 2",
            "Make sure you have enough capacity",
            "Having the right voltage is only part of the equation. You also need to be able to support "
            "the number of trailers that may be plugged in at the same time. This is where capacity "
            "planning comes in. A facility might technically have the right power available, but still "
            "run into issues if multiple trailers are drawing power simultaneously during peak periods. "
            "That's why it's important to look at your operation as a whole: when trailers arrive, how "
            "long they dwell, and how many are likely to be connected at once. Planning around those "
            "realities helps avoid bottlenecks later.",
        ),
        (
            "STEP 3",
            "Think carefully about where power needs to go",
            "One of the most common challenges is getting power to the right places. In most facilities, "
            "trailers move between dock doors, staging areas, and different parts of the yard throughout "
            "the day. That means power needs to be available where trailers actually spend time — not "
            "just where it's easiest to install. When placement isn't aligned with real workflows, it "
            "can create small inefficiencies that add up quickly: extra steps for drivers, longer "
            "connection times, or workarounds that weren't part of the original plan.",
        ),
        (
            "STEP 4",
            "Match the system to your operation",
            "There's no one-size-fits-all setup for eTRU infrastructure. Some facilities are best "
            "served by dock-based connections. Others benefit from yard pedestals or shared configurations "
            "that support multiple trailers from a single circuit. The right approach depends on how "
            "your facility operates day to day — how many trailers you handle, how space is laid out, "
            "and how power can be distributed efficiently. Choosing a configuration that fits your "
            "operation upfront can make a big difference in both installation cost and long-term usability.",
        ),
        (
            "STEP 5",
            "Design for safety and reliability from the start",
            "Because eTRU systems involve high-voltage power, safety truly needs to be built into the "
            "design. That includes thinking through how connections are made and broken, where equipment "
            "is positioned, and how to minimize risk in a busy yard environment. Situations like "
            "accidental drive-offs or exposed connections can lead to equipment damage or safety concerns "
            "if they're not addressed properly. Well-designed systems account for those realities and "
            "are built to operate reliably within them — and not just under ideal conditions.",
        ),
    ]

    for label, heading, body in steps:
        story.append(KeepTogether([
            Paragraph(label,   STYLES["step_label"]),
            Paragraph(heading, STYLES["step_head"]),
            Paragraph(body,    STYLES["body"]),
        ]))

    # ── Common Mistakes ───────────────────────────────────────────────────
    story.append(Paragraph("Common mistakes to avoid", STYLES["h2"]))
    story.append(Paragraph(
        "A lot of challenges with electrification don't come from how the technological transition is "
        "planned out. Facilities often run into trouble when they underestimate how much power they'll "
        "need, wait too long to involve utility providers, or focus heavily on equipment without "
        "considering how it will actually function in the yard. In other cases, electrification is "
        "treated as a simple upgrade, when in reality it changes how parts of the operation work day "
        "to day. Taking a more holistic view early on helps avoid those issues.",
        STYLES["body"]))

    # ── ROI ───────────────────────────────────────────────────────────────
    story.append(Paragraph("What does ROI actually depend on?", STYLES["h2"]))
    story.append(Paragraph(
        "When people think about ROI, they often focus on fuel savings first. That's part of the "
        "picture, but it's not the whole story. In practice, the return tends to come from a "
        "combination of factors — reduced diesel use, fewer maintenance demands, longer equipment life, "
        "and more predictable energy costs. Over time, those benefits stack up, especially in operations "
        "where trailers spend significant time in the yard. Facilities that plan infrastructure carefully "
        "tend to see those returns sooner, because they avoid rework and minimize disruption during "
        "implementation.",
        STYLES["body"]))

    # ── Bottom Line ───────────────────────────────────────────────────────
    story.append(Paragraph("The Bottom Line", STYLES["h2"]))
    story.append(Paragraph(
        "Most facilities can support eTRU — but the difference between a smooth rollout and a "
        "difficult one usually comes down to planning. Understanding your power needs, aligning "
        "infrastructure with real operations, and designing with safety in mind are what set "
        "successful projects apart.",
        STYLES["body"]))

    # ── Thinking About eTRU ───────────────────────────────────────────────
    story.append(Paragraph(
        "Thinking About eTRU? Start with Your Facility", STYLES["h2"]))
    story.append(Paragraph(
        "Every facility is different — and the details matter. If you're evaluating electric standby, "
        "the most effective place to start is with a clear understanding of your current infrastructure "
        "and how your operation actually runs day to day.",
        STYLES["body"]))
    story.append(Paragraph(
        "A facility assessment can help you:", STYLES["body"]))

    for bullet in [
        "Identify power and capacity gaps",
        "Understand what upgrades may be required",
        "Estimate installation scope and cost",
        "Avoid common planning mistakes",
    ]:
        story.append(Paragraph(f"•  {bullet}", STYLES["body_bullet"]))

    story.append(sp(8))
    story.append(Paragraph(
        "More importantly, it helps you make the decision with confidence — "
        "before committing time and capital.",
        STYLES["body"]))

    # ── CTA Block ─────────────────────────────────────────────────────────
    story.append(sp(12))
    story.append(cta_block(
        avail_w,
        "Ready to get started? Visit safeconnectsystems.com, email "
        "info@SafeConnectSystems.com, or call (844) 787-2332. If you're "
        "planning a conversion to eTRU and want a no-obligation quote, "
        "we're happy to help.",
    ))
    story.append(sp(28))
    story.append(rule())

    # ── FAQ ───────────────────────────────────────────────────────────────
    story.append(Paragraph("Frequently Asked Questions", STYLES["h2"]))
    story.append(sp(10))

    faqs = [
        (
            "How much power do I need to support eTRU at my facility?",
            "The amount of power required depends on how many trailers you plan to support at once and "
            "how long they remain plugged in. Most facilities need to evaluate peak demand — when "
            "multiple trailers are drawing power simultaneously — to ensure they have sufficient "
            "electrical capacity.",
        ),
        (
            "Can existing facilities be upgraded for eTRU, or do they need to be rebuilt?",
            "Most existing facilities can be upgraded to support eTRU. In many cases, this involves "
            "adding or expanding electrical service, upgrading panels, and distributing power to dock "
            "doors or yard locations. Early coordination with your utility provider is key.",
        ),
        (
            "What voltage is required for electric standby systems?",
            "eTRU systems typically operate on three-phase power, most commonly 480V or 230V. The "
            "optimal setup depends on your facility and equipment, but 480V is often preferred for "
            "efficiency.",
        ),
        (
            "What are the biggest challenges when preparing a facility for eTRU?",
            "The most common challenges include limited electrical capacity, delays in utility "
            "upgrades, and aligning power distribution with real-world yard operations. Operational "
            "flow — where trailers sit and for how long — is often overlooked but critical.",
        ),
        (
            "How long does it take to get a facility ready for eTRU?",
            "Timelines vary depending on infrastructure upgrades and utility involvement. Some "
            "projects can move quickly if power is already available, while others may take longer "
            "if new service or capacity increases are required.",
        ),
        (
            "Is eTRU infrastructure worth the investment?",
            "For many operations, the return comes from a combination of reduced fuel use, lower "
            "maintenance, longer equipment life, and more predictable energy costs. Facilities that "
            "plan infrastructure correctly tend to see faster and more reliable ROI.",
        ),
    ]

    for i, (q, a) in enumerate(faqs):
        story.append(KeepTogether([
            faq_block(avail_w, q, a),
            sp(10) if i < len(faqs) - 1 else sp(4),
        ]))

    doc.build(story)
    size = os.path.getsize(OUT_PATH)
    print(f"PDF written to: {OUT_PATH}  ({size:,} bytes)")


if __name__ == "__main__":
    build()
