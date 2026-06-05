import time

from modules.rag_engine import (
    retrieve_context
)

from modules.coverage_engine import (
    evaluate_coverage
)

from modules.analysis_engine import (
    analyze_single_test_case
)

from modules.scoring_engine import (
    calculate_final_score
)


def analyze_all_test_cases(
    df,
    progress_callback=None
):

    results = []

    total = len(df)

    start_time = time.time()

    for index, row in df.iterrows():

        test_case = row.to_dict()

        test_case_text = " ".join(
            [
                str(v)
                for v in test_case.values()
            ]
        )

        coverage = (
            evaluate_coverage(
                test_case_text
            )
        )

        similarity = coverage[
            "similarity_score"
        ]

        if similarity >= 70:

            analysis = {
                "quality_score": similarity,
                "priority": "Medium",
                "strengths":
                    "Requirement coverage detected",
                "gaps":
                    "No major gaps detected",
                "recommendations":
                    "Review manually if needed"
            }

        else:

            context = retrieve_context(
                test_case_text
            )

            analysis = (
                analyze_single_test_case(
                    context,
                    test_case
                )
            )

        final_score = (
            calculate_final_score(
                analysis
            )
        )

        analysis[
            "final_score"
        ] = final_score

        merged = {
            **test_case,
            **coverage,
            **analysis
        }

        results.append(
            merged
        )

        if progress_callback:

            elapsed = (
                time.time()
                - start_time
            )

            processed = (
                index + 1
            )

            avg = (
                elapsed
                / processed
            )

            remaining = (
                total
                - processed
            )

            eta = int(
                avg
                * remaining
            )

            progress_callback(
                processed,
                total,
                eta
            )

    return results