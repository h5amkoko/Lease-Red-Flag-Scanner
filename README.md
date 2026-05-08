# Lease Red Flag Scanner

A Python API that scans residential lease agreements and surfaces risky, 
unfair, or potentially unenforceable clauses using Claude.

## Background

Living in Berkeley as a student, I watched a lot of people sign leases 
without reading them. Not because they didn't care, but rather, they just didn't know 
what to look for. Clauses about automatic renewal, landlord entry rights, 
security deposit deductions, and subletting restrictions. For example, some agreements 
may say that a landlord can enter at any time, but under California Civil Code 1954, a 
landlord generally cannot enter a rental unit without permission or prior notice. 
People usually would find out months later when something went wrong, and they had no recourse because they'd 
already signed.

That's what this is for. Upload a lease, get back a plain-English breakdown 
of anything worth flagging before you sign.

## How it works

1. Upload a PDF lease via the `/analyze` endpoint
2. PyMuPDF extracts the raw text
3. Claude reads it as a legal expert and identifies red flags
4. Returns structured JSON with severity levels, exact clause text, and explanations

## Stack

- FastAPI
- PyMuPDF (text extraction)
- Anthropic Claude API (analysis)

## Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
uvicorn main:app --reload
```

## Example Response

```json
{
  "redFlags": [
    {
      "issue": "Automatic Renewal Clause",
      "severity": "high",
      "clause": "Lease shall automatically renew for successive terms...",
      "explanation": "Tenant is locked into another term unless written 
                      notice is given 60 days before expiration."
    }
  ],
  "riskScore": 72,
  "summary": "This lease contains several clauses that heavily favor 
              the landlord."
}
```

## Project Structure

```
RedFlag/
├── main.py          # FastAPI app and route handling
├── extractor.py     # PDF text extraction via PyMuPDF
├── scanner.py       # Claude API call and response parsing
└── requirements.txt
```
