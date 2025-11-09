from langchain_core.prompts import PromptTemplate

code_analysis_prompt = PromptTemplate(
    input_variables=["code_chunk"],
    template="""
You are an architect. Analyze the following code chunk and extract structured insights:

1. Project purpose and functionality (if identifiable).
2. Key classes, methods, and their signatures.
3. Method descriptions and responsibilities.
4. Complexity indicators (low | medium | high) based on logic used.
5. Any noteworthy design patterns or architectural choices.

Return the result in this JSON format:
{{
  "overview": "...",
  "methods": [
    {{
      "class": "...",
      "name": "...",
      "signature": "...",
      "description": "...",
      "complexity": "low | medium | high"
    }}
  ],
  "notes": "..."
}}

Code chunk:
{code_chunk}
"""
)
