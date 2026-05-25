import os
import subprocess

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

input_filepath = "./projects/ozone/campaigns/wine/articoli/input/study-0000.md"
input_folderpath = "./projects/ozone/campaigns/wine/articoli/input"
output_filepath = "./projects/ozone/campaigns/wine/articoli/output/study-0000.pdf"
output_folderpath = "./projects/ozone/campaigns/wine/articoli/output"



for input_filename in os.listdir(input_folderpath):
    filename_raw = input_filename.split('.')[0].strip()
    input_filepath = f'{input_folderpath}/{filename_raw}.md'
    output_filepath = f'{output_folderpath}/{filename_raw}.pdf'

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

    # BUILD
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

    # subprocess.run(["xdg-open", "doc.pdf"])


def protocol_gen():
    protocol_folderpath = "./projects/ozone/campaigns/wine/protocol"

    input_filepath = f'{protocol_folderpath}/input/protocol.md'
    output_filepath = f'{protocol_folderpath}/output/protocol.pdf'

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

    # BUILD
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

    # subprocess.run(["xdg-open", "doc.pdf"])


def product_gen():
    protocol_folderpath = "./projects/ozone/campaigns/wine/product"

    input_filepath = f'{protocol_folderpath}/input/product.md'
    output_filepath = f'{protocol_folderpath}/output/product.pdf'

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

    # BUILD
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

    # subprocess.run(["xdg-open", "doc.pdf"])


# protocol_gen()
product_gen()