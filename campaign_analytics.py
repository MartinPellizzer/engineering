import os
import subprocess

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

import matplotlib.pyplot as plt

report_slug = 'vino-fruttaie'
report_version = '2.0'
report_folderpath = f'./tmp/{report_slug}-{report_version}'
report_filepath = f'./tmp/{report_slug}-{report_version}/{report_slug}-{report_version}.pdf'

try: os.mkdir(report_folderpath)
except: pass

################################################################################
# DOCUMENT SETUP
################################################################################
doc = SimpleDocTemplate(
    report_filepath,
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
    leading=20,
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
body_bold_style = ParagraphStyle(
    name="body_style",
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14.5,              # line spacing
    textColor=colors.HexColor("#222222"),
    alignment=0,               # left align
    spaceAfter=10,             # spacing between paragraphs
    spaceBefore=0,
    allowWidows=1,
    allowOrphans=0,
)
list_style = ParagraphStyle(
    name="list_style",
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,              # spacing within lines
    textColor=colors.HexColor("#222222"),
    leftIndent=0,
    spaceAfter=0,
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

def ul_gen(items):
    items_formatted = []
    for item in items:
        items_formatted.append(Paragraph(item, list_style))
    elements.append(
        ListFlowable(
            items_formatted,
            bulletType='bullet',
            leftIndent=12,
            bulletIndent=0,
            bulletFontName='Helvetica',
            bulletFontSize=8,
            bulletOffsetY=-2,
            spaceBefore=6,
            spaceAfter=12,
        )
    )

def ol_gen(items):
    items_formatted = []
    for item in items:
        items_formatted.append(Paragraph(item, list_style))
    elements.append(
        ListFlowable(
            items_formatted,
            bulletType='1',
            leftIndent=12,
            bulletIndent=0,
            bulletFontName='Helvetica',
            bulletFontSize=8,
            bulletOffsetY=-2,
            spaceBefore=6,
            spaceAfter=12,
        )
    )

################################################################################
# HEADER / FOOTER
################################################################################
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(70, 810, 525, 810)

    canvas.setFont("Helvetica", 8)
    canvas.drawString(70, 820, "OTREGROUP")
    canvas.drawRightString(525, 820, f"Confidenziale V{report_version}")

    canvas.drawString(70, 30, f"Confidenziale V{report_version}")
    canvas.drawRightString(525, 30, str(doc.page))
    canvas.restoreState()

################################################################################
# PARSE
################################################################################
def parse(lines, elements):
    ul_start = False
    ul_items = []
    ol_start = False
    ol_items = []
    for line in lines:
        line = line.strip()
        if line == '': continue
        
        if line.startswith('-----'):
            break
        
        if line.startswith('---'):
            elements.append(PageBreak())
            continue
        
        if line[0] == '-':
            line = line[1:].strip()
            ul_items.append(line)
            ul_start = True
            continue
        if ul_start == True:
            ul_start = False
            ul_gen(ul_items)
            ul_items = []
            
        if line[0].isdigit() and line[1] == '.':
            line = line[2:].strip()
            ol_items.append(line)
            ol_start = True
            continue
        if ol_start == True:
            ol_start = False
            ol_gen(ol_items)
            ol_items = []

        if line.startswith('###'):
            line = line.replace('###', '').strip()
            elements.append(Paragraph(line, h3))
        elif line.startswith('##'):
            line = line.replace('##', '').strip()
            elements.append(Paragraph(line, h2))
        elif line.startswith('#'):
            line = line.replace('#', '').strip()
            elements.append(Paragraph(line, h1))
            
        elif line.startswith('**'):
            line = line.replace('**', '').strip()
            # elements.append(Paragraph(line, body_bold_style))
            elements.append(Paragraph(line, body_style))
        else:
            line = line.strip()
            elements.append(Paragraph(line, body_style))
    if lines:
        elements.append(PageBreak())

################################################################################
# CONTENT
################################################################################
elements = []


# ANALYTICS
# ------------------------------------------------------------------------------
metrics = [
    "Email Inviate",
    "Risposte Totali",
    "Risposte Positive",
    "Chiamate Conoscitive",
    "Appuntamenti Fissati"
]
values = [210, 7, 0, 0, 0]
plt.figure(figsize=(10, 6))
bars = plt.bar(metrics, values)
# Labels on bars
for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f'{int(bar.get_height())}',
        ha='center',
        va='bottom',
        fontweight='bold'
    )
plt.title("Risultati Campagnia Fruttaie 18/05/2026", fontsize=16, fontweight='bold')
plt.ylabel("Numero di Contatti")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("risultati-campagnia-fruttaie-18-05-2026.png", dpi=300, bbox_inches="tight")

line = 'Risultati Campagnia Fruttaie 05/06/2026'
elements.append(Paragraph(line, h1))
line = 'Il seguente grafico mostra i risultati della campagnia fruttaie 05/06/2026 - 19/06/2026 (usando email a freddo). Maggiori dettagli sulle email verranno dati nelle prossime sezioni.'
elements.append(Paragraph(line, body_style))
mul = 0.15
image_w = 2970 * mul
image_h = 1774 * mul
img = Image(f"risultati-campagnia-fruttaie-18-05-2026.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)


elements.append(PageBreak())

doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

'''

GIORNO 	NUMERO MAIL					
18/05/2026	20					
19/05/2026	20					
20/05/2026	20					
21/05/2026	20					
22/05/2026	20					
23/05/2026						
24/05/2026						
25/05/2026	20					
26/05/2026	15					
27/05/2026	25					
28/05/2026	20					
29/05/2026	20					
						
TOTALE	200					
						
						
						
						
CHI	RISPOSTA	ESITO RISP	TELEFONATA	RISULT TELEFONATA	APPUNTAMENTO	
cantine nepos	1	no				
vini montresor	1	si	in attesa ( chiamato un paio di volte, riprovare)			
vigne san pietro	1	no				
Cadis 1898	1	si	si	non interessato		
farina	1	Forse ( segretaria inoltrato mail all’enologo)				
Il Pignetto	1	no				
Annafrancesca	1	No ( no appassimento)				
Raval Bardolino	1	No ( no appassimento)				
Cesari	1	si	in attesa ( chiamato un paio di volte, riprovare)			
Corte saibante	1	si	in attesa (da sentire venerdì)			
Benedetti la villa	1	no				
Cantina viviani	1	no				
San dionigi	1	no				
Pasini san giovanni 	1	No ( no appassimento)				
Cantrina	1	no				
Accordini stefano	1	Forse ( io ho inoltrato mail all’enologo)				
Fraghe	1	No ( no appassimento)				
Trabucchi wine	1 ( ha chiamato il pomeriggio  e l’ho richiamato)		si	si	si il 7 giugno 	
						
						
	NUMERO MAIL	RISPOSTE TOTALI 	POSITIVE	NEGATIVE	TELEFONATE	INCONTRI
05/06/2026	10 n – 10 r					
06/06/2026						
07/06/2026						
08/06/2026	10 n – 10 r					
09/06/2026	10 n – 10 r					
10/06/2026	10 n – 10 r					
11/06/2026	10 n – 10 r					
12/06/2026	10 n – 10 r					
13/06/2026						
14/06/2026						
15/06/2026	10 n – 10 r					
16/06/2026	10 n – 10 r					
17/06/2026	10 n – 10 r					
18/06/2026	10 n – 10 r					
19/06/2026	10 n – 10 r	6+ 1 RICONTATTO	0	6 + 1 HA GIRATO MAIL AL RESPONSABILE 		
'''