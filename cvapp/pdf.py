"""PDF ģenerēšana.

CV tiek uzzīmēts ar reportlab un nosūtīts pārlūkam kā lejupielādējams PDF fails.
Teksts PDF failā paliek atlasāms un kopējams.
"""
import os
from datetime import date
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Fonti ar latviešu burtiem (ā, č, ē, ģ, ī, ķ, ļ, ņ, š, ū, ž).
# Standarta PDF fonti tos neatbalsta, tāpēc meklējam sistēmas TTF fontu.
FONT_CANDIDATES = [
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
]

BRAND = colors.HexColor("#3b5bdb")

# Dizaini: tie paši trīs, kas ir lapā (classic, modern, minimal)
THEMES = {
    "classic": {"center": True, "band": False, "accent": colors.HexColor("#222222"), "rule": True},
    "modern": {"center": False, "band": True, "accent": BRAND, "rule": False},
    "minimal": {"center": False, "band": False, "accent": colors.HexColor("#888888"), "rule": False},
}


def _register_fonts():
    """Atrod pirmo pieejamo fontu pāri un reģistrē to. Atgriež (parastais, treknais)."""
    for regular, bold in FONT_CANDIDATES:
        if os.path.exists(regular) and os.path.exists(bold):
            pdfmetrics.registerFont(TTFont("CVFont", regular))
            pdfmetrics.registerFont(TTFont("CVFont-Bold", bold))
            # Lai <b>...</b> darbotos ar šo fontu
            pdfmetrics.registerFontFamily("CVFont", normal="CVFont", bold="CVFont-Bold")
            return "CVFont", "CVFont-Bold"
    # Rezerves variants: latviešu burti var neparādīties pareizi
    return "Helvetica", "Helvetica-Bold"


def _text(value):
    """Droši pārveido tekstu priekš Paragraph (izslēdz <, &, saglabā jaunas rindas)."""
    return escape(str(value)).replace("\n", "<br/>")


def _month_year(d):
    return d.strftime("%m.%Y") if isinstance(d, date) else ""


def build_cv_pdf(cv):
    """Izveido PDF no CV objekta un atgriež baitus."""
    font, bold = _register_fonts()
    theme = THEMES.get(cv.template, THEMES["classic"])
    accent = theme["accent"]

    margin = 18 * mm
    width = A4[0] - 2 * margin - 12  # 12 = iekšējās atstarpes dokumenta rāmī

    base = ParagraphStyle("base", fontName=font, fontSize=10, leading=14, textColor=colors.HexColor("#222222"))
    h1 = ParagraphStyle("h1", parent=base, fontName=bold, fontSize=22, leading=26,
                        alignment=TA_CENTER if theme["center"] else 0,
                        textColor=colors.white if theme["band"] else colors.HexColor("#222222"))
    job = ParagraphStyle("job", parent=base, fontSize=12, leading=16,
                         alignment=TA_CENTER if theme["center"] else 0,
                         textColor=colors.white if theme["band"] else colors.HexColor("#222222"))
    contacts = ParagraphStyle("contacts", parent=base, fontSize=9, textColor=colors.HexColor("#dfe5ff") if theme["band"] else colors.HexColor("#555555"),
                              alignment=TA_CENTER if theme["center"] else 0)
    h2 = ParagraphStyle("h2", parent=base, fontName=bold, fontSize=11, leading=14, textColor=accent, spaceBefore=10, spaceAfter=3)
    dates = ParagraphStyle("dates", parent=base, fontSize=9, textColor=colors.HexColor("#555555"), alignment=TA_RIGHT)

    story = []

    # ----- Galvene -----
    contact_parts = [cv.email, cv.phone, cv.city]
    header = [Paragraph(_text(cv.full_name), h1)]
    if cv.job_title:
        header.append(Paragraph(_text(cv.job_title), job))
    header.append(Paragraph(_text(" · ".join(p for p in contact_parts if p)), contacts))

    if theme["band"]:
        band = Table([[header]], colWidths=[width])
        band.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BRAND),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        story.append(band)
    else:
        story.extend(header)
        if theme["rule"] is False:
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"), spaceBefore=6, spaceAfter=2))

    def section(title):
        story.append(Paragraph(title.upper(), h2))
        if theme["rule"]:
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#222222"), spaceAfter=4))

    def item(left_html, right_text, description=""):
        row = Table([[Paragraph(left_html, base), Paragraph(_text(right_text), dates)]],
                    colWidths=[width * 0.72, width * 0.28])
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(row)
        if description:
            story.append(Paragraph(_text(description), base))
        story.append(Spacer(1, 5))

    # ----- Profils -----
    if cv.summary:
        section("Profils")
        story.append(Paragraph(_text(cv.summary), base))

    # ----- Darba pieredze -----
    experiences = list(cv.experiences.all())
    if experiences:
        section("Darba pieredze")
        for e in experiences:
            end = _month_year(e.end_date) if e.end_date else "līdz šim"
            item(f"<b>{_text(e.position)}</b>, {_text(e.company)}",
                 f"{_month_year(e.start_date)} – {end}", e.description)

    # ----- Izglītība -----
    educations = list(cv.educations.all())
    if educations:
        section("Izglītība")
        for ed in educations:
            end = ed.end_year if ed.end_year else "līdz šim"
            item(f"<b>{_text(ed.degree)}</b>, {_text(ed.institution)}", f"{ed.start_year} – {end}")

    # ----- Prasmes un valodas -----
    for title, rows in (("Prasmes", list(cv.skills.all())), ("Valodas", list(cv.languages.all()))):
        if rows:
            section(title)
            line = "   •   ".join(f"{_text(r.name)} ({_text(r.get_level_display())})" for r in rows)
            story.append(Paragraph(line, base))

    buffer = BytesIO()
    SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=margin, rightMargin=margin, topMargin=margin, bottomMargin=margin,
        title=f"{cv.full_name} – CV", author=cv.full_name,
    ).build(story)
    return buffer.getvalue()