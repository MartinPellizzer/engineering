from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ----------------------------
# DOCUMENT SETUP
# ----------------------------
doc = SimpleDocTemplate(
    "industrial_ozone_proposal.pdf",
    pagesize=A4,
    rightMargin=60,
    leftMargin=60,
    topMargin=80,
    bottomMargin=60
)

styles = getSampleStyleSheet()

# ----------------------------
# CUSTOM STYLES
# ----------------------------
title = ParagraphStyle(
    'Title',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    spaceAfter=20
)

h1 = ParagraphStyle(
    'Heading1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=16,
    spaceBefore=20,
    spaceAfter=10
)

h2 = ParagraphStyle(
    'Heading2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    spaceBefore=15,
    spaceAfter=8
)

body = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10.5,
    leading=14
)

small = ParagraphStyle(
    'Small',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    textColor=colors.grey
)

right_small = ParagraphStyle(
    'RightSmall',
    parent=small,
    alignment=TA_RIGHT
)

# ----------------------------
# HEADER / FOOTER
# ----------------------------
def add_header_footer(canvas, doc):
    canvas.saveState()

    # Header line
    canvas.setStrokeColor(colors.grey)
    canvas.setLineWidth(0.5)
    canvas.line(60, 800, 535, 800)

    # Header text
    canvas.setFont("Helvetica", 9)
    canvas.drawString(60, 810, "YOUR COMPANY NAME S.R.L.")
    canvas.drawRightString(535, 810, "Industrial Ozone Engineering")

    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.drawString(60, 30, "Confidential")
    canvas.drawRightString(535, 30, f"Page {doc.page}")

    canvas.restoreState()

# ----------------------------
# CONTENT BUILDER
# ----------------------------
elements = []

# ----------------------------
# COVER PAGE
# ----------------------------
elements.append(Paragraph("YOUR COMPANY NAME S.R.L.", title))
elements.append(Paragraph("Industrial Ozone Engineering & Consulting", small))

elements.append(Spacer(1, 80))

elements.append(Paragraph("TECHNICAL AND COMMERCIAL PROPOSAL", title))
elements.append(Paragraph(
    "Design, Supply and Integration of Industrial Ozone Systems",
    body
))

elements.append(Spacer(1, 60))

elements.append(Paragraph("Prepared for:", h2))
elements.append(Paragraph("CLIENT COMPANY NAME", h1))

elements.append(Spacer(1, 40))

meta_data = [
    ["Project Reference:", "OZ-2026-001"],
    ["Date:", "March 2026"],
    ["Prepared by:", "Your Company Name S.R.L."],
    ["Confidentiality:", "Strictly Private & Confidential"]
]

meta_table = Table(meta_data, colWidths=[150, 300])
meta_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey),
]))

elements.append(meta_table)

elements.append(Spacer(1, 120))

elements.append(Paragraph(
    "This document contains proprietary engineering and commercial information.",
    right_small
))

elements.append(PageBreak())

# ----------------------------
# TABLE OF CONTENTS (STATIC)
# ----------------------------
elements.append(Paragraph("TABLE OF CONTENTS", h1))

toc_items = [
    "1. Executive Summary",
    "2. Company Overview",
    "3. Project Understanding",
    "4. Technical Solution",
    "5. System Architecture",
    "6. Implementation Plan",
    "7. Commercial Proposal",
    "8. Terms and Conditions"
]

for item in toc_items:
    elements.append(Paragraph(item, body))
    elements.append(Spacer(1, 6))

elements.append(PageBreak())

# ----------------------------
# 1. EXECUTIVE SUMMARY
# ----------------------------
elements.append(Paragraph("1. EXECUTIVE SUMMARY", h1))

elements.append(Paragraph(
    "This proposal outlines the design, engineering, and supply of an industrial ozone "
    "generation system tailored to the client's operational requirements. "
    "The solution is developed to ensure efficiency, compliance, and long-term reliability.",
    body
))

# ----------------------------
# 2. COMPANY OVERVIEW
# ----------------------------
elements.append(Paragraph("2. COMPANY OVERVIEW", h1))

elements.append(Paragraph(
    "Your Company Name S.R.L. specializes in advanced ozone technologies "
    "for industrial applications, including water treatment, air purification, "
    "and process oxidation.",
    body
))

# ----------------------------
# 3. PROJECT UNDERSTANDING
# ----------------------------
elements.append(Paragraph("3. PROJECT UNDERSTANDING", h1))

elements.append(Paragraph(
    "Based on the information provided, the system must achieve defined performance targets "
    "under specified environmental and operational constraints.",
    body
))

# ----------------------------
# 4. TECHNICAL SOLUTION
# ----------------------------
elements.append(Paragraph("4. TECHNICAL SOLUTION", h1))

elements.append(Paragraph(
    "The proposed solution consists of a modular ozone generation system, including "
    "feed gas preparation, ozone generator, injection system, and monitoring units.",
    body
))

# Example table (technical specs)
tech_data = [
    ["Parameter", "Value"],
    ["Ozone Output", "XX g/h"],
    ["Power Consumption", "XX kW"],
    ["Cooling System", "Air/Water"],
]

tech_table = Table(tech_data, colWidths=[200, 200])
tech_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
]))

elements.append(Spacer(1, 10))
elements.append(tech_table)

# ----------------------------
# 5. IMPLEMENTATION PLAN
# ----------------------------
elements.append(Paragraph("5. IMPLEMENTATION PLAN", h1))

elements.append(Paragraph(
    "The project will be executed in structured phases, including design, procurement, "
    "assembly, testing, and commissioning.",
    body
))

# ----------------------------
# 6. COMMERCIAL PROPOSAL
# ----------------------------
elements.append(Paragraph("6. COMMERCIAL PROPOSAL", h1))

pricing_data = [
    ["Description", "Amount (€)"],
    ["Ozone System Supply", "XXXXX"],
    ["Installation", "XXXXX"],
    ["Commissioning", "XXXXX"],
    ["Total", "XXXXX"]
]

pricing_table = Table(pricing_data, colWidths=[300, 100])
pricing_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
]))

elements.append(pricing_table)

# ----------------------------
# 7. TERMS
# ----------------------------
elements.append(Paragraph("7. TERMS AND CONDITIONS", h1))

elements.append(Paragraph(
    "This proposal is valid for 30 days from the date of issue. "
    "All equipment remains property of the supplier until full payment is received.",
    body
))

# ----------------------------
# BUILD DOCUMENT
# ----------------------------
doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)