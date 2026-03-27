import subprocess

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
body = ParagraphStyle('body', fontSize=body_size, leading=body_leading)
paragraph = ParagraphStyle('paragraph', fontSize=body_size, leading=body_leading, spaceAfter=body_space_after)
list_style = ParagraphStyle('list', parent=body, leftIndent=0, spaceAfter=2)

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

# elements.append(Paragraph("Proposta Tecnico-Strategica", cover_title))
elements.append(Paragraph("Automazione del Processo di Ozonizzazione nei Sistemi di Spillatura", cover_title))
elements.append(Spacer(1, 20))
elements.append(Paragraph(
    "Analisi Tecnica",
    body
))

elements.append(Spacer(1, 100))
elements.append(Paragraph("Preparata per", meta))
elements.append(Paragraph("Otregroup | Sweesh", section))

elements.append(Spacer(1, 60))
elements.append(Paragraph("Marzo 2026", meta))

elements.append(Spacer(1, 120))
elements.append(Paragraph(
    "Strettamente Confidenziale – Proibita la divulgazione non autorizzata",
    footer
))

elements.append(PageBreak())

# EXECUTIVE SUMMARY (1 pagina max)
elements.append(Paragraph("Executive Summary", h2))
elements.append(
    Paragraph(f'''
        Si propone lo sviluppo di un sistema automatizzato per la sanificazione delle linee di distribuzione della birra, basato su tecnologia di ozonizzazione, in grado di operare in modo autonomo ad ogni cambio fusto.
    ''', paragraph)
)
###
elements.append(Paragraph("Contesto e problema", h3))
elements.append(
    Paragraph(f'''
        L’attuale processo di sanificazione è completamente manuale e richiede l’intervento periodico di un tecnico presso il cliente finale. Questo approccio comporta:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("costi operativi elevati legati alla manodopera", list_style)),
        ListItem(Paragraph("dipendenza dalla disponibilità dei tecnici", list_style)),
        ListItem(Paragraph("ritardi nelle operazioni di pulizia", list_style)),
        ListItem(Paragraph("variabilità nella qualità della sanificazione", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(Spacer(1, 10))
elements.append(
    Paragraph(f'''
        Tali criticità impattano direttamente sulla qualità del prodotto finale, con conseguente rischio di perdita di clientela e danno reputazionale per gli operatori.
    ''', paragraph)
)
###
elements.append(Paragraph("Soluzione proposta", h3))
elements.append(
    Paragraph(f'''
        Il progetto prevede lo sviluppo di un sistema automatizzato in grado di eseguire l’intero ciclo di sanificazione delle linee di spillatura in modo autonomo ad ogni cambio fusto.
    ''', paragraph)
)
elements.append(
    Paragraph(f'''
        Il sistema gestirà:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("il ciclo completo di lavaggio e sanificazione", list_style)),
        ListItem(Paragraph("il cambio dal ciclo di lavaggio all'erogazione della bevanda", list_style)),
        ListItem(Paragraph("il controllo delle fasi operative senza intervento umano", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(Spacer(1, 10))
###
elements.append(Paragraph("Benefici attesi", h3))
elements.append(
    Paragraph(f'''
        L’introduzione del sistema automatizzato consentirà:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("mantenimento costante della qualità del prodotto nel tempo", list_style)),
        ListItem(Paragraph("eliminazione della manodopera per le operazioni di sanificazione", list_style)),
        ListItem(Paragraph("riduzione dei costi operativi", list_style)),
        ListItem(Paragraph("eliminazione degli errori umani", list_style)),
        ListItem(Paragraph("maggiore affidabilità e ripetibilità del processo", list_style)),
        ListItem(Paragraph("miglioramento della soddisfazione del cliente finale", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(Spacer(1, 10))
###
elements.append(Paragraph("Fattibilità e prossimi passi", h3))
elements.append(
    Paragraph(f'''
        Il progetto risulta tecnicamente realizzabile, con necessità di validare nel dettaglio l’integrazione con il sistema di generazione di ozono e i parametri del processo di sanificazione.
    ''', paragraph)
)
elements.append(
    Paragraph(f'''
        I prossimi passi prevedono:
    ''', paragraph)
)
elements.append(Spacer(1, 10))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("raccolta dettagliata dei dati di processo", list_style)),
        ListItem(Paragraph("progettazione di un sistema prototipo", list_style)),
        ListItem(Paragraph("fase di test per validare l’efficacia della sanificazione automatica", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(Spacer(1, 10))
###
elements.append(PageBreak())

########################################
# CONTESTO E PROBLEMA
########################################
elements.append(Paragraph("Contesto e Problema", h2))
elements.append(
    Paragraph(f'''
        L’attuale gestione manuale della sanificazione limita qualità del prodotto, efficienza operativa e affidabilità del servizio.
    ''', paragraph)
)
###
elements.append(Paragraph("Sistema attuale", h3))
elements.append(
    Paragraph(f'''
        Attualmente, la sanificazione delle linee di distribuzione della birra viene eseguita manualmente tramite interventi periodici di un tecnico specializzato presso il cliente finale.
    ''', paragraph)
)
elements.append(
    Paragraph(f'''
        Il servizio viene generalmente effettuato con frequenza mensile, ma la pianificazione non è garantita e dipende dalla disponibilità dei tecnici o dalla richiesta del cliente stesso. In molti casi, l’intervento avviene solo in seguito alla comparsa di problemi evidenti nel prodotto.
    ''', paragraph)
)
elements.append(
    Paragraph(f'''
        Il costo del servizio è sostenuto dal cliente finale o dal distributore, generando un modello operativo basato su interventi manuali e non continuativi.
    ''', paragraph)
)
###
elements.append(Paragraph("Criticità operative", h3))
elements.append(
    Paragraph(f'''
        L’attuale approccio presenta diverse criticità strutturali:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Elevata dipendenza dalla manodopera: ogni operazione richiede la presenza fisica di un tecnico", list_style)),
        ListItem(Paragraph("Limitata scalabilità: il numero di interventi è vincolato alla disponibilità del personale", list_style)),
        ListItem(Paragraph("Variabilità del servizio: la qualità della sanificazione può variare tra operatori", list_style)),
        ListItem(Paragraph("Bassa attrattività operativa: si tratta di un’attività poco gradita ai tecnici", list_style)),
        ListItem(Paragraph("Gestione reattiva: gli interventi vengono spesso richiesti solo quando il problema è già presente", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Impatto sul cliente e sul business", h3))
elements.append(
    Paragraph(f'''
        Le criticità del sistema attuale generano conseguenze rilevanti:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("restituzione del prodotto da parte dei consumatori", list_style)),
        ListItem(Paragraph("perdita di reputazione per il cliente finale", list_style)),
        ListItem(Paragraph("riduzione della fiducia nel servizio e nel prodotto", list_style)),
        ListItem(Paragraph("potenziale perdita di clientela", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(Spacer(1, 10))
elements.append(
    Paragraph(f'''
        Inoltre, la natura manuale del servizio comporta:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("costi operativi elevati", list_style)),
        ListItem(Paragraph("inefficienze nella gestione degli interventi", list_style)),
        ListItem(Paragraph("impossibilità di garantire un livello di servizio costante nel tempo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Limiti strutturali", h3))
elements.append(
    Paragraph(f'''
        Il modello attuale è limitato da due fattori principali:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("dipendenza dalla disponibilità dei tecnici, che impedisce interventi tempestivi", list_style)),
        ListItem(Paragraph("approccio reattivo dei clienti, che tendono a richiedere la sanificazione solo quando il problema è già manifestato", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(Spacer(1, 10))
elements.append(
    Paragraph(f'''
        Questi elementi rendono il sistema intrinsecamente inefficiente e non adatto a garantire standard qualitativi elevati e costanti.
    ''', paragraph)
)
###
elements.append(PageBreak())

########################################
# OBIETTIVI DEL PROGETTO
########################################
elements.append(Paragraph("Obiettivi del Progetto", h2))
elements.append(
    Paragraph(f'''
        L’automazione mira a garantire la sanificazione completa delle linee di distribuzione, ripetibile e senza intervento manuale, mantenendo costante la qualità del prodotto.
    ''', paragraph)
)
###
elements.append(Paragraph("Obiettivi principali", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Automazione completa del processo di lavaggio e sanificazione delle linee di spillatura, eliminando la necessità di interventi manuali da parte dei tecnici.", list_style)),
        ListItem(Paragraph("Sanificazione ad ogni cambio fusto, con l’utente che seleziona la linea da trattare tramite un’interfaccia semplice.", list_style)),
        ListItem(Paragraph("Mantenimento costante della qualità del prodotto, assicurando che la birra distribuita sia sempre sicura e di eccellente qualità.", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Obiettivi secondari / desiderati", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Ridurre il rischio che il prodotto diventi non consumabile o potenzialmente dannoso per la salute dei consumatori.", list_style)),
        ListItem(Paragraph("Migliorare la soddisfazione del cliente finale grazie a un servizio più affidabile e puntuale.", list_style)),
        ListItem(Paragraph("Ridurre i costi operativi legati agli interventi dei tecnici.", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Collegamento con i benefici attesi", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("L’automazione del ciclo di sanificazione garantisce clienti soddisfatti e riduce le lamentele.", list_style)),
        ListItem(Paragraph("L’eliminazione della manodopera tecnica comporta una riduzione dei costi operativi.", list_style)),
        ListItem(Paragraph("Il controllo preciso del processo garantisce qualità costante del prodotto e sicurezza per i consumatori.", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(PageBreak())

########################################
# SOLUZIONE PROPOSTA
########################################
elements.append(Paragraph("Soluzione Proposta", h2))
elements.append(
    Paragraph(f'''
        Il sistema automatizzato gestisce l’intero ciclo di sanificazione delle linee di spillatura, garantendo qualità costante del prodotto e assenza di intervento manuale.
    ''', paragraph)
)
###
elements.append(Paragraph("Sintesi", h3))
elements.append(
    Paragraph(f'''
        Il progetto prevede lo sviluppo di un sistema che consenta all’utente finale di avviare la sanificazione delle linee semplicemente selezionando la linea tramite un’interfaccia touchscreen. Tutte le impostazioni dei parametri del ciclo, inclusi tempi e gestione del generatore di ozono, saranno preconfigurate e gestite automaticamente dal sistema, senza bisogno di intervento tecnico.
    ''', paragraph)
)
elements.append(
    Paragraph(f'''
        Il ciclo previsto per una linea comprende:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("10 secondi di passaggio di acqua ozonizzata attraverso la linea, sanificando internamente il sistema", list_style)),
        ListItem(Paragraph("Al termine, ripristino automatico dell’erogazione della birra", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Nel caso base, il sistema gestirà una linea alla volta, con possibilità futura di estensione fino a 8–10 linee simultanee.
    ''', paragraph)
)
###
elements.append(Paragraph("Dettaglio tecnico", h3))
elements.append(
    Paragraph(f'''
        Controllo e logica
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Un PLC o sistema di controllo gestisce automaticamente il ciclo di sanificazione", list_style)),
        ListItem(Paragraph("Il sistema avvia e spegne il generatore di ozono tramite segnale di controllo o, se necessario, tramite commutazione dell’alimentazione", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Attuatori principali
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Valvole per passare dal ciclo di sanificazione all’erogazione normale del prodotto", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Sensori
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Possibile utilizzo di sensori di flusso per monitorare il corretto avanzamento del ciclo di lavaggio", list_style)),
        ListItem(Paragraph("Eventuali sensori aggiuntivi per sicurezza e conferma del completamento del ciclo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Interfaccia utente
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("L’utente finale interagisce unicamente tramite un pulsante su touchscreen per selezionare la linea da sanificare", list_style)),
        ListItem(Paragraph("Tutte le fasi operative, inclusi tempi e flussi, sono gestite automaticamente dal sistema", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Benefici diretti", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Zero manodopera: l’utente finale non deve intervenire sul ciclo, eliminando la necessità di tecnici sul posto", list_style)),
        ListItem(Paragraph("Qualità costante del prodotto: ogni ciclo di sanificazione è ripetibile e controllato, garantendo birra sicura e di ottima qualità", list_style)),
        ListItem(Paragraph("Sicurezza: riduzione del rischio di contaminazioni e prodotto non consumabile", list_style)),
        ListItem(Paragraph("Affidabilità operativa: il ciclo è automatico, veloce (10–30 secondi) e trasparente all’utente finale", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Collegamento agli obiettivi", h3))
data = [
    ["Obiettivo", "Come la soluzione lo raggiunge"],
    ["Automazione completa", "Tutto il ciclo gestito dal PLC, utente finale solo avvia il processo"],
    ["Sanificazione ad ogni cambio fusto", "L’avvio del ciclo è legato alla selezione della linea post-cambio fusto"],
    ["Qualità costante del prodotto", "Tempo e flusso dell’acqua ozonizzata predefiniti e controllati automaticamente"],
    ["Eliminazione rischi e riduzione costi", "Nessun tecnico necessario, minori costi operativi, prodotto sempre sicuro"],
]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))
elements.append(table)
###
elements.append(Paragraph("Diagramma sistema corrente (manuale)", h3))
elements.append(Spacer(1, 10))
mul = 0.4
image_w = 736 * mul
image_h = 64 * mul
img = Image(f"projects/spillatura/diagram-0001.png", image_w, image_h)
elements.append(img)
###
elements.append(Spacer(1, 20))
elements.append(Paragraph("Diagramma sistema da sviluppare (automatico)", h3))
elements.append(Spacer(1, 10))
mul = 0.4
image_w = 768 * mul
image_h = 416 * mul
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
    ''', paragraph)
)
###
elements.append(Paragraph("Visione semplificata", h3))
elements.append(
    Paragraph(f'''
        Il ciclo operativo si sviluppa secondo le seguenti fasi:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Selezione della linea da parte dell’utente", list_style)),
        ListItem(Paragraph("Avvio manuale del ciclo tramite interfaccia", list_style)),
        ListItem(Paragraph("Erogazione di acqua ozonizzata per la sanificazione della linea", list_style)),
        ListItem(Paragraph("Ripristino automatico dell’erogazione della birra", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Il processo è progettato per essere trasparente all’utente e integrato nelle normali operazioni di spillatura.
    ''', paragraph)
)
###
elements.append(Paragraph("Sequenza tecnica dettagliata", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Trigger del ciclo: L’utente, dopo aver sostituito il fusto, seleziona la linea da sanificare tramite interfaccia e avvia manualmente il ciclo.", list_style)),
        ListItem(Paragraph("Attivazione del sistema: Il sistema di controllo riceve il comando di avvio e inizializza la sequenza operativa.", list_style)),
        ListItem(Paragraph("Commutazione del flusso: Le valvole vengono attivate per deviare il flusso dalla modalità erogazione birra alla modalità sanificazione.", list_style)),
        ListItem(Paragraph("Attivazione generatore di ozono: Il sistema attiva il generatore di ozono tramite segnale di controllo o alimentazione diretta.", list_style)),
        ListItem(Paragraph("Fase di sanificazione: L’utente inizia a spillare; durante questa fase, (1) viene erogata acqua ozonizzata, (2) il fluido attraversa l’intera linea di distribuzione, (3) la sanificazione avviene lungo tutto il percorso fino alla spillatrice.", list_style)),
        ListItem(Paragraph("Controllo temporale: Il sistema mantiene la fase di sanificazione per un tempo predefinito (attualmente 10 secondi, configurabile in futuro).", list_style)),
        ListItem(Paragraph("Terminazione sanificazione: Al termine del tempo impostato, (1) il generatore di ozono viene disattivato, (2) le valvole riportano il sistema alla configurazione di erogazione normale.", list_style)),
        ListItem(Paragraph("Ripristino erogazione prodotto: La birra torna automaticamente a fluire dalla spillatrice, segnalando implicitamente all’utente il completamento del ciclo.", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Note operative e condizioni", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Il ciclo è attualmente configurato con durata fissa (10 secondi), con possibilità futura di parametrizzazione da parte di personale tecnico.", list_style)),
        ListItem(Paragraph("Durante la fase di sanificazione, l’utente deve mantenere attiva la spillatura per consentire il passaggio completo dell’acqua ozonizzata nella linea.", list_style)),
        ListItem(Paragraph("Il sistema, nella configurazione attuale, gestisce una linea alla volta; è prevista un’evoluzione futura per la gestione simultanea di più linee in modo indipendente.", list_style)),
        ListItem(Paragraph("La gestione di condizioni anomale (es. interruzione del ciclo, assenza di flusso) non è ancora definita e rappresenta un punto di attenzione per le fasi successive di progettazione.", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Flusso operativo del ciclo di sanificazione", h3))
elements.append(Spacer(1, 20))
mul = 0.6
image_w = 321 * mul
image_h = 864 * mul
img = Image(f"projects/spillatura/diagram-0000.png", image_w, image_h)
elements.append(img)

elements.append(PageBreak())

########################################
# ARCHITETTURA DEL SISTEMA
########################################
elements.append(Paragraph("Architettura del Sistema", h2))
elements.append(
    Paragraph(f'''
        Il sistema è basato su un’architettura modulare controllata da microcontrollore, progettata per garantire integrazione, affidabilità operativa e scalabilità futura.
    ''', paragraph)
)
###
elements.append(Paragraph("Vista ad alto livello", h3))
elements.append(
    Paragraph(f'''
        L’architettura del sistema si compone dei seguenti sottosistemi principali:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Sistema di controllo centrale, responsabile della gestione della logica operativa", list_style)),
        ListItem(Paragraph("Sistema idraulico, per la gestione dei flussi di acqua ozonizzata e prodotto", list_style)),
        ListItem(Paragraph("Interfaccia utente, per l’avvio e il controllo del ciclo", list_style)),
        ListItem(Paragraph("Sistema di generazione ozono, fornito dal partner e integrato nel processo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Questi elementi operano in modo coordinato per garantire l’esecuzione automatica del ciclo di sanificazione.
    ''', paragraph)
)
###
elements.append(Paragraph("Componenti principali", h3))
elements.append(
    Paragraph(f'''
        Sistema di controllo:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Microcontrollore integrato su PCB custom progettata ad hoc", list_style)),
        ListItem(Paragraph("Gestione della logica di controllo, temporizzazioni e sequenze operative", list_style)),
        ListItem(Paragraph("Interfacciamento con sensori, attuatori e sistema ozono", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Attuatori:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Elettrovalvole on/off per (1) commutazione tra modalità sanificazione ed erogazione prodotto, (2) gestione delle linee di distribuzione", list_style)),
        ListItem(Paragraph("Il sistema sfrutta la pressione della rete idrica (rubinetto), senza necessità di pompe dedicate", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Sensori:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Possibile integrazione futura di sensori di flusso per (1) monitoraggio del corretto svolgimento del ciclo, (2) rilevamento di anomalie (es. assenza di flusso)", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Touchscreen con interfaccia semplificata:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Touchscreen con interfaccia semplificata", list_style)),
        ListItem(Paragraph("Funzionalità attuale (1) selezione linea, (2) avvio ciclo", list_style)),
        ListItem(Paragraph("Possibili evoluzioni (1) configurazione parametri, (2) monitoraggio stato sistema", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Sistema di generazione ozono (partner):
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Il generatore di ozono viene integrato nel sistema tramite (1) segnale di controllo digitale (modalità preferita), (2) controllo diretto dell’alimentazione (soluzione alternativa di backup)", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Logica di interconnessione:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("L’utente interagisce con l’interfaccia e il comando viene inviato al microcontrollore", list_style)),
        ListItem(Paragraph("Il microcontrollore (1) attiva/disattiva il generatore di ozono, (2) controlla le elettrovalvole, (3) gestisce la temporizzazione del ciclo", list_style)),
        ListItem(Paragraph("I sensori (quando presenti) forniscono feedback al sistema di controllo per garantire il corretto funzionamento", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Questa architettura consente una gestione centralizzata e automatizzata dell’intero processo.
    ''', paragraph)
)
###
elements.append(Paragraph("Scalabilità e sviluppi futuri", h3))
elements.append(
    Paragraph(f'''
        L’architettura è progettata per supportare evoluzioni future, tra cui:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("gestione di più linee di spillatura in parallelo (8–10 linee)", list_style)),
        ListItem(Paragraph("implementazione di controlli indipendenti per ciascuna linea, con valvole dedicate", list_style)),
        ListItem(Paragraph("introduzione di sensori aggiuntivi per migliorare sicurezza e affidabilità", list_style)),
        ListItem(Paragraph("espansione delle funzionalità dell’interfaccia utente", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        La modularità del sistema consente di adattare facilmente la soluzione a configurazioni più complesse senza modifiche sostanziali alla logica di base.
    ''', paragraph)
)
###
elements.append(Paragraph("Diagramma Architettura Sistema", h3))
elements.append(Spacer(1, 10))
mul = 0.4
image_w = 640 * mul
image_h = 576 * mul
img = Image(f"projects/spillatura/diagram-0003.png", image_w, image_h)
elements.append(img)
###
elements.append(PageBreak())

# 

########################################
# INTEGRAZIONE CON SISTEMA PARTNER
########################################
elements.append(Paragraph("Integrazione con Sistema Partner", h2))
elements.append(
    Paragraph(f'''
        L’integrazione con il sistema di generazione di ozono del partner è tecnicamente realizzabile, con alcune specifiche di interfaccia ancora da validare.
    ''', paragraph)
)
###
elements.append(Paragraph("Modalità di integrazione", h3))
elements.append(
    Paragraph(f'''
        Il sistema proposto prevede l’integrazione diretta con il generatore di ozono fornito dal partner, al fine di coordinare automaticamente la produzione di acqua ozonizzata durante il ciclo di sanificazione.
    ''', paragraph)
)
elements.append(
    Paragraph(f'''
        L’integrazione si basa su:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("attivazione e disattivazione del generatore in funzione del ciclo operativo", list_style)),
        ListItem(Paragraph("sincronizzazione tra produzione di ozono e flusso idraulico", list_style)),
        ListItem(Paragraph("gestione coordinata tramite il sistema di controllo centrale", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Interfacce tecniche previste", h3))
elements.append(
    Paragraph(f'''
        L’architettura prevede due possibili modalità di controllo del generatore:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Controllo tramite segnale digitale (modalità preferita): Il sistema invia un segnale di start/stop al generatore di ozono, consentendo un’integrazione diretta e controllata.", list_style)),
        ListItem(Paragraph("Controllo tramite alimentazione (modalità alternativa): In assenza di interfacce di controllo dedicate, il sistema può gestire l’accensione e lo spegnimento del generatore intervenendo direttamente sull’alimentazione elettrica.", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Eventuali segnali di feedback dal generatore (es. stato attivo, errore) potranno essere integrati qualora disponibili.
    ''', paragraph)
)
###
elements.append(Paragraph("Aree da validare", h3))
elements.append(
    Paragraph(f'''
        Alcuni aspetti tecnici risultano attualmente non definiti e richiedono approfondimento con il partner:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("disponibilità e tipologia di interfacce di controllo (segnali digitali/analogici)", list_style)),
        ListItem(Paragraph("caratteristiche elettriche del generatore (tensione, potenza, modalità di avvio)", list_style)),
        ListItem(Paragraph("tempi di risposta e comportamento all’avvio/arresto", list_style)),
        ListItem(Paragraph("eventuale disponibilità di segnali di stato o diagnostica", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Questi elementi sono fondamentali per definire in modo preciso la strategia di integrazione.
    ''', paragraph)
)
###
elements.append(Paragraph("Criticità e rischi", h3))
elements.append(
    Paragraph(f'''
        L’integrazione con il sistema del partner rappresenta uno dei principali punti di attenzione del progetto, in quanto:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("la mancanza di interfacce standard potrebbe richiedere soluzioni alternative", list_style)),
        ListItem(Paragraph("comportamenti non noti del generatore potrebbero influenzare il ciclo operativo", list_style)),
        ListItem(Paragraph("eventuali tempi di avvio non trascurabili potrebbero richiedere adattamenti nella sequenza di controllo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Strategia di integrazione", h3))
elements.append(
    Paragraph(f'''
        Per mitigare i rischi identificati, si prevede un approccio progressivo:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("raccolta dettagli tecnici dal partner", list_style)),
        ListItem(Paragraph("sviluppo di un prototipo di integrazione", list_style)),
        ListItem(Paragraph("test funzionali per validare il comportamento del sistema", list_style)),
        ListItem(Paragraph("eventuale adattamento della logica di controllo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Questo approccio consente di ridurre le incertezze e garantire una integrazione robusta ed affidabile.
    ''', paragraph)
)

elements.append(PageBreak())

########################################
# BENEFICI ATTESI
########################################
elements.append(Paragraph("Benefici Attesi", h2))
elements.append(
    Paragraph(f'''
        L’automazione del processo di sanificazione genera benefici significativi in termini di qualità del prodotto, efficienza operativa e riduzione dei costi, migliorando l’affidabilità complessiva del servizio.
    ''', paragraph)
)
###
elements.append(Paragraph("Qualità del prodotto", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Mantenimento costante della qualità della birra durante la spillatura", list_style)),
        ListItem(Paragraph("Eliminazione del rischio di contaminazioni nelle linee di distribuzione", list_style)),
        ListItem(Paragraph("Preservazione delle caratteristiche organolettiche del prodotto", list_style)),
        ListItem(Paragraph("Riduzione del rischio di prodotto non consumabile", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Efficienza operativa", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Eliminazione della necessità di interventi da parte di tecnici specializzati", list_style)),
        ListItem(Paragraph("Possibilità di eseguire la sanificazione direttamente da parte dell’operatore", list_style)),
        ListItem(Paragraph("Processo immediato e integrato nel normale flusso di lavoro (cambio fusto)", list_style)),
        ListItem(Paragraph("Eliminazione dei tempi di attesa legati alla disponibilità dei tecnici", list_style)),
        ListItem(Paragraph("Assenza di tempi di fermo dell’impianto", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Riduzione dei costi", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Riduzione dei costi di manodopera tecnica", list_style)),
        ListItem(Paragraph("Riduzione delle perdite legate a prodotto scartato o restituito", list_style)),
        ListItem(Paragraph("Eliminazione dei costi indiretti legati a inefficienze operative", list_style)),
        ListItem(Paragraph("Riduzione del rischio di perdita di clienti e conseguente impatto economico", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Affidabilità e valore per il business", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Maggiore affidabilità del servizio offerto al cliente finale", list_style)),
        ListItem(Paragraph("Miglioramento della reputazione degli operatori (bar, ristoranti)", list_style)),
        ListItem(Paragraph("Maggiore controllo sulla qualità del prodotto distribuito", list_style)),
        ListItem(Paragraph("Vantaggio competitivo per il fornitore di birra, che può garantire standard qualitativi costanti senza dipendere da interventi esterni", list_style)),
        ListItem(Paragraph("Possibilità di scalare il servizio su più clienti senza aumentare proporzionalmente i costi operativi", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(PageBreak())

########################################
# FATTIBILITA E RISCHI
########################################
elements.append(Paragraph("Fattibilità e Rischi", h2))
elements.append(
    Paragraph(f'''
        Questo approccio consente di ridurre le incertezze e garantire una integrazione robusta ed affidabile.
    ''', paragraph)
)
###
elements.append(Paragraph("Affidabilità e valore per il business", h3))
elements.append(
    Paragraph(f'''
        Il sistema proposto si basa su componenti e tecnologie consolidate, tra cui:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("sistemi di controllo basati su microcontrollore", list_style)),
        ListItem(Paragraph("elettrovalvole per la gestione dei flussi", list_style)),
        ListItem(Paragraph("integrazione con sistemi di generazione di ozono", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        L’architettura complessiva è relativamente semplice e non richiede lo sviluppo di tecnologie innovative, rendendo il progetto realizzabile nel breve-medio termine.
    ''', paragraph)
)
###
elements.append(Paragraph("Rischi principali", h3))
data = [
    ["Rischio", "Impatto", "Mitigazione"],
    ["Esecuzione non corretta del ciclo di sanificazione", "Alto", "Validazione del ciclo tramite test reali, introduzione di sensori (es. flusso) per monitoraggio"],
    ["Parametri di sanificazione non ottimali (tempo/volume)", "Alto", "Test sperimentali per determinare durata e quantità di fluido necessarie"],
    ["Incertezza sull’integrazione con il generatore di ozono", "Medio-Alto", "Raccolta dati tecnici dal partner e test di integrazione su prototipo"],
    ["Utilizzo non corretto da parte dell’utente (es. mancato avvio ciclo)", "Medio", "Valutazione di sistemi automatici di rilevazione cambio fusto"],
    ["Guasti o anomalie del sistema (valvole, flusso, assenza acqua)", "Medio", "Progettazione con controlli di sicurezza e diagnostica base"],
]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))
elements.append(table)
###
elements.append(Paragraph("Strategia di mitigazione", h3))
elements.append(
    Paragraph(f'''
        Per ridurre i rischi identificati, si prevede un approccio iterativo basato su:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("sviluppo di un prototipo funzionante", list_style)),
        ListItem(Paragraph("esecuzione di test reali di sanificazione per validare l’efficacia del processo", list_style)),
        ListItem(Paragraph("raccolta e integrazione dei dati tecnici del sistema del partner", list_style)),
        ListItem(Paragraph("introduzione progressiva di sensori e controlli di sicurezza", list_style)),
        ListItem(Paragraph("eventuale adattamento della logica di controllo sulla base dei risultati ottenuti", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
elements.append(
    Paragraph(f'''
        Questo approccio consente di affrontare in modo strutturato le incertezze e garantire la robustezza del sistema finale.
    ''', paragraph)
)
###
elements.append(PageBreak())

########################################
# PIANO DI IMPLEMENTAZIONE
########################################
elements.append(Paragraph("Piano di Implementazione", h2))
elements.append(
    Paragraph(f'''
        Il progetto sarà sviluppato in fasi iterative, con prototipo e test in laboratorio per validare il sistema su una singola linea, garantendo la fattibilità del processo prima di eventuali sviluppi commerciali.
    ''', paragraph)
)
###
elements.append(Paragraph("Fasi del progetto", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Raccolta requisiti: (1) Definizione dettagliata dei parametri di sanificazione, interfacce e flussi di controllo. (2) Identificazione dei punti critici da validare con il partner.", list_style)),
        ListItem(Paragraph("Progettazione rapida: (1) Sviluppo della logica di controllo su microcontrollore. (2) Progettazione PCB custom e schema idraulico della linea di test.", list_style)),
        ListItem(Paragraph("Sviluppo prototipo: (1) Realizzazione di un prototipo funzionante su una singola linea. (2) Integrazione con elettrovalvole e generatore di ozono (modalità segnale o alimentazione).", list_style)),
        ListItem(Paragraph("Test e validazione in laboratorio: (1) Verifica della corretta esecuzione del ciclo. (2) Misurazione dei parametri di sanificazione (tempo, quantità di acqua ozonizzata). (3) Identificazione e correzione di eventuali anomalie.", list_style)),
        ListItem(Paragraph("Ottimizzazione iterativa: (1) Adattamento della logica di controllo sulla base dei risultati dei test. (2) Possibile aggiunta di sensori o miglioramenti dell’interfaccia utente.", list_style)),
        ListItem(Paragraph("Documentazione e conclusioni: (1) Raccolta dei dati sperimentali. (2) Valutazione finale della fattibilità e preparazione delle linee guida per eventuale sviluppo futuro del prodotto vendibile.", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Approccio", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Iterativo e test-driven: ogni fase produce dati concreti e consente adattamenti rapidi", list_style)),
        ListItem(Paragraph("Prototipo singola linea: per validare il concetto senza investimenti iniziali troppo grandi", list_style)),
        ListItem(Paragraph("Validazione in laboratorio: riduce rischi prima di qualsiasi test sul campo", list_style)),
        ListItem(Paragraph("Obiettivo primario: validare il processo e dimostrare la fattibilità del sistema completo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(PageBreak())

########################################
# STIMA COMPONENTI
########################################
elements.append(Paragraph("Stima Componenti", h2))
elements.append(
    Paragraph(f'''
        Il sistema può essere realizzato utilizzando componenti standard e facilmente reperibili, con una struttura modulare che consente scalabilità e ottimizzazione dei costi.
    ''', paragraph)
)
###
elements.append(Paragraph("Componenti principali", h3))
elements.append(
    Paragraph(f'''
        Di seguito una stima preliminare dei principali componenti necessari per la realizzazione del sistema su una singola linea:
    ''', paragraph)
)
elements.append(Paragraph("Sistema di controllo", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Microcontrollore (es. ESP32)", list_style)),
        ListItem(Paragraph("PCB custom progettata ad hoc, (1) gestione I/O, (2) interfacciamento con attuatori e sensori", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Alimentazione", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Alimentazione principale 12V DC (preferita)", list_style)),
        ListItem(Paragraph("Eventuale conversione da 230V AC a 12V DC tramite alimentatore dedicato", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Attuatori", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Elettrovalvole on/off (n. 2 per linea), (1) una per commutazione flusso, (2) una per gestione linea / isolamento", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Sensori (opzionali / da validare)", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Sensore di flusso, (1) monitoraggio del corretto passaggio del fluido, (2) rilevamento anomalie (assenza flusso)", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Interfaccia utente", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Touchscreen con display embedded, (1) selezione linea, (2) avvio ciclo", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Infrastruttura e integrazione", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Quadro elettrico / box di contenimento", list_style)),
        ListItem(Paragraph("Cablaggi elettrici e connessioni idrauliche", list_style)),
        ListItem(Paragraph("Interfaccia di collegamento con il generatore di ozono", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Infrastruttura e integrazione", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Quadro elettrico / box di contenimento", list_style)),
        ListItem(Paragraph("Cablaggi elettrici e connessioni idrauliche", list_style)),
        ListItem(Paragraph("Interfaccia di collegamento con il generatore di ozono", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Considerazioni", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("La scelta di componenti standard consente facilità di approvvigionamento e manutenzione", list_style)),
        ListItem(Paragraph("L’architettura modulare permette di replicare il sistema su più linee con incremento lineare dei componenti", list_style)),
        ListItem(Paragraph("Alcuni elementi (es. sensori) potranno essere confermati o ottimizzati in fase di test", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
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
###
elements.append(PageBreak())

########################################
# DECISIONE RICHIESTA
########################################
elements.append(Paragraph("Decisione Richiesta", h2))
elements.append(
    Paragraph(f'''
        Si richiede l’approvazione per avviare la fase di sviluppo prototipale e validazione del sistema di sanificazione automatizzata.
    ''', paragraph)
)
###
elements.append(Paragraph("Approvazioni richieste", h3))
elements.append(
    Paragraph(f'''
        Si richiede l’approvazione per:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Avvio del progetto di sviluppo di un prototipo funzionante su singola linea", list_style)),
        ListItem(Paragraph("Allocazione di un budget preliminare per la realizzazione del prototipo (componenti, sviluppo hardware e test)", list_style)),
        ListItem(Paragraph("Avvio della collaborazione tecnica con il partner per la definizione delle modalità di integrazione con il generatore di ozono", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Obiettivo della fase approvata", h3))
elements.append(
    Paragraph(f'''
        La fase oggetto di approvazione ha l’obiettivo di:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Validare l’efficacia del processo di sanificazione automatizzata", list_style)),
        ListItem(Paragraph("Verificare la fattibilità tecnica del sistema", list_style)),
        ListItem(Paragraph("Identificare eventuali criticità e ottimizzazioni necessarie", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Passi successivi", h3))
elements.append(
    Paragraph(f'''
        Al termine della fase di prototipazione e test, verrà effettuata una valutazione dei risultati al fine di:
    ''', paragraph)
)
elements.append(ListFlowable(
    [
        ListItem(Paragraph("confermare la validità tecnica della soluzione", list_style)),
        ListItem(Paragraph("definire eventuali evoluzioni del sistema", list_style)),
        ListItem(Paragraph("valutare lo sviluppo di una versione industrializzabile del prodotto", list_style)),
    ],
    bulletType='bullet',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(PageBreak())

########################################
# APPENDICE TECNICA
########################################
elements.append(Paragraph("Appendice Tecnica", h2))
###
elements.append(Paragraph("Logica di controllo (pseudo-codice)", h3))
elements.append(
    Paragraph(f'''
START
    Attesa input utente (selezione linea + avvio ciclo)
    IF comando_avvio = TRUE THEN
        Seleziona linea
        Attiva elettrovalvole → modalità sanificazione
        Attiva generatore ozono
        Avvia timer (T = 10s)
        WHILE timer < T DO
            IF sensore_flusso = FALSE (opzionale) THEN
                Segnala errore
                STOP ciclo
            ENDIF
        ENDWHILE
        Disattiva generatore ozono
        Ripristina elettrovalvole → modalità erogazione birra
    END IF
END
    ''', paragraph)
)
###
elements.append(Paragraph("Sequenza operativa formalizzata", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Input utente (touchscreen)", list_style)),
        ListItem(Paragraph("Selezione linea", list_style)),
        ListItem(Paragraph("Attivazione valvole → modalità sanificazione", list_style)),
        ListItem(Paragraph("Attivazione ozono", list_style)),
        ListItem(Paragraph("Spillatura acqua ozonizzata", list_style)),
        ListItem(Paragraph("Temporizzazione (10s)", list_style)),
        ListItem(Paragraph("Disattivazione ozono", list_style)),
        ListItem(Paragraph("Ripristino erogazione birra", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("I/O preliminare", h3))
###
elements.append(Paragraph("Input", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Comando avvio ciclo (utente)", list_style)),
        ListItem(Paragraph("Selezione linea", list_style)),
        ListItem(Paragraph("Sensore di flusso (opzionale)", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Output", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Controllo elettrovalvole (x2 per linea)", list_style)),
        ListItem(Paragraph("Controllo generatore ozono (ON/OFF)", list_style)),
        ListItem(Paragraph("Output interfaccia utente (stato sistema)", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Assunzioni tecniche", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Il flusso d’acqua è garantito dalla rete idrica (pressione rubinetto)", list_style)),
        ListItem(Paragraph("Il generatore di ozono è controllabile via segnale o alimentazione", list_style)),
        ListItem(Paragraph("Il tempo di sanificazione iniziale è fissato a 10 secondi (da validare)", list_style)),
        ListItem(Paragraph("L’utente esegue correttamente la procedura di avvio ciclo", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
###
elements.append(Paragraph("Punti da validare", h3))
elements.append(ListFlowable(
    [
        ListItem(Paragraph("Tempo ottimale di sanificazione", list_style)),
        ListItem(Paragraph("Necessità e tipologia di sensori", list_style)),
        ListItem(Paragraph("Modalità di integrazione con il generatore di ozono", list_style)),
        ListItem(Paragraph("Gestione condizioni di errore (interruzione ciclo, assenza flusso, ecc.)", list_style)),
    ],
    bulletType='1',   # or '1' for numbered
    leftIndent=15,
    bulletFontName='Helvetica',
    bulletFontSize=8
    )
)
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
