import pandas as pd


def export_excel(
    results_df,
    traceability_df
):

    output_file = (
        "reports/QA_Analysis_Report.xlsx"
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        results_df.to_excel(
            writer,
            sheet_name="Analysis",
            index=False
        )

        traceability_df.to_excel(
            writer,
            sheet_name="Traceability",
            index=False
        )

    return output_file