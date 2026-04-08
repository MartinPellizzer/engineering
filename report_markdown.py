import subprocess

########################################
# DOC ELECTROLYSIS
########################################
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

def list_gen(items):
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

# ----------------------------
# DOCUMENT SETUP
# ----------------------------


doc = SimpleDocTemplate(
    "progetto-spillatrice-prototipo-fasi.pdf",
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

body_leading = 14
body_size = 9
body_space_after = 8

cover_title = ParagraphStyle('cover', fontName='Helvetica-Bold', fontSize=28, leading=32, textColor=PRIMARY)
section = ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=16, textColor=PRIMARY)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=16, textColor=PRIMARY, spaceBefore=0, spaceAfter=body_leading, leading=20)
h3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=12, textColor=PRIMARY, spaceBefore=body_leading*1.5, spaceAfter=body_leading)
h4 = ParagraphStyle('h4', fontName='Helvetica-Bold', fontSize=10, textColor=PRIMARY, spaceBefore=body_leading*1.5, spaceAfter=body_leading)
body = ParagraphStyle('body', fontSize=body_size, leading=body_leading)
paragraph = ParagraphStyle('paragraph', fontSize=body_size, leading=body_leading, spaceAfter=body_space_after)
list_style = ParagraphStyle('list', parent=body, leftIndent=0, spaceAfter=2)

insight = ParagraphStyle('insight', fontName='Helvetica-Bold',
                         fontSize=11.5, textColor=PRIMARY)
meta = ParagraphStyle('meta', fontSize=9, textColor=GREY)
footer = ParagraphStyle('footer', fontSize=8,
                        textColor=GREY, alignment=TA_RIGHT)

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

list_style = ParagraphStyle(
    name="list_style",
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,              # spacing within lines
    textColor=colors.HexColor("#222222"),
    leftIndent=0,
    spaceAfter=0,
)
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
    canvas.drawRightString(525, 820, "Confidenziale")

    canvas.drawString(70, 30, "Confidenziale")
    canvas.drawRightString(525, 30, str(doc.page))
    
    canvas.setTitle('Progetto Spillatura - Fasi Prototipo')
    canvas.setAuthor('Otregroup')
    canvas.restoreState()

# ----------------------------
# CONTENT
# ----------------------------
elements = []

# COVER
elements.append(Spacer(1, 100))

elements.append(AccentLine())
elements.append(Spacer(1, 25))

elements.append(Paragraph("Progetto Spillatrice - Fasi Prototipo", cover_title))
elements.append(Spacer(1, 20))
elements.append(Paragraph(
    "Proposta Tecnica Preliminare",
    body_style,
))

elements.append(Spacer(1, 100))
elements.append(Paragraph("Preparata per", meta))
elements.append(Spacer(1, 15))
elements.append(Paragraph("Otregroup | Sweesh | Pozzobon Distribuzione", section))

