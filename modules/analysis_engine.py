import json

from modules.ollama_client import (
    call_qwen
)


def analyze_single_test_case(
    requirement_context,
    test_case
):

    prompt = f"""
You are a Senior QA Test Architect.

Analyze the test case against the requirement.

Requirement:
{requirement_context[:1500]}

Test Case:
{test_case}

Respond ONLY with valid JSON.

{{
  "quality_score": 0,
  "severity": "",
  "priority": "",
  "risk_level": "",
  "missing_scenarios": []
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

        parsed = json.loads(
            response[start:end]
        )

        return {
            "quality_score":
                parsed.get(
                    "quality_score",
                    0
                ),

            "severity":
                parsed.get(
                    "severity",
                    "Medium"
                ),

            "priority":
                parsed.get(
                    "priority",
                    "Medium"
                ),

            "risk_level":
                parsed.get(
                    "risk_level",
                    "Medium"
                ),

            "missing_scenarios":
                parsed.get(
                    "missing_scenarios",
                    []
                )
        }

    except Exception:

        return {
            "quality_score": 0,
            "severity": "Unknown",
            "priority": "Unknown",
            "risk_level": "Unknown",
            "missing_scenarios": []
        }