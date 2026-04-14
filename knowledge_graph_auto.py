
# 1. DOMAIN DISCOVERY (scraping/books)


def pdf_to_text():
    import fitz  # PyMuPDF
    pdf_folderpath = f'/home/ubuntu/vault/books/herbalism/preparations'
    pdf_filename_raw = "The-Herbal-Medicine-Makers-Handbook"
    pdf_path = f"{pdf_folderpath}/{pdf_filename_raw}.pdf"
    txt_path = f"{pdf_folderpath}/{pdf_filename_raw}.txt"
    doc = fitz.open(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as out:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")  # plain text extraction
            if text:
                out.write(text)
                out.write("\n")  # page break
            # optional progress indicator
            if page_num % 100 == 0:
                print(f"Processed {page_num} pages")
    doc.close()

pdf_to_text()
