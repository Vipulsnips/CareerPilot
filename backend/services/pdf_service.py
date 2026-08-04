from fastapi import UploadFile
import pymupdf

async def extract_text(file:UploadFile)->str:
    pdf_bytes= await file.read()
    document= pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )
    pages=[]
    try:
      for page in document:
          pages.append(page.get_text())
      return "\n".join(pages)
    finally:
      document.close()
