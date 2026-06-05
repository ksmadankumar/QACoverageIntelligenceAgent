from modules.rag_engine import (
    retrieve_matches
)


def match_test_case_to_requirements(
    test_case_text,
    top_k=5
):

    matches = retrieve_matches(
        test_case_text,
        top_k=top_k
    )

    return matches


def get_best_requirement_match(
    test_case_text
):

    matches = retrieve_matches(
        test_case_text,
        top_k=1
    )

    if len(matches) == 0:

        return {
            "requirement": "",
            "similarity": 0
        }

    return matches[0]