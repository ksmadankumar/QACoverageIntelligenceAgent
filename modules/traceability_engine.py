import pandas as pd


def build_traceability_matrix(
    requirements_text,
    results_df
):

    requirements = []

    lines = requirements_text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 10:

            requirements.append(line)

    traceability = []

    for req in requirements:

        matched = 0

        for _, row in results_df.iterrows():

            row_text = str(
                row.to_dict()
            ).lower()

            words = req.lower().split()

            hits = sum(
                1
                for w in words
                if w in row_text
            )

            if hits >= 3:

                matched += 1

        if matched == 0:

            status = "Missing"

        elif matched < 3:

            status = "Partial"

        else:

            status = "Covered"

        traceability.append(
            {
                "requirement": req,
                "coverage_status": status,
                "matched_test_cases": matched
            }
        )

    return pd.DataFrame(
        traceability
    )