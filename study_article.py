import subprocess

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

input_filepath = "./projects/ozone/campaigns/wine/articoli/input/study-0000.md"
output_filepath = "./projects/ozone/campaigns/wine/articoli/output/study-0000.pdf"

################################################################################
# DOCUMENT SETUP
################################################################################
doc = SimpleDocTemplate(
    output_filepath,
    pagesize=A4,
    rightMargin=70,
    leftMargin=70,
    topMargin=90,
    bottomMargin=60
)

################################################################################
# STYLES
################################################################################
styles = getSampleStyleSheet()
PRIMARY = colors.HexColor("#0B1F3B")
GREY = colors.HexColor("#6B7280")
LIGHT_GREY = colors.HexColor("#E5E7EB")
body_leading = 14
body_size = 9
body_space_after = 8
meta_style = ParagraphStyle(
    'meta', 
    fontSize=9, 
    textColor=GREY
)
cover_title_style = ParagraphStyle(
    'cover', 
    fontName='Helvetica-Bold', 
    fontSize=28, 
    leading=32, 
    textColor=PRIMARY
)
h1 = ParagraphStyle(
    'h1', 
    fontName='Helvetica-Bold', 
    fontSize=24, 
    leading=24,
    textColor=PRIMARY, 
    spaceBefore=0, 
    spaceAfter=body_leading
)
h2 = ParagraphStyle(
    'h2', 
    fontName='Helvetica-Bold', 
    fontSize=16, 
    textColor=PRIMARY, 
    spaceBefore=0, 
    spaceAfter=body_leading
)
h3 = ParagraphStyle(
    'h3', 
    fontName='Helvetica-Bold', 
    fontSize=12, 
    textColor=PRIMARY, 
    spaceBefore=body_leading*1.5, 
    spaceAfter=body_leading
)
section_style = ParagraphStyle(
    'section', 
    fontName='Helvetica-Bold', 
    fontSize=16, 
    textColor=PRIMARY
)
body_style = ParagraphStyle(
    name="body_style",
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,              # line spacing
    textColor=colors.HexColor("#222222"),
    alignment=0,               # left align
    spaceAfter=10,             # spacing between paragraphs
    spaceBefore=0,
    allowWidows=1,
    allowOrphans=0,
)
footer_style = ParagraphStyle(
    'footer', 
    fontSize=8,
    textColor=GREY, 
    alignment=TA_RIGHT
)

################################################################################
# COMPONENTS
################################################################################
class AccentLine(Flowable):
    def draw(self):
        self.canv.setFillColor(PRIMARY)
        self.canv.rect(0, 0, 70, 4, fill=1, stroke=0)

################################################################################
# HEADER / FOOTER
################################################################################
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(70, 810, 525, 810)

    canvas.setFont("Helvetica", 8)
    canvas.drawString(70, 820, "OTREGROUP")
    canvas.drawRightString(525, 820, "Confidenziale")

    canvas.drawString(70, 30, "Confidenziale")
    canvas.drawRightString(525, 30, str(doc.page))
    canvas.restoreState()


################################################################################
# CONTENT
################################################################################
elements = []

# EXECUTIVE SUMMARY
# ------------------------------------------------------------------------------
with open(input_filepath, encoding='utf-8') as f: lines = f.read().split('\n')
print(lines)
for line in lines:
    if line.startswith('###'):
        line = line.replace('###', '').strip()
        elements.append(Paragraph(line, h3))
    elif line.startswith('##'):
        line = line.replace('##', '').strip()
        elements.append(Paragraph(line, h2))
    elif line.startswith('#'):
        line = line.replace('#', '').strip()
        elements.append(Paragraph(line, h1))
    elif line.startswith('---'):
        elements.append(PageBreak())

        
    else:
        line = line.strip()
        elements.append(Paragraph(line, body_style))


# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

# subprocess.run(["xdg-open", "doc.pdf"])