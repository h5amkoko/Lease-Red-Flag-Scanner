import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

async def analyze_lease(text: str) -> dict:
    
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"""You are a legal expert specializing in residential lease agreements. 
Analyze the following lease and identify any suspicious, unfair, risky, 
or potentially unenforceable clauses.

For each red flag found provide:
1. A short title
2. Severity level: critical, high, medium, or low
3. The exact clause text from the lease
4. Why it's risky and what the tenant should do

Return ONLY a JSON object, no preamble, no markdown:
{{
  "redFlags": [
    {{
      "issue": "short title",
      "severity": "critical|high|medium|low",
      "clause": "exact text from lease",
      "explanation": "why this is risky and what to do"
    }}
  ],
  "riskScore": 0-100,
  "summary": "brief overall assessment"
}}

Lease text:
{text}"""
            }
        ]
    )

    # pull text out of response
    raw = message.content[0].text

    # strip markdown backticks if Claude adds them
    clean = raw.replace("```json", "").replace("```", "").strip()

    result = json.loads(clean)

    return result