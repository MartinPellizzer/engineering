
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

# ----------------------------
# DOCUMENT SETUP
# ----------------------------
doc = SimpleDocTemplate(
    "elite_ozone_food_proposal.pdf",
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
# CHARTS & DIAGRAMS
# ----------------------------
def roi_chart():
    d = Drawing(400, 200)
    lp = LinePlot()
    lp.x = 50
    lp.y = 50
    lp.height = 125
    lp.width = 300

    lp.data = [[(0, -100), (6, -50), (12, 0), (18, 40), (24, 100)]]
    lp.lines[0].strokeWidth = 2

    d.add(lp)
    return d

def process_diagram():
    d = Drawing(400, 150)

    d.add(Rect(10, 60, 80, 30))
    d.add(Rect(110, 60, 80, 30))
    d.add(Rect(210, 60, 80, 30))
    d.add(Rect(310, 60, 80, 30))

    d.add(String(20, 70, "Air/O2"))
    d.add(String(120, 70, "Ozone Gen"))
    d.add(String(220, 70, "Injection"))
    d.add(String(320, 70, "Food Line"))

    return d

def cost_comparison_table():
    data = [
        ["Cost Category", "Traditional Chemicals", "Ozone System"],
        ["Annual Chemicals", "€50,000", "€5,000"],
        ["Water Usage", "High", "Reduced"],
        ["Residues", "Present", "None"],
        ["Total 3-Year Cost", "€150,000+", "€80,000"]
    ]

    table = Table(data, colWidths=[150, 130, 130])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_GREY),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, LIGHT_GREY),
    ]))

    return table

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

# COVER
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

# EXECUTIVE SUMMARY
elements.extend(divider("Executive Summary"))

elements.append(Paragraph("Executive Summary", section))

elements.append(insight_box(
    "Key Insight",
    "Ozone-based sanitation enables significant reduction in microbial load "
    "while eliminating chemical residues, improving food safety and shelf life."
))

elements.append(Spacer(1, 15))

elements.append(Paragraph(
    "Based on Alpine Fresh Foods S.p.A.'s high-throughput processing environment, "
    "the proposed ozone system integrates seamlessly into existing production lines "
    "while significantly improving hygiene performance.",
    body
))

# ROI
elements.append(Paragraph("ROI Projection", section))
elements.append(roi_chart())

# BUSINESS IMPACT
elements.append(Paragraph("Business Impact", section))
elements.append(insight_box(
    "Expected Outcomes",
    "• Reduced chemical usage\n• Extended shelf life\n• Lower contamination risk\n• HACCP compliance"
))

# TECHNICAL
elements.extend(divider("Technical Solution"))

elements.append(Paragraph("Process Flow Diagram", section))
elements.append(process_diagram())

elements.append(Paragraph("System Specifications", section))
elements.append(Table([
    ["Ozone Output", "XX g/h"],
    ["Application", "Surface / Air"],
    ["Control", "PLC Automated"]
], colWidths=[200, 200]))

# ECONOMIC
elements.extend(divider("Economic Impact"))

elements.append(Paragraph("Cost Comparison", section))
elements.append(cost_comparison_table())

# COMMERCIAL
elements.extend(divider("Commercial Proposal"))

elements.append(Table([
    ["System Supply", "XXXXX €"],
    ["Installation", "XXXXX €"],
    ["Total", "XXXXX €"]
], colWidths=[300, 120]))

# SIGNATURE
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

# APPENDIX
elements.extend(divider("Appendix"))

elements.append(Paragraph("Technical Documentation", section))
elements.append(Paragraph(
    "Detailed specifications, certifications, and compliance documents are included.",
    body
))

# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
