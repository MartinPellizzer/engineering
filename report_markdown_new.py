import subprocess

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

################################################################################
# DOCUMENT SETUP
################################################################################
doc = SimpleDocTemplate(
    "./projects/ozone/reports/wine-brettanomyces-barrels.pdf",
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

# COVER
# ------------------------------------------------------------------------------
elements.append(Spacer(1, 100))
elements.append(AccentLine())
elements.append(Spacer(1, 25))
cover_title_text = "Riduzione dei Brettanomyces nelle Botti di Vino"
elements.append(Paragraph(cover_title_text, cover_title_style))
elements.append(Spacer(1, 20))
elements.append(Paragraph("Proposta Applicazione", body_style))
elements.append(Spacer(1, 100))
elements.append(Paragraph("Preparata per", meta_style))
elements.append(Spacer(1, 15))
elements.append(Paragraph("Elena Ceccato", section_style))
elements.append(Spacer(1, 60))
elements.append(Paragraph("Maggio 2026", meta_style))
mul = 0.15
image_w = 239 * mul
image_h = 230 * mul
img = Image(f"projects/spillatura/logo.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
elements.append(Spacer(1, 120))
elements.append(Paragraph("Non consentita la divulgazione", footer_style))
elements.append(PageBreak())

# EXECUTIVE SUMMARY
# ------------------------------------------------------------------------------
with open('wine-brettanomyces-barrels.md', encoding='utf-8') as f: lines = f.read().split('\n')
print(lines)
for line in lines:
    if line.startswith('###'):
        line = line.replace('###', '').strip()
        elements.append(Paragraph(line, h3))
    elif line.startswith('##'):
        line = line.replace('##', '').strip()
        elements.append(Paragraph(line, h2))

        
    else:
        line = line.strip()
        elements.append(Paragraph(line, body_style))


# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

# subprocess.run(["xdg-open", "doc.pdf"])