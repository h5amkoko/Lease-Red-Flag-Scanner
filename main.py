from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_text
from scanner import analyze_lease

app = FastAPI()

# allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    
    # only accept PDFs
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="only PDF files are accepted")
    
    pdf_bytes = await file.read()
    
    # step 1 - pull text out of the PDF
    text = extract_text(pdf_bytes)
    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="could not extract text from PDF — may be a scanned image")
    
    # step 2 - send to Claude and get analysis back
    result = await analyze_lease(text)
    
    return result