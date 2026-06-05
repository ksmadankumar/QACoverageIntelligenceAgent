from modules.vector_matcher import (
    get_best_requirement_match
)


def evaluate_coverage(
    test_case_text
):

    match = (
        get_best_requirement_match(
            test_case_text
        )
    )

    similarity = (
        match["similarity"]
    )

    if similarity >= 90:

        coverage = "Fully Covered"

    elif similarity >= 75:

        coverage = "Partially Covered"

    else:

        coverage = "Gap Detected"

    return {
        "coverage_status": coverage,
        "similarity_score": similarity,
        "matched_requirement":
        match["requirement"]
    }