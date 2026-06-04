def calculate_final_score(
    analysis
):

    scores = [

        analysis.get(
            "requirement_coverage",
            0
        ),

        analysis.get(
            "functional_coverage",
            0
        ),

        analysis.get(
            "ui_coverage",
            0
        ),

        analysis.get(
            "ux_coverage",
            0
        ),

        analysis.get(
            "security_coverage",
            0
        )

    ]

    return round(
        sum(scores)
        /
        len(scores),
        2
    )