import subprocess

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Image
from reportlab.platypus import PageBreak

from reportlab.lib.styles import ParagraphStyle

doc = SimpleDocTemplate("doc.pdf")
styles = getSampleStyleSheet()

content = []

# heading
content.append(Paragraph("My Report", styles["Heading1"]))

# spacing
content.append(Spacer(1, 20))

# paragraph
content.append(Paragraph("This is a paragraph of text.", styles["Normal"]))

content.append(Spacer(1, 20))

# table
data = [
    ["Product", "Price"],
    ["Apple", "$1"],
    ["Banana", "$2"]
]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))
content.append(table)

# image
img = Image("logo.jpg", width=100, height=100)
content.append(img)

# page break
content.append(PageBreak())


custom_style = ParagraphStyle(
    name="Custom",
    fontSize=30,
    leading=16,
    spaceAfter=10
)
content.append(Paragraph("new page", custom_style))

def header(canvas, doc):
    canvas.drawString(100, 800, "My Header")

doc.build(content, onFirstPage=header)

subprocess.run(["xdg-open", "doc.pdf"])


quit()

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
                             fontSize=28, leading=32, textColor=PRIMARY)

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

# ----------------------------
# HEADER / FOOTER
# ----------------------------
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(70, 810, 525, 810)

    canvas.setFont("Helvetica", 8)
    canvas.drawString(70, 820, "OTREGROUP")
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


# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
