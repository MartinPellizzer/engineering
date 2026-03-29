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
    "doc.pdf",
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
section = ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=16, textColor=PRIMARY, spaceBefore=30)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=16, textColor=PRIMARY, spaceBefore=0, spaceAfter=body_leading)
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
    canvas.restoreState()

# ----------------------------
# CONTENT
# ----------------------------
elements = []

# COVER
elements.append(Spacer(1, 140))
elements.append(AccentLine())
elements.append(Spacer(1, 25))

elements.append(Paragraph("Automazione del Processo di Ozonizzazione nei Sistemi di Spillatura", cover_title))
elements.append(Spacer(1, 20))
elements.append(Paragraph(
    "Proposta Tecnica Preliminare",
    body_style,
))

elements.append(Spacer(1, 100))
elements.append(Paragraph("Preparata per", meta))
elements.append(Paragraph("Otregroup | Sweesh", section))

elements.append(Spacer(1, 60))
elements.append(Paragraph("Marzo 2026", meta))

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
        Si propone lo sviluppo di un sistema automatizzato per la sanificazione delle linee di distribuzione delle bevande (ad ogni cambio di fusto), basato su tecnologia di ozonizzazione.
    ''', body_style,)
)
###
elements.append(Paragraph("Problema da risolvere", h3))
elements.append(
    Paragraph(f'''
        L’attuale processo di sanificazione è completamente manuale e richiede l’intervento periodico di un tecnico presso il cliente. Questo approccio comporta:
    ''', body_style,)
)

list_gen(f'''
costi operativi elevati legati alla manodopera
variabilità nella qualità della sanificazione
dipendenza dalla disponibilità dei tecnici
ritardi nelle operazioni di pulizia
'''.split('\n'))
###
elements.append(
    Paragraph(f'''
        Queste criticità hanno un impatto diretto sulla qualità del prodotto, con conseguente rischio di perdita di clienti e danno alla reputazione.
    ''', body_style,)
)
###
elements.append(Paragraph("Soluzione proposta", h3))
elements.append(
    Paragraph(f'''
        Il progetto prevede lo sviluppo di un sistema automatizzato in grado di eseguire l’intero ciclo di sanificazione delle linee di spillatura in modo autonomo ad ogni cambio fusto.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        Il sistema gestirà:
    ''', body_style,)
)
list_gen(f'''
il ciclo completo di lavaggio sanificazione
il cambio dal ciclo di lavaggio a quello di erogazione della bevanda (e viceversa)
'''.split('\n'))
###
elements.append(Paragraph("Benefici attesi", h3))
list_gen(f'''
riduzione dei costi operativi
eliminazione degli errori umani
maggiore affidabilità e ripetibilità del processo
miglioramento della soddisfazione del cliente finale
mantenimento costante della qualità del prodotto nel tempo
eliminazione della manodopera per le operazioni di sanificazione
'''.split('\n'))

###
elements.append(Paragraph("Fattibilità e prossimi passi", h3))
elements.append(
    Paragraph(f'''
        Il progetto risulta tecnicamente realizzabile, con necessità di validare nel dettaglio l’integrazione con il sistema di generazione di ozono (partner) e i parametri del processo di sanificazione.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        I prossimi passi prevedono:
    ''', body_style,)
)
ol_gen(f'''
raccolta dei dati di processo
progettazione di un sistema prototipo
fase di test per validare l’efficacia della sanificazione automatica
'''.strip().split('\n'))
###
elements.append(PageBreak())

########################################
# CONTESTO E PROBLEMA
########################################
elements.append(Paragraph("Contesto e Problema", h2))
elements.append(
    Paragraph(f'''
        L’attuale gestione manuale della sanificazione limita qualità del prodotto, efficienza operativa e affidabilità del servizio.
    ''', body_style,)
)
###
elements.append(Paragraph("Sistema attuale", h3))
elements.append(
    Paragraph(f'''
        Attualmente, la sanificazione delle linee di distribuzione delle bevande viene eseguita manualmente tramite interventi periodici di un tecnico specializzato presso il cliente.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        Il servizio viene generalmente effettuato con frequenza mensile, ma la pianificazione non è garantita e dipende dalla disponibilità dei tecnici o dalla richiesta del cliente stesso. In molti casi, l’intervento avviene solo in seguito alla comparsa di problemi evidenti nel prodotto.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        Il costo del servizio è sostenuto dal cliente o dal distributore, generando un modello operativo basato su interventi manuali e non continuativi.
    ''', body_style,)
)
###
elements.append(Paragraph("Criticità operative", h3))
list_gen(f'''
Gestione reattiva: gli interventi vengono spesso richiesti quando il problema è già presente
Limitata scalabilità: il numero di interventi è vincolato alla disponibilità del personale
Dipendenza dalla manodopera: ogni operazione richiede la presenza fisica di un tecnico
Variabilità del servizio: la qualità della sanificazione può variare tra operatori
Bassa attrattività operativa: si tratta di un’attività poco gradita ai tecnici
'''.strip().split('\n'))
###
elements.append(Paragraph("Impatto sul cliente", h3))
list_gen(f'''
costi operativi elevati
potenziale perdita di clientela
perdita di reputazione per il cliente finale
inefficienze nella gestione degli interventi
restituzione del prodotto da parte dei consumatori
riduzione della fiducia nel servizio e nel prodotto
impossibilità di garantire un livello di servizio costante nel tempo
'''.strip().split('\n'))
###
elements.append(Paragraph("Limiti strutturali", h3))
elements.append(
    Paragraph(f'''
        Il modello attuale è limitato da due fattori principali:
    ''', body_style,)
)
list_gen(f'''
dipendenza dalla disponibilità dei tecnici, che impedisce interventi tempestivi
approccio reattivo dei clienti, che tendono a richiedere la sanificazione solo quando il problema è già manifestato
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Questi elementi rendono il sistema inefficiente e non adatto a garantire standard qualitativi elevati e costanti.
    ''', body_style,)
)
###
elements.append(PageBreak())

########################################
# OBIETTIVI DEL PROGETTO
########################################
elements.append(Paragraph("Obiettivi del Progetto", h2))
elements.append(
    Paragraph(f'''
        L'obiettivo del progetto è di garantire la sanificazione completa delle linee di distribuzione tramite un processo automatizzato (ripetibile e senza intervento di tecnici), mantenendo costante la qualità del prodotto.
    ''', body_style,)
)
###
elements.append(Paragraph("Obiettivi principali", h3))
list_gen(f'''
Automazione completa del processo di lavaggio e sanificazione delle linee di spillatura, eliminando la necessità di interventi manuali da parte dei tecnici.
Sanificazione ad ogni cambio fusto, con l’utente che seleziona la linea da trattare tramite un’interfaccia semplice.
'''.strip().split('\n'))
###
elements.append(Paragraph("Conseguenze degli obiettivi", h3))
list_gen(f'''
Ridurre i costi operativi legati agli interventi dei tecnici.
Migliorare la soddisfazione del cliente finale grazie a un servizio più affidabile e puntuale.
Mantenimento costante della qualità del prodotto, assicurando che la bibita distribuita sia sempre di qualità.
Ridurre il rischio che il prodotto diventi non consumabile o potenzialmente dannoso per la salute dei consumatori.
'''.strip().split('\n'))
###
elements.append(Paragraph("Collegamento tra obiettivi e benefici attesi", h3))
list_gen(f'''
L’eliminazione della manodopera tecnica comporta una riduzione dei costi operativi.
L’automazione del ciclo di sanificazione garantisce clienti soddisfatti e riduce le lamentele.
Il controllo preciso del processo garantisce qualità costante del prodotto e sicurezza per i consumatori.
'''.strip().split('\n'))
###
elements.append(PageBreak())

########################################
# SOLUZIONE PROPOSTA
########################################
elements.append(Paragraph("Soluzione Proposta", h2))
elements.append(
    Paragraph(f'''
        Si propone un sistema automatizzato che gestisce l’intero ciclo di sanificazione delle linee di spillatura, garantendo qualità costante del prodotto e assenza di intervento manuale.
    ''', body_style,)
)
###
elements.append(Paragraph("Sintesi", h3))
elements.append(
    Paragraph(f'''
        Il progetto prevede lo sviluppo di un sistema che consenta all’utente di avviare il ciclo di sanificazione delle linee semplicemente selezionando la linea tramite un’interfaccia touchscreen. 
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        Tutte le impostazioni dei parametri del ciclo, inclusi tempi e gestione del generatore di ozono, saranno preconfigurate e gestite automaticamente dal sistema, senza bisogno di intervento tecnico.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        Il ciclo previsto per una linea comprende:
    ''', body_style,)
)
ol_gen(f'''
N secondi di passaggio di acqua ozonizzata attraverso la linea, sanificandola
Al termine, ripristino automatico dell’erogazione della bevanda
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Nel caso base, il sistema gestirà una linea alla volta, con possibilità futura di estensione fino a 8-10 linee simultanee.
    ''', body_style,)
)
###
elements.append(Paragraph("Dettagli tecnici", h3))
elements.append(Paragraph("Controllo e logica", h4))
list_gen(f'''
Una PCB (scheda di controllo) gestisce automaticamente il ciclo di sanificazione
Il sistema avvia e spegne il generatore di ozono tramite segnale di controllo o, se necessario, tramite commutazione dell’alimentazione
'''.strip().split('\n'))
###
elements.append(Paragraph("Attuatori", h4))
list_gen(f'''
Valvole per passare dal ciclo di sanificazione all’erogazione normale del prodotto
'''.strip().split('\n'))
###
elements.append(Paragraph("Sensori", h4))
list_gen(f'''
Possibile utilizzo di sensori di flusso per monitorare il corretto avanzamento del ciclo di lavaggio
Eventuali sensori aggiuntivi per sicurezza e conferma del completamento del ciclo
'''.strip().split('\n'))
###
elements.append(Paragraph("Interfaccia utente", h4))
list_gen(f'''
L’utente finale interagisce unicamente tramite un pulsante su touchscreen per selezionare la linea da sanificare
Tutte le fasi operative, inclusi tempi e flussi, sono gestite automaticamente dal sistema
'''.strip().split('\n'))
###
elements.append(Paragraph("Obiettivi della proposta", h3))
list_gen(f'''
Sicurezza: riduzione del rischio di contaminazioni e prodotto non consumabile
Affidabilità operativa: il ciclo è automatico, dura N secondi ed è trasparente all’utente finale
Zero manodopera: l’utente finale non deve intervenire sul ciclo, eliminando la necessità di tecnici sul posto
Qualità costante del prodotto: ogni ciclo di sanificazione è ripetibile e controllato, garantendo bevande sicure e di qualità
'''.strip().split('\n'))
###

def p(text):
    return Paragraph(text, body_style)

elements.append(Paragraph("Collegamento tra soluzione e obiettivi", h3))
table_style = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),  # important for wrapped text
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
])

data = [
    ["Obiettivo", "Come la soluzione raggiunge l'obiettivo"],
    ["Automazione completa", p("Tutto il ciclo gestito dalla PCB, l'utente avvia solo il processo")],
    ["Sanificazione ad ogni cambio fusto", p("L’avvio del ciclo è legato alla selezione della linea post-cambio fusto")],
    ["Qualità costante del prodotto", p("Tempo e flusso dell’acqua ozonizzata predefiniti e controllati automaticamente")],
    ["Eliminazione rischi e riduzione costi", p("Nessun tecnico necessario, minori costi operativi, prodotto sempre sicuro")],
]

'''
table_style = TableStyle([
    # Header
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#222222")),

    # Alignment
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

    # Padding (tight but readable)
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),

    # Lines (minimalist)
    ('LINEBELOW', (0, 0), (-1, 0), 0.75, colors.black),          # header line
    ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.HexColor("#D0D0D0")),  # row lines

    # No vertical lines
    # (intentionally omitted)
])
'''

available_width = doc.width
col_count = len(data[0])
col_widths = [available_width / col_count] * col_count

table = Table(data, colWidths=col_widths)
table.setStyle(table_style)
elements.append(table)

###
elements.append(Paragraph("Diagramma sistema corrente (manuale)", h3))
elements.append(Spacer(1, 10))
mul = 0.35
image_w = 864 * mul
image_h = 64 * mul
img = Image(f"projects/spillatura/diagram-0001.png", image_w, image_h)
elements.append(img)
###
elements.append(Spacer(1, 20))
elements.append(Paragraph("Diagramma sistema da sviluppare (automatico)", h3))
elements.append(Spacer(1, 10))
mul = 0.35
image_w = 1184 * mul
image_h = 448 * mul
img = Image(f"projects/spillatura/diagram-0002.png", image_w, image_h)
elements.append(img)
###
elements.append(PageBreak())

########################################
# PROCESSO OPERATIVO
########################################
elements.append(Paragraph("Processo Operativo", h2))
elements.append(
    Paragraph(f'''
        Il processo di sanificazione è gestito automaticamente tramite una sequenza controllata di fasi operative attivata dall’utente al cambio fusto.
    ''', body_style,)
)
###
elements.append(Paragraph("Visione semplificata", h3))
elements.append(
    Paragraph(f'''
        Il ciclo operativo si sviluppa secondo le seguenti fasi:
    ''', body_style,)
)
ol_gen(f'''
Selezione della linea da parte dell’utente
Avvio del ciclo
Erogazione di acqua ozonizzata per la sanificazione della linea
Ripristino automatico dell’erogazione della bevanda dopo il ciclo di sanificazione
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Il processo è progettato per essere trasparente all’utente e integrato nelle normali operazioni di spillatura.
    ''', body_style,)
)
###
elements.append(Paragraph("Sequenza tecnica dettagliata", h3))
elements.append(Paragraph("1 Trigger del ciclo", h4))
elements.append(
    Paragraph(f'''
        L’utente, dopo aver sostituito il fusto, seleziona la linea da sanificare tramite interfaccia.
    ''', body_style,)
)
elements.append(Paragraph("2 Attivazione del sistema", h4))
elements.append(
    Paragraph(f'''
        Il sistema di controllo riceve il comando di avvio e inizializza la sequenza operativa.
    ''', body_style,)
)
elements.append(Paragraph("3 Commutazione del flusso", h4))
elements.append(
    Paragraph(f'''
        Le valvole vengono attivate per deviare il flusso dalla modalità erogazione bevanda alla modalità sanificazione.
    ''', body_style,)
)
elements.append(Paragraph("4 Attivazione generatore di ozono", h4))
elements.append(
    Paragraph(f'''
        Il sistema attiva il generatore di ozono tramite segnale di controllo o alimentazione diretta.
    ''', body_style,)
)
elements.append(Paragraph("5 Fase di sanificazione", h4))
elements.append(
    Paragraph(f'''
        L’utente inizia a spillare. Durante questa fase:
    ''', body_style,)
)
ol_gen(f'''
viene erogata acqua ozonizzata
il fluido attraversa l’intera linea di distribuzione
la sanificazione avviene lungo tutto il percorso fino alla spillatrice
'''.strip().split('\n'))
###
elements.append(PageBreak())
###
elements.append(Paragraph("6 Controllo temporale", h4))
elements.append(
    Paragraph(f'''
        Il sistema mantiene la fase di sanificazione per un tempo predefinito (attualmente N secondi, configurabili in futuro).
    ''', body_style,)
)
elements.append(Paragraph("7 Terminazione sanificazione", h4))
elements.append(
    Paragraph(f'''
        Al termine del tempo predefinito:
    ''', body_style,)
)
ol_gen(f'''
il generatore di ozono viene disattivato
le valvole riportano il sistema alla configurazione di erogazione normale
'''.strip().split('\n'))
elements.append(Paragraph("8 Ripristino erogazione prodotto", h4))
elements.append(
    Paragraph(f'''
        La bevanda torna automaticamente a fluire dalla spillatrice, segnalando implicitamente all’utente il completamento del ciclo.
    ''', body_style,)
)
###
# elements.append(PageBreak())
###
elements.append(Paragraph("Diagramma flusso operativo del ciclo di sanificazione", h3))
elements.append(Spacer(1, 10))
mul = 0.45
image_w = 960 * mul
image_h = 288 * mul
img = Image(f"projects/spillatura/diagram-0000.png", image_w, image_h)
elements.append(img)
###
elements.append(Paragraph("Note operative e condizioni", h3))
list_gen(f'''
Il ciclo è attualmente configurato con durata fissa (N secondi), con possibilità futura di parametrizzazione da parte di personale tecnico.
Durante la fase di sanificazione, l’utente deve mantenere attiva la spillatura per consentire il passaggio completo dell’acqua ozonizzata nella linea.
Il sistema, nella configurazione attuale, gestisce una linea alla volta; è prevista un’evoluzione futura per la gestione simultanea di più linee in modo indipendente.
La gestione di condizioni anomale (es. interruzione del ciclo, assenza di flusso) non è ancora definita e rappresenta un punto di attenzione per le fasi successive di progettazione.
'''.strip().split('\n'))

elements.append(PageBreak())

########################################
# ARCHITETTURA DEL SISTEMA
########################################
elements.append(Paragraph("Architettura del Sistema", h2))
elements.append(
    Paragraph(f'''
        Il sistema è basato su un’architettura modulare controllata da microcontrollore, progettata per garantire integrazione, affidabilità operativa e scalabilità futura.
    ''', body_style,)
)
###
elements.append(Paragraph("Sintesi", h3))
elements.append(
    Paragraph(f'''
        L’architettura del sistema si compone dei seguenti sottosistemi principali:
    ''', body_style,)
)
list_gen(f'''
Sistema di controllo centrale, responsabile della gestione della logica operativa
Sistema idraulico, per la gestione dei flussi di acqua ozonizzata e prodotto
Interfaccia utente, per l’avvio (e futuro controllo) del ciclo
Sistema di generazione ozono, fornito dal partner e integrato nel processo
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Questi elementi operano in modo coordinato per garantire l’esecuzione automatica del ciclo di sanificazione.
    ''', body_style,)
)
###
elements.append(Paragraph("Componenti principali", h3))
elements.append(Paragraph("Sistema di controllo", h4))
list_gen(f'''
Microcontrollore integrato su PCB custom
Gestione della logica di controllo, temporizzazioni e sequenze operative
Interfacciamento con sensori, attuatori e sistema ozono
'''.strip().split('\n'))
elements.append(Paragraph("Attuatori", h4))
list_gen(f'''
Elettrovalvole on/off per commutazione tra modalità sanificazione ed erogazione prodotto
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Il sistema sfrutta la pressione della rete idrica (rubinetto), senza necessità di pompe dedicate
    ''', body_style,)
)
elements.append(Paragraph("Sensori", h4))
elements.append(
    Paragraph(f'''
        Possibile integrazione futura di sensori di flusso per: 
    ''', body_style,)
)
list_gen(f'''
monitoraggio del corretto svolgimento del ciclo
rilevamento di anomalie (es. assenza di flusso)
'''.strip().split('\n'))
elements.append(Paragraph("Touchscreen con interfaccia semplificata", h4))
elements.append(
    Paragraph(f'''
        Funzionalità attuale:
    ''', body_style,)
)
list_gen(f'''
selezione linea (avvio ciclo)
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Possiblili evoluzioni:
    ''', body_style,)
)
list_gen(f'''
configurazione parametri
monitoraggio stato sistema
'''.strip().split('\n'))
elements.append(Paragraph("Sistema di generazione ozono (partner)", h4))
elements.append(
    Paragraph(f'''
        Il generatore di ozono viene integrato nel sistema tramite tramite uno dei seguenti modi:
    ''', body_style,)
)
list_gen(f'''
segnale di controllo digitale (modalità preferita)
controllo diretto dell’alimentazione (soluzione alternativa di backup)
protocollo di comunicazione (soluzione sconsigliata a questo punto del progetto, in quanto potrebbe allungare i tempi del test)
'''.strip().split('\n'))

elements.append(Paragraph("Logica di interconnessione", h4))
ol_gen(f'''
L’utente interagisce con l’interfaccia e il comando viene inviato al microcontrollore
Il microcontrollore (1) attiva/disattiva il generatore di ozono, (2) controlla le elettrovalvole, (3) gestisce la temporizzazione del ciclo
I sensori (quando presenti) forniscono feedback al sistema di controllo per garantire il corretto funzionamento
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Questa architettura consente una gestione centralizzata e automatizzata dell’intero processo.
    ''', body_style,)
)
###
elements.append(Paragraph("Scalabilità e sviluppi futuri", h3))
elements.append(
    Paragraph(f'''
        L’architettura è progettata per supportare evoluzioni future, tra cui:
    ''', body_style,)
)
list_gen(f'''
gestione di più linee di spillatura in parallelo (8-10 linee)
implementazione di controlli indipendenti per ciascuna linea, con valvole dedicate
introduzione di sensori aggiuntivi per migliorare sicurezza e affidabilità
espansione delle funzionalità dell’interfaccia utente
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        La modularità del sistema consente di adattare facilmente la soluzione a configurazioni più complesse senza modifiche sostanziali alla logica di base.
    ''', body_style,)
)
###
# elements.append(PageBreak())
###
elements.append(Paragraph("Diagramma Architettura Sistema", h3))
elements.append(Spacer(1, 10))
mul = 0.4
image_w = 1056 * mul
image_h = 336 * mul
img = Image(f"projects/spillatura/diagram-0003.png", image_w, image_h)
elements.append(img)
###
elements.append(PageBreak())

########################################
# INTEGRAZIONE CON SISTEMA PARTNER
########################################
elements.append(Paragraph("Integrazione con Sistema Partner", h2))
elements.append(
    Paragraph(f'''
        L’integrazione con il sistema di generazione di ozono (partner) devrebbe essere tecnicamente realizzabile, con alcune specifiche di interfaccia ancora da validare.
    ''', body_style,)
)
###
elements.append(Paragraph("Modalità di integrazione", h3))
elements.append(
    Paragraph(f'''
        Il sistema proposto prevede l’integrazione diretta con il generatore di ozono fornito dal partner, al fine di coordinare automaticamente la produzione di acqua ozonizzata durante il ciclo di sanificazione.
    ''', body_style,)
)
elements.append(
    Paragraph(f'''
        L’integrazione si basa su:
    ''', body_style,)
)
list_gen(f'''
attivazione e disattivazione del generatore in funzione del ciclo operativo
sincronizzazione tra produzione di ozono e flusso idraulico
'''.strip().split('\n'))
###
elements.append(Paragraph("Interfacce tecniche previste", h3))
elements.append(
    Paragraph(f'''
        L’architettura prevede due possibili modalità di controllo del generatore:
    ''', body_style,)
)
list_gen(f'''
Controllo tramite segnale digitale (modalità preferita): Il sistema invia un segnale di start/stop al generatore di ozono, consentendo un’integrazione diretta e controllata.
Controllo tramite alimentazione (modalità alternativa): In assenza di interfacce di controllo dedicate, il sistema può gestire l’accensione e lo spegnimento del generatore intervenendo direttamente sull’alimentazione elettrica.
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Eventuali segnali di feedback dal generatore (es. stato attivo, errore) potranno essere integrati qualora disponibili.
    ''', body_style,)
)
###
elements.append(Paragraph("Aree da validare", h3))
elements.append(
    Paragraph(f'''
        Alcuni aspetti tecnici risultano attualmente non definiti e richiedono approfondimento con il partner:
    ''', body_style,)
)
list_gen(f'''
disponibilità e tipologia di interfacce di controllo (segnali digitali/analogici)
caratteristiche elettriche del generatore (tensione, potenza, modalità di avvio)
tempi di risposta e comportamento all’avvio/arresto
eventuale disponibilità di segnali di stato o diagnostica
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Questi elementi sono fondamentali per definire in modo preciso la strategia di integrazione.
    ''', body_style,)
)
###
elements.append(PageBreak())
###
elements.append(Paragraph("Criticità e rischi", h3))
elements.append(
    Paragraph(f'''
        L’integrazione con il sistema del partner rappresenta uno dei principali punti di attenzione del progetto, in quanto:
    ''', body_style,)
)
list_gen(f'''
la mancanza di interfacce standard potrebbe richiedere soluzioni alternative
comportamenti non noti del generatore potrebbero influenzare il ciclo operativo
eventuali tempi di avvio non trascurabili potrebbero richiedere adattamenti nella sequenza di controllo
'''.strip().split('\n'))
###
elements.append(Paragraph("Strategia di integrazione", h3))
elements.append(
    Paragraph(f'''
        Per mitigare i rischi identificati, si prevede un approccio progressivo:
    ''', body_style,)
)
list_gen(f'''
raccolta dettagli tecnici dal partner
sviluppo di un prototipo di integrazione
test funzionali per validare il comportamento del sistema
eventuale adattamento della logica di controllo
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Questo approccio consente di ridurre le incertezze e garantire una integrazione robusta ed affidabile.
    ''', body_style,)
)

elements.append(PageBreak())

########################################
# BENEFICI ATTESI
########################################
elements.append(Paragraph("Benefici Attesi", h2))
elements.append(
    Paragraph(f'''
        Si ritiene che l’automazione del processo di sanificazione possa portare benefici significativi in termini di qualità del prodotto, efficienza operativa e riduzione dei costi, migliorando l’affidabilità complessiva del servizio.
    ''', body_style,)
)
###
elements.append(Paragraph("Qualità del prodotto", h3))
list_gen(f'''
Mantenimento costante della qualità della bevanda durante la spillatura
Eliminazione del rischio di contaminazioni nelle linee di distribuzione
Preservazione delle caratteristiche organolettiche del prodotto
Riduzione del rischio di prodotto non consumabile
'''.strip().split('\n'))
###
elements.append(Paragraph("Efficienza operativa", h3))
list_gen(f'''
Eliminazione della necessità di interventi da parte di tecnici specializzati
Possibilità di eseguire la sanificazione direttamente da parte dell’operatore
Processo immediato e integrato nel normale flusso di lavoro (cambio fusto)
Eliminazione dei tempi di attesa legati alla disponibilità dei tecnici
Assenza di tempi di fermo dell’impianto
'''.strip().split('\n'))
###
elements.append(Paragraph("Riduzione dei costi", h3))
list_gen(f'''
Riduzione dei costi di manodopera tecnica
Riduzione delle perdite legate a prodotto scartato o restituito
Eliminazione dei costi indiretti legati a inefficienze operative
Riduzione del rischio di perdita di clienti e conseguente impatto economico
'''.strip().split('\n'))
###
elements.append(Paragraph("Affidabilità e valore per il business", h3))
list_gen(f'''
Maggiore affidabilità del servizio offerto al cliente finale
Miglioramento della reputazione degli operatori
Maggiore controllo sulla qualità del prodotto distribuito
Vantaggio competitivo per il fornitore di bevande, che può garantire standard qualitativi costanti senza dipendere da interventi esterni
Possibilità di scalare il servizio su più clienti senza aumentare proporzionalmente i costi operativi
'''.strip().split('\n'))
###
elements.append(PageBreak())

########################################
# FATTIBILITA E RISCHI
########################################
elements.append(Paragraph("Fattibilità e Rischi", h2))
elements.append(
    Paragraph(f'''
        Lo scopo di questa proposta tecnica è quello di ridurre le incertezze progettuali e garantire una integrazione robusta ed affidabile.
    ''', body_style,)
)
###
elements.append(Paragraph("Affidabilità", h3))
elements.append(
    Paragraph(f'''
        Il sistema proposto si basa su componenti e tecnologie consolidate, tra cui:
    ''', body_style,)
)
list_gen(f'''
sistemi di controllo basati su microcontrollore
elettrovalvole per la gestione dei flussi
integrazione con sistemi di generazione di ozono
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        L’architettura complessiva è relativamente semplice e non richiede lo sviluppo di tecnologie innovative, rendendo il progetto realizzabile nel breve-medio termine.
    ''', body_style,)
)
###
elements.append(Paragraph("Rischi principali", h3))
data = [
    ["Rischio", "Impatto", "Mitigazione"],
    [p("Esecuzione non corretta del ciclo di sanificazione"), "Alto", p("Validazione del ciclo tramite test reali, introduzione di sensori (es. flusso) per monitoraggio")],
    [p("Parametri di sanificazione non ottimali (tempo/volume)"), "Alto", p("Test sperimentali per determinare durata e quantità di fluido necessarie")],
    [p("Incertezza sull’integrazione con il generatore di ozono"), "Medio-Alto", p("Raccolta dati tecnici dal partner e test di integrazione su prototipo")],
    [p("Utilizzo non corretto da parte dell’utente (es. mancato avvio ciclo)"), "Medio", p("Valutazione di sistemi automatici di rilevazione cambio fusto")],
    [p("Guasti o anomalie del sistema (valvole, flusso, assenza acqua)"), "Medio", p("Progettazione con controlli di sicurezza e diagnostica base")],
]
available_width = doc.width
col_count = len(data[0])
col_widths = [available_width / col_count] * col_count
col_widths = [available_width*0.40, available_width*0.20, available_width*0.40]
table = Table(data, colWidths=col_widths)
table.setStyle(table_style)
elements.append(table)
###
elements.append(Paragraph("Strategia di mitigazione", h3))
elements.append(
    Paragraph(f'''
        Per ridurre i rischi identificati, si prevede un approccio iterativo basato su:
    ''', body_style,)
)
list_gen(f'''
sviluppo di un prototipo funzionante
esecuzione di test reali di sanificazione per validare l’efficacia del processo
raccolta e integrazione dei dati tecnici del sistema del partner
introduzione progressiva di sensori e controlli di sicurezza
eventuale adattamento della logica di controllo sulla base dei risultati ottenuti
'''.strip().split('\n'))
elements.append(
    Paragraph(f'''
        Questo approccio consente di affrontare in modo strutturato le incertezze e garantire la robustezza del sistema finale.
    ''', body_style,)
)
###
elements.append(PageBreak())

########################################
# PIANO DI IMPLEMENTAZIONE
########################################
elements.append(Paragraph("Piano di Implementazione", h2))
elements.append(
    Paragraph(f'''
        Il progetto sarà sviluppato in fasi iterative, con prototipo e test in laboratorio per validare il sistema su una singola linea, garantendo la fattibilità prima di eventuali sviluppi commerciali.
    ''', body_style,)
)
###
elements.append(Paragraph("Fasi del progetto", h3))
elements.append(Paragraph("1 Raccolta requisiti", h4))
list_gen(f'''
Definizione dettagliata dei parametri di sanificazione, interfacce e flussi di controllo 
Identificazione dei punti critici da validare con il partner
'''.strip().split('\n'))
elements.append(Paragraph("2 Progettazione rapida", h4))
list_gen(f'''
Sviluppo della logica di controllo su microcontrollore
Progettazione PCB custom (per test preliminari utilizzare una scheda preesistente se idonea) 
Progettazione schema idraulico della linea di test
'''.strip().split('\n'))
elements.append(Paragraph("3 Sviluppo prototipo", h4))
list_gen(f'''
Realizzazione di un prototipo funzionante su una singola linea
Integrazione con elettrovalvole e generatore di ozono (tramite segnale o alimentazione)
'''.strip().split('\n'))
elements.append(Paragraph("4 Test e validazione in laboratorio", h4))
list_gen(f'''
Verifica della corretta esecuzione del ciclo
Misurazione dei parametri di sanificazione (tempo, quantità di acqua ozonizzata)
Identificazione e correzione di eventuali anomalie
'''.strip().split('\n'))
elements.append(Paragraph("5 Ottimizzazione iterativa", h4))
list_gen(f'''
Adattamento della logica di controllo sulla base dei risultati dei test
Possibile aggiunta di sensori o miglioramenti dell’interfaccia utente
'''.strip().split('\n'))
elements.append(Paragraph("6 Documentazione e conclusioni", h4))
list_gen(f'''
Raccolta dei dati sperimentali
Valutazione finale della fattibilità e preparazione delle linee guida per eventuale sviluppo
'''.strip().split('\n'))
###
elements.append(Paragraph("Approccio proposto", h3))
list_gen(f'''
Iterativo e test-driven: ogni fase produce dati concreti e consente adattamenti rapidi
Prototipo singola linea: per validare il concetto senza investimenti iniziali troppo grandi
Validazione in laboratorio: riduce rischi prima di qualsiasi test sul campo
Obiettivo primario: validare il processo e dimostrare la fattibilità del sistema completo
'''.strip().split('\n'))
###
elements.append(PageBreak())

########################################
# STIMA COMPONENTI
########################################
elements.append(Paragraph("Stima Componenti", h2))
elements.append(
    Paragraph(f'''
        Il sistema può essere realizzato utilizzando componenti standard e facilmente reperibili, con una struttura modulare che consente scalabilità e ottimizzazione dei costi.
    ''', body_style,)
)
###
elements.append(Paragraph("Componenti principali", h3))
elements.append(
    Paragraph(f'''
        Di seguito una stima preliminare dei principali componenti necessari per la realizzazione del sistema su una singola linea.
    ''', body_style,)
)
elements.append(Paragraph("Sistema di controllo", h4))
list_gen(f'''
Microcontrollore (ESP32)
PCB custom progettata ad hoc per gestione I/O e interfacciamento con attuatori e sensori
'''.strip().split('\n'))
###
elements.append(Paragraph("Alimentazione", h4))
list_gen(f'''
Alimentazione principale 12V DC (preferita)
Eventuale conversione da 230V AC a 12V DC tramite alimentatore dedicato
'''.strip().split('\n'))
###
elements.append(Paragraph("Attuatori", h4))
list_gen(f'''
Elettrovalvole on/off (n. 2 per linea) per commutazione flusso
'''.strip().split('\n'))
###
elements.append(Paragraph("Sensori (opzionali / da validare)", h4))
list_gen(f'''
Sensore di flusso per monitoraggio del corretto passaggio del fluido e rilevamento anomalie (assenza flusso)
'''.strip().split('\n'))
###
elements.append(Paragraph("Interfaccia utente", h4))
list_gen(f'''
Touchscreen con display embedded per selezione linea
'''.strip().split('\n'))
###
elements.append(Paragraph("Infrastruttura e integrazione", h4))
list_gen(f'''
Quadro elettrico / box di contenimento
Cablaggi elettrici e connessioni idrauliche
Interfaccia di collegamento con il generatore di ozono
'''.strip().split('\n'))
###
elements.append(Paragraph("Considerazioni", h4))
list_gen(f'''
La scelta di componenti standard consente facilità di approvvigionamento e manutenzione
L’architettura modulare permette di replicare il sistema su più linee con incremento lineare dei componenti
Alcuni elementi (es. sensori) potranno essere confermati o ottimizzati in fase di test
'''.strip().split('\n'))
###
'''
data = [
    ["Componente", "Descrizione", "Quantità", "Costo unitario (€)", "Costo totale (€)"],
    ["Microcontrollore (ESP32)", "Controllo logica sistema", "1", "5-15", "5-15"],
]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))
elements.append(table)
'''
###
elements.append(PageBreak())

########################################
# DECISIONE RICHIESTA
########################################
elements.append(Paragraph("Decisione Richiesta", h2))
elements.append(
    Paragraph(f'''
        Si richiede l’approvazione per avviare la fase di sviluppo prototipale e validazione del sistema di sanificazione automatizzata.
    ''', body_style,)
)
###
elements.append(Paragraph("Approvazioni richieste", h3))
elements.append(
    Paragraph(f'''
        Si richiede l’approvazione per:
    ''', body_style,)
)
list_gen(f'''
Avvio del progetto di sviluppo di un prototipo funzionante su singola linea
Allocazione di un budget preliminare per la realizzazione del prototipo (componenti, sviluppo hardware e test)
Avvio della collaborazione tecnica con il partner per la definizione delle modalità di integrazione con il generatore di ozono
'''.strip().split('\n'))
###
elements.append(Paragraph("Obiettivo della fase di prototipazione", h3))
elements.append(
    Paragraph(f'''
        La fase oggetto di approvazione ha l’obiettivo di:
    ''', body_style,)
)
list_gen(f'''
Validare l’efficacia del processo di sanificazione automatizzata
Verificare la fattibilità tecnica del sistema
Identificare eventuali criticità e ottimizzazioni necessarie
'''.strip().split('\n'))
###
elements.append(Paragraph("Passi successivi", h3))
elements.append(
    Paragraph(f'''
        Al termine della fase di prototipazione e test, verrà effettuata una valutazione dei risultati al fine di:
    ''', body_style,)
)
list_gen(f'''
confermare la validità tecnica della soluzione
definire eventuali evoluzioni del sistema
valutare lo sviluppo di una versione industrializzabile del prodotto
'''.strip().split('\n'))
###
elements.append(PageBreak())

########################################
# APPENDICE TECNICA
########################################
elements.append(Paragraph("Appendice Tecnica", h2))
###
elements.append(Paragraph("Logica di controllo (pseudo-codice)", h3))

from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# McKinsey-style code paragraph
code_style = ParagraphStyle(
    name="Code",
    fontName="Courier",          # monospace feel
    fontSize=9,
    leading=12,
    leftIndent=6,
    textColor=colors.black,
    alignment=TA_LEFT,
)

def code_block(text, width):
    # preserve indentation and line breaks
    formatted = text.replace(" ", "&nbsp;").replace("\n", "<br/>")
    para = Paragraph(formatted, code_style)

    table = Table([[para]], colWidths=[width])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    return table

pseudo = """
START
    Attesa input utente (selezione linea + avvio ciclo)
    IF comando_avvio = TRUE THEN
        Seleziona linea
        Attiva elettrovalvole → modalità sanificazione
        Attiva generatore ozono
        Avvia timer (T = N secondi)
        WHILE timer < T DO
            IF sensore_flusso = FALSE (opzionale) THEN
                Segnala errore
                STOP ciclo
            ENDIF
        ENDWHILE
        Disattiva generatore ozono
        Ripristina elettrovalvole → modalità erogazione bevanda
    END IF
END
""".strip()

elements.append(code_block(pseudo, doc.width))

def code_block(text, width):
    # preserve indentation and line breaks
    formatted = text.replace(" ", "&nbsp;").replace("\n", "<br/>")
    para = Paragraph(formatted, code_style)

    table = Table([[para]], colWidths=[width])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    return table
###
elements.append(Paragraph("Sequenza operativa formalizzata", h3))
list_gen(f'''
Input utente (touchscreen)
Selezione linea
Attivazione valvole → modalità sanificazione
Attivazione ozono
Spillatura acqua ozonizzata
Temporizzazione (N secondi)
Disattivazione ozono
Ripristino erogazione bevanda
'''.strip().split('\n'))
###
elements.append(Paragraph("I/O preliminare", h3))
###
elements.append(Paragraph("Input", h4))
list_gen(f'''
Selezione linea per avvio ciclo (utente)
Sensore di flusso (opzionale)
'''.strip().split('\n'))
###
elements.append(Paragraph("Output", h4))
list_gen(f'''
Controllo elettrovalvole (x2 per linea)
Controllo generatore ozono (ON/OFF)
Output interfaccia utente (stato sistema)
'''.strip().split('\n'))
###
elements.append(PageBreak())
###
elements.append(Paragraph("PCB proposta per primo test", h3))
elements.append(Spacer(1, 10))
mul = 0.2
image_w = 2160 * mul
image_h = 1509 * mul
img = Image(f"projects/spillatura/pcb-preliminary-test.png", image_w, image_h)
elements.append(img)
###
elements.append(Paragraph("Interfaccia utente semplificata per primi test", h3))
elements.append(Spacer(1, 10))
mul = 0.5
image_w = 800 * mul
image_h = 480 * mul
img = Image(f"projects/spillatura/p_home.png", image_w, image_h)
elements.append(img)
###
elements.append(PageBreak())
###
elements.append(Paragraph("Assunzioni tecniche", h3))
list_gen(f'''
Il flusso d’acqua è garantito dalla rete idrica (pressione rubinetto)
Il generatore di ozono è controllabile via segnale o alimentazione
Il tempo di sanificazione iniziale è fissato a N secondi (da validare)
L’utente esegue correttamente la procedura di avvio ciclo
'''.strip().split('\n'))
###
elements.append(Paragraph("Punti da validare", h3))
list_gen(f'''
Tempo ottimale di sanificazione
Necessità e tipologia di sensori
Modalità di integrazione con il generatore di ozono
Gestione condizioni di errore (interruzione ciclo, assenza flusso, ecc.)
'''.strip().split('\n'))
###
elements.append(Paragraph("Chiarimenti", h3))
list_gen(f'''
Il sistema è implementabile senza sensore di flusso? Ovvero, come faccio a calcolare quanto tempo del timer è passato se non riesco a verificare che l'utente sta effettivamente spinando?
Qual'è la probabilità che l'utente dimentichi di selezionare la linea per avviare il ciclo di sanificazione post-cambio fusto? Si ritiene utile automatizzare anche questa parte del processo, rilevando il cambio del fusto in modo automatico in qualche modo per eliminare completamente l'errore umano? 
Cove viene sanificata la parte della linea che va dal fusto fino alla valvola di commutazione? Potrebbe provocare problemi di contaminazione crociata significativi sul resto della linea?
'''.strip().split('\n'))
###
elements.append(PageBreak())

# BUILD
doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

subprocess.run(["xdg-open", "doc.pdf"])

'''
1. ad oggi, il sistema funziona che un tecnico va dal cliente a fare un operazione di lavaggio / sanificazione manuale ogni mese, e deve essere pagato da qualcuno (utente finale, o fornitore del servizio di birra)
2. completamente manuale, deve andare un tecnico a fare l'operazione
3. costi, tecnici non sempre reperibili, perdita di reputazione e di clientela del cliente che serve birra che non buona
4. qualia scarsa del prodotto, inefficenze di pulizia, ritardi delle operazioni di lavaggio
5. si vuole costruire un sistema che sanifichi le linee di distribuzione delle spillatrici ad ogni cambio fusto birra in modo automatizzato
6. il processo completo di sanificazione delle spillatrici per il mantenimento della qualita del prodotto
7. qualita massima del prodotto mantenuta costante nel tempo, zero manodopera, sanificazione garantita, no errori, no tempi di fermo, no clienti che bevono birra insoddisfatti, no costi dei tecnici che devono fare le operazioni
8. non lo so
9. no
10. raccola dati del processo (ciclo) di sanificazione, progettazione di un sistema campione, test per confermare la buona sanificazione con processo automatico
'''

'''
1. una volta al mese, ma non e detto a causa della disponibilita del tecnico
2. non lo so
3. o il cliente che lo richiede, o l'azienda che fornisce di birra il cliente
4. non lo so
5. si, non tanto errori ma differenza in qualita del servizio, inoltre non e un lavoro che piace fare ai tecnici
6. si
7. limitato dai tecnici
8. contaminazioni, cattivi odori nel prodotto, la birra venduta torna indietro
9. tantissimo, al punto che il prodotto non e piu consumabile
10. ha i consumatori che gli rimandano indietro la birra, con perdita di reputazione e potenziali consumatori
11. decisamente si
12. incuranza dei clienti che chiamano i tecnici solo quando e gia tardi e gli torna indietro la birra e la scarsa disponibilita del tecnico che non riesce andare dal cliente immediatamente
'''

'''
1. automatizzare l'intero processo di lavaggio e sanificazione
2. processo di lavaggio e sanificazione delle linee di distribuzione del prodotto utilizzando l'acqua ozonizzata ogni volta che cambia il fusto, l'utente deve solo selezionare la linea da sanificare tramite un iterfaccial quando cambia il fusto
3. zero manodopera intesa come interventi di tecnici, qualita costante del prodotto
4. per adesso no
5. rischio che il prodotto non sia piu consumabile o addirittura dannoso per la salute dei consumatori
6. clienti soddisfatti, riduzione costi
'''

'''
1. al momento solo una alla volta, in futuro probabilmente diverse linee contemporaneamente (caso medio 8/10 linee)
2. l'utente deve solo selezionare la linea per avviare il ciclo, tutte le altre impostazioni dei parametri devono essere fatte da un tecnico specializzato
3. non e stato definito, ma per un test iniziale prendiamo come caso base 10-30 secondi
4. valvole per cambiare tra ciclo di sanificazione ed erogazione normale del prodotto 
5. non definito al momento, forse sensori di flusso per monitorare il ciclo di lavaggio
6. il nostro sistema deve essere in grado di avviare e spegnere il generatore di ozono, se possibile via un segnale, altrimenti dandogli e togliendoli corrente direttamente sull'alimentazione
7. l'utente finale deve al massimo premere un pulsante su un touchscreen per avviare il ciclo, tutto il resto deve essere automatizzato 
8. non definito
9. al momento no
per spiegarti come funziona, l'utente finale cambia il fusto, avvia il ciclo, e comincia a spinare. mentre spina, esce acqua ozonizzata per 10 secondi, la quale passa per la linea sanificandola. al termine dei 10 secondi ricomincia ad uscire la birra dalla spina al posto dell'acqua.
'''

'''
1. manualmente, utente preme un bottone (operazione da fare al cambio fusto)
2. per ora i 10 secondi sono fissi, in futuro opzione regolabile
3. durante il cicle l'utende deve spillare, dalla spillatrice uscira acqua ozonizzata quindi lo scopo e di sanificare tutta la linea facendo passare l'acqua ozonizzata per tutta la linea e facendola uscire dalla spillatrice. dopo 10 secondi che si sta spillando acqua, in modo automatico comincia ad uscire birra quindi l'utente sa che e pronta.
4. se il ciclo viene interrotto, non definito al momento, grazie per aver notato questa criticita
5. nel caso multi-linea, in futuro cicle indipendenti, per ora solo una linea
'''

'''
1. utilizzeremo un microcontrollore, con una PBC custom progettata su misura da noi.
2. l'impianto di sanificazione viene attaccato ad un rubinetto, quindi l'acqua la prende con pressione di rubinetto.
3. elettrovalvole on/off
4. solo idea per ora
5. controllo via segnale se compatibile con microcotrollore, altrimenti si interviene sull alimentazione diretta come backup
6. per ora un bottone per linea, in futuro probabilmente qualcosa di piu complesso come la scelta di parametri ecc.
7. da definire, ma probabilmente ogni linea ha valvole dedicate
'''

'''
1. non ancora chiarito
2. non ancora chiarito
3. non ancora chiarito
4. non ancora chiarito
5. non ancora chiarito
'''

'''
1. la qualita della birra resta intatta durante la spillatura e non viene contaminata
2. minore richiesta di interventi, zero tempi di fermo, facilita nel sanificare le linee, puo essere fatto da chi spilla la birra invece che da un tecnico specializzato, sanificazione istantanea e costante invece di attesa uscita tecnico
3. manodopera tecnici, prodotto scartato, ritorno prodotto da parte di clienti, perdita di potenziali clienti e reputazione,
4. non saprei, deducilo tu
'''

'''
1. al momento rischio piu grande e avere la certezza che il cicle venga eseguito correttamente, considerando tempistiche, rilevamento flusso, ecc.
2. 10 secondi sono un valore fittizio, bisogna verificare il valore reale di secondi (o quantita ti acqua ozonizzata da far passare) per validare il risultato.
3. non si conosce ancora il comportamento del sistema partner
4. salti il ciclo, valutare se rilevazione del cambio fusto viene fatta in automatico invece che indicata dall'utente
5. possibili guasti sistema, valvole, flusso, manca acqua.
'''

'''
1. si, per una sola linea
2. partire rapido e iterare
3. in laboratorio
4. si
5. solo validare, il prodotto vendibile sara un passo successivo
'''

'''
1. esp32
2. PCB custom
3. alimentazione 12V DC preferibile, se necessario 220V AC
4. 2 valvole per linea
5. inserisci sensore flusso (da valutare)
6. touchscreen, integrato display embedded
7. quadro e cablaggi
'''

if 0:
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

    # subprocess.run(["xdg-open", "doc.pdf"])



