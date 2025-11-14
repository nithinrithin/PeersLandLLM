import json
import re

def clean_llm_json(raw_text: str):
    """
    Takes raw LLM output (possibly wrapped in ```json fences) and returns a Python dict.
    """
    # Remove markdown fences if present
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # fallback: return as plain string if not valid JSON
        return {"text": cleaned}