elements.append(Spacer(1, 60))
elements.append(Paragraph("Marzo 2026", meta))
###
mul = 0.15
image_w = 239 * mul
image_h = 230 * mul
img = Image(f"projects/spillatura/logo.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###

elements.append(Spacer(1, 120))
elements.append(Paragraph(
    "Non consentita la divulgazione",
    footer
))

elements.append(PageBreak())

# EXECUTIVE SUMMARY (1 pagina max)
elements.append(Paragraph("Executive Summary", h2))
elements.append(
    Paragraph(f'''
A seguito di vari incontri preliminari tra Otregroup, Sweesh e Pozzobon Distribuzione, si ritiene fattibile (a livello tecnico) lo sviluppo di un sistema automatizzato per il lavaggio/disinfezione dei sistemi di spillatura delle bevande. Come discusso in questi incontri, Otregroup ha il compito di sviluppare il sistema di automazione (centralina, attuatori e sensori), Sweesh ha il compito di fornire il generatore di ozono (più eventuali protocolli/analisi se lo ritiene opportuno) e Pozzobon Distribuzione ha il compito di fornire un sistema di spillatura (incluso linea di distribuzione e fusto con bevanda) assieme ad un tecnico che ne spiega il funzionamento. 
    ''', body_style,)
)
###
elements.append(
    Paragraph(f'''
Se tutte le parti coinvolte sono d'accordo con queste premesse, si intende procedere con la progettazione/sviluppo di un sistema prototipo che viene realizzato nella sede di Otregroup.
    ''', body_style,)
)
###
elements.append(Paragraph("Obbiettivi del prototipo", h3))
list_gen(f'''
validare l'avvenuta sanificazione della linea tramite analisi
validare il corretto funzionamento del sistema di automatizzatione 
'''.split('\n'))
###
elements.append(Paragraph("Ambito del prototipo", h3))
elements.append(
    Paragraph(f'''
L'ambito di questo prototipo è circoscritto alla sanificazione di UNA SOLA linea di distribuzione (non tutte).
    ''', body_style,)
)
###
elements.append(Paragraph("Criteri di successo", h3))
elements.append(
    Paragraph(f'''
Il prototipo viene considerato un "successo" se entrambi gli obbiettivi indicati nella sezione precedente ("Obiettivo del prototipo") vengono raggiunti. Maggiori dettagli sulle metriche utilizzate per validare il successo del prototipo devono essere ancora forniti.
    ''', body_style,)
)
###
elements.append(Paragraph("Modalità di esecuzione", h3))
elements.append(
    Paragraph(f'''
Per progettare/sviluppare questo prototipo viene proposto di procedere in modo "passo-passo" (modalità iterativa). Ovvero, al posto di implementare la versione finale del prototipo, si ritiene opportunto introdurre fasi intermedie. Queste fasi vengono descritte in sezioni dedicate.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
Questo modo di procedere viene suggerito in quanto si ritiene il più adeguato per ridurre costi, tempi ed errori complessivi nella fase di progettazione/sviluppo. Procedendo in questo modo, si stima un tempo di realizzazione del prototipo non superiore ai 60 giorni.
    ''', body_style,)
)
###
elements.append(Paragraph("Richiesta autorizzazione a procedere", h3))
elements.append(
    Paragraph(f'''
Se tutte le entità concordano con le premesse elencate fino ad ora, si chiede l'autorizzazione a procedere con la fase di progettazione/sviluppo. Se anche solo una di queste entità non è d'accordo con una di queste premesse o ha dei dubbi a rigurado, chiediamo di essere notificati in merito, così da rivalutare la fase di progettazione/sviluppo.
    ''', body_style,)
)
###
elements.append(PageBreak())

###
elements.append(Paragraph("Fasi Sviluppo", h2))
elements.append(
    Paragraph(f'''
Si propone di progettare/sviluppare il prototipo in 5 fasi:
    ''', body_style,)
)
ol_gen(f'''
verifica sistema spillatura (caso base)
verifica sistema ozono (produzione ozono, procedure e analisi)
verifica elettrovalvole (commutazione manuale)
implementazione ciclo (commutazione automatica, tempo statico)
implementazione sensori (commutazione automatica, tempo dinamico)
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
Queste fasi sono state pensate per ridurre il tempo di progettazione e i costi di sviluppo. Inoltre, ogni fase permette di raccogliere i dati/test necessari all'implementazione delle fasi sucessive.
    ''', body_style,)
)
###
elements.append(Paragraph("Tempo Sviluppo", h3))
elements.append(
    Paragraph(f'''
Si stima un tempo totale di sviluppo non superiore ai 60 giorni. Questo a patto che (1) tutti i componenti siano già disponibili (o che vengano forniti nell'immediato), (2) che le figure coinvolte forniscano massima disponibilità e collaborazione e (3) che le fasi di implementazione vengano rispettate con disciplina.
    ''', body_style,)
)
###
elements.append(Paragraph("Costi Sviluppo", h3))
elements.append(
    Paragraph(f'''
I costi stimati per lo sviluppo di questo prototipo sono relativamente bassi. Se Pozzobono Distribuzione mette a disposizione una spillatrice, Sweesh mette a disposizione un generatore di ozono e Otregroup mette a disposizione la centralina di controllo, i costi dei materiali sono limitati a valvole, sensori ed eventuali componenti accessori. I costi maggiori di questo progetto derivano dalle ore di manodopera delle figure coinvolte, nonchè da eventuali analisi di laboratorio effettuate per provare l'efficacia del sistema.
    ''', body_style,)
)
###
elements.append(Paragraph("Dettagli Sviluppo (Fase per Fase)", h3))
elements.append(
    Paragraph(f'''
I dettagli di ogni singola fase vengono forniti nelle seguenti sezioni.
    ''', body_style,)
)
elements.append(PageBreak())

