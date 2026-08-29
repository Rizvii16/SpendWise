import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def generate_csv_report(df):
    return df.to_csv(index=False).encode("utf-8")


def generate_pdf_report(df, total_spending, average_spending):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("SpendWise - Financial Report", styles["Title"])
    )

    elements.append(Spacer(1, 20))

    report_data = [
        ["Metric", "Value"],
        ["Total Spending", f"₹{total_spending:,.2f}"],
        ["Average Expense", f"₹{average_spending:,.2f}"],
        ["Transactions", str(len(df))]
    ]

    table = Table(report_data, colWidths=[220, 180])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ])
    )

    elements.append(table)

    document.build(elements)

    buffer.seek(0)

    return buffer.getvalue()