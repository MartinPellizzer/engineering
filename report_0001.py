
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT

# ----------------------------
# SETUP
# ----------------------------
doc = SimpleDocTemplate(
    "elite_ozone_food_proposal_0001.pdf",
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
# STYLES
# ----------------------------
cover_title = ParagraphStyle('cover', fontName='Helvetica-Bold',
                             fontSize=28, textColor=PRIMARY)

section = ParagraphStyle('section', fontName='Helvetica-Bold',
                         fontSize=16, textColor=PRIMARY, spaceBefore=30)

body = ParagraphStyle('body', fontSize=10.5, leading=15)

insight = ParagraphStyle('insight', fontName='Helvetica-Bold',
                         fontSize=11.5, textColor=PRIMARY)

meta = ParagraphStyle('meta', fontSize=9, textColor=GREY)

footer = ParagraphStyle('footer', fontSize=8,
                        textColor=GREY, alignment=TA_RIGHT)

# ----------------------------
# COMPONENTS
# ----------------------------
class AccentLine(Flowable):
    def draw(self):
        self.canv.setFillColor(PRIMARY)
        self.canv.rect(0, 0, 70, 4, fill=1, stroke=0)

def insight_box(title, text):
    t = Table([
        [Paragraph(title, insight)],
        [Paragraph(text, body)]
    ], colWidths=[420])

    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, LIGHT_GREY),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def divider(title):
    return [
        Spacer(1, 200),
        AccentLine(),
        Spacer(1, 20),
        Paragraph(title.upper(), cover_title),
        PageBreak()
    ]

# ----------------------------
# HEADER / FOOTER
# ----------------------------
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(70, 810, 525, 810)

    canvas.setFont("Helvetica", 8)
    canvas.drawString(70, 820, "OZONE INDUSTRIAL SOLUTIONS")
    canvas.drawRightString(525, 820, "Confidential Proposal")

    canvas.drawString(70, 30, "Confidential")
    canvas.drawRightString(525, 30, str(doc.page))
    canvas.restoreState()

# ----------------------------
# CONTENT
# ----------------------------
elements = []

# ----------------------------
# COVER
# ----------------------------
elements.append(Spacer(1, 140))
elements.append(AccentLine())
elements.append(Spacer(1, 25))

elements.append(Paragraph("Technical & Commercial Proposal", cover_title))
elements.append(Spacer(1, 20))
elements.append(Paragraph(
    "Advanced Ozone Treatment for Food Processing Environments",
    body
))

elements.append(Spacer(1, 100))

elements.append(Paragraph("Prepared for", meta))
elements.append(Paragraph("Alpine Fresh Foods S.p.A.", section))

elements.append(Spacer(1, 60))
elements.append(Paragraph("March 2026", meta))

elements.append(Spacer(1, 120))
elements.append(Paragraph(
    "Strictly Confidential – Unauthorized distribution prohibited",
    footer
))

elements.append(PageBreak())

# ----------------------------
# EXECUTIVE SUMMARY
# ----------------------------
elements.extend(divider("Executive Summary"))

elements.append(Paragraph("Executive Summary", section))

elements.append(insight_box(
    "Key Insight",
    "Ozone-based sanitation enables significant reduction in microbial load "
    "while eliminating chemical residues, improving both food safety compliance "
    "and product shelf life."
))

elements.append(Spacer(1, 15))

elements.append(Paragraph(
    "This proposal outlines the implementation of an advanced ozone treatment system "
    "for food processing applications, targeting improved hygiene standards, "
    "reduced operational costs, and enhanced product quality.",
    body
))

# ----------------------------
# BUSINESS IMPACT
# ----------------------------
elements.append(Paragraph("Business Impact", section))

elements.append(insight_box(
    "Expected Outcomes",
    "• Reduction in chemical sanitizers\n"
    "• Extended shelf life of products\n"
    "• Lower microbiological contamination risk\n"
    "• Improved compliance with HACCP protocols"
))

# ----------------------------
# TECHNICAL SOLUTION
# ----------------------------
elements.extend(divider("Technical Solution"))

elements.append(Paragraph("System Architecture", section))

elements.append(Paragraph(
    "The system integrates ozone generation, controlled injection, and monitoring "
    "into existing processing lines, ensuring minimal disruption.",
    body
))

specs = [
    ["Ozone Output", "XX g/h"],
    ["Application", "Surface / Air Treatment"],
    ["Integration", "Inline / Standalone"],
    ["Control System", "Automated PLC"]
]

elements.append(Table(specs, colWidths=[200, 200]))

# ----------------------------
# ROI SECTION
# ----------------------------
elements.extend(divider("Economic Impact"))

elements.append(Paragraph("Return on Investment", section))

elements.append(insight_box(
    "Financial Impact",
    "Typical installations achieve ROI within 12–24 months through "
    "chemical savings, waste reduction, and improved operational efficiency."
))

# ----------------------------
# RISK
# ----------------------------
elements.append(Paragraph("Risk Considerations", section))

elements.append(Paragraph(
    "The system is designed with safety interlocks, ozone destruct units, "
    "and full compliance with industrial safety standards.",
    body
))

# ----------------------------
# COMMERCIAL
# ----------------------------
elements.extend(divider("Commercial Proposal"))

pricing = [
    ["Ozone System Supply", "XXXXX €"],
    ["Installation & Integration", "XXXXX €"],
    ["Total Investment", "XXXXX €"]
]

elements.append(Table(pricing, colWidths=[300, 120]))

# ----------------------------
# SIGNATURE
# ----------------------------
elements.append(PageBreak())

elements.append(Paragraph("Approval", section))

elements.append(Table([
    ["Client Representative", ""],
    ["Name", ""],
    ["Signature", ""],
    ["Date", ""],
    ["", ""],
    ["Supplier", ""],
    ["Name", ""],
    ["Signature", ""],
    ["Date", ""],
], colWidths=[200, 200]))

# ----------------------------
# BUILD
# ----------------------------
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
