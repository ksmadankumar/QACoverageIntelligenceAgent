import json

from modules.ollama_client import (
    call_qwen
)


def analyze_single_test_case(
    requirement_context,
    test_case
):

    prompt = f"""
You are a Senior QA Architect.

Requirement Context:

{requirement_context}

Test Case:

{test_case}

Return ONLY JSON.

{{
  "requirement_coverage":0,
  "functional_coverage":0,
  "ui_coverage":0,
  "ux_coverage":0,
  "security_coverage":0,
  "quality_score":0,
  "severity":"",
  "priority":"",
  "risk_level":"",
  "missing_scenarios":[]
}}
"""

    response = call_qwen(
        prompt
    )

    try:

        start = response.find("{")

        end = (
            response.rfind("}")
            + 1
        )

        return json.loads(
            response[start:end]
        )

    except:

        return {
            "requirement_coverage": 0,
            "functional_coverage": 0,
            "ui_coverage": 0,
            "ux_coverage": 0,
            "security_coverage": 0,
            "quality_score": 0,
            "severity": "Unknown",
            "priority": "Unknown",
            "risk_level": "Unknown",
            "missing_scenarios": []
        }