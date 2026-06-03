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
report_folderpath = f'./projects/ozone/reports/{report_slug}-{report_version}'
report_filepath = f'./projects/ozone/reports/{report_slug}-{report_version}/{report_slug}-{report_version}.pdf'

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

# COVER
# ------------------------------------------------------------------------------
elements.append(Spacer(1, 100))
elements.append(AccentLine())
elements.append(Spacer(1, 25))
cover_title_text = "Campagna Sanificazione Fruttaie Con Ozono Gassoso"
elements.append(Paragraph(cover_title_text, cover_title_style))
elements.append(Spacer(1, 20))
elements.append(Paragraph("Proposta Campagna", body_style))
elements.append(Spacer(1, 100))
elements.append(Paragraph("Preparata per", meta_style))
elements.append(Spacer(1, 15))
elements.append(Paragraph("Elena Ceccato | Mauro Dottori", section_style))
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
with open('vino-fruttaie.md', encoding='utf-8') as f: lines = f.read().split('\n')
print(lines)
parse(lines, elements)

# PROTOCOL
# ------------------------------------------------------------------------------
protocol_folderpath = "./projects/ozone/campaigns/wine/protocol"
input_filepath = f'{protocol_folderpath}/input/protocol.md'
with open(input_filepath, encoding='utf-8') as f: lines = f.read().split('\n')
print(lines)
parse(lines, elements)

# STUDIES
# ------------------------------------------------------------------------------
line = 'Studi Scientifici'
elements.append(Paragraph(line, h1))
line = '''Nelle seguenti pagine sono stati analizzati e riassunti alcuni studi scientifici inerenti all'applicazione in oggetto.'''
elements.append(Paragraph(line, body_style))
line = '''La seguente lista mostra un'anteprima degli studi.'''
elements.append(Paragraph(line, body_style))
ul_items = [
    '''Miglioramento delle proprietà sensoriali dei vini rossi''',
    '''Fumigazione con ozono per la sicurezza e la qualità delle uve da vino durante l'appassimento post-raccolta''',
    '''L'ozono influenza il sistema antiossidante e la qualità dell'uva da vino durante l'appassimento parziale''',
    '''Effetti metabolici dei trattamenti post-raccolta con appassimento e ozono sull'uva da vino''',
]
ul_gen(ul_items)
elements.append(PageBreak())

input_filepath = "./projects/ozone/campaigns/wine/articoli/input/study-0000.md"
input_folderpath = "./projects/ozone/campaigns/wine/articoli/input"
for input_filename in os.listdir(input_folderpath):
    filename_raw = input_filename.split('.')[0].strip()
    input_filepath = f'{input_folderpath}/{filename_raw}.md'
    with open(input_filepath, encoding='utf-8') as f: lines = f.read().split('\n')
    print(lines)
    parse(lines, elements)

# ANALYTICS
# ------------------------------------------------------------------------------
metrics = [
    "Email Inviate",
    "Risposte Totali",
    "Risposte Positive",
    "Chiamate Conoscitive",
    "Appuntamenti Fissati"
]
values = [200, 18, 5, 2, 1]
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

line = 'Risultati Campagnia Fruttaie 18/05/2026'
elements.append(Paragraph(line, h1))
line = 'Il seguente grafico mostra i risultati della campagnia fruttaie 18/05/2026 - 1/06/2026 (usando email a freddo). Maggiori dettagli sulle email verranno dati nelle prossime sezioni.'
elements.append(Paragraph(line, body_style))
mul = 0.15
image_w = 2970 * mul
image_h = 1774 * mul
img = Image(f"risultati-campagnia-fruttaie-18-05-2026.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)

elements.append(Spacer(1, 25))
line = 'Proiezione Vendite'
elements.append(Paragraph(line, h2))

line = f'''
Sulla base dei risulati ottenuti, si è cercato di fare una proiezione delle vendite per capire se la campagna è stata positiva o meno.
'''
elements.append(Paragraph(line, body_style))
line = f'''
Consideriamo il caso in cui si decida di vendere un'attrezzatura da 10.000€. Dato che il risultato ottenuto è stato quello di fissare 1 appuntamento in 2 settimane, si ipotizza di riuscire a fissare 2 appuntamenti ogni mese (ipotizzando sempre di avere un bacino di contatti infinito). Questo si traduce in un potenziale di vendita di 20.000€ mensile (2 appuntamenti al mese * 10.000€ per vendita, ammesso che si venda il 100% delle volte).
'''
elements.append(Paragraph(line, body_style))
line = f'''
In conclusione, 20.000€ al mese si traducono in 240.000€ all'anno, una cifra cifra è ritenuta "borderline" per la sopravvivenza dell'azienda secondo discussioni avvenute in passato. Di conseguenza, il risutato ottenuto da questa campagni non sembra dei migliori.
'''
elements.append(Paragraph(line, body_style))

elements.append(PageBreak())

# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

# subprocess.run(["xdg-open", "doc.pdf"])