###
elements.append(Paragraph("Fase 1. Verifica Sistema Spillatura", h2))
elements.append(
    Paragraph(f'''
Lo scopo di questa fase è quello di ottenere un sistema di spillatura funzionante e contaminato, il quale viene utilizzato come base di partenza (baseline) per progettare/sviluppare/testare il prototipo.
    ''', body_style,)
)
###
elements.append(Paragraph("Diagramma Flusso", h3))
elements.append(
    Paragraph(f'''
Il seguente diagramma di flusso rappresenta lo stato del sistema al termine di questa fase.
    ''', body_style,)
)
mul = 0.35
image_w = 1280 * mul
image_h = 720 * mul
img = Image(f"projects/spillatura/prototipo/diagram-0000.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###
elements.append(Paragraph("Descrizione Diagramma", h3))
elements.append(
    Paragraph(f'''
Il precedente diagramma mostra il sistema di spillatura nella sua forma base. Il componente "TN 01" (sulla destra) rappresenta il fusto contente la bevanda da erogare, mentre il componente "MV 01" (sulla sinistra) rappresenta il rubinetto della spillatrice da azionare manualmente per erogare la bevanda. Le frecce indicano il flusso di erogazione della bevanda.
    ''', body_style,)
)
###
elements.append(Paragraph("Obbiettivi", h3))
elements.append(
    Paragraph(f'''
Questa fase viene considerata un successo se si raggiungono i seguenti obbiettivi:
    ''', body_style,)
)
list_gen(f'''
il sistema di spillatura (spillatrice, fusto con bevanda, linea di distribuzione) sono forniti a Otregroup
il sistema di spillatura è confermato essere contaminato
il sistema di spillatura è installato e operativo (i tecnici di Otregroup possono spillare)
'''.strip().split('\n'))
###
elements.append(Paragraph("Prerequisiti", h3))
elements.append(
    Paragraph(f'''
I prerequisiti necessari per raggiungere gli obbiettivi sopra elencati sono i sguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup deve richiedere il materiale necessario a Pozzobon Distribuzione
Otregroup deve richiedere l'intervento di un tecnico a Pozzobon Distribuzione per l'installazione e il collaudo del sistema in sede Otregroup
Otregroup deve richiedere un dimostrazione pratica dell'utilizzo corretto del sistema di spillatura al tecnico di Pozzobon Distribuzione
Otregroup deve richiedere la massima disponibilità da parte del tecnico di Pozzobon Distribuzione di fornire tutti i dati necessari per lo sviluppo delle fasi sucessive e di rispondere a eventuali dubbi riguardo il funzionamento del sistema di spillatura
'''.strip().split('\n'))
###
elements.append(Paragraph("Figure Coinvolte", h3))
elements.append(
    Paragraph(f'''
Le figure coinvolte in questa fase sono i seguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup
Pozzobon Distribuzione
Sweesh (valuta autonomante se vuole partecipare a questa fase)
'''.strip().split('\n'))
###
elements.append(PageBreak())

elements.append(Paragraph("Fase 2. Verifica Sistema Ozono", h2))
elements.append(
    Paragraph(f'''
Lo scopo di questa fase è quello di ottenere/testare un generatore di ozono in grado di produrre acqua ozonizzata "in linea", nonchè di scrivere i protocolli di utilizzo e di verificare la loro efficacia con analisi microbiologiche.
    ''', body_style,)
)
###
elements.append(Paragraph("Diagramma Flusso", h3))
elements.append(
    Paragraph(f'''
Il seguente diagramma di flusso rappresenta lo stato del sistema al termine di questa fase.
    ''', body_style,)
)
###
mul = 0.35
image_w = 1280 * mul
image_h = 720 * mul
img = Image(f"projects/spillatura/prototipo/diagram-0001.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###
elements.append(Paragraph("Descrizione Diagramma", h3))
elements.append(
    Paragraph(f'''
Il precendente diagramma mostra l'utilizzo del generatore di ozono "O3 01" per sanificare la linea di distribuzione della spillatrice. Il generatore di ozono va sostituito al fusto della bevanda e testato in isolamento durante questa fase, per verificare che l'acqua ozonizzata venga erogata correttamente e che la linea venga sanificata di conseguenza.
    ''', body_style,)
)
###
elements.append(Paragraph("Obbiettivi", h3))
elements.append(
    Paragraph(f'''
Questa fase viene considerata un successo se si raggiungono i seguenti obbiettivi:
    ''', body_style,)
)
list_gen(f'''
il generatore di ozono è fornito a Otregroup
il generatore di ozono è funzionante
il generatore di ozono è attivo solo quando c'è passaggio d'acqua
il sistema di spillatura eroga acqua quando il generatore di ozono è installato in linea
il sensore di ozono disciolto in acqua rileva una concentrazione di ozono (PPM) idonea al processo di sanificazione nell'acqua erogata dalla spillatrice
il protocollo di sanificazione viene scritto e testato da analisi microbiologiche
'''.strip().split('\n'))
###
elements.append(Paragraph("Prerequisiti", h3))
elements.append(
    Paragraph(f'''
I prerequisiti necessari per raggiungere gli obbiettivi sopra elencati sono i sguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup deve richiedere un generatore di ozono idoneo per l'applicazione a Sweesh
Otregroup deve richiedere il manuale tecnico relativo al generatore di ozono utilizzato (se non già fornito)
Otregroup deve richiedere una dimostrazione pratica dell'utilizzo corretto del generatore di ozono a Sweesh
Otregroup deve richiedere a Sweesh di contribuire allo sviluppo del protocollo di sanificazione (se Sweesh è d'accordo)
Otregroup deve richiedere a Sweesh di valutare quale sia il miglior modo possibile di procedere per quando riguarda la fase di analisi microbiologica (se Sweesh è d'accordo)
'''.strip().split('\n'))
###
elements.append(Paragraph("Figure Coinvolte", h3))
elements.append(
    Paragraph(f'''
Le figure coinvolte in questa fase sono i seguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup
Sweesh
Laboratorio Analisi
'''.strip().split('\n'))
###
elements.append(PageBreak())

elements.append(Paragraph("Fase 3. Verifica Elettrovalvole", h2))
elements.append(
    Paragraph(f'''
Lo scopo di questa fase è quello di ottenere/testare 2 elettrovalvole (valvole solienoidi) e di simulare manualmente un ciclo di sanificazione.
    ''', body_style,)
)
###
elements.append(Paragraph("Diagramma Flusso", h3))
elements.append(
    Paragraph(f'''
Il seguente diagramma di flusso rappresenta lo stato del sistema al termine di questa fase.
    ''', body_style,)
)
###
mul = 0.35
image_w = 1280 * mul
image_h = 720 * mul
img = Image(f"projects/spillatura/prototipo/diagram-0002.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###
elements.append(Paragraph("Descrizione Diagramma", h3))
elements.append(
    Paragraph(f'''
Il precedente diagramma mostra come integrare il generatore di ozono "O3 01" e il fusto con la bibita "TN 01" nella stessa linea di distribuzione, utilizzando due valvole solenoidi "SV 01" e "SV 02" per la commutazione dei processi di sanificazione e normale erogazione. In questa fase, la commutazione viene fatta manualmente.
    ''', body_style,)
)
###
elements.append(Paragraph("Obbiettivi", h3))
elements.append(
    Paragraph(f'''
Questa fase viene considerata un successo se si raggiungono i seguenti obbiettivi:
    ''', body_style,)
)
list_gen(f'''
le elettrovalvole sono fornite a Otregroup (da valutare chi è il fornitore)
le elettrovalvole sono funzionanti
le elettrovalvole commutano correttamente se applicata la tensione richiesta
la spillatrice eroga correttamenta acqua ozonizzata o bevanda del fusto alla commutazione delle elettrovalvole
'''.strip().split('\n'))
###
elements.append(Paragraph("Prerequisiti", h3))
elements.append(
    Paragraph(f'''
I prerequisiti necessari per raggiungere gli obbiettivi sopra elencati sono i sguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup deve identificare un fornitore di elettrovalvore idoneo per ottenere delle valvole di test (eventualmente chiedere a Pozzobon Distribuzione se ha delle valvole da fornire e/o se può consigliare delle valvole idonee ad essere installate nelle loro linee)
Otregroup deve avere la possibilità di installare le elettrovalvole sulla linea della spillatrice (per questo si richiede il supporto del tecnico di Pozzobon Distribuzione)
Otregroup deve identificare i componenti elettronici necessari per fare il primo test manuale (alimentazione, pulsanti e altro)
'''.strip().split('\n'))
###
elements.append(Paragraph("Figure Coinvolte", h3))
elements.append(
    Paragraph(f'''
Le figure coinvolte in questa fase sono i seguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup
Pozzobon Distribuzion
Sweesh (valuta autonomante se vuole partecipare a questa fase)
'''.strip().split('\n'))
###
elements.append(PageBreak())

elements.append(Paragraph("Fase 4. Implementazione Ciclo", h2))
elements.append(
    Paragraph(f'''
Lo scopo di questa fase è quello di integrare una centralina di controllo e di sviluppare il software necessario per automatizzare il cliclo di sanificazione, il quale viene effettuato post-cambio fusto premendo un pulsante nel touchscreen della centralina.
    ''', body_style,)
)
###
elements.append(Paragraph("Diagramma Flusso", h3))
elements.append(
    Paragraph(f'''
Il seguente diagramma di flusso rappresenta lo stato del sistema al termine di questa fase.
    ''', body_style,)
)
mul = 0.35
image_w = 1280 * mul
image_h = 720 * mul
img = Image(f"projects/spillatura/prototipo/diagram-0003.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###
elements.append(Paragraph("Descrizione Diagramma", h3))
elements.append(
    Paragraph(f'''
Il precedente diagramma mostra come integrare la centralina di controllo "PLC 01" per la gestione automatica del ciclo di sanificazione. Questo ciclo ha un tempo prestabilito e viene effettuato quando l'operatore dà il comando di avvio tramite touchscreen. L'automazione è resa possibile collegando la centralina alle 2 solenoidi ("SV 01" e "SV 02") tramite collegamenti elettrici indicati nel diagramma da linee tratteggiate (al contrario delle linee continue con frecce che indicano flussi con passaggio di liquido).
    ''', body_style,)
)
###
elements.append(Paragraph("Obbiettivi", h3))
elements.append(
    Paragraph(f'''
Questa fase viene considerata un successo se si raggiungono i seguenti obbiettivi:
    ''', body_style,)
)
list_gen(f'''
le elettrovalvole vengono commutate correttamente in maniera automatizzata alla pressione di un pulsante sullo schermo touchscreen della centralina di controllo
il ciclo si sanificazione viene eseguito correttamente secondo le procedure sviluppate durante la fase di implementazione del generatore di ozono
il ciclo termina dopo la procedura di sanificazione e la spillatrice ritorna ad erogare la bibita al poste dell'acqua ozonizzata
'''.strip().split('\n'))
###
elements.append(Paragraph("Prerequisiti", h3))
elements.append(
    Paragraph(f'''
I prerequisiti necessari per raggiungere gli obbiettivi sopra elencati sono i sguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup deve confermare la disponibilità di una centralia di controllo (PCB con microcontrollore, o PLC) idonea a questa applicazione
Otregroup deve rifornirsi o progettare tale centralina se non disponibile/idonea (questo aumenta significativamente i tempi di sviluppo del prototipo)
'''.strip().split('\n'))
###
elements.append(Paragraph("Figure Coinvolte", h3))
elements.append(
    Paragraph(f'''
Le figure coinvolte in questa fase sono i seguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup
Sweesh (valuta autonomante se vuole partecipare a questa fase)
'''.strip().split('\n'))
###
elements.append(PageBreak())

elements.append(Paragraph("Fase 5. Implementazione Sensori", h2))
elements.append(
    Paragraph(f'''
Lo scopo di questa fase è quello di integrare sensori per il monitoraggio delle linee (linea ozono e linea bevanda) al fine di garantire un ciclo di sanificazione affidabile.
    ''', body_style,)
)
###
elements.append(Paragraph("Diagramma Flusso", h3))
elements.append(
    Paragraph(f'''
Il seguente diagramma di flusso rappresenta lo stato del sistema al termine di questa fase.
    ''', body_style,)
)
###
mul = 0.35
image_w = 1280 * mul
image_h = 720 * mul
img = Image(f"projects/spillatura/prototipo/diagram-0004.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###
elements.append(Paragraph("Descrizione Diagramma", h3))
elements.append(
    Paragraph(f'''
Il precedente diagramma mostra come integrare 2 sensori ritenuti fondamentali per ottenere un ciclo di sanificazione completamente automatico e affidabile. Il primo sensore è un sensore di flusso "FM 01" da mettere in linea con il generatore di ozono, il quale indica se c'è un effettivo passaggio d'acqua e aggiorna il timer impostato per la sanificazione solo in questa condizione. Il secondo sensore, invece, è un sensore da mettere in linea con il fusto della bevanda o direttamente sull'accoppiatore da agganciare al fusto "CM 01" per rilevare in modo automatico il cambio del fusto ed evitare che l'avvio del ciclo venga effettuato dall'operatore tramite touchscreen.
    ''', body_style,)
    )
###
elements.append(Paragraph("Obbiettivi", h3))
elements.append(
    Paragraph(f'''
Questa fase viene considerata un successo se si raggiungono i seguenti obbiettivi:
    ''', body_style,)
)
list_gen(f'''
il tempo del ciclo viene aggiornato solo quando il sensore di flusso rileva passaggio di acqua ozonizzata
il ciclo parte in automatico dopo il cambio del fusto, senza avvio manuale da parte dell'operatore
'''.strip().split('\n'))
###
elements.append(Paragraph("Prerequisiti", h3))
elements.append(
    Paragraph(f'''
I prerequisiti necessari per raggiungere gli obbiettivi sopra elencati sono i sguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup deve ottenere un sensore di flusso (flussostato) idoneo all'applicazione e interfacciabile alla centralina di controlo (chiedere supporto a Pozzobon Distribuzione)
Otregroup deve ottenere un sensore di contatto (micro switch) o sensore di pressione (pressostato) idoneo all'applicazione e interfacciabile alla centralina di controlo (chiedere supporto a Pozzobon Distribuzione)
'''.strip().split('\n'))
###
elements.append(Paragraph("Figure Coinvolte", h3))
elements.append(
    Paragraph(f'''
Le figure coinvolte in questa fase sono i seguenti:
    ''', body_style,)
)
list_gen(f'''
Otregroup
Pozzobon Distribuzione
Sweesh (valuta autonomante se vuole partecipare a questa fase)
'''.strip().split('\n'))
###
elements.append(PageBreak())

elements.append(Paragraph("Sviluppi Futuri", h2))
###
elements.append(Paragraph("Diagramma Flusso", h3))
elements.append(
        Paragraph(f'''
Il seguente diagramma di flusso rappresenta come scalare il sistema per renderlo multi-linea.
    ''', body_style,)
        )
mul = 0.35
image_w = 1280 * mul
image_h = 720 * mul
img = Image(f"projects/spillatura/prototipo/diagram-0005.png", image_w, image_h)
elements.append(Spacer(1, 20))
img.hAlign = "LEFT"
elements.append(img)
###
elements.append(Paragraph("Descrizione Diagramma", h3))
elements.append(
        Paragraph(f'''
Il precedente diagramma mostra come scalare il sistema di automazione da 1 linea a 2 linee. Il blocco di componenti nella parte inferiore del diagramma rappresenta la seconda linea. Per avere più di 2 linee, la strategia è quella di replicare il secondo blocco tante volte quante il numero di linee desiderate e di incrementare il numero di input/output (I/O) della centralina di controllo. 
    ''', body_style,)
        )
###
elements.append(Paragraph("Fase Esclusa Dal Primo Prototipo", h3))
elements.append(
        Paragraph(f'''
Questa fase al momento non è inclusa nello sviluppo del primo prototipo. Lo sviluppo di un sistema multi-linea ha una complessità esponenziale confrontata col prototipo a singola linea. Per questo motivo si chiede di sviluppare/testare il prototipo a singola linea prima di scalare al multi-linea, in modo da consolidare il funzionameto del sistema prima di investire risorse e di rischiare sia un allungamento significativo dei tempi di sviluppo che un incremento degli errori di progettazione a causa di insufficienza di dati raccolti.
    ''', body_style,)
        )
###
elements.append(PageBreak())


# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

# subprocess.run(["xdg-open", "doc.pdf"])

