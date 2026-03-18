from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT

# ----------------------------
# SETUP
# ----------------------------
doc = SimpleDocTemplate(
    "elite_ozone_food_proposal_0000.pdf",
    pagesize=A4,
    rightMargin=70,
    leftMargin=70,
    topMargin=90,
    bottomMargin=60
)

styles = getSampleStyleSheet()

PRIMARY = colors.HexColor("#0B1F3B")
GREY = colors.HexColor("#6B7280")
LIGHT_GREY = colors.HexColor("#E5E7EB")

# ----------------------------
# VISUAL ELEMENTS
# ----------------------------
class AccentLine(Flowable):
    def __init__(self, width=50, height=3):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(PRIMARY)
        self.canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)

# ----------------------------
# STYLES
# ----------------------------
cover_title = ParagraphStyle(
    'cover_title', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=28, leading=32,
    textColor=PRIMARY
)

big_section = ParagraphStyle(
    'big_section', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=22,
    textColor=PRIMARY
)

section = ParagraphStyle(
    'section', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=16,
    textColor=PRIMARY, spaceBefore=30, spaceAfter=10
)

body = ParagraphStyle(
    'body', parent=styles['Normal'],
    fontSize=10.5, leading=15
)

insight = ParagraphStyle(
    'insight', parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    textColor=PRIMARY,
    spaceAfter=6
)

meta = ParagraphStyle(
    'meta', parent=styles['Normal'],
    fontSize=9, textColor=GREY
)

footer = ParagraphStyle(
    'footer', parent=styles['Normal'],
    fontSize=8, textColor=GREY, alignment=TA_RIGHT
)

# ----------------------------
# HEADER / FOOTER
# ----------------------------
def header_footer(canvas, doc):
    canvas.saveState()

    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(70, 810, 525, 810)

    canvas.setFont("Helvetica", 8)
    canvas.drawString(70, 820, "YOUR COMPANY NAME")
    canvas.drawRightString(525, 820, "Industrial Ozone Consulting")

    canvas.drawString(70, 30, "Confidential")
    canvas.drawRightString(525, 30, str(doc.page))

    canvas.restoreState()

# ----------------------------
# COMPONENTS
# ----------------------------
def divider_page(title_text):
    return [
        Spacer(1, 200),
        AccentLine(80, 4),
        Spacer(1, 20),
        Paragraph(title_text.upper(), big_section),
        PageBreak()
    ]

def insight_box(title, content):
    table = Table([
        [Paragraph(title, insight)],
        [Paragraph(content, body)]
    ], colWidths=[420])

    table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, LIGHT_GREY),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))

    return table

# ----------------------------
# CONTENT
# ----------------------------
elements = []

# ----------------------------
# COVER (ULTRA CLEAN)
# ----------------------------
elements.append(Spacer(1, 140))
elements.append(AccentLine(70, 4))
elements.append(Spacer(1, 25))

elements.append(Paragraph(
    "Technical & Commercial Proposal",
    cover_title
))

elements.append(Spacer(1, 20))

elements.append(Paragraph(
    "Industrial Ozone System Implementation",
    body
))

elements.append(Spacer(1, 100))

elements.append(Paragraph("CLIENT COMPANY NAME", section))
elements.append(Paragraph("March 2026", meta))

elements.append(Spacer(1, 120))

elements.append(Paragraph(
    "Strictly Confidential – Do not distribute",
    footer
))

elements.append(PageBreak())

# ----------------------------
# DIVIDER: EXECUTIVE SUMMARY
# ----------------------------
elements.extend(divider_page("Executive Summary"))

# ----------------------------
# EXECUTIVE SUMMARY CONTENT
# ----------------------------
elements.append(Paragraph("Executive Summary", section))

elements.append(insight_box(
    "Key Insight",
    "A properly engineered ozone system can reduce operational costs "
    "while improving treatment efficiency by over 30%."
))

elements.append(Spacer(1, 15))

elements.append(Paragraph(
    "This proposal outlines a structured approach to the design, supply, "
    "and integration of a high-performance ozone system tailored to the client's needs.",
    body
))

# ----------------------------
# DIVIDER: TECHNICAL SOLUTION
# ----------------------------
elements.extend(divider_page("Technical Solution"))

elements.append(Paragraph("System Overview", section))

elements.append(insight_box(
    "Engineering Approach",
    "The system is designed using a modular architecture, ensuring scalability, "
    "ease of maintenance, and operational resilience."
))

elements.append(Spacer(1, 10))

specs = [
    ["Ozone Output", "XX g/h"],
    ["Power", "XX kW"],
    ["Cooling", "Air/Water"]
]

table = Table(specs, colWidths=[200, 200])
table.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,-1), 0.25, LIGHT_GREY),
]))

elements.append(table)

# ----------------------------
# DIVIDER: COMMERCIAL
# ----------------------------
elements.extend(divider_page("Commercial Proposal"))

elements.append(Paragraph("Investment Overview", section))

pricing = [
    ["System Supply", "XXXXX €"],
    ["Installation", "XXXXX €"],
    ["Total Investment", "XXXXX €"]
]

price_table = Table(pricing, colWidths=[300, 120])
price_table.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,-1), 0.25, LIGHT_GREY),
]))

elements.append(price_table)

# ----------------------------
# SIGNATURE PAGE
# ----------------------------
elements.append(PageBreak())

elements.append(Paragraph("Approval", section))

signature_table = Table([
    ["For the Client", ""],
    ["Name:", ""],
    ["Signature:", ""],
    ["Date:", ""],
    ["", ""],
    ["For Your Company", ""],
    ["Name:", ""],
    ["Signature:", ""],
    ["Date:", ""],
], colWidths=[200, 200])

elements.append(signature_table)

# ----------------------------
# APPENDIX
# ----------------------------
elements.extend(divider_page("Appendix"))

elements.append(Paragraph("Technical Documentation", section))
elements.append(Paragraph(
    "Detailed system specifications, certifications, and compliance documents "
    "are included in this section.",
    body
))

# ----------------------------
# BUILD
# ----------------------------
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
